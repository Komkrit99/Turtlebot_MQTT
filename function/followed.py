import cv2
import mediapipe as mp
# import tensorflow as tf

cap = cv2.VideoCapture(0)
mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils
while (True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    results = pose.process(frame)
    if results.pose_landmarks:
        mpDraw.draw_landmarks(
            frame, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = frame.shape
            cx, cy = int(lm.x*w), int(lm.y*h)
            wc = ((w/2)-cx)
            hc = ((h/2)-cy)
            if (wc > 200):
                print('left')
            elif (wc < -100):
                print('right')
            else:
                print('middle')

    # Display the resulting frame
    cv2.imshow('black and white', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
