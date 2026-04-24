# Noob Writing Assistant: Creative Writing Critic (Beta)

<img width="1600" height="789" alt="image" src="https://github.com/user-attachments/assets/7750bb98-3aee-4d9d-8fcb-5944a0dc8c54" />

**Noob Writing Aid** is an analytical writing assistant designed to help authors identify common prose pitfalls such as "filter words," "telling vs. showing," and "monotonous pacing." 

Unlike generic spellcheckers, this tool focuses specifically on the **craft of fiction** using Natural Language Processing (NLP).

---

## Features

The engine analyzes your manuscript across three distinct levels:

### 1. Word-Level Analysis
* **Weak Verbs & Adverbs:** Flags non-descriptive words (e.g., "was," "very," "just").
* **Passive Voice:** Identifies `auxpass` dependencies to encourage active prose.
* **Filler Detection:** Catches "empty" words like "stuff" or "things."

### 2. Sentence-Level Analysis
* **Repetitive Starts:** Flags sentences that begin with the same word as the previous one.
* **Immediate Echoes:** Catches adjacent repeated words.
* **Telling vs. Showing:** Detects `To-Be + Adjective` structures that indicate passive description.

### 3. Paragraph-Level Analysis
* **Monotonous Pacing:** Analyzes sentence lengths; if three or more sentences have nearly identical word counts, it flags a "pacing" warning.
* **Word Echoes:** Scans for unique nouns, verbs, or adjectives used too closely together within a paragraph.

---

## Tech Stack

* **Frontend:** React (State management for real-time writing feedback)
* **Backend:** FastAPI (High-performance Python API)
* **NLP Engine:** [spaCy](https://spacy.io/) (Statistical models for POS tagging and dependency parsing)

---

## Installation & Setup

### 1. Backend (Python/FastAPI)

Navigate to the `backend` folder and run the following commands:

```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download the required spaCy language model
python -m spacy download en_core_web_md

# Run the server
uvicorn main:app --reload
```

### 2. Frontend (React)

Navigate to the `frontend` folder and run the following commands:

```bash
npm install
npm start
uvicorn main:app --reload
```
