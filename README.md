# beatbite

Custom News Breaking News Briefings Powered by A.I.

BeatBite allows the user to generate a custom news report on any topic simply by typing that topic in and pressing submit.

Please note that BeatBite was made for the LabLabAI/ElevenLabs Hackathon, and as such requires an ElevenLabs API key to run. The code also requires several dependencies, and two other API's to function.

You will need the ElevenLabsAPI key, which you can find information on here: https://elevenlabs.io/

You will need a ChatGPT API key from OpenAI (with access to GPT-4): https://openai.com/blog/openai-api

And you will need a NewsAPI key (free for projects in development, like this one): https://newsapi.org


Please reach out to me at v@violetcastles.com if you are having trouble accessing anything. Put BeatBite URGENT as the subject for a faster response.

There are two ways to run BeatBite, as of Jul 31 2023.

The first is the preferred method, which uses a local Flask app to allow for ease of use. If you run BeatBite in this way, the final BeatBite audio file (beatbite_final.wav) will be sent to your browsers download folder.

To do this, simply clone the repo locally, and run app.py and navigate to http://127.0.0.1:5000

On this page, you will simply have to input your various API keys, and choose a topic for the first field. Then click submit, and Diane will prepare your BeatBite breifing :)

If you wish to run beatbite in the command line, you can do so with beatbite_CL.py which will require a .env file with the API keys.

To do this, simply create a .env folder in the root directory (/beatbite/, not the /beatbite_v1 subfolder) and prepare the following.
Replace the api_key_here respective with each api key (include the single quotes in the file surrounding the API key).

OPENAI_API_KEY='api_key_here'

NEWS_API_KEY='api_key_here'

ELEVENLABS_API_KEY='api_key_here'


Then simply run beatbite_CL.py and input your topic. The file (beatbite_final.wav) will be saved in the /beatbite_v1/ folder.

Don't forget to stay curious, and tune back for your BeatBite Briefing with Diane the A.I.
