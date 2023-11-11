from flask import Flask, render_template, request
from transformers import BartForConditionalGeneration, BartTokenizer, MarianMTModel, MarianTokenizer

app = Flask(__name__)

# Load the summarization and translation models
summarizer_model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')
summarizer_tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')

translator_model = MarianMTModel.from_pretrained('Helsinki-NLP/opus-mt-en-de')
translator_tokenizer = MarianTokenizer.from_pretrained('Helsinki-NLP/opus-mt-en-de')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    if request.method == 'POST':
        text = request.form['text']

        # Summarize the text
        input_ids = summarizer_tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=1024, truncation=True)
        summary_ids = summarizer_model.generate(input_ids, max_length=150, min_length=50, length_penalty=2.0, num_beams=4, early_stopping=True)
        summary = summarizer_tokenizer.decode(summary_ids[0], skip_special_tokens=True)

        # Translate the summary
        translation_ids = translator_tokenizer.encode(summary, return_tensors="pt", max_length=1024, truncation=True)
        translated_summary_ids = translator_model.generate(translation_ids, max_length=150, num_beams=4, early_stopping=True)
        translated_summary = translator_tokenizer.decode(translated_summary_ids[0], skip_special_tokens=True)

        return render_template('index.html', text=text, summary=summary, translation=translated_summary)

if __name__ == '__main__':
    app.run(debug=True)
