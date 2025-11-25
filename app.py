import streamlit as st
import traceback

# Import your orchestrator from Phase 2
from westmarch.orchestrator.workflows import WestmarchOrchestrator
from westmarch.agents.jeeves import JeevesAgent
from westmarch.agents.perkins import PerkinsAgent
from westmarch.agents.miss_pennington import MissPenningtonAgent
from westmarch.agents.lady_hawthorne import LadyHawthorneAgent
from westmarch.core.models import ModelClient

DEMO_9_MESSAGES = [
    # Scene 1 — The Discovery
    {
        "role": "assistant",
        "content": (
            "✒️ Pennington: Sir, while preparing the monthly archival index, I discovered "
            "a parchment filed under *‘Agricultural Affairs → Troublingly Damp Potatoes’.* "
            "A most improbable classification."
        ),
    },
    {
        "role": "user",
        "content": "👤 User: What sort of parchment is it?",
    },
    {
        "role": "assistant",
        "content": (
            "✒️ Pennington: A brittle sheet labelled only: "
            "**‘UNEXPLAINED RATTLING — DO NOT DISTURB.’**  "
            "Naturally, I disturbed it at once."
        ),
    },
    {
        "role": "assistant",
        "content": "🎩 Jeeves: Most intriguing. I shall summon Perkins.",
    },

    # Scene 2 — Perkins Begins the Investigation
    {
        "role": "assistant",
        "content": (
            "📚 Perkins: A misfiled parchment with a dire warning. Excellent. "
            "Miss Pennington: hand it over. I shall examine the metadata immediately."
        ),
    },
    {
        "role": "assistant",
        "content": (
            "✒️ Pennington: The ink trembles — as though the writer’s hand shook with dread."
        ),
    },
    {
        "role": "assistant",
        "content": "📚 Perkins: Then let us begin **Parallel Analysis Round 1**.",
    },

    # Scene 3 — Parallel Agents Activated
    {
        "role": "assistant",
        "content": (
            "📚 Perkins: I will analyze ink density, tremor frequency, and crumb distribution."
        ),
    },
    {
        "role": "assistant",
        "content": "✒️ Pennington: I shall prepare an official Discrepancy Report.",
    },
    {
        "role": "assistant",
        "content": "🎩 Jeeves: Very good. I shall keep the process orderly.",
    },

    # Scene 4 — Custom Tool Invocation (narrative only)
    {
        "role": "assistant",
        "content": (
            "📚 Perkins: Jeeves, activate the **Archival Metadata Scrutinizer**, if you please."
        ),
    },
    {
        "role": "assistant",
        "content": (
            "🧰 Tool (Archival Metadata Scrutinizer v3.2):\n"
            "Ink dated 1847.\n"
            "Tremor frequency: pronounced.\n"
            "Foreign substances: biscuit crumbs (0.7 g).\n"
            "Ambient dread: moderate."
        ),
    },
    {
        "role": "assistant",
        "content": "📚 Perkins: As expected. Biscuit-fear correlation remains strong.",
    },

    # Scene 5 — Lady Hawthorne Arrives
    {
        "role": "assistant",
        "content": (
            "🕯️ Hawthorne: My dears, if you require a device to tell you your papers are "
            "dusty and frightened, perhaps we should install cushions in the archives "
            "to prevent fainting."
        ),
    },
    {
        "role": "assistant",
        "content": "📚 Perkins: I assure Your Ladyship, this is legitimate research.",
    },
    {
        "role": "assistant",
        "content": (
            "🕯️ Hawthorne: Perkins, the only legitimate research is into how quickly "
            "I can leave this conversation."
        ),
    },

    # Scene 6 — Investigation Loop 2
    {
        "role": "assistant",
        "content": "📚 Perkins: The metadata envelope for 1847, if you please, Jeeves.",
    },
    {
        "role": "assistant",
        "content": "🎩 Jeeves: At once, sir.",
    },
    {
        "role": "assistant",
        "content": (
            "📚 Perkins: Aha! A record of a rattling chest kept in the Westmarch cellar, "
            "described only as ‘noisy,’ ‘ominous,’ and ‘containing a turnip of considerable "
            "menace.’"
        ),
    },

    # Scene 7 — Long-Running Pause/Resume Operation (narrative)
    {
        "role": "assistant",
        "content": (
            "🕯️ Narrator: A sudden metallic **CLANG** echoes through the archives. "
            "The Automated Card Catalogue Carousel has unmoored itself."
        ),
    },
    {
        "role": "assistant",
        "content": (
            "🎩 Jeeves: Oh dear. That would be the Automated Card Catalogue Carousel. "
            "It occasionally unmoors itself."
        ),
    },
    {
        "role": "user",
        "content": "👤 User: Shall we pause the investigation until the noise settles?",
    },
    {
        "role": "assistant",
        "content": (
            "🎩 Jeeves: Very prudent, sir.\n"
            "**Pausing investigation…**\n"
            "…\n"
            "…\n"
            "**Resuming investigation now.**"
        ),
    },

    # Scene 8 — Resolution
    {
        "role": "assistant",
        "content": (
            "📚 Perkins: The rattling parchment refers to the chest in the cellar — "
            "the one containing only a cracked vase, a spoon, and a turnip that dried "
            "into a rather menacing shape."
        ),
    },
    {
        "role": "assistant",
        "content": "✒️ Pennington: In other words: harmless.",
    },
    {
        "role": "assistant",
        "content": (
            "🎩 Jeeves: Precisely. And at some point, a startled archivist abandoned their "
            "post and misfiled the warning with the potatoes."
        ),
    },
    {
        "role": "user",
        "content": "👤 User: So the mystery is solved?",
    },
    {
        "role": "assistant",
        "content": "🎩 Jeeves: Entirely, sir.",
    },

    # Scene 9 — Pennington’s Final Report
    {
        "role": "assistant",
        "content": (
            "✒️ Pennington:\n"
            "**Archival Mystery Report – Final Findings**\n\n"
            "**Cause:** Misfiled warning parchment from 1847.\n"
            "**Custom Tool Used:** Archival Metadata Scrutinizer v3.2.\n"
            "**Long-Running Interruption:** Card Catalogue Carousel incident.\n"
            "**Contributing Factors:** Biscuit crumbs, trembling handwriting, "
            "potato subdirectory error.\n"
            "**Resolution:** Reclassified under ‘Persistent Noises.’\n"
            "**Recommendation:** Reduce biscuit consumption in archives; reconsider "
            "the Carousel’s freedom of movement."
        ),
    },

    # Scene 10 — Hawthorne’s Final Commentary
    {
        "role": "assistant",
        "content": (
            "🕯️ Hawthorne: Well, you’ve successfully wasted a morning identifying a "
            "frightened turnip. I suppose congratulations are in order. Now if you’ll "
            "excuse me, the ficus is behaving suspiciously again."
        ),
    },
]

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
        st.session_state.messages = DEMO_9_MESSAGES.copy()
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
            result = orchestrator.run("query_archive", prompt)

        elif mode == "Her Ladyship's Critique (Proceed with Caution)":
            speaker = "Lady Hawthorne"
            result = orchestrator.run("critique", prompt)

        elif mode == "Matters Requiring the Whole Household":
            speaker = "Jeeves"
            result = orchestrator.run("whole_household", prompt)

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