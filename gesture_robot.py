import cv2
import mediapipe as mp
from collections import deque

# ---------------- INITIALIZATION ----------------
cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2)
mp_draw = mp.solutions.drawing_utils

tip_ids = [4, 8, 12, 16, 20]

command_buffer = deque(maxlen=5)

speed = 0
command = "IDLE"
final_command = "IDLE"

robot_x, robot_y = 300, 300
robot_size = 40
# ------------------------------------------------

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for idx, handLms in enumerate(result.multi_hand_landmarks):

            lm_list = []
            h, w, _ = frame.shape

            for id, lm in enumerate(handLms.landmark):
                lm_list.append((id, int(lm.x * w), int(lm.y * h)))

            fingers = []

            # Thumb
            if lm_list[4][1] > lm_list[3][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            # Other fingers
            for i in range(1, 5):
                if lm_list[tip_ids[i]][2] < lm_list[tip_ids[i] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            count = fingers.count(1)

            # ---------- TWO HAND LOGIC ----------
            if idx == 0:
                # Right hand → Direction
                if count == 1:
                    command = "FORWARD"
                elif count == 2:
                    command = "LEFT"
                elif count == 3:
                    command = "RIGHT"
                elif count == 4:
                    command = "BACKWARD"
                elif count == 0:
                    command = "STOP"
                else:
                    command = "IDLE"


            elif idx == 1:
                # Left hand → Speed
                speed = count * 10

            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

    # ---------- TEMPORAL FILTERING ----------
    command_buffer.append(command)
    final_command = max(set(command_buffer), key=command_buffer.count)
    # ---------------------------------------

    # ---------- ROBOT MOTION ----------
    frame_h, frame_w, _ = frame.shape

    if final_command == "FORWARD" and robot_y > 0:
        robot_y -= speed

    elif final_command == "BACKWARD" and robot_y < frame_h - robot_size:
        robot_y += speed

    elif final_command == "LEFT" and robot_x > 0:
        robot_x -= speed

    elif final_command == "RIGHT" and robot_x < frame_w - robot_size:
        robot_x += speed

    elif final_command == "STOP":
        pass


    # ---------- DRAW ROBOT ----------
    cv2.rectangle(frame,
                  (robot_x, robot_y),
                  (robot_x + robot_size, robot_y + robot_size),
                  (0, 0, 255), -1)

    cv2.putText(frame, "ROBOT",
                (robot_x, robot_y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # ---------- DISPLAY INFO ----------
    cv2.putText(frame, f"Command: {final_command}", (20, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.putText(frame, f"Speed: {speed}", (20, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)
    # ----------------------------------

    cv2.imshow("Gesture Controlled Robot", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
