import streamlit as st
import traceback

# Import your orchestrator from Phase 2
from westmarch.orchestrator.workflows import WestmarchOrchestrator
from westmarch.agents.jeeves import JeevesAgent
from westmarch.agents.perkins import PerkinsAgent
from westmarch.agents.miss_pennington import MissPenningtonAgent
from westmarch.agents.lady_hawthorne import LadyHawthorneAgent
from westmarch.core.models import ModelClient


# ------------------------------------
# Configuration
# ------------------------------------
DEBUG_MODE = False  # Set to True to see debug messages

# Use simpler emojis that work reliably across all platforms
AGENT_AVATARS = {
    "user": "👤",              # The Patron
    "Jeeves": "🎩",            # Head Butler
    "Perkins": "📚",           # Research Footman
    "Miss Pennington": "✒️",   # Scribe & Archivist
    "Lady Hawthorne": "🕯️",   # Dowager Countess
    "assistant": "🏰",         # Fallback household emblem
}


# ------------------------------------
# Initialize Backend Westmarch Agents
# ------------------------------------
@st.cache_resource
def initialize_agents():
    """Initialize agents once and cache them."""
    jeeves = JeevesAgent(ModelClient(agent_name="Jeeves"))
    perkins = PerkinsAgent(ModelClient(agent_name="Perkins"))
    pennington = MissPenningtonAgent(ModelClient(agent_name="Miss Pennington"))
    hawthorne = LadyHawthorneAgent(ModelClient(agent_name="Lady Hawthorne"))
    return jeeves, perkins, pennington, hawthorne


# -----------------------------
# Session State Initialization
# -----------------------------
if "orchestrator" not in st.session_state:
    jeeves, perkins, pennington, hawthorne = initialize_agents()
    st.session_state.orchestrator = WestmarchOrchestrator(
        jeeves=jeeves,
        perkins=perkins,
        pennington=pennington,
        hawthorne=hawthorne,
    )

if "messages" not in st.session_state:
    st.session_state.messages = []


# ------------------------------------
# Custom CSS — Westmarch UI Refinement
# ------------------------------------
st.markdown(
    """
    <style>
        /* Import the EB Garamond font from Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;500;600;700&display=swap');

        /* Apply EB Garamond to the whole app */
        html, body, [class*="css"] {
            font-family: 'EB Garamond', serif;
        }

        /* Force sidebar text to use the font */
        [data-testid="stSidebar"] * {
            font-family: 'EB Garamond', serif !important;
        }

        /* Sidebar width */
        [data-testid="stSidebar"] {
            width: 340px;
        }
        [data-testid="stSidebar"] > div:first-child {
            width: 340px;
        }       

        /* Chat message styling */
        /* User messages - Royal purple background */
        [data-testid="stChatMessageContainer"] [data-testid="stChatMessage"]:has(div[data-testid="stChatMessageContent"]:first-child) {
            background-color: #5b1fa6;
        }
        
        /* User message text - white for contrast */
        [data-testid="stChatMessageContainer"] [data-testid="stChatMessage"]:has(div[data-testid="stChatMessageContent"]:first-child) p {
            color: #ffffff;
        }

        /* Assistant messages - Soft lilac background */
        [data-testid="stChatMessageContainer"] [data-testid="stChatMessage"]:not(:has(div[data-testid="stChatMessageContent"]:first-child)) {
            background-color: #f6f1ff;
        }

        /* Avatar container styling */
        .stChatMessage [data-testid="stAvatarContainer"] {
            border-radius: 50%;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# -----------------------------
# Sidebar Controls
# -----------------------------
with st.sidebar:
    st.markdown("## 🏰 The House of Westmarch")
    st.markdown(
        '<em style="font-family:EB Garamond; font-size:16px;">Pray, command your staff — the estate awaits your direction.</em>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown(
        '<h3 style="font-family:EB Garamond; font-weight:600;">The Estate\'s Available Services:</h3>',
        unsafe_allow_html=True
    )

    mode = st.radio(
        "Choose Mode",
        [
            "Parlour Discussions (General Conversation)",
            "Arrangements for the Day",
            "Matters Requiring Investigation",
            "Correspondence & Drafting",
            "Records & Summaries from the Archive",
            "Her Ladyship's Critique (Proceed with Caution)",
        ],
        label_visibility="collapsed",
    )

    st.markdown("---")
    
    # Clear conversation button
    if st.button("🔄 Clear Conversation"):
        st.session_state.messages = []
        st.rerun()


# -----------------------------
# Display Conversation History
# -----------------------------
for msg in st.session_state.messages:
    role = msg.get("role", "assistant")
    content = msg.get("content", "")
    speaker = msg.get("speaker", "user" if role == "user" else "assistant")
    
    avatar_key = "user" if role == "user" else speaker
    avatar = AGENT_AVATARS.get(avatar_key, AGENT_AVATARS["assistant"])

    with st.chat_message(role, avatar=avatar):
        st.markdown(content)


# -----------------------------
# User Input & Processing
# -----------------------------
prompt = st.chat_input("How may the household assist you?")

if prompt:
    # Debug output (only if enabled)
    if DEBUG_MODE:
        st.write("DEBUG: Prompt received:", prompt)
        st.write("DEBUG: Mode is:", mode)

    # 1) Show the user message immediately
    st.session_state.messages.append({"role": "user", "content": prompt, "speaker": "user"})
    with st.chat_message("user", avatar=AGENT_AVATARS["user"]):
        st.markdown(prompt)

    # 2) Dispatch to appropriate workflow with error handling
    orchestrator = st.session_state.orchestrator
    
    try:
        if mode == "Parlour Discussions (General Conversation)":
            speaker = "Jeeves"
            result = orchestrator.run("parlour_discussion", prompt)

        elif mode == "Arrangements for the Day":
            speaker = "Jeeves"
            result = orchestrator.run("daily_planning", prompt)

        elif mode == "Matters Requiring Investigation":
            speaker = "Perkins"
            result = orchestrator.run("research", prompt)

        elif mode == "Correspondence & Drafting":
            speaker = "Miss Pennington"
            result = orchestrator.run("drafting", prompt)

        elif mode == "Records & Summaries from the Archive":
            speaker = "Jeeves"
            # Pass prompt instead of empty string if user input is relevant
            result = orchestrator.run("memory_summary", prompt or "Provide a summary of recent activities.")

        elif mode == "Her Ladyship's Critique (Proceed with Caution)":
            speaker = "Lady Hawthorne"
            result = orchestrator.run("critique", prompt)

        else:
            speaker = "Jeeves"
            result = "I'm afraid something has gone quite amiss, sir. The household is in disarray."

    except Exception as e:
        speaker = "Jeeves"
        result = f"*Clears throat apologetically* \n\nI do beg your pardon, but it appears we've encountered an unexpected difficulty in the household. Perhaps you might rephrase your request?\n\n"
        
        if DEBUG_MODE:
            result += f"\n\n**Technical Details:**\n```\n{traceback.format_exc()}\n```"
        
        st.error(f"Error: {str(e)}")

    # 3) Display the household's reply
    if DEBUG_MODE:
        st.write("DEBUG: Orchestrator result:", str(result)[:200])

    st.session_state.messages.append(
        {"role": "assistant", "content": result, "speaker": speaker}
    )

    with st.chat_message("assistant", avatar=AGENT_AVATARS.get(speaker, AGENT_AVATARS["assistant"])):
        st.markdown(result)