from flask import Blueprint, request

from app.models.lead import Lead
from app.services.lead_service import LeadService
from app.utils.response import error_response, success_response
from app.utils.validators import ValidationError, parse_batch_request, validate_single_find_payload

lead_bp = Blueprint("lead", __name__)
lead_service = LeadService()


@lead_bp.post("/lead/find")
def find_lead():
    try:
        payload = request.get_json(silent=True)
        company = validate_single_find_payload(payload)
        result = lead_service.find_or_create_lead(company)
        response_body = {
            "email": result.get("email"),
            "confidence": result.get("confidence"),
            "pitch": result.get("pitch"),
            "short_pitch": result.get("short_pitch"),
        }
        return success_response(response_body, 200)
    except ValidationError as exc:
        return error_response(str(exc), 400)
    except ValueError as exc:
        return error_response(str(exc), 500)
    except RuntimeError as exc:
        return error_response(str(exc), 500)


@lead_bp.post("/lead/batch")
def batch_lead():
    try:
        json_payload = request.get_json(silent=True)
        companies = parse_batch_request(
            json_payload=json_payload,
            raw_data=request.data,
            content_type=request.content_type or "",
        )
        results = lead_service.process_batch(companies)
        return success_response(results, 200)
    except ValidationError as exc:
        return error_response(str(exc), 400)


@lead_bp.get("/leads")
def list_leads():
    page = request.args.get("page", default=1, type=int)
    page_size = min(request.args.get("page_size", default=20, type=int), 100)

    pagination = Lead.query.order_by(Lead.created_at.desc()).paginate(
        page=page, per_page=page_size, error_out=False
    )

    return success_response(
        {
            "items": [lead.to_dict() for lead in pagination.items],
            "page": page,
            "page_size": page_size,
            "total": pagination.total,
        },
        200,
    )
