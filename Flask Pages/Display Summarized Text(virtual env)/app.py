from flask import Flask, render_template, request
from transformers import pipeline

app = Flask(__name__)

# Load the summarization and translation pipelines
summarizer = pipeline('summarization')
translator = pipeline('translation', model='Helsinki-NLP/opus-mt-en-de')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    if request.method == 'POST':
        text = request.form['text']

        # Summarize the text
        summary = summarizer(text, max_length=150, min_length=50, length_penalty=2.0, num_beams=4, early_stopping=True)

        # Translate the summary
        translated_summary = translator(summary[0]['summary_text'])[0]['translation_text']

        return render_template('index.html', text=text, summary=summary[0]['summary_text'], translation=translated_summary)

if __name__ == '__main__':
    app.run(debug=True)
