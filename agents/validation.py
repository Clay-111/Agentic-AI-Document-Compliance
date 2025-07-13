import json
from datetime import datetime

with open("rules.json") as f:
    RULES = json.load(f)

def parse_date(value):
    try: return datetime.strptime(value, "%Y-%m-%d")
    except: return None

def evaluate_condition(field, condition, fields):
    try:
        value = fields.get(field)

        if condition == "missing":
            return not value or str(value).strip() == "" or str(value).endswith(":")
        if condition == "not_string":
            return not isinstance(value, str)
        if condition == "invalid_date":
            return parse_date(value) is None
        if condition.startswith(("<", ">", "==", "!=", "<=", ">=")):
            return eval(f"{value} {condition}") if value is not None else True
        if condition == "expression":
            return eval(field, {}, fields)

    except:
        return False

    return False

def run_rule_based_validation(doc_type, fields, doc_name):
    issues = []
    for rule in RULES.get(doc_type, []):
        field = rule["field"]
        condition = rule["condition"]
        if evaluate_condition(field, condition, fields):
            issues.append({
                "rule_id": rule.get("rule_id", "N/A"),
                "document": doc_type,
                "pdf": doc_name,
                "issue": rule["issue"],
                "severity": rule["severity"],
                "action": rule["action"]
            })
    return issues
