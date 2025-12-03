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
            width: 380px;
        }
        [data-testid="stSidebar"] > div:first-child {
            width: 380px;
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

        /* Fix Streamlit sidebar collapse tooltip (“keyb…”) artifact */
        [data-testid="stSidebar"] [title] {
            max-width: 0 !important;
            overflow: hidden !important;
            white-space: nowrap !important;
            text-overflow: clip !important;
            opacity: 0 !important;
            pointer-events: none;
        }

    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Sidebar Controls
# -----------------------------
with st.sidebar:

    # Title (safe HTML wrapper to prevent disappearing)
    st.markdown(
        """
        <div style="padding-bottom:0.5rem;">
            <h2 style="font-family:EB Garamond; margin-bottom:0;">
                🏰 The House of Westmarch
            </h2>
            <em style="font-family:EB Garamond; font-size:16px; color:#4a4a4a;">
                Pray, command your staff — the estate awaits your direction.
            </em>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    # Services heading (wrapped to make it stable)
    st.markdown(
        """
        <div style="padding-top:0.3rem;">
            <h3 style="font-family:EB Garamond; font-weight:600; margin-top:0;">
                The Estate's Available Services:
            </h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Mode selector
    mode = st.radio(
        "Choose Mode",
        [
            "📜 Instructions for Running the Demos",
            "Parlour Discussions (General Conversation)",
            "Arrangements for the Day",
            "Matters Requiring Investigation",
            "Correspondence & Drafting",
            "Records & Summaries from the Archive",
            "Her Ladyship's Critique (Proceed with Caution)",
            "Matters Requiring the Whole Household",
            "Jeeves Remembers",          
        ],
        label_visibility="collapsed",
    )

    st.markdown("---")


    # Clear conversation button
    if st.button("🔄 Clear Conversation"):
        st.session_state.messages = []
        st.rerun()


# -----------------------------
# Mode-Specific UI (Before Prompt)
# -----------------------------
if mode == "Matters Requiring the Whole Household":
    st.subheader("Matters Requiring the Whole Household")

    if st.button("▶ Run Demo 9 – A Mystery in the Archives"):
        orchestrator = st.session_state.orchestrator
        demo9_messages = orchestrator.run("archive_mystery", None)

        # If run() returns a list (Demo 9), use it directly
        if isinstance(demo9_messages, list):
            st.session_state.messages = demo9_messages
        else:
            # Fallback: wrap as single assistant message
            st.session_state.messages = [
                {"role": "assistant", "content": demo9_messages, "speaker": "Jeeves"}
            ]

        st.rerun()


# -----------------------------
# Demo Instructions Page
# -----------------------------
if mode == "📜 Instructions for Running the Demos":
    st.header("📜 Instructions for Running the Demos")

    st.markdown(
        """
        This page provides quick instructions for running Demonstrations 1–9 of the House of Westmarch.
        
        For the full guide, please see:
        """
    )

    # Link to full Markdown file in docs/
    st.link_button("📄 Open Full How-To Guide", "/static/how_to_run_demos.md")

    st.markdown("---")

    # Demo 9 section
    st.subheader("🎭 Automated Demo (Demo 9)")
    st.markdown(
        """
        1. Select **Matters Requiring the Whole Household** in the sidebar  
        2. Click **Run Demo 9 – A Mystery in the Archives**  
        3. No further input required  
        """
    )

    st.markdown("---")

    # Manual demos section
    st.subheader("📝 Manual Demonstrations (Demos 1–8)")
    st.markdown(
        """
        To run the manual demos:

        1. Select the correct sidebar mode  
        2. Open the matching script in `westmarch/demos_in_universe/`  
        3. Type each scripted prompt into the chat window  
        """
    )

    # Script links inside expanders
    with st.expander("📚 View Demo Scripts"):
        st.markdown(
            """
            - [demo01_parlour_discussion.md](https://github.com/groundhog-21/westmarch-house/blob/main/westmarch/demos_in_universe/demo01_parlour_discussion.md)  
            - [demo02_daily_arrangements.md](https://github.com/groundhog-21/westmarch-house/blob/main/westmarch/demos_in_universe/demo02_daily_arrangements.md)  
            - [demo03_matter_requiring_investigation.md](https://github.com/groundhog-21/westmarch-house/blob/main/westmarch/demos_in_universe/demo03_matter_requiring_investigation.md)  
            - [demo04_correspondence_and_drafting.md](https://github.com/groundhog-21/westmarch-house/blob/main/westmarch/demos_in_universe/demo04_correspondence_and_drafting.md)  
            - [demo05_records_and_summaries.md](https://github.com/groundhog-21/westmarch-house/blob/main/westmarch/demos_in_universe/demo05_records_and_summaries.md)  
            - [demo06_her_ladyships_critique.md](https://github.com/groundhog-21/westmarch-house/blob/main/westmarch/demos_in_universe/demo06_her_ladyships_critique.md)  
            - [demo07_multi_agent_garden_gnome.md](https://github.com/groundhog-21/westmarch-house/blob/main/westmarch/demos_in_universe/demo07_multi_agent_garden_gnome.md)  
            - [demo08_memory_continuity.md](https://github.com/groundhog-21/westmarch-house/blob/main/westmarch/demos_in_universe/demo08_memory_continuity.md)  
            - [demo09_a_mystery_in_the_archives.md](https://github.com/groundhog-21/westmarch-house/blob/main/westmarch/demos_in_universe/demo09_a_mystery_in_the_archives.md)   
            """
        )

    # Early return to avoid showing chat UI
    st.stop()


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
            result = orchestrator.run("parlour_discussion", prompt, selected_mode=mode)

        elif mode == "Arrangements for the Day":
            speaker = "Jeeves"
            result = orchestrator.run("daily_planning", prompt, selected_mode=mode)

        elif mode == "Matters Requiring Investigation":
            speaker = "Perkins"
            result = orchestrator.run("research", prompt, selected_mode=mode)

        elif mode == "Correspondence & Drafting":
            speaker = "Miss Pennington"
            result = orchestrator.run("drafting", prompt, selected_mode=mode)

        elif mode == "Records & Summaries from the Archive":
            speaker = "Jeeves"
            result = orchestrator.run("archive", prompt, selected_mode=mode)

        elif mode == "Her Ladyship's Critique (Proceed with Caution)":
            speaker = "Lady Hawthorne"
            result = orchestrator.run("critique", prompt, selected_mode=mode)

        elif mode == "Jeeves Remembers":
            speaker = "Jeeves"
            result = orchestrator.run("recall_memory", prompt, selected_mode=mode)

        elif mode == "Matters Requiring the Whole Household":
            speaker = "Jeeves"
            result = orchestrator.run("whole_household", prompt, selected_mode=mode)

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