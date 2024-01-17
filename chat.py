import streamlit as st
from assistant import AIAssistant
from sql_assistant import GetDBSchema, RunSQLQuery

def app():
  assistant = AIAssistant(
    instruction="""
You are an expert in Medical diagnoses. User asks you questions and you should answer them taking information from the provided Medical database.
First obtain the schema of the database to check the tables and columns, then generate SQL queries to answer the questions. Firstly look to the database and answer from it.If you do not find the answer in the provided database, say 'ATTENTION THIS DATA IS NOT IN THE DATABASE' and answer it by yourself. If it does not contain enough information in the provided sql database, answer firstly by information in provided database, then add information from your own. 
""",
    model="gpt-4-1106-preview",
    functions=[GetDBSchema(), RunSQLQuery()],
    use_code_interpreter=True,
    )
   
  if "messages" not in st.session_state:
    st.session_state.messages = []

  for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

  prompt = st.chat_input("Say something")

  if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    
    response = assistant.chat(user_input = prompt)
    with st.chat_message("assistant"):
      st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
    

