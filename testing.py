import os
from dotenv import load_dotenv
from google.cloud import dialogflow_v2 as dialogflow

load_dotenv()

def test_connection():
    try:
        project_id = os.getenv("DIALOGFLOW_PROJECT_ID")
        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(project_id, "test-session")
        print("✅ Connection Successful! Your JSON file is working.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_connection()