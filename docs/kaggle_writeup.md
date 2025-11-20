# The House of Westmarch: A Fully Staffed, Mildly Unhinged Multi-agent Concierge

Prepared by the Household Staff of Westmarch:  
🎩 Jeeves · 📚 Perkins · ✒️ Miss Pennington · 🕯️ Lady Hawthorne · 👤 The Master

Track: **Concierge Agents**

---

## Problem Statement

✒️ *Miss Pennington writes:*

In this modern age, even the most capable individuals are beset by a dreadful assortment of small but insistent tasks:

- planning one’s day,  
- conducting research,  
- composing civil correspondence,  
- keeping notes and summaries in order,  
- remembering what one said yesterday.

These indignities accumulate in inboxes, notebooks, and browser tabs until the mind resembles a cluttered attic. Human beings are expected to act as their own secretaries, researchers, editors, and archivists—all while attempting to live a life.

🎩 *Jeeves observes:*  
> “Modern life, sir, is perilously cluttered with administrative trifles.”

📚 *Perkins adds:*  
> “Cognitive overload is a menace, sir.”

🕯️ *Lady Hawthorne concludes:*  
> “The inefficiency of it all is tragic, though occasionally picturesque.”

From this arises the need for **proper staff**: discrete, specialised agents that can attend to planning, inquiry, drafting, memory, and critique—co-ordinated by a butler with impeccable taste.

---

## Solution: A Fully Staffed Digital Household

**The House of Westmarch** is a multi-agent concierge system presented as an aristocratic household. Instead of “Agent A” and “Tool B,” the user interacts with **staff**:

### 🎩 Jeeves — Butler & Orchestrator

Jeeves is the Master’s primary point of contact. He:

- receives all instructions,  
- breaks them into subtasks,  
- delegates to other staff,  
- keeps track of context and memory,  
- and reports back in an orderly fashion.

He is responsible for daily planning (“Arrangements for the Day”), summaries, and overall co-ordination.

### 📚 Perkins — Valet of Scholarly Inquiry

Perkins conducts research with alarming enthusiasm. He:

- queries external tools,  
- performs structured analysis,  
- organises findings into numbered arguments,  
- and cheerfully over-explains everything.

He is invoked for “Matters Requiring Investigation,” such as teacup psychology or the mysterious movement of a garden gnome.

### ✒️ Miss Pennington — Secretary & Correspondent

Miss Pennington rescues shambolic notes and drafts. She:

- turns bullet points into polished emails,  
- writes summaries and records,  
- maintains consistent tone and politeness,  
- and gently corrects the Master’s more chaotic phrasing.

Her domain is “Correspondence & Drafting” and “Records & Summaries.”

### 🕯️ Lady Hawthorne — Critic-in-Residence

Her Ladyship is the Estate’s evaluation loop. She:

- critiques poems, prose, and even the other agents,  
- highlights structural issues, clichés, and melodrama,  
- suggests targeted revisions,  
- and never sugar-coats anything.

Her chamber, “Her Ladyship’s Critique,” turns creative output into something sturdier—or at least more interesting.

---

## Architecture

🎩 *Jeeves explains from the Map Room:*

The Estate’s implementation follows a clear layered architecture:

1. **Orchestration Hall (`westmarch/orchestrator/`)**  
   - `router.py` decides which agent (Jeeves, Perkins, Pennington, Hawthorne) should handle a request.  
   - `workflows.py` defines multi-step flows (e.g. research → draft → critique).

2. **Core Services (`westmarch/core/`)**  
   - `models.py` configures Gemini and OpenAI models.  
   - `memory.py` provides session and long-term memory based on a JSON store.  
   - `messages.py` defines message formats and roles.  
   - `logging.py` adds observability and basic telemetry.

3. **Agents (`westmarch/agents/`)**  
   - Each staff member is a persona agent inheriting from a base class.  
   - System messages define persona, tone, and capabilities.  
   - All agents can call tools where appropriate (e.g., research).

