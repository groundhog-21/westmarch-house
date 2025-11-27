# 🏰 The House of Westmarch  
### *A Fully Staffed, Mildly Unhinged Multi-Agent Concierge*  
🎩 Jeeves · 📚 Perkins · ✒️ Miss Pennington · 🕯️ Lady Hawthorne · 👤 The Master

---

## **Project Description**

**The House of Westmarch** is a narrative-forward, technically complete multi-agent concierge system presented as an Edwardian household. It demonstrates multi-agent orchestration, memory, tool use, critique loops, hybrid LLM usage, an interactive Streamlit UI, and nine in-universe demos that reveal the underlying architecture.

Instead of interacting with anonymous “agents,” the user delegates tasks to staff: a butler, a research valet, a secretary, and a critic. Beneath the theatrical presentation is a real, engineered agentic platform.

---

## **1. Problem Statement**

Modern users face a continuous stream of small cognitive burdens: planning, research, drafting, summarising, and remembering what was discussed previously. These tasks accumulate until the user becomes, effectively, their own secretary, researcher, editor, and archivist.

The House of Westmarch addresses this by providing specialised staff:

- 🎩 **Jeeves:** planning, orchestration, memory  
- 📚 **Perkins:** structured research and analysis  
- ✒️ **Miss Pennington:** drafting and summarisation  
- 🕯️ **Lady Hawthorne:** critique and evaluation  

This staff reduces cognitive load and reframes multi-agent AI as a comfortable, character-driven experience.

---

## **2. Solution Overview**

Westmarch is built around four persona agents, each with a clear role, coordinated by an orchestrator using both **Gemini** and **OpenAI** models. It includes:

- Multi-agent coordination  
- Tool-assisted reasoning  
- Session + long-term memory  
- Context compaction  
- Critique loops  
- Model switching  
- A polished Streamlit interface  
- Nine theatrical demonstrations  

The system provides real capability wrapped inside a narrative of household staff performing their duties.

---

## **3. Agent Roster**

### 🎩 Jeeves — Butler & Orchestrator
The central coordinator. Jeeves receives all user instructions, decomposes tasks, delegates to other agents, manages memory, and produces daily plans or summaries.

### 📚 Perkins — Valet of Scholarly Inquiry
A research and reasoning agent who uses numbered analyses, external tools, and structured thinking to generate investigations and reports.

### ✒️ Miss Pennington — Secretary & Correspondent
Transforms chaotic notes into refined prose, writes summaries, letters, and digests, and maintains a consistent tone and style.

### 🕯️ Lady Hawthorne — Critic-in-Residence
Powered by OpenAI. Reviews poetry, prose, arguments, and agent output. Provides targeted critique and revision guidance with a sharp editorial voice.

---

## **4. Architecture Summary**

### **4.1 Orchestration Hall — `westmarch/orchestrator/`**
- `router.py`: determines which agent handles a request  
- `workflows.py`: defines sequences such as *research → draft → critique*

### **4.2 Core Services — `westmarch/core/`**
- `models.py`: configures Gemini and OpenAI models  
- `memory.py`: session memory + summarised long-term memory  
- `messages.py`: internal message schema  
- `logging.py`: observability and debugging utilities  

### **4.3 Agents — `westmarch/agents/`**
Each agent inherits from a shared base class. Personas are defined through system messages, including tone, capabilities, and tool access.

### **4.4 Memory Layer — `westmarch/data/memory.json`**
A compacted, summarised memory store enabling agent recall. Supports demonstrations such as “What did I tell you yesterday?”

### **4.5 Streamlit Front-End — `app.py`**
The Estate’s public interface. Users select from eight modes:
- Parlour Discussions (General Conversation)  
- Arrangements for the Day  
- Matters Requiring Investigation  
- Correspondence & Drafting  
- Records & Summaries from the Archive  
- Her Ladyship’s Critique (Proceed with Caution)  
- Matters Requiring the Whole Household  
- Jeeves Remembers  

Each mode maps directly to a workflow in the orchestrator.

---

## **5. Features Demonstrated**

The House of Westmarch implements key patterns from the Agents Intensive:

- **Multi-agent delegation** with explicit personas  
- **Sequential + parallel workflows**  
- **Tool-assisted reasoning** (Perkins)  
- **Long-term memory** with summarisation  
- **Evaluation loop** via a dedicated critic  
- **Model switching** (Gemini ↔ OpenAI)  
- **Logging and observability**  
- **Interactive, stateful UI** in Streamlit  

The system balances technical capability with narrative presentation.

---

## **6. Demonstrations (1–9)**

The Estate contains nine in-universe demonstration scripts showcasing the system’s behaviour.

### **Demo 1 — Parlour Discussions**  
Introduction to staff and base conversational patterns.

### **Demo 2 — Arrangements for the Day**  
Jeeves constructs a realistic daily plan from rough goals.

### **Demo 3 — Matters Requiring Investigation**  
Perkins conducts structured analysis (“teacup psychology”), demonstrating tools + reasoning.

### **Demo 4 — Correspondence & Drafting**  
Miss Pennington converts fragmented notes into polished correspondence.

### **Demo 5 — Records & Summaries**  
Jeeves produces archival summaries of a mismanaged household project.

### **Demo 6 — Her Ladyship’s Critique**  
Lady Hawthorne dissects the poem “O Languid Moon of Yesteryear.”

### **Demo 7 — The Case of the Misbehaving Garden Gnome**  
Full multi-agent orchestration: collaborative reasoning and multi-step flow.

### **Demo 8 — Memory Demonstration**  
Jeeves retrieves summarised memory entries (“What did I tell you yesterday?”).

### **Demo 9 — A Mystery in the Archives**  
Flagship demo. Fully automated in Streamlit. Demonstrates:
- Multi-agent coordination  
- Looping/iterative investigation  
- Metadata reasoning  
- Critique escalation  
- Model switching  
- Pause/resume logic  
- Theatrical narrative  

---

## **7. Value & Impact**

Westmarch shows how a multi-agent system can be made friendly and readable without sacrificing capability.

### Practical Value
- Reduces planning and cognitive load  
- Produces higher-quality writing  
- Structures research  
- Provides useful critique  
- Maintains continuity through memory  

### Experiential Value
- Narrative framing improves user engagement  
- Characters clarify agent roles  
- The household metaphor reduces cognitive friction  
- Streamlit makes the system accessible to non-technical users  

As the staff note:

- 🎩 Jeeves: “The Estate restores dignity to everyday tasks.”  
- ✒️ Miss Pennington: “No more wrestling with blank pages.”  
- 📚 Perkins: “Delegation improves clarity.”  
- 🕯️ Lady Hawthorne: “And the prose improves.”  

---

## **8. Conclusion**

The House of Westmarch is a complete, narrative-driven multi-agent concierge system demonstrating orchestration, memory, tool use, critique loops, and structured workflows across two LLM platforms. Its Streamlit UI and nine theatrical demos allow users and judges to explore the system interactively.

🕯️ *Lady Hawthorne:* “If this does not satisfy the judges, nothing will.”