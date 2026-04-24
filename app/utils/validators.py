import csv
import io


class ValidationError(Exception):
    pass


def validate_single_find_payload(payload: dict) -> str:
    if not isinstance(payload, dict):
        raise ValidationError("Invalid JSON object")

    company = payload.get("company")
    if not company or not isinstance(company, str):
        raise ValidationError("Field 'company' is required and must be a string")

    return company


def parse_batch_request(json_payload, raw_data: bytes, content_type: str) -> list[str]:
    if "text/csv" in content_type:
        return parse_csv(raw_data)

    if not isinstance(json_payload, list):
        raise ValidationError("JSON batch payload must be an array")

    companies = []
    for item in json_payload:
        if isinstance(item, str):
            companies.append(item)
        elif isinstance(item, dict) and isinstance(item.get("company"), str):
            companies.append(item["company"])
        else:
            raise ValidationError("Each batch item must be string or {'company': 'domain'}")

    if not companies:
        raise ValidationError("Batch payload is empty")

    return companies


def parse_csv(raw_data: bytes) -> list[str]:
    text_stream = io.StringIO(raw_data.decode("utf-8"))
    reader = csv.DictReader(text_stream)

    if "company" not in (reader.fieldnames or []):
        raise ValidationError("CSV must contain 'company' column")

    companies = [row["company"].strip() for row in reader if row.get("company")]
    if not companies:
        raise ValidationError("CSV contains no valid company values")

    return companies
