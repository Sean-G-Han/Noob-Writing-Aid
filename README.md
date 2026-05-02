# Noob Writing Assistant: Creative Writing Critic (Beta)

<img width="1906" height="872" alt="image" src="https://github.com/user-attachments/assets/3b29b85e-c005-4008-9a3e-cf921ee9ff49" />

**Noob Writing Assistant** is a writing analysis tool designed to help authors identify and fix common issues in prose such as weak phrasing, repetition, unclear references, and unnatural pacing.

Unlike generic grammar checkers, it focuses on **style, clarity, and narrative quality**, rather than only correctness.

## Tech Stack

- **Frontend:** React (real-time editor + annotation rendering)
- **Backend:** FastAPI (Python API server)
- **NLP Engine:** spaCy (dependency parsing + POS tagging)

## Features
The engine analyzes writing across multiple levels of language structure:

### 1. Word-Level Analysis
Detects issues at the lexical level:
- Weak Verbs & Adverbs (e.g. *was, very, just*)
- Passive Voice Detection
- Filler Words (e.g. *stuff, things*)
- Spelling Issues
- Ambiguous Pronouns

### 2. Sentence-Level Analysis
Evaluates sentence structure and flow:
- Repetitive Sentence Starts
- Immediate Word Repetition
- Telling vs Showing Patterns
- Tense Inconsistencies
- Double Negatives
- Sentence Fragments
- Weak Determiners
- Word Echoing Across Sentences

### 3. Paragraph-Level Analysis
Evaluates narrative rhythm and pacing:
- Monotonous Sentence Lengths
- Repetitive Sentence Structures

### 4. Window-Based Context Analysis
Cross-sentence pattern detection:
- Repeated Subject Usage in Close Proximity

## Rule System
The analysis engine is modular and rule-based:

### Word Rules
- AdverbRule
- WeakVerbRule
- WeakAdverbRule
- WeakFillerRule
- PassiveVoiceRule
- SpellingRule
- AmbiguousPronounRule

### Sentence Rules
- RepeatedWordRule
- ToBeAdjectiveRule
- PerfectTenseSVARule
- PastToBeSVARule
- PresentSVARule
- InconsistentTenseRule
- DeterminerRule
- DoubleNegativeRule
- SentenceFragmentRule
- WordEchoRule

### Paragraph Rules
- SentenceStartRepetitionRule
- MonotonousLengthRule

### Window Rules
- RepeatedSubjectRule

## Installation & Setup

### 1. Backend Setup

```bash
cd backend

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt

python -m spacy download en_core_web_sm
```
### 2. Frontend Setup

```bash
cd frontend
npm install
```

### 3. Run the Application
From the project root:

- Double-click dev.bat
<img width="300" height="112" alt="image" src="https://github.com/user-attachments/assets/bea61e02-56a2-4d23-8cc2-f84f6239febf" />

Then:
- Open the terminal link in your browser
- Use Ctrl + Click if needed
- Keep terminals running

---

## Usage Guide
Follow these steps to use the application:

### Novel
Novels are the main project container.

#### 1. Creating a Novel 
To create a novel, go `File` >> `New Novel`

<img width="600" alt="image" src="https://github.com/user-attachments/assets/60a8523b-51ee-4834-b14d-abe5b3075c8f" />

#### 2. Loading a Novel 
Once the novel is created, go `File` >> `Load Novel`

<img width="600" alt="image" src="https://github.com/user-attachments/assets/cc0f7e7a-5aa7-4591-8606-9124f5432cff" />

#### 3. Edit/Deleting a Novel
In the event that Novel is named wrongly or you wish to delete the project, go `File` >> `Edit Novel`

<img width="600" alt="image" src="https://github.com/user-attachments/assets/d0155755-96b4-432c-bab4-6723edd532af" />

### Chapter
Chapters are the sub-projects that will actually be graded.

### 1. Creating a Chapter
Once a novel is loaded, you can create a chapter by clicking `Create` on the left panel

<img width="600" alt="image" src="https://github.com/user-attachments/assets/244b6d16-9ec4-4c8f-809b-53013fdabdb1" />

### 2. Editing and Deleting a Chapter
Click `Edit` or `Delete` accordingly. This is where you can change the chapter number. Note that the other chapters will shift accordingly

<img width="600" alt="image" src="https://github.com/user-attachments/assets/07738f8d-8ea9-440f-9890-a5da51457f87" />

### 3. Selecting a Chapter
To use grading feature, select a chapter from this page. This can be done by clicking the chapter anywhere but the button. You should notice changes in the circled parts indicating the selected chapter

<img width="800" alt="image" src="https://github.com/user-attachments/assets/33b8eb27-68c2-496d-8281-3d297cb8a742" />

### 4. Using Editor/Grader
Once a chapter and novel is selected, you can go to the editor. The options to `save`, `load` and `analyze` are at the top right corner.

(Note: Users are required to save first before analyzing)

<img width="600" alt="image" src="https://github.com/user-attachments/assets/b99b1e17-d6ab-476b-843a-882922b643d0" />

### Characters (Optional)
Characters are optional additives to a chapter. They are required for `AmbiguousPronounRule` to work and will be used in future features

### 1. Creating a Character
To create a character, press `Create`. Each chapter will be assigned their own set of characters.

<img width="600" alt="image" src="https://github.com/user-attachments/assets/ec037431-30e3-4cf4-84ef-3fa2a4d6975e" />

### 2. Linking Characters
To re-use characters from previous chapters, you can use the link feature by clicking `Link`. This would hopeully reduce the need to create duplicate character per chapter.

<img width="600" alt="image" src="https://github.com/user-attachments/assets/9410b1a5-16be-4b85-99e0-e1a890dcd150" />

Note that linked chapters are all the same, meaning if you edit the same character in one chapter, you will also edit the same one in another



