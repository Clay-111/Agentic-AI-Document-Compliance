import pytesseract
from pdf2image import convert_from_path
import re

pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

def extract_text_from_pdf(pdf_path):
    pages = convert_from_path(pdf_path)
    return "".join([pytesseract.image_to_string(page) for page in pages])

def classify_document(text):
    text_lower = text.lower()
    if "invoice number" in text_lower or "total amount" in text_lower or "supplier" in text_lower:
        return "invoice"
    elif "bill of lading" in text_lower or "port of loading" in text_lower or "carrier" in text_lower:
        return "bill_of_lading"
    elif "id number" in text_lower or "nationality" in text_lower or "issuing authority" in text_lower:
        return "id"
    elif "pay date" in text_lower or "net pay" in text_lower or "gross pay" in text_lower:
        return "paystub"
    else:
        return "unknown"


# ✅ Extract Key Fields
def extract_bol_fields(text):
    fields = {}

    shipper_match = re.search(r'Shipper:\s*(.+?)(?:\n|$)', text)
    if shipper_match:
        fields['shipper'] = shipper_match.group(1).strip()

    consignee_match = re.search(r'Consignee:\s*(.+?)(?:\n|$)', text)
    if consignee_match:
        fields['Consignee'] = consignee_match.group(1).strip()

    port_load_match = re.search(r'Port of Loading:\s*(.+?)(?:\n|$)', text)
    if port_load_match:
        fields['port_loading'] = port_load_match.group(1).strip()

    port_discharge_match = re.search(r'Port of Discharge:\s*(.+?)(?:\n|$)', text)
    if port_discharge_match:
        fields['port_discharge'] = port_discharge_match.group(1).strip()

    goods_desc_match = re.search(r'Goods Description:\s*(.+?)(?:\n|$)', text)
    if goods_desc_match:
        fields['goods_desc'] = goods_desc_match.group(1).strip()

    shipment_date_match = re.search(r'Shipment Date:\s*(\d{4}-\d{2}-\d{2})', text)
    if shipment_date_match:
        fields['shipment_date'] = shipment_date_match.group(1)

    expiry_date_match = re.search(r'Expiry Date:\s*(\d{4}-\d{2}-\d{2})', text)
    if expiry_date_match:
        fields['expiry_date'] = expiry_date_match.group(1)

    lc_expiry_match = re.search(r'LC Expiry Date:\s*(\d{4}-\d{2}-\d{2})', text)
    if lc_expiry_match:
        fields['lc_expiry_date'] = lc_expiry_match.group(1)

    signed_match = re.search(r'Signed:\s*(Yes|No)', text, re.IGNORECASE)
    if signed_match:
        fields['signed'] = signed_match.group(1).strip()

    carrier_match = re.search(r'Carrier:\s*(.+?)(?:\n|$)', text)
    if carrier_match:
        fields['carrier'] = carrier_match.group(1).strip()

#        # === CLEANUP SECTION START ===
#    known_labels = {
#        'Shipper:', 'Consignee:', 'Port of Loading:', 'Port of Discharge:',
#        'Goods Description:', 'Shipment Date:', 'Expiry Date:',
#        'LC Expiry Date:', 'Signed:', 'Carrier:'
#    }

#    for key in list(fields.keys()):
#        if fields[key] in known_labels:
#            del fields[key]  # Remove the field if value is just another label
#    # === CLEANUP SECTION END ===
    
    # === CLEANUP SECTION START ===
    suspicious_prefixes = [
        "Shipper:", "Consignee:", "Port of Loading:", "Port of Discharge:", "Goods Description:",
        "Shipment Date:", "Expiry Date:", "LC Expiry Date:", "Signed:", "Carrier:"
    ]

    for key, value in list(fields.items()):
        for prefix in suspicious_prefixes:
            if value.strip().startswith(prefix):
                del fields[key]
                break
    # === CLEANUP SECTION END ===


    return fields


def extract_id_fields(text):
    fields = {}

    id_match = re.search(r'ID Number:\s*(.+?)(?:\n|$)', text)
    if id_match:
        fields['id_number'] = id_match.group(1).strip()

    name_match = re.search(r'Name:\s*(.+?)(?:\n|$)', text)
    if name_match:
        fields['name'] = name_match.group(1).strip()

    dob_match = re.search(r'DOB:\s*(\d{4}-\d{2}-\d{2})', text)
    if dob_match:
        fields['dob'] = dob_match.group(1)

    expiry_match = re.search(r'Expiry Date:\s*(\d{4}-\d{2}-\d{2})', text)
    if expiry_match:
        fields['expiry_date'] = expiry_match.group(1)

    submission_match = re.search(r'Submission Date:\s*(\d{4}-\d{2}-\d{2})', text)
    if submission_match:
        fields['submission_date'] = submission_match.group(1)

    nationality_match = re.search(r'Nationality:\s*(.+?)(?:\n|$)', text)
    if nationality_match:
        fields['nationality'] = nationality_match.group(1).strip()

    issue_match = re.search(r'Issue Date:\s*(\d{4}-\d{2}-\d{2})', text)
    if issue_match:
        fields['issue_date'] = issue_match.group(1)

    doc_type_match = re.search(r'Document Type:\s*(.+?)(?:\n|$)', text)
    if doc_type_match:
        fields['document_type'] = doc_type_match.group(1).strip()

    gender_match = re.search(r'Gender:\s*(.+?)(?:\n|$)', text)
    if gender_match:
        fields['gender'] = gender_match.group(1).strip()

    authority_match = re.search(r'Issuing Authority:\s*(.+?)(?:\n|$)', text)
    if authority_match:
        fields['issuing_authority'] = authority_match.group(1).strip()

    # === CLEANUP SECTION START ===
    suspicious_prefixes = [
        "ID Number:", "Name:", "DOB:", "Expiry Date:", "Submission Date:",
        "Nationality:", "Issue Date:", "Document Type:", "Gender:", "Issuing Authority:"
    ]

    for key, value in list(fields.items()):
        for prefix in suspicious_prefixes:
            if value.strip().startswith(prefix):
                del fields[key]
                break
    # === CLEANUP SECTION END ===

    return fields


