import streamlit as st
import google.generativeai as genai

# Initialize Gemini-Pro 
try:
    genai.configure(api_key="AIzaSyBqG_0W5UpwPKLbjKT-xcCQmEwYtlDiA9U")
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error(f"An error occurred while initializing the Gemini API: {e}")

# Gemini uses 'model' for assistant; Streamlit uses 'assistant'
def role_to_streamlit(role):
  if role == "model":
    return "assistant"
  else:
    return role

# Add a Gemini Chat history object to Streamlit session state
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history = [])

# Display Form Title
st.title("Chat with KB")
html_temp = """
<div style="background-color:cyan;padding:5px">
<h2 style="color:Black;text-align:center;font-weight:bold;">Welcome to My Chatbot</h2>
</div>
"""
st.markdown(html_temp, unsafe_allow_html=True)

# Display chat messages from history above current input box
if "chat" in st.session_state:
    for message in st.session_state.chat.history:
        with st.chat_message(role_to_streamlit(message.role)):
            st.markdown(message.parts[0].text)

# Accept user's next message, add to context, resubmit context to Gemini
if prompt := st.chat_input("I possess a well of knowledge. What would you like to know?"):
    # Display user's last message
    st.chat_message("user").markdown(prompt)
    
    # Send user entry to Gemini and read the response
    response = st.session_state.chat.send_message(prompt) 
    
    # Display last 
    with st.chat_message("assistant"):
        st.markdown(response.text)
