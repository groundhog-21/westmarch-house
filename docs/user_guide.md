# 🏰 User Guide  
### *A Practical Handbook for Patrons of the Estate*  
House of Westmarch — Streamlit Interface Guide (Updated)

---

# 1. Introduction  
This guide explains how to operate **The House of Westmarch** through the Streamlit interface.  
It covers:

- **Manual operation** for all standard Estate services (Demos 1–8)  
- **Automatic operation** for *Demo 9 — A Mystery in the Archives*  
- Navigation, example prompts, and practical notes on interacting with the household staff

All interactions occur through the sidebar menu inside `app.py`.

---

# 2. Using the Interface

## 2.1 Selecting a Mode  
The sidebar presents the Estate’s available services:

- **Parlour Discussions (General Conversation)**  
- **Arrangements for the Day**  
- **Matters Requiring Investigation**  
- **Correspondence & Drafting**  
- **Records & Summaries from the Archive**  
- **Her Ladyship’s Critique (Proceed with Caution)**  
- **Matters Requiring the Whole Household**  
- **Jeeves Remembers**

Each mode maps to an orchestrated workflow managed by **Jeeves** and the household staff.

---

# 3. Two Ways to Use the Estate  

Westmarch supports **two distinct interaction styles**, depending on whether you are exploring the standard demos or running the fully automated Demo 9.

---

# 🟦 Use Case 1 — Manual Operation (Demos 1–8)  
Use this method for all modes except Demo 9.

## How It Works  
1. Choose a mode in the **sidebar**.  
2. Begin a normal chat interaction in the main panel.  
3. If you wish to reenact one of the in-universe demonstrations (Demos 1–8),  
   open the corresponding `.md` script from `westmarch/demos_in_universe/`  
   and follow the prompts manually in the UI.

---

## Example Manual Workflows  

### **Parlour Discussions**  
```
“Jeeves, kindly introduce the household staff.”
“Tell me something amusing from the morning papers.”
```

### **Arrangements for the Day**  
```
“My goals today are light errands, one meeting, and quiet reading.”  
```

### **Matters Requiring Investigation (Perkins)**  
```
“Perkins, compare ETFs and mutual funds.”  
```

### **Correspondence & Drafting (Pennington)**  
```
“I need a polite email explaining why my tax form is late.”  
```

### **Her Ladyship’s Critique**  
```
“Lady Hawthorne, your verdict on this paragraph, if you please.”  
```

---

# 🟧 Use Case 2 — Automatic Operation (Demo 9 Only)  

**Demo 9 — A Mystery in the Archives** runs **entirely automatically** with one button press.

## How To Run Demo 9  
1. In the sidebar, select:  
   **“Matters Requiring the Whole Household”**  
2. Press the button labelled:  
   **“Run Demo 9 — A Mystery in the Archives”**

The entire multi-round narrative unfolds without further input:
- Pennington → Perkins → Jeeves → Hawthorne  
- Parallel analysis  
- Metadata Scrutinizer tool call  
- Household council  
- Branching choice  
- Final discovery and critique  

**No user prompts are required** once the demo begins.

---

# 4. Service Descriptions (Manual Mode)

## 4.1 Parlour Discussions  
General conversation with **Jeeves** using his lighter Parlour-mode prompt.  
Perfect for introductions, small talk, and gentle requests.

---

## 4.2 Arrangements for the Day  
Jeeves constructs structured daily plans based on:
- goals  
- time constraints  
- preferences  

---

## 4.3 Matters Requiring Investigation  
Research and analysis via **Perkins**.  
Expect structured reasoning, numbered points, clear evidence, and factual grounding.

---

## 4.4 Correspondence & Drafting  
**Miss Pennington** transforms rough notes into polished writing:
- letters  
- emails  
- summaries  
- outlines  
- official reports  

---

## 4.5 Records & Summaries from the Archive  
Jeeves retrieves useful summaries from past interactions or session notes.

---

## 4.6 Her Ladyship’s Critique  
Submit writing for an incisive evaluation by **Lady Hawthorne**.  
Expect wit, elegance, and actionable revision guidance.

---

## 4.7 Matters Requiring the Whole Household  
In manual mode, you may orchestrate a multi-agent task manually.  
In practice, this menu item is **reserved for Demo 9’s automated run-through**.

---

## 4.8 Jeeves Remembers  
The Estate’s memory system provides:
- semantic search  
- keyword scoring  
- domain inference  
- agent hint recognition  
- recall of Pennington-archived events  

Examples:
```
“What did I tell you yesterday about my poem?”
“What were Perkins’s findings about the gnome?”
“Have we ever discussed investing?”
```

---

# 5. Interaction Guidelines

## 5.1 Tone  
The staff respond well to polite, natural phrasing, but are fully capable of casual conversation.

---

## 5.2 Closure Detection  
To gracefully end a conversation, you may say:
- “Thank you, Jeeves.”  
- “That will be all.”  
- “Much obliged.”

Jeeves will retire with decorum.

---

## 5.3 Memory Queries  
Memory queries trigger Jeeves’s advanced recall method.  
Provide clues when possible:
- agent involved  
- topic  
- approximate time  
- keywords  

---

# 6. Troubleshooting

## 6.1 No Relevant Memory Found  
Jeeves provides a gentle fallback and may request further detail.

---

## 6.2 Ambiguous Queries  
If a request is unclear, try specifying:
- topic  
- an approximate date  
- agent name  
- domain (finance, poetry, planning, etc.)  

---

# 7. Conclusion  
This guide equips you with everything needed to explore the rooms, agents, services, and stories of the Westmarch Estate — whether through manual direction of the staff or the fully automated Mystery in the Archives.
