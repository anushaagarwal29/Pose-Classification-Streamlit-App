"""Object detection demo with MobileNet SSD.
This model and code are based on
https://github.com/robmarkcole/object-detection-app
"""

import logging
import queue
from pathlib import Path
from typing import List, NamedTuple

import av
import cv2
import numpy as np
import streamlit as st
from streamlit_webrtc import WebRtcMode, webrtc_streamer

from sample_utils.download import download_file
from sample_utils.turn import get_ice_servers

webrtc_ctx = webrtc_streamer(
    key="object-detection",
    mode=WebRtcMode.SENDRECV,
    rtc_configuration={
        "iceServers": get_ice_servers(),
        "iceTransportPolicy": "relay",
    },
    video_frame_callback=video_frame_callback,
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True,
)

if st.checkbox("Show the detected labels", value=True):
    if webrtc_ctx.state.playing:
        labels_placeholder = st.empty()
        # NOTE: The video transformation with object detection and
        # this loop displaying the result labels are running
        # in different threads asynchronously.
        # Then the rendered video frames and the labels displayed here
        # are not strictly synchronized.
        while True:
            result = result_queue.get()
            labels_placeholder.table(result)
