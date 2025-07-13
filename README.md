# Agentic-AI-Document-Compliance

## 📌 Project Overview

Agentic AI Document Compliance is a modular prototype designed to automate document compliance validation using an agent-based architecture. It processes documents such as invoices, bills of lading, IDs, paystubs etc. by extracting relevant fields, validating them against predefined rules, detecting discrepancies across documents, and providing a user-friendly interface for review.

This project demonstrates how multiple specialized agents work together in an orchestrated workflow to streamline document processing and compliance checks.

---

## 📁 Project Structure

Agentic-AI-Document-Compliance/
│
├── agents/
│ ├── extraction.py # Performs OCR and extracts fields from documents
│ ├── validation.py # Applies rule-based validation (schema or expressions)
│ └── discrepancy.py # Detects and maps inconsistencies across documents
│
├── orchestrator.py # Coordinates the agents and manages the overall pipeline workflow
│
├── ui/
│ └── app.py # Streamlit-based user interface for interacting with the system
│
├── sample_docs/ # Sample input documents (PDFs, images) for testing and demo
│
├── reports/ # Folder for storing extraction results, JSON reports, Excel exports, and logs
│ └── .gitkeep # Placeholder to keep this folder tracked in Git
│
├── requirements.txt # Python dependencies required to run the project
│
└── README.md # Project documentation (this file)

