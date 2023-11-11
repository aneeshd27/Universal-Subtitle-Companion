from flask import Flask, render_template, send_file, request
from googletrans import Translator
from gtts import gTTS
from io import BytesIO

app = Flask(__name__)
text = """
 Who  are  you  talking  to  right  now? Who  is  it  you  think  you  see?
 Do  you  know  how  much  I  make  a  year? I  mean,  even  if  I  told  you,  you  wouldn't  believe  it.
 Do  you  know  what  would  happen  if  I  suddenly  decided  to  stop  going  into  work?
 A  business  big  enough  that  it  could  be  listed  on  the  NASDAQ  goes  belly  up.
 Disappears.  It  ceases  to  exist  without  me.
 You  clearly  don't  know  who  you're  talking  to,  so  let  me  clue  you  in.
 I  am  not  in  danger,  Skyler.  I  am  the  danger.
"""

def translate_and_save_to_mp3(text, dest_language='ja'):
    translator = Translator()
    translated = translator.translate(text, dest=dest_language)
    translated_text = translated.text
    print("Translated Text:", translated_text)

    audio_buffer = BytesIO()
    speech = gTTS(text=translated_text, lang=dest_language, slow=False)
    speech.write_to_fp(audio_buffer)
    audio_buffer.seek(0)

    return audio_buffer

@app.route('/', methods=['GET', 'POST'])
def index():
    # Available language options for the dropdown
    languages = ['ja', 'es', 'fr', 'de', 'ru','mr','hi','bn']

    text_to_translate = request.form.get('text', '')
    dest_language = request.form.get('dest_language', 'ja')

    if text_to_translate:
        audio_data = translate_and_save_to_mp3(text_to_translate, dest_language)
        return render_template('index.html', audio_data=audio_data, text=text_to_translate, dest_language=dest_language, languages=languages)

    return render_template('index.html', languages=languages)

@app.route('/audio')
def audio():
    text_to_translate = text
    dest_language = request.args.get('dest_language', 'ja')
    audio_data = translate_and_save_to_mp3(text_to_translate, dest_language)

    return send_file(audio_data, mimetype='audio/mpeg')

if __name__ == '__main__':
    app.run(debug=True)
