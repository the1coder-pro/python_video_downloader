from flask import Flask, request, jsonify, render_template
from yt_dlp import YoutubeDL
import os

app = Flask(__name__)

# Save path
SAVE_PATH = "C:\\Users\\aamut\\Desktop\\Personal Projects\\video_downloader\\downloads"

# Route for downloading video or audio
@app.route('/download', methods=['POST'])
def download_video():
    data = request.json
    link = data.get("link")
    format_choice = data.get("format")

    if not link:
        return jsonify({"error": "No link provided"}), 400

    if format_choice not in ['mp4', 'mp3']:
        return jsonify({"error": "Invalid format choice"}), 400

    URLS = [link]

    try:
        ydl_opts = {
            'format': 'bestaudio' if format_choice == 'mp3' else 'bestvideo',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }] if format_choice == 'mp3' else [],
            'outtmpl': os.path.join(SAVE_PATH, '%(title)s.%(ext)s')
        }
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=True)
            title = info_dict.get('title', None)
            ext = 'mp3' if format_choice == 'mp3' else 'mp4'
            filename = f"{title}.{ext}"
            ydl.download(URLS)
        file_path = os.path.join(SAVE_PATH, filename)
        return jsonify({"status": "Download complete", "file": file_path}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route for serving the HTML file
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
