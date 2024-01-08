import cv2
from ultralytics import YOLO
from paho.mqtt.client import Client


# [GLOBAL VARABLE]
MODEL_PATH = "./model/ColorVision.pt"
TOPIC = "flexflow/asm/jetson01/"
ROI = (210, 302, 154, 152)
color_counter = {"red" : 0, "green" : 0, "yellow" : 0, "white" : 0}
model, capture = None, None


# [CREATE CLASS INSTANCE]
client = Client()


# [PROGRAM INIT]
def init(model_path, device_index = 0):
    global model, capture
    
    # 모델 가져오기 시도
    try:
        print("모델을 불러오고 있습니다...")
        model = YOLO(model_path)
        model.to("cuda")
        print("모델을 불러왔습니다!")
    except:
        print("모델을 불러오던 중, 오류가 발생했습니다!")
        exit()
    
    # 캡쳐 장치 할당 시도
    try:
        print("캡쳐 장치를 할당하고 있습니다...")
        capture = cv2.VideoCapture(device_index)
        print("캡쳐 장치를 할당했습니다!")
    except:
        print("캡쳐 장치 할당 중, 오류가 발생했습니다!")
        exit()
    
    # MQTT 브로커와 연결 시도
    try:
        print("MQTT 브로커와 연결을 시도하고 있습니다...")
        client.connect("127.0.0.1", 2006)
        print("MQTT 브로커와 연결했습니다!")
    except:
        print("MQTT 브로커와 연결하지 못했습니다!")
        exit()


# [MAIN PROGRAM]
def main():
    color_cache = ""                                # 이전 클래스 저장을 위한 변수 선언
    
    while capture.isOpened():
        success, frame = capture.read()             # 프레임 캡쳐 & 성공 여부 가져오기
        
        if success:
            # 관심 영역으로 축소 후 연산
            ROI_frame = ROI_generator(frame, ROI)
            result = model(ROI_frame, verbose=False)[0]
            
            classes = result.names                  # 전체 클래스 가져오기
            best    = result.probs.top1             # 최상위 확률의 클래스 인덱스 가져오기
            best_v  = result.probs.top1conf         # 최상위 확률의 확률 값 가져오기
            color   = classes[best]                 # 변수를 감지 된 클래스로 설정
            
            if best_v > 0.75:                       # 최상위 확률이 0.75 이상일 때만, 반영
                if color != color_cache:            # 이전과 같은 결과 값이라면, 패스
                    process_input(color)            # 감지 된, 색상의 카운터 증가
                    publish_value(color)            # 현재 색상 카운터 값 발행
 
            color_cache = color                     # 현재 클래스를 캐싱
            
            DEBUGGER(frame, result)                 # 디버거 실행
        
            # 'q' 입력 시, 연산 종료
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            break
    
    # 캡쳐 장치 할당 중지
    capture.release()
    cv2.destroyAllWindows()


# [FUNCTION]
# 입력 된 클래스의 카운터를 1씩 증가시킵니다.
def process_input(color):
    global color_counter
    if color != "none":
        color_counter[color] += 1


# [FUNCTION]
# 현재 모든 클래스 카운터를 토픽에 발행합니다.
def publish_value(color):
    if color != "none":
        print(f"{color} 토픽이 {color_counter[color]}으로 업데이트 되었습니다!")
        client.publish(TOPIC + f"COUNTER/{color}", color_counter[color])


# [FUNCTION]
# 전체 프레임을 ROI 프레임으로 반환합니다.
def ROI_generator(frame, ROI):
    return frame[ROI[1]:ROI[1] + ROI[3],
                 ROI[0]:ROI[0] + ROI[2]]


# [FUNCTION]
# ROI 값을 (시작점, 종료점) 좌표로 반환합니다.
def ROI_to_Boxed(ROI):
    return ((ROI[0], ROI[1]), (ROI[2] + ROI[0], ROI[3] + ROI[1]))


# [FUNCTION]
# 주어진 프레임에 사각형과 라벨을 추가하여, 반환합니다.
def labeling_rect(frame, pos, label, color = (0, 0, 255)):
    frame = cv2.rectangle(frame, pos[0], pos[1], color, 2)
    frame = cv2.putText(frame, label, (pos[0][0], pos[0][1] - 8), cv2.FONT_HERSHEY_PLAIN, 1, color)
    return frame


# [FUNCTION]
# 주어진 프레임에 현재 클래스 카운터를 추가합니다.
def labeling_counter(frame, counter_dict, color = (0, 0, 255)):
    for index, item in enumerate(counter_dict.items()):
        frame = cv2.putText(frame, f"{item[0]} : {item[1]}", (16, 32 * (index + 1)), cv2.FONT_HERSHEY_PLAIN, 2, color)
    return frame


# [FUNCTION]
# 전체 프레임 영역과 ROI 프레임을 보여줍니다.
def DEBUGGER(frame, ROI_frame):
    frame   = labeling_rect(frame, ROI_to_Boxed(ROI), "VisionROI")
    frame   = labeling_counter(frame, color_counter)
    preview = ROI_frame.plot()
    cv2.imshow("FlexVision - Live", frame)
    cv2.imshow("FlexVision - ROI", preview)


# [PROGRAM START FUNCTION]
def start():
    init(MODEL_PATH)
    main()
    
    
# [PROGRAM START POINT]
if __name__ == "__main__":
    start()