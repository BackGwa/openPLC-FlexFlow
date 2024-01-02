import cv2
import numpy as np
import paho.mqtt.client as mqtt
from FlexMQTT import INT, MEMORY, SESSION_ID, TOPIC
from time import sleep as delay


# MQTT 브로커 선언
BROKER = "broker.hivemq.com"
PORT = 1883

# MQTT 세션 선언
SESSION = "asm"
MODULE = "rpi01"

# 색상 별 메모리 주소 선언
TOPIC_RED   = TOPIC(SESSION, MODULE, MEMORY(INT, 1, 0))
TOPIC_GREEN = TOPIC(SESSION, MODULE, MEMORY(INT, 1, 1))
TOPIC_BLUE  = TOPIC(SESSION, MODULE, MEMORY(INT, 1, 2))

# 카메라 디바이스 번호
DEVICE_INDEX = 0


# 프로그램 메인
def main():
    
    # MQTT 클라이언트 초기화
    ID = SESSION_ID(SESSION, MODULE)
    client = mqtt.Client(ID)
    client.connect(BROKER, PORT, 60)
    
    print(f"SESSION ID : {ID}")
    print(f"TOPIC RED   : {TOPIC_RED}")
    print(f"TOPIC GREEN : {TOPIC_GREEN}")
    print(f"TOPIC BLUE  : {TOPIC_BLUE}")
    
    # OpenCV 캡쳐 디바이스 설정
    capture = cv2.VideoCapture(DEVICE_INDEX)
    
    
    # 각 색상별 카운터
    RED_COUNTER = 0
    GREEN_COUNTER = 0
    BLUE_COUNTER = 0
    
    # 색상 감지 연속 제한 변수 선언
    detected = False
    
    while True:
        ret, frame = capture.read()                     # 프레임 읽기
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)    # BGR에서 HSV로 변환

        # 빨간색 감지 범위
        lower_red = np.array([0, 100, 100])
        upper_red = np.array([10, 255, 255])
        red_mask = cv2.inRange(hsv, lower_red, upper_red)

        # 초록색 감지 범위
        lower_green = np.array([40, 40, 40])
        upper_green = np.array([80, 255, 255])
        green_mask = cv2.inRange(hsv, lower_green, upper_green)

        # 파란색 감지 범위
        lower_blue = np.array([110, 50, 50])
        upper_blue = np.array([130, 255, 255])
        blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

        # 빨간색 감지
        if not detected and cv2.countNonZero(red_mask) > 10000:
            RED_COUNTER += 1
            client.publish(
                TOPIC_RED,
                RED_COUNTER
            )
            delay(0.1)
            print(f"RED : {RED_COUNTER}")
        
        # 초록색 감지
        elif not detected and cv2.countNonZero(green_mask) > 10000:
            GREEN_COUNTER += 1
            client.publish(
                TOPIC_GREEN,
                GREEN_COUNTER
            )
            delay(0.1)
            print(f"GREEN : {GREEN_COUNTER}")
       
        # 파란색 감지
        elif not detected and cv2.countNonZero(blue_mask) > 10000:
            BLUE_COUNTER += 1
            client.publish(
                TOPIC_BLUE,
                BLUE_COUNTER
            )
            delay(0.1)
            print(f"BLUE : {BLUE_COUNTER}")

        # 색상 감지 연속 제한
        if detected and (not (cv2.countNonZero(red_mask) > 10000) and (not (cv2.countNonZero(green_mask) > 10000)) and (not (cv2.countNonZero(blue_mask) > 10000))):
            detected = False
        else:
            detected = True

        # 원본 이미지에 마스크 적용
        result_frame = cv2.bitwise_and(frame, frame, mask=red_mask + green_mask + blue_mask)

        # 결과 프레임 출력
        cv2.imshow('FlexVision', result_frame)

        # 종료 키 감지
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # 캡쳐 리소스 할당 해제
    capture.release()
    cv2.destroyAllWindows()


# 프로그램 시작점
if __name__ == '__main__':
    main()