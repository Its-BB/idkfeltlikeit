import pickle
import cv2
import mediapipe as mp
import numpy as np

# Load the model
model_dict = pickle.load(open('./model.p', 'rb'))
model = model_dict['model']

# Initialize the video capture
cap = cv2.VideoCapture(0)  # Change to the correct camera index if necessary

# Initialize Mediapipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=False, min_detection_confidence=0.3)

# Label dictionary for A-Z
labels_dict = {i: chr(65 + i) for i in range(26)}  # chr(65) is 'A', chr(66) is 'B', ..., chr(90) is 'Z'

while True:
    data_aux = []
    x_ = []
    y_ = []

    ret, frame = cap.read()

    if not ret:
        print("Failed to capture frame")
        break  # Exit loop if frame capture fails

    H, W, _ = frame.shape

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(frame_rgb)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame,  # image to draw
                hand_landmarks,  # model output
                mp_hands.HAND_CONNECTIONS,  # hand connections
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())

        for hand_landmarks in results.multi_hand_landmarks:
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y

                x_.append(x)
                y_.append(y)

            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                data_aux.append(x - min(x_))
                data_aux.append(y - min(y_))

        # Ensure data_aux is of consistent length
        max_length = 84  # Assuming 21 landmarks each with x and y coordinates
        if len(data_aux) < max_length:
            data_aux += [0] * (max_length - len(data_aux))

        x1 = int(min(x_) * W) - 10
        y1 = int(min(y_) * H) - 10

        x2 = int(max(x_) * W) - 10
        y2 = int(max(y_) * H) - 10

        # Convert numpy.str_ to Python string
        predicted_character = str(model.predict([np.asarray(data_aux)])[0])

        # Find the index of the predicted character in labels_dict
        predicted_index = [k for k, v in labels_dict.items() if v == predicted_character]

        # Debug: Print the predicted character and index
        print(f"Prediction: {predicted_character}, Type: {type(predicted_character)}")
        print(f"Displaying Character: {predicted_character}, Index: {predicted_index}")

        if predicted_index:
            predicted_character = labels_dict[predicted_index[0]]
        else:
            predicted_character = '?'  # Fallback if prediction is not found

        # Draw the predicted character on the frame
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
        cv2.putText(frame, predicted_character, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3, cv2.LINE_AA)

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
