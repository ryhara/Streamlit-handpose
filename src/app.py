import streamlit as st
from streamlit_webrtc import webrtc_streamer
import mediapipe as mp
import cv2
import av


st.title('Hand Pose Estimation')
st.write('This app uses MediaPipe to estimate hand pose in real-time.')

thickness = st.slider('Drawing Thickness', min_value=1, max_value=10, value=2, step=1)
circle_radius = st.slider('Circle Radius', min_value=1, max_value=10, value=2, step=1)
min_detection_confidence = st.slider('Min Detection Confidence', min_value=0.0, max_value=1.0, value=0.5, step=0.1)
min_tracking_confidence = st.slider('Min Tracking Confidence', min_value=0.0, max_value=1.0, value=0.3, step=0.1)


def callback(frame):
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    image = frame.to_ndarray(format="bgr24")
    with mp_hands.Hands(
        min_detection_confidence=min_detection_confidence,
        min_tracking_confidence=min_tracking_confidence,) as hands:
        image = cv2.flip(image, 1)
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True
        if results.multi_hand_landmarks:
            for num, hand in enumerate(results.multi_hand_landmarks):
                mp_drawing.draw_landmarks(
                    image, hand, mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=thickness, circle_radius=circle_radius),
                    mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=thickness, circle_radius=circle_radius),
                )
        return av.VideoFrame.from_ndarray(image, format="bgr24")




webrtc_streamer(key="hand-pose", video_frame_callback=callback, async_processing=True, media_stream_constraints={'video': True, 'audio': False}, rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})


st.write("Created by [ryhara](https://github.com/ryhara)")
st.write("Repository [Streamlit-handpose](https://github.com/ryhara/Streamlit-handpose)")
