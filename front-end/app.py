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

    if transcript:
        if current_time:
            return render_template("video.html", video=video_path, video_id=video_id, time=current_time, transcript=transcript)
        else:
            return render_template("video.html", video=video_path, video_id=video_id, transcript=transcript)
    else:
        if current_time:
            return render_template("video.html", video=video_path, video_id=video_id, time=current_time)
        else:
            return render_template("video.html", video=video_path, video_id=video_id)

@app.route("/video/<video_id>/generate-transcript", methods=["POST"])
def get_transcript(video_id: str):
    """
    get the ocr for a given time (in seconds) from the API
    redirect to /video with the transcript
    """
    video_position = request.form.get('video_pos')
    # video_id = session.get('video_id')
    url = f"http://127.0.0.1:8000/video/{video_id}/frame/{video_position}/ocr"
    response = requests.get(url).content

    response = response.decode(encoding='utf-8')

    return redirect(url_for(f"video", video_id=video_id, time=video_position, transcript=response))
