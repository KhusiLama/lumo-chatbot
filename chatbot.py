import streamlit as st
import os
import random
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

st.set_page_config(page_title="Lumo Chat", layout="centered")
st.title("💡 Lumo – Your Friendly Chat Companion")

quotes = [
    "You're doing better than you think. Keep going. 🌟",
    "This too shall pass. One step at a time. 💪",
    "You’ve survived 100% of your bad days. That’s a perfect record. 📈",
    "Every storm runs out of rain. ⛈️☀️",
    "Even the darkest night will end and the sun will rise. 🌅"
]

jokes = [
    "Why don't scientists trust atoms? Because they make up everything. 🤓",
    "I'm reading a book on anti-gravity. It's impossible to put down! 📘",
    "Why did the math book look sad? It had too many problems. ➕➖",
    "Not to brag, but I just went into another room and remembered why. 🧠"
]

emoji_reactions = ["😊", "💖", "😄", "🙌", "🤗", "🌈", "🫶"]

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "bot", "text": "Hey 👋 I'm **Lumo**. Here to talk or listen. How are you feeling today?"}
    ]

for msg in st.session_state.messages:
    with st.chat_message("assistant" if msg["role"] == "bot" else "user"):
        st.markdown(msg["text"])
        if msg["role"] == "bot":
            st.markdown(f"<div style='font-size:20px;'>{random.choice(emoji_reactions)}</div>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("😂 Need a Joke"):
        joke = random.choice(jokes)
        st.session_state.messages.append({"role": "bot", "text": joke})
        st.chat_message("assistant").markdown(joke)
with col2:
    if st.button("🌟 Send Quote"):
        quote = random.choice(quotes)
        st.session_state.messages.append({"role": "bot", "text": quote})
        st.chat_message("assistant").markdown(quote)

user_input = st.chat_input("Talk to Lumo...")

if user_input:
    st.session_state.messages.append({"role": "user", "text": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    prompt = f"""
    You're Lumo, a friendly, emotionally intelligent chatbot.
    Respond warmly, casually, and supportively to the user's message.
    Message: "{user_input}"
    """

    try:
        response = model.generate_content(prompt)
        reply = response.text
    except:
        reply = "Oops! Something went wrong. Try again in a moment."

    st.session_state.messages.append({"role": "bot", "text": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)
        st.markdown(f"<div style='font-size:20px;'>{random.choice(emoji_reactions)}</div>", unsafe_allow_html=True)
