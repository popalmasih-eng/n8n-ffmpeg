from flask import Flask, request, jsonify
import os
import uuid

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/create-video", methods=["POST"])
def create_video():
    data = request.get_json()

    image_url = data.get("imageUrl")
    title = data.get("title", "video")
    story = data.get("story", "")

    # fake output for now (we will add ffmpeg next step)
    video_id = str(uuid.uuid4())

    output_path = f"/tmp/{video_id}.mp4"

    # TEMP placeholder file
    with open(output_path, "w") as f:
        f.write("video placeholder")

    return jsonify({
        "status": "success",
        "videoUrl": f"https://your-domain.onrender.com/download/{video_id}.mp4"
    })

@app.route("/download/<file>", methods=["GET"])
def download(file):
    return jsonify({"message": "replace with static file server later"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
