from flask import Flask, request, send_file
from gtts import gTTS
from moviepy.editor import *
import requests

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate_video():
    data = request.json
    script = data['script']
    image_url = data['image_url']

    tts = gTTS(script)
    tts.save("voice.mp3")

    img_data = requests.get(image_url).content
    with open("image.jpg", 'wb') as handler:
        handler.write(img_data)

    clip = ImageClip("image.jpg").set_duration(10).resize(height=720)
    audio = AudioFileClip("voice.mp3")
    final_video = clip.set_audio(audio)
    final_video.write_videofile("output.mp4", fps=24)

    return send_file("output.mp4", as_attachment=True)

app.run(host="0.0.0.0", port=8080)
