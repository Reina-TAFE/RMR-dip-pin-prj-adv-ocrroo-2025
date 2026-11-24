import requests

from flask import Flask
from flask import render_template, redirect
from flask import request, url_for, session
from pathlib import Path
import json
from datetime import datetime, timezone
from .bookmark_utils import BookmarkManager

# Bookmark format: { id: timestamp(seconds) }
BOOKMARK_DB_PATH = '../front-end/bookmark_utils/resources/bookmarks.db'
bookmark_manager = None

# NOTE: flask run --port 8001 --debug

app = Flask(__name__)
app.secret_key = "very_secret_key"

VIDEOS: dict[str, str] = {
    "demo": "tesseract_test.mp4",
    "oop": "oop.mp4",
}

@app.route("/")
def index():
    """gets a list of videos from the api and loads the indexs/login page"""

    videos = requests.get("http://127.0.0.1:8000/video").json()

    if videos['count'] == 0:
        videos = None

    print(videos['videos'])

    return render_template("index.html", videos=videos['videos'])

@app.route("/login", methods=["POST"])
def login():
    """
    gets the username and selected video entered by the user,
    enters video id and path, and the user's name to the session.
    """
    global bookmark_manager, BOOKMARK_DB_PATH
    user = request.form.get('username')
    video_id = request.form.get('video')
    path = str(VIDEOS[video_id])


    # path = f"front-end/static/media/{video_id}.mp4"
    session['video_id'] = video_id
    session['video_path'] = path
    session['user'] = user
    if bookmark_manager is None:
        bookmark_manager = BookmarkManager(BOOKMARK_DB_PATH, user)
    else:
        bookmark_manager.user = user
    tables = bookmark_manager.get_tables()
    # check if database has been populated with tables
    if len(tables) == 0:
        bookmark_manager.create_bookmarks_db()
    # if user not in database, add them
    bookmark_manager.check_user_in_db()
    # if video not in database, add it
    if not bookmark_manager.check_video_in_db(video_id):
        bookmark_manager.add_video(video_id, VIDEOS[video_id])
    print(video_id, user)

    return redirect(url_for(f"video", video_id=video_id))

@app.route("/video/<video_id>")
def video(video_id: str ):
    """
    and a sends a transcript to the template if possible
    """
    global bookmark_manager

    transcript = request.args.get("transcript")

    current_time = request.args.get("time")
    if bookmark_manager is not None:
        bookmarks = bookmark_manager.load_bookmarks_for_video(video_id)
        video_path = bookmark_manager.get_video(video_id)["path"]
        if video_path is None and video_id in VIDEOS.keys():
            video_path = VIDEOS[video_id] # default
            bookmark_manager.update_video_path(video_id, video_path)
    else:
        bookmarks = None
        video_path = VIDEOS[video_id]
    if current_time is None:
        current_time = 0
    if transcript is None:
        transcript = 'Transcript Text Here...'
    print(transcript)
    if bookmarks:
        if transcript:
            if current_time:
                return render_template("video.html", video=video_path, video_id=video_id, time=current_time, transcript=transcript, bookmarks=bookmarks)
            else:
                return render_template("video.html", video=video_path, video_id=video_id, transcript=transcript, bookmarks=bookmarks)
        else:
            if current_time:
                return render_template("video.html", video=video_path, video_id=video_id, time=current_time, bookmarks=bookmarks)
            else:
                return render_template("video.html", video=video_path, video_id=video_id, bookmarks=bookmarks)
    else:
        if transcript:
            if current_time:
                return render_template("video.html", video=video_path, video_id=video_id, time=current_time,
                                       transcript=transcript)
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

@app.route("/video/<video_id>/load-bookmark", methods=["POST"])
def load_bookmark(video_id: str):
    """Loads the timestamp associated with the bookmark"""
    global bookmark_manager
    if bookmark_manager is not None:
        bookmark_id = request.form['bookmark_id']
        bookmark = bookmark_manager.get_bookmark(bookmark_id)
        return redirect(url_for("video", video_id=video_id, time=bookmark['time']))
    else:
        time = request.form['bookmark_pos']
        return redirect(url_for("video", video_id=video_id, time=time))

@app.route("/video/<video_id>/add-bookmark", methods=["POST"])
def add_bookmark(video_id: str):
    global bookmark_manager

    time = request.form.get('bookmark_timer')
    title = request.form.get('bookmark_title')
    if time is None or time == '':
        time = 0
    if title is None or title == '':
        title = "unnamed"
    # if bookmark_manager is not None:
    bookmark_manager.add_bookmark(video_id, int(time), title)
    return redirect(url_for("video", video_id=video_id, time=int(time)))


@app.template_filter('format_time')
def format_time(seconds):
    seconds = int(seconds)
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)

    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"