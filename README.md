# 📡 AI-Powered Telecom Training Assistant

An intelligent AI assistant for telecom education, powered by **IBM Granite 3.3** on **watsonx.ai** with a **RAG** (Retrieval-Augmented Generation) pipeline.

---

## 🏗️ Architecture

```
User Interface (Gradio)
        │
        ▼
  app.py  ──────────────────────────────────────────────┐
        │                                                │
        ▼                                                ▼
  rag_pipeline.py                                 llm_engine.py
  (ChromaDB + HuggingFace Embeddings)             (IBM Granite via watsonx.ai)
        │                                                │
        ▼                                                ▼
  knowledge_base.py                            quiz_engine.py
  (8 Telecom Topics)                           (Quiz parsing & session)
```

## 📁 Project Structure

```
├── app.py              # Main Gradio chatbot UI
├── config.py           # watsonx.ai credentials & model config
├── llm_engine.py       # IBM Granite LLM wrapper
├── rag_pipeline.py     # RAG: document loading, embedding, retrieval
├── knowledge_base.py   # Curated telecom knowledge base (8 topics)
├── quiz_engine.py      # Quiz generation, parsing, session management
├── test_app.py         # Unit tests
├── requirements.txt    # Python dependencies
└── README.md
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Tests
```bash
python test_app.py
```

### 3. Launch the App
```bash
python app.py
```
Visit: http://localhost:7860

---

## ✨ Features

### 1. 📖 Concept Explanation (RAG-powered)
- Select any topic from the dropdown or type a custom query
- RAG retrieves relevant chunks from the knowledge base
- Granite generates a structured, student-friendly explanation

### 2. 🧪 Interactive Quiz
- Choose any topic and number of questions (3–10)
- Granite generates multiple-choice questions from the knowledge base
- Interactive Q&A — answer with A/B/C/D in the chat
- Automatic scoring with explanations for wrong answers

### 3. 💬 Real-time Q&A Chatbot
- Ask any telecom question in free-form text
- RAG retrieves relevant context
- Granite answers with full conversation history awareness

### 4. 📋 Study Summaries
- Generate concise cheat-sheet style summaries for any topic
- Perfect for quick review before exams

### 5. 🗺️ Learning Path Suggestions
- Get personalized learning path recommendations
- Understand prerequisites and what to study next

---

## 📚 Knowledge Base Topics

| Topic | Key Concepts |
|-------|-------------|
| 5G Network Architecture | gNB, AMF, SMF, UPF, Network Slicing, mmWave |
| LTE / 4G Technology | eNodeB, EPC, MME, OFDMA, SC-FDMA |
| OSI Model & Protocols | 7 Layers, SS7, SIP, Diameter, GTP |
| Wireless Fundamentals | OFDM, MIMO, Modulation (QAM/PSK), Multiple Access |
| Network Security | 5G-AKA, SUCI, SEPP, SS7 Firewalls |
| Cloud / SDN / NFV | SDN Controller, VNF, CNF, MEC, O-RAN |
| Fiber Optics | SMF/MMF, WDM, DWDM, EDFA, PON/GPON |
| IoT & M2M | NB-IoT, LTE-M, LoRaWAN, MQTT, CoAP |

---

## ⚙️ Configuration

Edit `config.py` to adjust:
- `GRANITE_MODEL_ID`: Change the IBM Granite model variant
- `GENERATE_PARAMS`: Tune temperature, max tokens, etc.
- `TOP_K_RETRIEVAL`: Number of RAG chunks retrieved (default: 4)
- `CHUNK_SIZE`: Document chunking size (default: 800)

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| LLM | IBM Granite 3.3 8B Instruct |
| LLM Platform | IBM watsonx.ai |
| RAG Vector Store | ChromaDB |
| Embeddings | sentence-transformers/all-MiniLM-L6-v2 |
| LLM Framework | LangChain |
| UI | Gradio 4.x |
| Language | Python 3.10+ |
