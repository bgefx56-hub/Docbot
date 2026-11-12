
import streamlit as st
from pypdf import PdfReader
from docx import Document
from openai import OpenAI
import os

MODEL = "gemini-flash-latest"

st.set_page_config(
    page_title="DocBot",
        page_icon="📚",
            layout="wide"
            )
st.title("📚 DocBot")
st.caption("Your Documents. Your Knowledge. One Conversation.")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
        st.error("Gemini API key not configured.")
        st.stop()

client = OpenAI(api_key=api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

def read_file(f):
        if f.name.endswith(".pdf"):
                 return "\n".join(p.extract_text() or ""    for p in PdfReader(f).pages)

        elif f.name.endswith(".docx"):
                 return "\n".join(p.text for p in Document(f).paragraphs)

        else:
             return f.getvalue().decode("utf-8", errors="ignore")


if "chat" not in st.session_state:
          st.session_state.chat = []

st.subheader("Upload your document")

f = st.file_uploader("Choose PDF, DOCX or TXT",type=["pdf", "docx", "txt"])

if f:
    if st.session_state.get("name") != f.name:
            st.session_state.name = f.name
            st.session_state.text = read_file(f)
            st.session_state.chat = []

    st.success(f"Document loaded: {f.name}")
    if not st.session_state.text.strip():
            st.warning("No readable text found in this document.")

if "text" in st.session_state and st.session_state.text.strip():

                st.divider()
                st.subheader("Chat with your document")

                for m in st.session_state.chat:
                        with st.chat_message(m["role"]):
                                st.write(m["content"])

                q= st.chat_input("Ask anything about your document..")
                if q:
                    st.session_state.chat.append({ "role": "user", "content": q})

                    with st.chat_message("user"):
                        st.write(q)

                    with st.chat_message("assistant"):
                        with st.spinner("Thinking..."):
                            try:
                                response = client.chat.completions.create(
                                                                        model=MODEL,
                                                                        messages=[{ "role": "system","content": ("Answer only using the document. "
                                                                                                            "If the answer is absent, say you don't know.\n\n"
                                                                                                                                                + st.session_state.text[:100000]
                                                                                                                                                                                )
                                                                                                                                                                                                            },
                                                                                                                                                                                                                                        *st.session_state.chat
                                                                                                                                                                                                                                                                ]
                                                                                                                                                                                                                                                                                    )
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                

                                
                                answer = response.choices[0].message.content
                                st.write(answer)

                                st.session_state.chat.append({"role": "assistant","content": answer})
                                                                                                                                                                

                            except Exception as e:
                                st.error(f"Error: {e}")
                                st.session_state.chat.pop()
                                
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
                                                                                                                                                                                                                                                        