4. **State & Sessions (`westmarch/data/memory.json`)**  
   - Recent interactions are compacted into summaries.  
   - Past context can be recalled (“What did I tell you yesterday?”).  
   - This powers the Memory Demonstration (Demo 8).

5. **Front-End (`app.py`)**  
   - Streamlit UI with the sidebar **“The House of Westmarch”**.  
   - Each menu item maps to a distinct workflow.  
   - Avatars: 👤 user, 🎩 Jeeves, 📚 Perkins, ✒️ Miss Pennington, 🕯️ Lady Hawthorne, 🏰 system.

This architecture cleanly separates concerns while keeping the narrative conceit intact.

---

## Features Demonstrated (Course Alignment)

The Estate demonstrates multiple concepts from the Agents Intensive Course:

- **Multi-agent system:** four distinct agents plus orchestrator.  
- **Sequential and parallel workflows:** e.g. Perkins research → Pennington draft → Hawthorne critique.  
- **Tool usage:** research and analysis tools for Perkins.  
- **Sessions & memory:** stateful conversations via `memory.py` and `memory.json`.  
- **Context compaction:** summarised memory entries to keep context slim.  
- **Evaluation loop:** Lady Hawthorne as a bespoke critic-agent.  
- **Observability:** custom logging and trace messages.

---

## Demonstrations & Use Cases

Eight narrative demos illustrate the Estate’s capabilities:

1. **Parlour Discussions** – The Master chats with Jeeves and is introduced to the staff.  
2. **Arrangements for the Day** – Jeeves builds a realistic daily plan from simple goals.  
3. **Matters Requiring Investigation** – Perkins performs “teacup psychology,” modelling a research workflow.  
4. **Correspondence & Drafting** – Miss Pennington converts chaotic notes into a polished email to the tax office.  
5. **Records & Summaries from the Archive** – Jeeves summarises an absurd household project involving a self-watering bookshelf.  
6. **Her Ladyship’s Critique** – Lady Hawthorne reviews the poem *“O Languid Moon of Yesteryear.”*  
7. **The Case of the Misbehaving Garden Gnome** – A grand multi-agent orchestration where all staff collaborate on a mystery.  
8. **Memory Demonstration** – Jeeves recalls what the Master said the previous day about the poem, showcasing state and recall.

Taken together, these demos show the system’s breadth—from mundane productivity to whimsical evaluation.

---

## Value

🎩 *Jeeves:*  
> “The Estate reduces cognitive load and restores dignity to everyday tasks.”

✒️ *Miss Pennington:*  
> “Users no longer have to fight with blank pages or awkward emails.”

📚 *Perkins:*  
> “Delegation to specialised agents increases efficiency and clarity of thought.”

🕯️ *Lady Hawthorne:*  
> “And the prose improves, which is what truly matters.”

Practically speaking, the House of Westmarch:

- Speeds up daily planning and prioritisation.  
- Produces higher-quality written communication from rough inputs.  
- Structures research into readable analyses.  
- Provides humorous but useful critique for creative work.  
- Demonstrates how multi-agent systems can be made approachable through narrative.

---

## Project Links

In the interest of scholarly rigor and proper estate documentation, the household staff respectfully provides the following references for those who wish to inspect the inner workings of Westmarch:

📜 The Estate’s Code Archives
Meticulously organized and preserved within the public wing of the GitHub Repository:
https://github.com/groundhog-21/westmarch-house

🎞️ Motion Picture Demonstration
A brief moving-picture account—illustrating the comportment, quarrels, and collaborative exertions of the household—is presently being prepared and shall be posted here when ready:
YouTube link forthcoming

---

## Conclusion

The House of Westmarch is both a working concierge agent system and a theatrical household. It showcases multi-agent orchestration, memory, tools, and evaluation in a form that is accessible, entertaining, and technically sound.

The staff remain at the Master’s disposal—and at the mercy of Lady Hawthorne’s critiques.

> 🕯️ *“If this does not satisfy the judges, nothing will.”*