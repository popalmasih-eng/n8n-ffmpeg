from flask import Flask, request, jsonify, send_file
import subprocess, os, glob, shutil, threading, requests, time

app = Flask(__name__)

def keep_alive():
    while True:
        time.sleep(600)
        try:
            requests.get("https://n8n-ffmpeg-bdnq.onrender.com/health", timeout=5)
        except:
            pass

threading.Thread(target=keep_alive, daemon=True).start()

@app.route('/')
def home():
    return jsonify({'message': 'FFmpeg Webservice Running!', 'status': 'ok'})

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

@app.route('/split', methods=['POST'])
def split():
    data = request.json
    url = data['url']
    movie_id = data['movieId']
    input_file = f'/tmp/{movie_id}.mp4'
    output_dir = f'/tmp/{movie_id}_clips'
    os.makedirs(output_dir, exist_ok=True)
    subprocess.run(['wget', '-q', '-O', input_file, url], check=True)
    subprocess.run(['ffmpeg', '-i', input_file, '-c:v', 'libx264', '-preset', 'fast', '-crf', '23', '-c:a', 'aac', '-b:a', '128k', '-segment_time', '180', '-f', 'segment', '-reset_timestamps', '1', '-map', '0', f'{output_dir}/clip_%03d.mp4'], check=True)
    clips = sorted(glob.glob(f'{output_dir}/*.mp4'))
    return jsonify({'clipCount': len(clips), 'outputDir': output_dir, 'clips': [os.path.basename(c) for c in clips]})

@app.route('/clips/<movie_id>/<filename>')
def get_clip(movie_id, filename):
    path = f'/tmp/{movie_id}_clips/{filename}'
    return send_file(path, mimetype='video/mp4')

@app.route('/cleanup', methods=['POST'])
def cleanup():
    movie_id = request.json['movieId']
    shutil.rmtree(f'/tmp/{movie_id}_clips', ignore_errors=True)
    f = f'/tmp/{movie_id}.mp4'
    if os.path.exists(f):
        os.remove(f)
    return jsonify({'cleaned': True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
