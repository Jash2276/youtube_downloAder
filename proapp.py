from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)

# Create downloads folder if it doesn't exist
if not os.path.exists('downloads'):
    os.makedirs('downloads')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    url = request.form['url']
    format_type = request.form['format']
    
    # Options for the downloader
    ydl_opts = {'outtmpl': 'downloads/%(title)s.%(ext)s'}

    if format_type == 'mp3':
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    else:
        ydl_opts['format'] = 'bestvideo+bestaudio/best'

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            # Adjust filename for MP3s
            if format_type == 'mp3':
                filename = filename.rsplit('.', 1)[0] + '.mp3'
                
            return send_file(filename, as_attachment=True)
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(debug=True)