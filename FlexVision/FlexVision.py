
import cv2                      # 이미지 처리를 위한 opencv 모듈 가져오기
import numpy as np              # numpy array를 위한 모듈 가져오기

# 배경 차분을 위한 객체 생성
bg_subtractor = cv2.createBackgroundSubtractorMOG2()

# 카메라 연결
cap = cv2.VideoCapture(0)

while True:
    # 프레임 읽기
    ret, frame = cap.read()

    # BGR을 HSV로 변환
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 빨간색의 HSV 범위 정의
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([180, 255, 255])

    # 노란색의 HSV 범위 정의
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])

    # 파란색의 HSV 범위 정의
    lower_blue = np.array([110, 50, 50])
    upper_blue = np.array([130, 255, 255])

    # 각 색상에 대한 마스크 생성
    mask_red1 = cv2.inRange(hsv, lower_red, upper_red)
    mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)

    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)

    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

    # 원본 이미지에서 각 색상 부분만 남기기
    result_red = cv2.bitwise_and(frame, frame, mask=mask_red)
    result_yellow = cv2.bitwise_and(frame, frame, mask=mask_yellow)
    result_blue = cv2.bitwise_and(frame, frame, mask=mask_blue)

    # 전체적인 결과 이미지 표시
    result_combined = cv2.bitwise_or(result_red, cv2.bitwise_or(result_yellow, result_blue))

    # 배경 차분을 통한 전경 추출
    fg_mask = bg_subtractor.apply(result_combined)

    # 노이즈 제거를 위한 모폴로지 연산
    kernel = np.ones((5, 5), np.uint8)
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)

    # 윤곽선 검출
    contours, hierarchy = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 윤곽선 그리기
    frame_with_contours = frame.copy()
    cv2.drawContours(frame_with_contours, contours, -1, (0, 255, 0), 2)

    cv2.imshow('Combined Result', result_combined)

    # 특정 색상이 감지되면 메시지 출력
    if cv2.countNonZero(mask_red) > 10000:
        print("빨간색이 감지되었습니다.")
    elif cv2.countNonZero(mask_yellow) > 10000:
        print("노란색이 감지되었습니다.")
    elif cv2.countNonZero(mask_blue) > 10000:
        print("파란색이 감지되었습니다.")

    # 종료 조건
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 작업 완료 후 해제
cap.release()
cv2.destroyAllWindows()