import requests

from flask import Flask
from flask import render_template, redirect
from flask import request, url_for, session
from pathlib import Path
import json

# NOTE: flask run --port 8001 --debug

app = Flask(__name__)
app.secret_key = "very_secret_key"

VIDEOS: dict[str, str] = {
    "demo": "tesseract_test.mp4",
    "oop": "oop.mp4",
}

@app.route("/video/<video_id>")
def video(video_id: str ):
    """
    and a sends a transcript to the template if possible
    """

    transcript = request.args.get("transcript")
    video_path = VIDEOS[video_id]
    current_time = request.args.get("time")
    if current_time is None:
        current_time = 0
    if transcript is None:
        transcript = 'Transcript Text Here...'
    print(transcript)

    if current_time:
        return render_template("video.html", video=video_path, video_id=video_id, time=current_time)
    else:
        return render_template("video.html", video=video_path, video_id=video_id)
