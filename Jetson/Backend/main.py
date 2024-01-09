from library.FlexVision import FlexVision
from library.FlexMQTT import FlexMQTT
from library.FlexDebug import FlexDebug


# 클래스 인스턴스 생성
vision = FlexVision("./model/StelraCMF.pt", 0)
mqtt = FlexMQTT("127.0.0.1", 2006)
debug = FlexDebug()


# 카운터 딕셔너리 선언
count = {"red" : 0, "green" : 0, "yellow" : 0, "white" : 0}

# 세션 및 모듈 이름 선언
SESSION = "asm"
MODULE = "jetson01"

# 색상 토픽 선언
TOPIC = {
    "red"    : mqtt.topic(SESSION, MODULE, mqtt.MEMORY, "1x0"),
    "green"  : mqtt.topic(SESSION, MODULE, mqtt.MEMORY, "1x1"),
    "yellow" : mqtt.topic(SESSION, MODULE, mqtt.MEMORY, "1x2"),
    "white"  : mqtt.topic(SESSION, MODULE, mqtt.MEMORY, "1x3")
}

# 카메라 데이터 토픽 선언
TOPIC_CAMERA = mqtt.topic(SESSION, MODULE, mqtt.MEMORY, "0x0")


# 프로그램 초기화
def init():
    vision.load_model(method="cuda")
    vision.set_ROI((210, 302, 154, 152))
    vision.detect_handler((count_update), ((vision.best)))
    
    mqtt.start()


# 메인 프로그램
def main():
    if vision.attach():
        vision.start(window=True, dict_labal=count)


# 카운터 업데이트
def count_update(value):
    if value[0] != "none":
        count[value[0]] += 1
        mqtt.publish(TOPIC[value[0]], count[value[0]])


if __name__ == '__main__':
    init()
    main()