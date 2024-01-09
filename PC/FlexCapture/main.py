import cv2


color = "none"


def main():
    cap = cv2.VideoCapture(0)
    cnt = 0

    while True:
        _, frame = cap.read()
        
        frame = frame[720:1080, 720:1080]
        cv2.imshow("CaptureFlow", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('c'):
            print("Capture Images")
            cv2.imwrite(f"./images/{color}{cnt}.jpg", frame)
            cnt += 1
        elif cnt == 16:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()