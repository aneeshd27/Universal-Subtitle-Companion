from flask import Flask, render_template, request
from googletrans import Translator
from gtts import gTTS
import random

app = Flask(__name__)

# A longer paragraph of text for the textarea
default_text = """Who are you talking to right now? Who is it you think you see?
Do you know how much I make a year? I mean, even if I told you, you wouldn't believe it.
Do you know what would happen if I suddenly decided to stop going into work?
A business big enough that it could be listed on the NASDAQ goes belly up.
Disappears. It ceases to exist without me.
You clearly don't know who you're talking to, so let me clue you in.
I am not in danger, Skyler. I am the danger."""

def translate_and_save_to_mp3(text, dest_language='mr', mp3_filename='/content/WALTER_WHITE.mp3'):
    # Translate the text
    translator = Translator()
    translated = translator.translate(text, dest=dest_language)

    # Output the translated text
    translated_text = translated.text

    # Convert the translated text to speech and save to an MP3 file
    

    return translated_text

@app.route('/', methods=['GET', 'POST'])
def index():
    translated_text = None

    # Use the longer paragraph as the default text for the textarea
    text_to_translate = default_text

    if request.method == 'POST':
        text_to_translate = request.form['text_to_translate']
        dest_language = request.form['dest_language']
        translated_text = translate_and_save_to_mp3(text_to_translate, dest_language)

    return render_template('index.html', text_to_translate=text_to_translate, translated_text=translated_text)

if __name__ == '__main__':
    app.run(debug=True)
