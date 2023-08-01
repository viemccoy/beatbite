from flask import Flask, request, send_file, render_template
from beatbite import BeatBite, add_intro_and_outro

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # get user input
        interest = request.form.get('interest')
        news_api_key = request.form.get('news_api_key')
        openai_api_key = request.form.get('openai_api_key')
        elevenlabs_api_key = request.form.get('elevenlabs_api_key')
         # create BeatBite instance and process audio
        beatbite_instance = BeatBite(news_api_key, openai_api_key, elevenlabs_api_key)
        beatbite_instance.main(interest)  # assuming you modified the main method to accept an interest parameter
        # add intro and outro music
        add_intro_and_outro("beatbite_unfinished.mp3", "beatbite_intro.wav", "beatbite_outro.wav", "beatbite_final.wav")
        # send the newly created file to the user
        return send_file('beatbite_final.wav', as_attachment=True)
    # render a simple form to get user input
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
