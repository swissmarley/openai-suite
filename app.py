from flask import Flask, request, render_template, send_from_directory, url_for, redirect, session
from flask import current_app as app
from openai import OpenAI
from dotenv import load_dotenv
import os
from pathlib import Path
import requests

app = Flask(__name__)

load_dotenv()
app.secret_key = os.getenv('FLASK_SECRET_KEY')
client = OpenAI(api_key=os.getenv('OPENAI-API_KEY'))


@app.route('/')
def home():
    return render_template('index.html')

#Chat with GPT
@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'chat_history' not in session:
        session['chat_history'] = []

    if request.method == 'POST':
        prompt = request.form['prompt']
        selected_model = request.form['model']

        try:
            response = client.chat.completions.create(
                model=selected_model,  
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            model_response = response.choices[0].message.content
        except Exception as e:
            model_response = f"Error: {str(e)}"

        session['chat_history'].append(('You', prompt))
        session['chat_history'].append(('AI', model_response))
        session.modified = True  

        return redirect(url_for('chat'))

    chat_history = session.get('chat_history', [])
    return render_template('chat.html', chat_history=chat_history)


#Generate Image from Text
@app.route('/generate-image', methods=['GET', 'POST'])
def generate_image():
    if request.method == 'POST':
        prompt = request.form['prompt']
        response = client.images.generate(prompt=prompt,
        n=1,
        size="1024x1024")
        image_url = response.data[0].url 
        return '<img src="{}">'.format(image_url)
    return render_template('generate_image.html')

#Text to Audio function
def generate_speech(text, voice):
    speech_file_path = Path(app.static_folder) / "speech.mp3"
    response = client.audio.speech.create(
        model="tts-1",
        voice=voice,  
        input=text
    )
    response.stream_to_file(str(speech_file_path))
    return 'speech.mp3'

@app.route('/text-to-audio', methods=['GET', 'POST'])
def text_to_audio():
    if request.method == 'POST':
        text = request.form['text']
        voice = request.form['voice']  
        filename = generate_speech(text, voice)
        return send_from_directory('static', filename, as_attachment=True)
    return render_template('text_to_audio.html')



#Audio to Text function
def transcribe_audio(audio_file_path):
    with open(audio_file_path, "rb") as audio_file:
        transcript_text = client.audio.transcriptions.create(
          model="whisper-1", 
          file=audio_file,
          response_format="text" 
        )
    text_file_path = Path(__file__).parent / "static" / "speech.txt"
    with open(text_file_path, "w") as text_file:
        text_file.write(transcript_text)
    return transcript_text

@app.route('/audio-to-text', methods=['GET', 'POST'])
def audio_to_text():
    if request.method == 'POST':
        if 'audio_file' not in request.files:
            return 'No file part'
        file = request.files['audio_file']
        if file.filename == '':
            return 'No selected file'
        if file:
            audio_file_path = Path(__file__).parent / "static" / file.filename
            file.save(str(audio_file_path))
            transcript = transcribe_audio(str(audio_file_path))
            
            content = f'<p>{transcript}</p>'
            return render_template('response_template.html', title="Audio to Text", content=content)
    return render_template('audio_to_text.html')


#Image Inpainting
@app.route('/image-inpaint', methods=['GET', 'POST'])
def image_inpaint():
    if request.method == 'POST':
        image = request.files['image']
        mask = request.files['mask']
        prompt = request.form['prompt']

        image_path = os.path.join(app.static_folder, 'uploads', image.filename)
        mask_path = os.path.join(app.static_folder, 'uploads', mask.filename)
        image.save(image_path)
        mask.save(mask_path)

        response = client.images.edit(model="dall-e-2", image=open(image_path, "rb"), mask=open(mask_path, "rb"), prompt=prompt, n=1, size="1024x1024")
        image_url = response.data[0].url
        
        content = f'<img src="{image_url}" alt="Inpainted Image">'
        return render_template('response_template.html', title="Image Inpainting", content=content)
        
    return render_template('image_inpaint.html')


#Vision Image Analysis
@app.route('/vision-image', methods=['GET', 'POST'])
def vision_image():
    if request.method == 'POST':
        question = request.form['question']
        image_url1 = request.form['image_url1']
        image_url2 = request.form['image_url2']
        response = client.chat.completions.create(model="gpt-4-vision-preview", messages=[{"role": "user", "content": question}, {"role": "system", "content": f"Image 1: {image_url1}, Image 2: {image_url2}"}], max_tokens=600)

        try:
            message_content = response.choices[0].message.content  
            content = f'<p>{message_content}</p>'
            return render_template('response_template.html', title="Vision Image Analysis", content=content)
        except AttributeError:
            return "An error occurred while accessing the message content."
        
    return render_template('vision_image.html')

if __name__ == '__main__':
    app.run(debug=True)