"""
Untuk jalankan,

streamlit run chatbot1.py
"""

import os

import streamlit as st
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# Bikin judul
st.title("ChatBot Desa Tuntungpait")

st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 500px !important; # Set the width to your desired value
            iframe style="width:500px"{
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# Cek apakah API key sudah ada
if "GOOGLE_API_KEY" not in os.environ:
    # Jika belum, minta user buat masukin API key
    st.sidebar.markdown("# Masukkan Google API Key anda untuk mulai")
    google_api_key = st.sidebar.text_input("Google API Key", type="password")
    # User harus klik Start untuk save API key
    start_button = st.sidebar.button("Start")

    if start_button:
        os.environ["GOOGLE_API_KEY"] = google_api_key
        st.rerun()
  # Jangan tampilkan chat dulu kalau belum pencet start
    st.stop()

# Inisiasi client LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

# Cek apakah data sebelumnya ttg message history sudah ada
if "messages_history" not in st.session_state:
    # Jika belum, bikin datanya, isinya hanya system message dulu
    st.session_state["messages_history"] = [
        SystemMessage(
            "You are a village government employee in Tuntungpait village, and you manage population data and population needs such as KTP, KK, BPJS, SPTM and others. Always response in less than 3 sentences in a chat style. Reply in bahasa indonesia"
        )
    ]

st.text("Dengan Pemdes AI, ada yang bisa aku bantu?")
st.text("Jangan lupa isi nama lengkap terlebih dahulu ya!")
# Jika messages_history sudah ada, tinggal di load aja
messages_history = st.session_state["messages_history"]


# Tampilkan messages history selama ini
for message in messages_history:
    # Tdk perlu tampilkan system message
    if type(message) is SystemMessage:
        continue
    # Pilih role, apakah user/AI
    role = "User" if type(message) is HumanMessage else "AI"
    # Tampikan chatnya!
    with st.chat_message(role):
        st.markdown(message.content)


# Baca prompt terbaru dari user perkenalan

prompt = st.chat_input("Chat with Pemdes AI")   
# Jika user tdk ada prompt, stop aja
if not prompt:
    st.stop()

# Jika user ada prompt, tampilkan promptnya langsung
with st.chat_message("User"):
    st.markdown(prompt)
# Masukin prompt ke message history, dan kirim ke LLM
messages_history.append(HumanMessage(prompt))
response = llm.invoke(messages_history)

# Simpan jawaban LLKM ke message history
messages_history.append(response)
# Tampilkan langsung jawaban LLM
with st.chat_message("AI"):
    st.markdown(response.content)

st.button("Bersihkan riwayat", on_click=lambda: st.session_state.pop("messages_history"))

# Tambahin sidebar ttg aplikasi
st.sidebar.title("Tentang Pemdes AI")
st.sidebar.markdown(
    """
    Aplikasi chatbot sederhana untuk membantu warga Desa Tuntungpait dalam mengakses informasi terkait data kependudukan dan kebutuhan administrasi seperti KTP, KK, BPJS, dll.

    Dibuat dengan Streamlit dan Langchain menggunakan model Google Gemini 2.0 Flash.

    Terima kasih telah menggunakan Pemdes AI!
    """
)