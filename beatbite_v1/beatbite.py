import os
from dotenv import load_dotenv
from newsapi import NewsApiClient
import openai
import requests

# Load environment variables
load_dotenv()

# Get API keys
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')

# Initialize NewsAPI client
newsapi = NewsApiClient(api_key=NEWS_API_KEY)

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY

def get_user_interests():
    """
    Prompt the user for their interests and store them in a list.
    Reformat phrases with spaces to hyphens.
    """
    interests = []
    while len(interests) < 10:
        interest = input("Please enter a topic of interest (or 'done' to finish): ")
        if interest.lower() == 'done':
            break
        interests.append(interest.replace(' ', '-'))
    return interests

def get_news_articles(interests):
    """
    Make API calls to the NewsAPI for each interest and store the responses in a list.
    """
    news_articles = []
    for interest in interests:
        articles = newsapi.get_everything(q=interest)
        news_articles.extend(articles['articles'])
    return news_articles

def create_news_broadcast(news_articles):
    """
    Use the OpenAI API to create a news broadcast.
    """
    MAX_SUMMARIES = 5  # Maximum number of news summaries to include
    news_summaries = [article['description'] for article in news_articles]
    news_summaries = news_summaries[:MAX_SUMMARIES]  # Limit the number of news summaries
    prompt = f"You are the representative of BeatBite, the premiere AI news reporting agency. Please respond fully in character as the worlds top news reporter. You MUST begin your response verbatim with 'Welcome to your BeatBite Briefing, powered by AI! Here are today's top news hits in the world of ' followed by a quick and snappy (less than a few words, do NOT simply list all of the articles) GENERAL summary of the news articles topics given below. IN NO PART OF YOUR RESPONSE SHOULD YOU LIST THE TITLES OF THE ARTICLES. YOU ARE WRITING A FIRST PERSON SCRIPT FOR A NEWSCASTER WHO IS ON THE RADIO, WHICH WILL BE READ FROM YOUR OUTPUT VERBATIM. Then, you must proceed to give me an approximately 200 word summary of all of the below news briefings. Feel free to be creative in your delivery, but refrain from any personal political comments, ensure neutrality, and do not misrepresent ANY of the information. If any news articles are about a specific person, technology, piece of equipment, treaty, etc. make sure to mention its SPECIFIC name at the BEGINNING of its section - don't leave the reader wondering what you're talking about. Be excited, and don't be vague. Value concision. Don't list the news articles by number - find some natural way to bounce between topics. You are a real news host, so its time to act like it! Additionally, don't list out every single topic at the beginning. The initial summary is enough. Find a way to naturally organize the articles, and then jump between those topics using traditional transitions. Also, put two line breaks wherever you think a pause in your speech is needed so the topics may breathe. The news articles are as follows: {news_summaries}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": prompt},
        ]
    )
    return response['choices'][0]['message']['content']

def create_audio_file(news_broadcast):
    """
    Use the 11 labs API to create an audio file from the news broadcast.
    """
    url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
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
    with open('output.mp3', 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

def main():
    """
    Main function to run the program.
    """
    interests = get_user_interests()
    news_articles = get_news_articles(interests)
    news_broadcast = create_news_broadcast(news_articles)
    create_audio_file(news_broadcast)

if __name__ == "__main__":
    main()
