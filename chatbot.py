# ============================================================
# AI CHATBOT using Groq API + Streamlit
# Skills: Python, LLM, Groq API, Streamlit
# Run: streamlit run chatbot.py
# ============================================================

import streamlit as st
from groq import Groq

# ── Page Config ──
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# ── Custom CSS ──
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #58a6ff, #bf91f3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
    .subtitle {
        text-align: center;
        color: #8b949e;
        font-size: 0.95rem;
        margin-bottom: 2rem;
    }
    .stChatMessage { border-radius: 12px; margin: 0.5rem 0; }
    </style>
""", unsafe_allow_html=True)

# ── Title ──
st.markdown('<div class="main-title">🤖 AI Chatbot</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Powered by Groq LLaMA 3 · Built by Mrinmoy Golder</div>', unsafe_allow_html=True)

# ── Sidebar ──
with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input(
        "🔑 Groq API Key",
        type="password",
        placeholder="gsk_...",
        help="Get your free key at console.groq.com"
    )
    model = st.selectbox(
        "🧠 Model",
        ["llama3-8b-8192", "llama3-70b-8192", "mixtral-8x7b-32768"],
        help="LLaMA 3 8B is fastest, 70B is smartest"
    )
    temperature = st.slider("🌡️ Creativity", 0.0, 1.0, 0.7, 0.1,
                           help="Higher = more creative responses")
    
    st.divider()
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.markdown("**About**")
    st.markdown("Built with [Groq API](https://console.groq.com) + [Streamlit](https://streamlit.io)")
    st.markdown("by [Mrinmoy Golder](https://github.com/mrinmoyBytes)")

# ── System Prompt ──
SYSTEM_PROMPT = """You are a helpful, friendly and intelligent AI assistant. 
You provide clear, accurate and concise answers. 
You are knowledgeable about technology, programming, machine learning, and general topics.
When asked about code, you provide clean and well-commented examples.
You are built by Mrinmoy Golder using the Groq API and Streamlit."""

# ── Initialize Chat History ──
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Display Chat History ──
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ── Chat Input ──
if prompt := st.chat_input("💬 Ask me anything..."):
    if not api_key:
        st.error("⚠️ Please enter your Groq API key in the sidebar first!")
        st.stop()

    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking..."):
            try:
                client = Groq(api_key=api_key)

                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        *[{"role": m["role"], "content": m["content"]}
                          for m in st.session_state.messages]
                    ],
                    temperature=temperature,
                    max_tokens=1024,
                )

                reply = response.choices[0].message.content
                st.markdown(reply)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": reply
                })

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("💡 Make sure your API key is correct from console.groq.com")

# ── Empty state ──
if not st.session_state.messages:
    st.markdown("""
    <div style='text-align:center; color:#8b949e; padding: 3rem 0;'>
        <h3>👋 Hello! I'm your AI Assistant</h3>
        <p>Ask me anything — coding, ML, general knowledge, or just chat!</p>
        <br>
        <p>💡 <b>Try asking:</b></p>
        <p>• "Explain machine learning in simple terms"</p>
        <p>• "Write a Python function to reverse a string"</p>
        <p>• "What is the difference between AI and ML?"</p>
    </div>
    """, unsafe_allow_html=True)
