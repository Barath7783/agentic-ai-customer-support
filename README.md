# 🤖 Agentic AI Customer Support

An AI-powered customer-support application built with **Agentic AI, LangGraph, Google Gemini, RAG, business tools, PostgreSQL, FastAPI, React, Docker, and Render**.

The system understands customer requests, identifies their intent, retrieves relevant company knowledge, executes the appropriate business action, and generates a natural-language response.

---

## 🌐 Live Demo

### Frontend

👉 https://agentic-customer-support-frontend.onrender.com

### Backend API

👉 https://agentic-customer-support-api.onrender.com

---

## 📌 Project Overview

Traditional customer-support chatbots mainly provide text responses.

This project goes a step further by using an **Agentic AI workflow** that can understand a customer's request and perform appropriate business actions.

For example:

- 📦 Check an order
- 💰 Submit a refund request
- ❌ Submit an order cancellation request
- 🎫 Create a support ticket
- 📚 Answer company policy questions

---

## 🧠 How It Works

```text
                    Customer
                       │
                       ▼
              React + Vite Frontend
                       │
                       ▼
                 FastAPI Backend
                       │
                       ▼
                LangGraph Agent
                       │
              ┌────────┴────────┐
              │                 │
              ▼                 ▼
       Intent Detection      RAG Retrieval
              │                 │
              └────────┬────────┘
                       ▼
               Business Tool
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
      Order Tool   Refund Tool   Ticket Tool
          │            │            │
          └────────────┼────────────┘
                       ▼
                 Gemini LLM
                       │
                       ▼
              Customer Response
