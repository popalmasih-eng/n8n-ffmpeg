from flask import Flask
import subprocess

app = Flask(__name__)

@app.route("/")
def home():
    return "FFmpeg Webservice Running!"

@app.route("/ffmpeg-version")
def ffmpeg_version():
    result = subprocess.check_output(["ffmpeg", "-version"]).decode("utf-8")
    return f"<pre>{result}</pre>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
