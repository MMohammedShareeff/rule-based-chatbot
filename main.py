import os

from flask import Flask, render_template, request, jsonify
from google.cloud import dialogflow_v2 as dialogflow
from dotenv import load_dotenv

app = Flask(__name__)

# PROJECT_ID = os.getenv("PROJECT_ID")
PROJECT_ID = "ppu-helper-r9hm"
GOOGLE_API_KEY = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
LANGUAGE_CODE = "ar"  # Arabic


def get_dialogflow_response(project_id, session_id, text):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.types.TextInput(text=text, language_code=LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)

    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
        return response.query_result.fulfillment_text
    except Exception as e:
        print(f"Error connecting to Dialogflow: {e}")
        return "عذراً، حدث خطأ في الاتصال بالمساعد الذكي."


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/get_response', methods=['POST'])
def get_response():
    # Matches the 'msg' key from your JavaScript formData
    msg = request.form.get('msg')

    if not msg:
        return jsonify({'reply': 'لم يتم استلام نص'})


    session_id = "ppu-user-session-001"

    reply = get_dialogflow_response(PROJECT_ID, session_id, msg)

    return jsonify({'reply': reply})


if __name__ == "__main__":
    app.run(debug=True, port=5000)