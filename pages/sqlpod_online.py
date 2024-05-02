import streamlit as st
import google.generativeai as genai
import os

genai.configure(api_key=os.environ["GEMINI_API_KEY"])


top_p = st.slider("Adjust top p", min_value=0.0, max_value=1.0, value=.95,)
top_k = st.slider("Adjust top k", min_value=0.0, max_value=1.0, value=0.0)
temperature = st.slider("Adjust temperature", min_value=0.0, max_value=1.0, value=1.0,step=.1)

# Set up the model
generation_config = {
  "temperature": temperature,
  "top_p": top_p,
  "top_k": top_k,
  "max_output_tokens": 8192,
}

st.write("Adjusted top p:", top_p)
st.write("Adjusted top k:", top_k)
st.write("Adjusted temperature:", temperature)





safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]
system_instruction = "You are SQLPod, a specialized assistant designed to help with SQL queries and database-related information. Your role is to understand and respond to SQL-related queries, provide database-related insights, and assist with SQL syntax and best practices.Only generate the query of the sql only with a single line descriptions for them . You should not engage in conversations outside this scope.\n  "
model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              system_instruction=system_instruction,
                              safety_settings=safety_settings)
convo = model.start_chat(history=[])
def LLM_Response(question):
    response = convo.send_message(question,stream=False)
    return response
query = st.chat_input("hi")
if query:
    result = LLM_Response(query)
    st.subheader("Response : ")
    for word in result:
        st.markdown(word.text)