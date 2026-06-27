A production-ready, stateful chatbot built using LangGraph and Streamlit. This project demonstrates how to manage complex LLM conversation states and maintain persistent chat history using SQLite.

🚀 Features
Persistent Conversations: All chat sessions are saved in a local SQLite database.

Intelligent Title Generation: Automatically generates concise, meaningful 3-4 word titles for new chats based on first chat.

Multi-Thread Support: Users can manage multiple separate chat threads effortlessly.

Stateful Architecture: Built on LangGraph for robust, scalable, and memory-aware interactions.

🛠 Tech Stack
Language: Python

Frameworks: LangGraph, LangChain, Streamlit

Database: SQLite

LLM: Groq_API key (llama-3.1-8b-instant)

📋 How to Run Locally
Clone the repository:

Bash
git clone https://github.com/UsmanTariq-542/LangGraph_Chatbot.git
cd LangGraph_Chatbot
Install dependencies:

Bash
pip install -r requirements.txt
Set up your API Key:
Create a .env file in the root directory and add your GROQ API key:

Plaintext
GROQ_API_KEY=your_sk_key_here
Run the application:

Bash
streamlit run chatbot_streamlit/frontend_sqlite_db_03.py
🧠 Why LangGraph?
Unlike standard LangChain chains, LangGraph allows for cyclic flows and state persistence. This project showcases how to maintain "memory" across sessions, which is crucial for modern AI-driven applications.

Built by M.Usman Tariq 
