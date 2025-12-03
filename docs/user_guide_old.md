# 🏰 User Guide  
### *A Practical Handbook for Patrons of the Estate*  
House of Westmarch — Streamlit Interface Guide (Updated)

---

## 1. Quick Start

To run the demonstrations locally:

1\. Clone the repository  
2\. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3\. Launch the Streamlit interface:  
   ```
   streamlit run app.py
   ```
4\. Navigate to the URL printed in your terminal (usually:  
`http://localhost:8501`).

(You will be welcomed by the assembled staff.)


5\. For manual demos (1–8):  
   Select the correct sidebar mode and follow the scripted prompts found in  
   `westmarch/demos_in_universe/`

6\. For the fully automated flagship demo (Demo 9):  
   Select **“Matters Requiring the Whole Household”** from the sidebar  
   and press the button **“▶ Run Demo 9 – A Mystery in the Archives”** near the top of the screen.

➡️ Full instructions:  
[How to Run Demos (1–9)](https://github.com/groundhog-21/westmarch-house/blob/main/docs/how_to_run_demos.md)

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
3. To reenact one of the in-universe demonstrations (Demos 1–8),  
   open the corresponding `.md` script from:  
   `westmarch/demos_in_universe/`  
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

**Demo 9 — A Mystery in the Archives** runs **entirely automatically** with a single button press.

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
Jeeves constructs structured plans based on:
- goals  
- time constraints  
- preferences  

---

## 4.3 Matters Requiring Investigation  
Research and analysis via **Perkins**.  
Expect structured reasoning, numbered steps, evidence, and clarity.

---

## 4.4 Correspondence & Drafting  
**Miss Pennington** transforms rough notes into refined writing:
- letters  
- emails  
- summaries  
- outlines  
- official reports  

---

## 4.5 Records & Summaries from the Archive  
Jeeves retrieves historical summaries and past session insights.

---

## 4.6 Her Ladyship’s Critique  
Submit writing for incisive evaluation by **Lady Hawthorne**.  
Expect elegance, severity, and actionable revision guidance.

---

## 4.7 Matters Requiring the Whole Household  
Supports multi-agent orchestration but is primarily used for  
**the fully automated Demo 9 experience**.

---

## 4.8 Jeeves Remembers  
The Estate’s memory system supports:
- semantic search  
- weighted keyword scoring  
- domain inference  
- agent-hint recognition  

Example prompts:
```
“What did I tell you yesterday about my poem?”
“What were Perkins’s findings about the gnome?”
“Have we ever discussed investing?”
```

---

# 5. Interaction Guidelines

## 5.1 Tone  
The staff respond well to polite phrasing but support casual requests too.

---

## 5.2 Closure Detection  
To end interactions gracefully, try:
- “That will be all.”  
- “Thank you, Jeeves.”  
- “Much obliged.”

---

## 5.3 Memory Queries  
Provide clues when possible:
- agent name  
- topic  
- approximate date  
- keywords  

---

# 6. Troubleshooting

## 6.1 No Relevant Memory Found  
Jeeves provides a fallback and may request more detail.

---

## 6.2 Ambiguous Queries  
Clarify with:
- topic  
- timing  
- agent  
- or domain (finance, poetry, etc.)

---

# 7. Conclusion  
This guide provides everything needed to explore the rooms, agents, services, and stories of the Westmarch Estate — whether manually or through the fully automated Mystery in the Archives.
