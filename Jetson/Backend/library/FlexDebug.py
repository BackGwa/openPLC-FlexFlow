
class FlexDebug:
    """
    # FlexDebug
    FlexFlow의 다양한 라이브러리를 위한, 디버거 라이브러리.
    """
    def __init__(self):
        """
        ## FlexDebug 초기화
        - FlexDebug를 사용하기 위하여, 새로운 클래스 인스턴스를 생성합니다.
        """
        
        self.RED    = "\033[31m"
        self.GREEN  = "\033[32m"
        self.YELLOW = "\033[33m"
        self.CYAN   = "\033[34m"
        self.BOLD   = "\033[1m"
        self.RESET  = "\033[0m"

    def __debug_message__(self, title: str, color: str, *args):
        """
        ## 디버거 메세지 출력
        - 디버거 메세지를 출력합니다.
        
        ---
        
        Args:
            title: 제목을 설정합니다.
            color: 색상을 설정합니다.
        """
        print(color + self.BOLD + title + self.RESET + self.BOLD + ": " + self.RESET, end="")
        for message in args:
            print(message)

    def err(self, *args):
        """
        ## 충돌 메세지 출력
        - 충돌 메세지를 출력합니다.
        """
        self.__debug_message__("충돌", self.RED, *args)
        
    def warn(self, *args):
        """
        ## 경고 메세지 출력
        - 경고 메세지를 출력합니다.
        """
        self.__debug_message__("경고", self.YELLOW, *args)
        exit()
        
    def success(self, *args):
        """
        ## 성공 메세지 출력
        - 성공 메세지를 출력합니다.
        """
        self.__debug_message__("성공", self.GREEN, *args)
        
    def alert(self, *args):
        """
        ## 알림 메세지 출력
        - 알림 메세지를 출력합니다.
        """
        self.__debug_message__("알림", self.CYAN, *args)