# 🦁 The Beast — Local AI Agent Lab  
**Project: gemma_agent**  
**Model:** Gemma 3 12B (Local via Ollama)  
**Hardware:** HP 35L 64 GIG 4 TB SSD RTX 4070 Super  
**OS:** Ubuntu Linux  

A fully local, tool‑calling autonomous agent designed for experimentation, clarity, and hands‑on AI engineering.  
This project represents my personal lab for building, testing, and refining agent architectures on my Linux workstation (“The Beast”).

---

## 🚀 Purpose

`gemma_agent` is my custom-built autonomous agent — not based on any external framework.  
It’s a ground‑up exploration of:

- agent loops  
- tool calling  
- safety gating  
- memory  
- retrieval  
- local execution  

This is where I experiment, learn, and push my understanding of how AI agents *actually* work under the hood.

---

## 🧩 Architecture Overview

The agent follows a clean, modular structure:
```text
gemma_agent/
│
├── agent.py                # Main agent loop (generation → tool → feedback)
│
├── config/
│   ├── system_prompt.txt   # Core system instructions
│   └── tools.json          # Tool definitions for the agent
│
├── core/
│   └── gatekeeper.py       # Validates and filters model outputs
│
├── tools/
│   ├── web_search.py
│   ├── visit_webpage.py
│   ├── shell.py
│   └── timezone.py
│
├── memory/
│   └── profile.json        # Persistent memory store
│
├── vector_db/              # FAISS + SQLite vector store for RAG
│
├── data/                   # Logs, reports, artifacts
│
├── requirements.txt
└── README.md
```



---

## 🛠️ Key Features

### **🔧 Custom Tool‑Calling System**
The agent uses a structured JSON tool‑calling format, parsed and executed locally.

### **🛡️ Gatekeeper Safety Layer**
All model outputs pass through a validator that ensures:

- correct JSON structure  
- safe tool usage  
- no malformed actions  

### **🧠 Persistent Memory**
A simple JSON‑based memory system stores:

- user preferences  
- past interactions  
- long‑term context  

### **📚 Local RAG**
FAISS + SQLite vector store for:

- document retrieval  
- contextual grounding  
- knowledge persistence  

### **🌐 Local Execution**
Everything runs on:

- **Ollama**  
- **Gemma 3 12B**  
- **Ubuntu Linux**  

No cloud dependencies.

---

## ▶️ Running the Agent

From the project root:



The agent will:

1. Load the system prompt  
2. Generate an action plan  
3. Call tools as needed  
4. Validate outputs  
5. Produce a final answer  

---

## 🎓 Background & Motivation

This project is part of my broader AI engineering journey, which includes:

- **Harvard CS50P** — Python fundamentals  
- **Harvard CS50AI** — search, logic, and classical AI  
- **Hugging Face Agents Course** — smolagents, tool use, and agent frameworks  

`gemma_agent` is where I apply those lessons in a fully custom, local environment.

---

## 🏷️ Tags

- ai-agent  
- local-ai  
- ollama  
- gemma  
- tool-calling  
- autonomous-agents  
- python  
- rag  
- faiss  
- linux  

---

## 📄 License

MIT License.

---

## 🌐 About

This repository is part of my ongoing exploration into human‑guided AI engineering, local agent systems, and practical autonomous workflows.



