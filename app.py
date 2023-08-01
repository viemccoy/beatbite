import os
import uuid
from flask import Flask, request, send_file, render_template
from beatbite import BeatBite, add_intro_and_outro
from celery import Celery

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'beatbites/'
app.config['CELERY_BROKER_URL'] = 'rediss://:p87b80e66e2e3f12598e7daaceac6cb1ce7fd2a7a3aa49d5c860b4697242b6a2e@ec2-54-166-254-3.compute-1.amazonaws.com:23650?ssl_cert_reqs=CERT_NONE'
app.config['CELERY_RESULT_BACKEND'] = 'rediss://:p87b80e66e2e3f12598e7daaceac6cb1ce7fd2a7a3aa49d5c860b4697242b6a2e@ec2-54-166-254-3.compute-1.amazonaws.com:23650?ssl_cert_reqs=CERT_NONE'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


@celery.task
def process_audio(interest, news_api_key, openai_api_key, elevenlabs_api_key, filepath):
    # create BeatBite instance and process audio
    beatbite_instance = BeatBite(news_api_key, openai_api_key, elevenlabs_api_key)
    beatbite_instance.main(interest)

    add_intro_and_outro("beatbite_unfinished.mp3", "beatbite_intro.wav", "beatbite_outro.wav", filepath)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # get user input
        interest = request.form.get('interest')
        news_api_key = request.form.get('news_api_key')
        openai_api_key = request.form.get('openai_api_key')
        elevenlabs_api_key = request.form.get('elevenlabs_api_key')
        # create a unique filename for each user
        filename = str(uuid.uuid4()) + '.wav'
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        # enqueue the audio processing task
        process_audio.delay(interest, news_api_key, openai_api_key, elevenlabs_api_key, filepath)
        # return a response to the user
        return "Processing audio. Please wait."
    return render_template('index.html')


@app.route('/file/<filename>', methods=['GET'])
def download_file(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return send_file(filepath, as_attachment=True)


if __name__ == '__main__':
    app.run(threaded=True, port=5000)
