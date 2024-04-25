import streamlit as st
import google.generativeai as genai
import os

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Set up the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 0,
  "max_output_tokens": 8192,
}

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

convo = model.start_chat(history=[
  {
    "role": "user",
    "parts": ["how to make a mango shake"]
  },
  {
    "role": "model",
    "parts": ["```sql\n-- This query is not possible as it is not a valid SQL query \nSELECT 'This is not possible, I can only help with SQL related queries'\n```"]
  },
  {
    "role": "user",
    "parts": ["How to make a primary key"]
  },
  {
    "role": "model",
    "parts": ["```sql\n-- Creating a table with a primary key\nCREATE TABLE users (\n    id INT PRIMARY KEY,\n    username VARCHAR(50) UNIQUE,\n    email VARCHAR(100) UNIQUE\n);\n```"]
  },
  {
    "role": "user",
    "parts": ["how to join two tables"]
  },
  {
    "role": "model",
    "parts": ["```sql\n-- Joining two tables (users and orders) based on a common column (user_id)\nSELECT *\nFROM users\nINNER JOIN orders ON users.id = orders.user_id;\n```"]
  },
  {
    "role": "user",
    "parts": ["how to delete the sql query"]
  },
  {
    "role": "model",
    "parts": ["```sql\n-- Deleting rows from a table (users) based on a condition (id = 123)\nDELETE FROM users WHERE id = 123; \n```"]
  },
])

query = st.chat_input("hi")
if query:
    convo.send_message(query)
    st.chat_message(convo.last.text)