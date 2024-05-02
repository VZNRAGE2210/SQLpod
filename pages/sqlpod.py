import ollama
import streamlit as st
#from database import Query, Response
import base64

@st.cache_data
def get_img_as_base64(file):
    with open(file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

img = get_img_as_base64("images.jpg")

page_by_img = f"""
<style>
[data-testid="stAppViewContainer"]>.main {{
    background-image: url('data:image/png;base64,{img}');
    background-size: cover;
    background-position:top left;
    background-repeat: no-repeat;
    background-attachment:loacl;
}}
[data-testid="stHeader"] {{
    background-color: rgba(0, 0, 0, 0);
}}
[data-testid="stToolbar"] {{
    right: 2rem;
}}
[data-testid="stSidebar"] > div:first-child {{
    background-image: url('data:image/png;base64,{img}');
    background-size: cover;
}}
</style>
"""

# Apply the CSS code to the Streamlit app
st.markdown(page_by_img, unsafe_allow_html=True)
st.sidebar.header("SQLPOD History...")




st.title("SQLpod")
st.sidebar.image('https://images.crunchbase.com/image/upload/c_pad,f_auto,q_auto:eco,dpr_1/mvcufghlazueuq9peryr', use_column_width=True)

# # initialize history
# if "messages" not in st.session_state:
#     st.session_state["messages"] = [
#         # set role
#         # set output
#         # and instructions
#     ]

# # init models
# if "model" not in st.session_state:
#     st.session_state["model"] = ""

# models = [model["name"] for model in ollama.list()["models"]]
# st.session_state["model"] = st.selectbox("Choose your model", models)

# def model_res_generator():
#     stream = ollama.chat(
#         model=st.session_state["model"],
#         messages=st.session_state["messages"],
#         stream=True,
#     )
#     for chunk in stream:
#         yield chunk["message"]["content"]

# # Display chat messages from history on app re-run
# for message in st.session_state.get('messages', []):
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# if prompt := st.chat_input("What is up?"):
#     # add latest message to history in format {role, content}
#     # add prompt to Query
#     # store query id in session
#     st.session_state["messages"].append({"role": "user", "content": prompt})

#     with st.chat_message("user"):
#         st.markdown(prompt)

#     with st.chat_message("assistant"):
#         message = st.write_stream(model_res_generator())
#         st.session_state["messages"].append({"role": "assistant", "content": message})
#         # extract query id from session
#         # add response to Response

# st.sidebar.title("SQLpod History")
# st.sidebar.markdown('''
#     - Basic queries
#     - Employee table info
# ''')



# Initialize history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Initialize models
if "models" not in st.session_state:
    models = [model["name"] for model in ollama.list()["models"]]
    st.session_state["models"] = models
    st.session_state["selected_model"] = models[0] if models else None

# Function to generate responses from Ollama model
def model_res_generator():
    while True:
        stream = ollama.chat(
            model=st.session_state["selected_model"],
            messages=st.session_state["messages"],
            stream=True,
        )
        for chunk in stream:
            yield chunk["message"]["content"]

# Main function to run the Streamlit app
def main():
    # Sidebar
    
    st.sidebar.markdown('''
        - Basic queries
        - Employee table info
    ''')

    # Select model
    st.session_state["selected_model"] = st.sidebar.selectbox("Choose your model", st.session_state["models"])

    # Display chat messages from history
    for message in st.session_state.get('messages', []):
        if message["role"] == "user":
            st.text(f"User: {message['content']}")
        elif message["role"] == "assistant":
            st.text(f"Assistant: {message['content']}")

    # Chat input
    prompt = st.text_input("What is up?")
    if prompt:
        prompt_persona = "You are SQLPod, a specialized assistant designed to help with SQL queries and database-related information. Your role is to understand and respond to SQL-related queries, provide database-related insights, and assist with SQL syntax and best practices. You should not engage in conversations outside this scope.also dont provide unnecessary  details just give the code"
        new_propmt=f'{prompt_persona}\n{prompt}'
        st.session_state["messages"].append({"role": "user", "content": prompt, 'full_prompt':new_propmt})
        with st.spinner("Thinking..."):
            assistant_response = next(model_res_generator())
            st.session_state["messages"].append({"role": "assistant", "content": assistant_response})
    



    with st.chat_message("assistant"):
        message = st.write_stream(model_res_generator())
        st.session_state["messages"].append({"role": "assistant", "content": message})



# Run the main function
if __name__ == "__main__":
  main()

