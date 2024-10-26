from flask import Flask, request, jsonify, render_template, send_file, url_for
import openai
from ttsservice import rep
from io import BytesIO
import yfinance as yf

app = Flask(__name__)

# Set your OpenAI API key here
openai.api_key = "sk-proj-qp1iW2zpD6iXZYclyfl4T3BlbkFJX3jyWZJTCUbHCgcS2JMf"
message = [{"role": "system", "content": '''You are a financial advisor and you are going to 
            explain things as of to a 10 year old with examples.'''}]

@app.route('/')
def home():
    return render_template('index1.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    message.append({"role": "user", "content": user_input})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message
    )
    # Extracting the assistant's reply
    assistant_reply = response['choices'][0]['message']['content'].strip()
    # Generate TTS audio
    audio_content = rep(assistant_reply)
    if audio_content is None:
        return jsonify({"text": assistant_reply, "audio_url": None})

    # audio = BytesIO(audio_content)
    # audio.seek(0)
    
    # return send_file(audio, mimetype='audio/mpeg', as_attachment=True, download_name='response.mp3')

    if audio_content is None:
        return jsonify({"text": assistant_reply, "audio_url": None})

    # Save the audio content to a file
    audio_filename = 'response.mp3'
    with open(audio_filename, 'wb') as f:
        f.write(audio_content)

    audio_url = url_for('static', filename=audio_filename, _external=True)
    print(audio_url)
    return jsonify({"text": assistant_reply, "audio_url":None})

# @app.route('/get_stock_price', methods=['POST'])
# def get_stock_price():
#     data = request.json
#     symbol = data['symbol']
#     lower_bound = float(data['lower_bound'])
#     upper_bound = float(data['upper_bound'])

#     stock = yf.Ticker(symbol)
#     price = stock.history(period='1d')['Close'].iloc[-1]

#     return jsonify({
#         'symbol': symbol,
#         'price': price,
#         'within_range': lower_bound <= price <= upper_bound
#     })

if __name__ == '__main__':
    app.run(debug=True)