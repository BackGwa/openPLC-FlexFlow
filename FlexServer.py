from threading import Thread
import FlexVision as vision


# [MAIN PROGRAM]
def main():
    vision_thread = Thread(target=vision.start)
    vision_thread.start()


# [PROGRAM START POINT]
if __name__ == "__main__":
    main()