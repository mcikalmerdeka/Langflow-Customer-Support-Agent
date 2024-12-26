import requests
import streamlit as st
from dotenv import load_dotenv
import os

# Load the environment variables
load_dotenv()

BASE_API_URL = "https://api.langflow.astra.datastax.com" # The base URL of the Langflow API
LANGFLOW_ID = os.environ.get("LANGFLOW_ID") # The flow ID to run
FLOW_ID = os.environ.get("FLOW_ID") # The flow ID to run
APPLICATION_TOKEN = os.environ.get("APP_TOKEN") # The application token to authenticate the API requests
ENDPOINT = "customer" # The endpoint name of the flow


def run_flow(message: str) -> dict:
    # The API URL to run the flow
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"

    # The payload to run the flow
    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }

    # The headers to run the flow
    headers = {"Authorization": "Bearer " + APPLICATION_TOKEN, "Content-Type": "application/json"}
    
    # Make a POST request to run the flow
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

def main():
    st.title("Customer Support Chat Interface")

    # Display the instructions in an expander
    with st.expander("Application Instructions"):
        st.markdown(
            """
            1. Enter a message in the text area.
            2. Click on the "Run Flow" button.
            3. The model response message will be displayed below.
            """
        )
    
    # Get the message from the user
    message = st.text_area("Message", placeholder="Ask something here...")
    
    if st.button("Run Flow"):
        if not message.strip(): # check if the message is empty
            st.error("Please enter a message")
            return
    
        try:
            with st.spinner("Running flow..."): # show a spinner while the flow is running
                response = run_flow(message) # run the flow
            
            response = response["outputs"][0]["outputs"][0]["results"]["message"]["text"] # get the response message
            st.markdown(response) # show the response message
        except Exception as e:
            st.error(str(e))

if __name__ == "__main__":
    main()