from paho.mqtt.client import Client


class FlexMQTT:
    """
    # FlexMQTT
    FlexFlow를 위한, 유연하고 빠른 MQTT 라이브러리.
    """
    
    def __init__(self, broker: str, port: int):
        """
        ## FlexMQTT 초기화
        - FlexMQTT을 사용하기 위하여, 새로운 클래스 인스턴스를 생성합니다.
        
        ---

        Args:
            broker: MQTT 브로커의 주소를 설정합니다.
            port: MQTT 브로커의 TCP/IP 포트를 설정합니다.
        """
        
        self.client = Client()
        
        self.broker = broker
        self.port = port
        
        self.INPUT = "INPUT"
        self.OUTPUT = "OUTPUT"
        self.MEMORY = "MEMORY"        
                
        self.BOOL = "BOOL"
        self.INT = "INT"
        self.REAL = "REAL"
        self.DATA = "DATA"

    def start(self):
        """
        ## MQTT 브로커 연결
        - MQTT 브로커와 연결을 시도합니다.

        ---

        Returns:
            success: 성공적으로 MQTT 브로커와 연결되었는지 반환합니다.
        """
        try:
            self.client.connect(host=self.broker, port=self.port)
            return True
        except:
            return False
        
    def topic(self, session: str, module: str, types: str, data: str):
        """
        ## MQTT 토픽 문자열 반환
        - FlexFlow에 적합한 토픽으로 반환합니다.

        ---

        Args:
            session: 기관 및 개인의 ID를 사용합니다.
            module: 모듈의 고유 ID 및 번호를 설정합니다.
            types: 토픽의 고유 타입을 설정합니다. `INPUT`, `OUTPUT`, `MEMORY`
            data: 주소 및 데이터를 설정합니다.
            
        ---

        Returns:
            topic: 합쳐진 토픽을 반환합니다.
        """
        return f"flexflow/{session}/{module}/{types}/{data}"
    
    def publish(self, topic: str, data: str):
        """
        ## 발행
        - 토픽에 데이터를 발행합니다.

        ---

        Args:
            topic: 어느 토픽에 발행할 지 설정합니다.
            data: 발행할 데이터를 설정합니다.

        ---

        Returns:
            success: 데이터가 성공적으로 발행되었는지 반환합니다.
        """
        try:
            self.client.publish(topic, data)
            return True
        except:
            return False