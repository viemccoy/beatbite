import os
from dotenv import load_dotenv
from newsapi import NewsApiClient
import openai
import requests

from pydub import AudioSegment

def add_intro_and_outro(audio_file, intro_file, outro_file, output_file):
    """
    Add intro and outro music to an audio file.
    """
    # Load the audio files
    audio = AudioSegment.from_mp3(audio_file)
    intro = AudioSegment.from_wav(intro_file)
    outro = AudioSegment.from_wav(outro_file)

    # Add 5 seconds of silence to the beginning and end of the audio
    silence = AudioSegment.silent(duration=5000)
    audio = silence + audio + silence

    # Overlay the intro and outro music
    audio = audio.overlay(intro)
    audio = audio.overlay(outro, position=len(audio)-10000)

    # Export the final audio file
    audio.export(output_file, format="wav")

def main():
    """
    Main function to run the program.
    """
    # Create an instance of the BeatBite class
    beatbite_instance = BeatBite()
    beatbite_instance.main()

    # Add the intro and outro music
    add_intro_and_outro("beatbite_unfinished.mp3", "beatbite_intro.wav", "beatbite_outro.wav", "beatbite_final.wav")

class BeatBite:
    def __init__(self, news_api_key, openai_api_key, elevenlabs_api_key):
        # Load environment variables
        load_dotenv()

        # Get API keys
        self.NEWS_API_KEY = news_api_key
        self.OPENAI_API_KEY = openai_api_key
        self.ELEVENLABS_API_KEY = elevenlabs_api_key

        # Initialize NewsAPI client
        self.newsapi = NewsApiClient(api_key=self.NEWS_API_KEY)

        # Set OpenAI API key
        openai.api_key = self.OPENAI_API_KEY

    def get_user_interest(self):
        """
        Prompt the user for their interest and return it.
        Reformat phrases with spaces to hyphens.
        """
        interest = input("Please enter a topic of interest: ")
        return interest.replace(' ', '-')

    def get_news_articles(self, interest):
        """
        Make API calls to the NewsAPI for the given interest and store the response in a list.
        """
        articles = self.newsapi.get_everything(q=interest)
        news_articles = articles['articles']
        return news_articles

    def create_news_broadcast(self, news_articles):
        """
        Use the OpenAI API to create a news broadcast.
        """
        MAX_SUMMARIES = 5  # Maximum number of news summaries to include
        news_summaries = [article['description'] for article in news_articles]
        news_summaries = news_summaries[:MAX_SUMMARIES]  # Limit the number of news summaries
        prompt = f"You are writing a script from the perspective of the host of the BeatBite news network. Your name " \
                 f"is Diane, and you are a brilliant news reporter who characterizes information in a helpful and " \
                 f"interesting way. Please respond fully in character as the worlds top news reporter. You MUST begin " \
                 f"your response verbatim with 'Welcome to your BeatBite Briefing, I’m your A.I. Host Diane, " \
                 f"Here are today's top news hits in the world of ' followed by a quick and snappyGENERAL summary of " \
                 f"the news articles topics given below. This quick summary should be less than a few words, " \
                 f"YOU MUST NOT simply list all of the articles. IN NO PART OF YOUR RESPONSE SHOULD YOU LIST THE " \
                 f"TITLES OF THE ARTICLES. YOU ARE WRITING A FIRST PERSON SCRIPT FOR A NEWSCASTER WHO IS ON THE " \
                 f"RADIO, WHICH WILL BE READ FROM YOUR OUTPUT VERBATIM. Then, you must proceed to give me an " \
                 f"approximately 200 word summary of all of the news briefings providing at the end of this prompt. " \
                 f"This summary should not suggest the reader to do anything, such as read the full article, " \
                 f"or download an app. You must simply summarize the most interesting relevant information from the " \
                 f"articles and deliver it in an interesting, novel, and ACCURATE manner. Parse out the separate " \
                 f"articles and divide your response to this prompt by going from article to article. Do not mix any " \
                 f"of the information into the same section. Feel free to be creative in your delivery, but refrain " \
                 f"from any personal political comments, ensure neutrality, and do not misrepresent ANY of the " \
                 f"information. If any news articles are about a specific person, technology, piece of equipment, " \
                 f"weapon, treaty, country, etc then make sure to mention its SPECIFIC name at the BEGINNING of its " \
                 f"section - don't leave the reader wondering what you're talking about. Be excited, and don't be " \
                 f"vague. Value concision. Don't list the news articles by number - find some natural way to bounce " \
                 f"between topics. You are a real news host, so its time to act like it! Find a way to naturally " \
                 f"organize the articles, and then jump between those topics using traditional transitions. Also, " \
                 f"put two line breaks wherever you think a pause in your speech is needed (even in the same section) " \
                 f"so the topics may breathe. Put two line breaks between each section regardless. Finally, " \
                 f"you must end your response with the following VERBATIM quote, without repeating yourself: “This has been your BeatBite " \
                 f"Briefing, don't forget to stay curious, and tune back for more breaking news on your favorite topics. " \
                 f"Until next time, I've been your A.I. host Diane, signing off.” The news articles to use for your news report are as " \
                 f"follows: {news_summaries}"
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": prompt},
            ]
        )
        return response['choices'][0]['message']['content']

    def create_audio_file(self, news_broadcast):
        """
        Use the 11 labs API to create an audio file from the news broadcast.
        """
        url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.ELEVENLABS_API_KEY
        }
        data = {
            "text": news_broadcast,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }
        response = requests.post(url, json=data, headers=headers)
        with open('beatbite_unfinished.mp3', 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

    def main(self, interest):
        """
        Main function to run the program.
        """
        news_articles = self.get_news_articles(interest)
        news_broadcast = self.create_news_broadcast(news_articles)
        self.create_audio_file(news_broadcast)


if __name__ == "__main__":
    main()
