# LangGraph Stateful Chatbot

> A production-ready, stateful chatbot built using **LangGraph** and **Streamlit** — demonstrating how to manage complex LLM conversation states and maintain persistent chat history using SQLite.

---

## ✨ Features

| Feature | Description |
|---|---|
| 💾 **Persistent Conversations** | All chat sessions are saved in a local SQLite database |
| 🏷️ **Intelligent Title Generation** | Auto-generates concise 3–4 word titles for new chats based on first message |
| 🧵 **Multi-Thread Support** | Manage multiple separate chat threads effortlessly |
| 🧠 **Stateful Architecture** | Built on LangGraph for robust, scalable, memory-aware interactions |

---

## 🛠️ Tech Stack

```
Language    →  Python
Frameworks  →  LangGraph · LangChain · Streamlit
Database    →  SQLite
LLM         →  Groq API  (llama-3.1-8b-instant)
```

---

## 📋 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/UsmanTariq-542/LangGraph_Chatbot.git
cd LangGraph_Chatbot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Your API Key
Create a `.env` file in the root directory and add your Groq API key:
```plaintext
GROQ_API_KEY=your_sk_key_here
```

### 4. Run the Application
```bash
streamlit run chatbot_streamlit/frontend_sqlite_db_03.py
```

---

## 🧠 Why LangGraph?

Unlike standard LangChain chains, **LangGraph allows for cyclic flows and state persistence**. This project showcases how to maintain *memory* across sessions — a crucial capability for modern AI-driven applications.

---

<div align="center">

**Built by M. Usman Tariq**
[github.com/UsmanTariq-542](https://github.com/UsmanTariq-542)

</div>
