from datetime import datetime

def run_discrepancy_agent(docs):
    results = []

    # Part 1: Consignee mismatch check
    consignee_map = {}
    for doc in docs:
        consignee = doc['fields'].get('Consignee')
        if consignee:
            key = consignee.strip()
            if key not in consignee_map:
                consignee_map[key] = []
            consignee_map[key].append(f"{doc['pdf_name']} ({doc['doc_type']})")

    if len(consignee_map) > 1:
        results.append({
            'rule_id': 'DISC-001',
            'document': ", ".join(sorted({doc['doc_type'] for doc in docs})),
            'pdfs_per_consignee': consignee_map,
            'issue': "Consignee name mismatch across documents.",
            'severity': 'High',
            'action': 'Verify consignee consistency across all related documents.'
        })

    # Part 2: Shipment date <= Invoice issue date check
    shipment_dates = {}
    invoice_dates = {}

    for doc in docs:
        c = doc['fields'].get('Consignee')
        if not c:
            continue
        if doc['doc_type'] == 'bill_of_lading':
            sd_str = doc['fields'].get('shipment_date')
            if sd_str:
                try:
                    sd = datetime.strptime(sd_str, "%Y-%m-%d")
                    shipment_dates.setdefault(c, []).append((sd, doc['pdf_name']))
                except:
                    pass
        elif doc['doc_type'] == 'invoice':
            id_str = doc['fields'].get('issue_date')
            if id_str:
                try:
                    idate = datetime.strptime(id_str, "%Y-%m-%d")
                    invoice_dates.setdefault(c, []).append((idate, doc['pdf_name']))
                except:
                    pass

    for consignee in shipment_dates:
        if consignee in invoice_dates:
            for (sd, sd_pdf) in shipment_dates[consignee]:
                for (idate, id_pdf) in invoice_dates[consignee]:
                    if sd > idate:
                        results.append({
                            'rule_id': 'DISC-002',
                            'document': 'bill_of_lading, invoice',
                            'pdf': f'{sd_pdf} (BOL), {id_pdf} (Invoice)',
                            'issue': f'Shipment date {sd.strftime("%Y-%m-%d")} on BOL is after Invoice issue date {idate.strftime("%Y-%m-%d")} for consignee {consignee}.',
                            'severity': 'High',
                            'action': 'Shipment date on BOL must be on or before Invoice issue date.'
                        })

    return results
