import streamlit as st
import requests

# Set up the Streamlit app
st.title("Chatbot with Flask Backend")

# Initialize session state to store chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello! How can I assist you today?"}]

# Chat history display
st.write("### Chat History")
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        if message["role"] == "user":
            st.write(f"**You:** {message['content']}")
        else:
            st.write(f"**Bot:** {message['content']}")

# Input box for user message
user_message = st.chat_input("Type your message here")

if user_message:
    if user_message.strip():
        with st.chat_message("user"):
                st.markdown(user_message)
        # Add user message to chat history
        st.session_state["messages"].append({"role": "user", "content": user_message})

        # Send user message to the Flask backend
        try:
            response = requests.post(
                "http://localhost:5000/generate",  # Flask backend URL
                json={"prompt": user_message},
                timeout=60,
            )
            if response.status_code == 200:
                # Get the bot's response from the Flask backend
                bot_response = response.json().get("generated_content", "Sorry, I couldn't understand that.")
            else:
                bot_response = "Error: Could not reach the backend."

        except requests.exceptions.RequestException as e:
            bot_response = f"Error: {str(e)}"

        # Add bot response to chat history
        st.session_state["messages"].append({"role": "assistant", "content": bot_response})
        with st.chat_message("assistant"):
            st.markdown(bot_response)

    else:
        st.warning("Please enter a message before sending.")