def extract_invoice_fields(text):
    fields = {}

    invoice_match = re.search(r'Invoice Number:\s*(.+?)(?:\n|$)', text)
    if invoice_match:
        fields['invoice_number'] = invoice_match.group(1).strip()

    date_match = re.search(r'(?:Date|Issue Date):\s*(\d{4}-\d{2}-\d{2})', text)
    if date_match:
        fields['issue_date'] = date_match.group(1)

    supplier_match = re.search(r'Supplier:\s*(.+?)(?:\n|$)', text)
    if supplier_match:
        fields['supplier'] = supplier_match.group(1).strip()

    consignee_match = re.search(r'Consignee:\s*(.+?)(?:\n|$)', text)
    if consignee_match:
        fields['Consignee'] = consignee_match.group(1).strip()

    amount_match = re.search(r'Total Amount:\s*(-?\d+)', text)
    if amount_match:
        fields['total_amount'] = int(amount_match.group(1).strip())

    currency_match = re.search(r'Currency:\s*(.+?)(?:\n|$)', text)
    if currency_match:
        fields['currency'] = currency_match.group(1).strip()

    due_date_match = re.search(r'Due Date:\s*(\d{4}-\d{2}-\d{2})', text)
    if due_date_match:
        fields['due_date'] = due_date_match.group(1)

    items_match = re.search(r'Items:\s*(.+?)(?:\n|$)', text)
    if items_match:
        fields['items'] = items_match.group(1).strip()

    # === CLEANUP SECTION START ===
    suspicious_prefixes = [
        "Invoice Number:", "Consignee:", "Supplier:", "Currency:", "Total Amount:",
        "Date:", "Issue Date:", "Due Date:", "Items:"
    ]

    for key, value in list(fields.items()):
        for prefix in suspicious_prefixes:
            if isinstance(value, str) and value.strip().startswith(prefix):
                del fields[key]
                break
    # === CLEANUP SECTION END ===

    return fields


def extract_paystub_fields(text):
    fields = {}

    emp_id_match = re.search(r'Employee ID:\s*(.+?)(?:\n|$)', text)
    if emp_id_match:
        fields['employee_id'] = emp_id_match.group(1).strip()

    employer_match = re.search(r'Employer Name:\s*(.+?)(?:\n|$)', text)
    if employer_match:
        fields['employer_name'] = employer_match.group(1).strip()

    pay_date_match = re.search(r'Pay Date:\s*(\d{4}-\d{2}-\d{2})', text)
    if pay_date_match:
        fields['pay_date'] = pay_date_match.group(1)

    salary_period_match = re.search(r'Salary Period:\s*(.+?)(?:\n|$)', text)
    if salary_period_match:
        fields['salary_period'] = salary_period_match.group(1).strip()

    monthly_income_match = re.search(r'Monthly Income:\s*(-?\d+)', text)
    if monthly_income_match:
        fields['monthly_income'] = int(monthly_income_match.group(1))

    deductions_match = re.search(r'Deductions:\s*(-?\d+)', text)
    if deductions_match:
        fields['deductions'] = int(deductions_match.group(1))

    net_pay_match = re.search(r'Net Pay:\s*(-?\d+)', text)
    if net_pay_match:
        fields['net_pay'] = int(net_pay_match.group(1))

    gross_pay_match = re.search(r'Gross Pay:\s*(-?\d+)', text)
    if gross_pay_match:
        fields['gross_pay'] = int(gross_pay_match.group(1))

    # === CLEANUP SECTION START ===
    suspicious_prefixes = [
        "Employee ID:", "Employer Name:", "Pay Date:", "Salary Period:",
        "Monthly Income:", "Deductions:", "Net Pay:", "Gross Pay:"
    ]

    for key, value in list(fields.items()):
        if isinstance(value, str):
            for prefix in suspicious_prefixes:
                if value.strip().startswith(prefix):
                    del fields[key]
                    break
    # === CLEANUP SECTION END ===

    return fields



def extract_entities(text, doc_type):
    if doc_type == "id":
        return extract_id_fields(text)
    elif doc_type == "bill_of_lading":
        return extract_bol_fields(text)
    elif doc_type == "invoice":
        return extract_invoice_fields(text)
    elif doc_type == "paystub":
        return extract_paystub_fields(text)
    else:
        return {}

