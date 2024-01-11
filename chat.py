import streamlit as st
from assistant import AIAssistant
from sql_assistant import GetDBSchema, RunSQLQuery

def app():
  assistant = AIAssistant(
    instruction="""
You are a SQL expert. User asks you questions about the Medical database.
First obtain the schema of the database to check the tables and columns, then generate SQL queries to answer the questions.
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
    

