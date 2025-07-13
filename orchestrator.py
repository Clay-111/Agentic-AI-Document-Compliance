from html import entities
import os, glob
from collections import defaultdict
import pandas as pd
from agents.extraction import extract_text_from_pdf, extract_entities, classify_document
from agents.validation import run_rule_based_validation
from agents.discrepancy import run_discrepancy_agent

def orchestrate(directory="sample_docs/"):
    pdfs = sorted(glob.glob(os.path.join(directory, "*.pdf")))
    docs, vres = [], []

    for pdf_path in pdfs:
        text = extract_text_from_pdf(pdf_path)
        doc_type = classify_document(text)
        if doc_type == "unknown":
            continue
        entities = extract_entities(text, doc_type)
        pdf_name = os.path.basename(pdf_path)

        print(f"\n[Extracted from {pdf_path}]")
        print(entities)
        
        docs.append({"pdf_name": pdf_name, "doc_type": doc_type, "fields": entities})
        vres.extend(run_rule_based_validation(doc_type, entities, pdf_name))

    dres = run_discrepancy_agent(docs)
    return vres, dres

def export_report_to_excel(validation_results, discrepancy_results, filename="reports/compliance_report.xlsx"):
    grouped = defaultdict(lambda: {
        "document_type": "",
        "rule_ids": [],
        "issues": [],
        "severities": [],
        "actions": []
    })

    for item in validation_results + discrepancy_results:
        pdf = item.get("pdf", "Unknown")
        grouped[pdf]["document_type"] = item.get("document", "General")
        grouped[pdf]["rule_ids"].append(item.get("rule_id", "N/A"))
        grouped[pdf]["issues"].append(item.get("issue", "N/A"))
        grouped[pdf]["severities"].append(item.get("severity", "N/A"))
        grouped[pdf]["actions"].append(item.get("action", "N/A"))

    data = []
    for pdf_name, info in grouped.items():
        data.append({
            "PDF Name": pdf_name,
            "Document Type": info["document_type"],
            "Rule IDs": ", ".join(info["rule_ids"]),
            "Issues": "\n".join(info["issues"]),
            "Severities": ", ".join(info["severities"]),
            "Actions": "\n".join(info["actions"])
        })

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    pd.DataFrame(data).to_excel(filename, index=False)
    print(f"✅ Report exported to {filename}")

    
