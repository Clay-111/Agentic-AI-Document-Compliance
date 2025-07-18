# 📄 Agentic-AI-Document-Compliance

## 🚀 Project Overview

Agentic AI Document Compliance is a modular prototype designed to automate document compliance validation using an agent-based architecture. It processes documents such as invoices, bills of lading, IDs, and paystubs by extracting relevant fields, validating them against predefined rules, detecting discrepancies across documents, and providing a user-friendly interface for review.

This project demonstrates how multiple specialized agents work together in an orchestrated workflow to streamline document processing and compliance checks.

---

## 📁 Project Structure

```
Agentic-AI-Document-Compliance/
│
├── agents/
│   ├── extraction.py         # Performs OCR and NLP-based field extraction from documents
│   ├── validation.py         # Applies rule-based validation
│   └── discrepancy.py        # Detects and maps inconsistencies across documents
│
├── orchestrator.py           # Coordinates the agents and manages the overall pipeline workflow
│
├── ui/
│   └── app.py                # Streamlit-based user interface for interacting with the system
│
├── sample_docs/              # Sample input documents (PDFs, images) for testing and demo
│
├── reports/                  # Folder for storing extraction results, Excel exports, and logs
│
├── requirements.txt          # Python dependencies required to run the project
│
│── rules.json                # Predefined validation rules for each document type
│
└── README.md                 # Project documentation (this file)
```

---
## 🛠️ Tech Stack

- **Python** – Core programming language for the entire system
- **Streamlit** – Lightweight web framework to build the interactive user interface
- **Tesseract OCR** – OCR engine used to extract text from images and PDFs
- **spaCy** – NLP library for entity recognition, pre-processing, and rule-based matching
- **openpyxl** – Generates and exports Excel reports

---
## ⚙️ How It Works 

**Note:** ⚠️ The validation rules are currently defined for the sample PDF files located in the `sample_docs` folder. To process new or different PDFs, the rules may need to be updated to match the fields and formats of those documents.



1. Download Tesseract-OCR and install it exactly in this folder `C:\\Program Files\\Tesseract-OCR\\tesseract.exe`
2. Download Poppler for Windows: https://github.com/oschwartz10612/poppler-windows/releases/
   - Extract the zip exactly here: `C:\poppler`
   - Add Poppler to PATH:
     - Open **Start Menu → Environment Variables**
     - Under **System Variables**, find Path and click Edit
     - Add this path: `C:\poppler\Library\bin`
4. Run the Streamlit UI:
   ```bash
   streamlit run ui/app.py
5. Wait for the UI to open automatically in your browser. If it doesn't, visit:
   ```bash
   http://localhost:8501
6. In the UI:
   - Use the file uploader to upload one or more documents (PDF)
   - Click the **🚀 Run Validation button**.
   - Wait for the processing to complete.
   - After that Click the **📋 View Extracted Fields button**.
     - Displays the extracted values from each PDF.
   - Click the **✅ Validation Issues button**
     - Shows the issues in each PDF and what needs to be fixed.
   - Click the **⚠️ Discrepancies button**.
     - Summarizes the outcome of the cross-document analysis.
    - After each run:
        - An Excel report is saved in the `reports/` folder.
        - Open this file to review the structured results.

    


