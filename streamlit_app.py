import streamlit as st
from openai import OpenAI


st.title("📄 Document question answering")
st.write(
    "Upload a document below and ask a question about it – GPT will answer! "
    "To use this app, you need to provide an OpenAI API key, which you can get "
    "[here](https://platform.openai.com/account/api-keys). "
)


openai_api_key = st.text_input("OpenAI API Key", type="password")


if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
    st.stop()


need_validate = (
    "last_key" not in st.session_state
    or st.session_state["last_key"] != openai_api_key
    or "api_valid" not in st.session_state
)

if need_validate:
    try:
        client = OpenAI(api_key=openai_api_key)
        
        _ = client.models.list()

        
        st.session_state["api_valid"] = True
        st.session_state["last_key"] = openai_api_key
        st.session_state["client"] = client
        st.success("✅ API key is valid!")
    except Exception as e:
        
        st.session_state["api_valid"] = False
        st.session_state["last_key"] = openai_api_key
        st.error("❌ Invalid OpenAI API key or network error. Please check and try again.")
        st.stop()


client = st.session_state.get("client", OpenAI(api_key=openai_api_key))


uploaded_file = st.file_uploader(
    "Upload a document (.txt or .md)", type=("txt", "md")
)

question = st.text_area(
    "Now ask a question about the document!",
    placeholder="Can you give me a short summary?",
    disabled=not uploaded_file,
)

if uploaded_file and question:
    document = uploaded_file.read().decode()
    messages = [
        {
            "role": "user",
            "content": f"Here's a document: {document} \n\n---\n\n {question}",
        }
    ]

    stream = client.chat.completions.create(
        model="gpt-5-chat-latest",   
        messages=messages,
        stream=True,
    )
    st.write_stream(stream)
