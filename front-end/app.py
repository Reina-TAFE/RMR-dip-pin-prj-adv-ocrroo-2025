import requests

from flask import Flask
from flask import render_template, redirect
from flask import request, url_for, session
from pathlib import Path
import json

# NOTE: flask run --port 8001 --debug

app = Flask(__name__)
app.secret_key = "very_secret_key"

