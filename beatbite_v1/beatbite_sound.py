from beatbite import BeatBite

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

if __name__ == "__main__":
    main()
