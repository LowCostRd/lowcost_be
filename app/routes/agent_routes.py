import datetime

from flask import Blueprint, request, jsonify, g

from app.exception.copy_exception import CopyException

from ..services.agent_service import ElevenLabsService
from ..services.auth.decorators import require_auth
from ..services.rate_limiter import limiter
from ..utils.success_builder import build_response
from ..constant.success_message import *


agent_bp = Blueprint("agent", __name__)
elevenlabs_service = ElevenLabsService()


@agent_bp.route("/v1/api/agents/create", methods=["POST"])
@require_auth
@limiter.limit("10 per minute")
def create_agent():
    user_id = g.current_user["sub"]
    data = request.get_json()
    result = elevenlabs_service.create_agent(data=data, user_id=user_id)
    json_response = build_response(result, 201)
    return jsonify(json_response), 201


@agent_bp.route("/v1/api/agents/<string:agent_id>/voice", methods=["PATCH"])
@require_auth
@limiter.limit("20 per minute")
def update_voice(agent_id: str):
    user_id = g.current_user["sub"]
    data = request.get_json()
    result = elevenlabs_service.update_voice(agent_id=agent_id, data=data, user_id=user_id)
    json_response = build_response(result, 200)
    return jsonify(json_response), 200


@agent_bp.route("/v1/api/agents/<string:agent_id>/roles", methods=["PATCH"])
@require_auth
@limiter.limit("20 per minute")
def update_roles(agent_id: str):
    user_id = g.current_user["sub"]
    data = request.get_json()
    result = elevenlabs_service.update_roles(agent_id=agent_id, data=data, user_id=user_id)
    json_response = build_response(result, 200)
    return jsonify(json_response), 200


@agent_bp.route("/v1/api/agents/voices", methods=["GET"])
@require_auth
@limiter.limit("30 per minute")
def get_voices():
    voices = elevenlabs_service.get_voices()
    json_response = build_response(voices, 200)
    return jsonify(json_response), 200


@agent_bp.route("/v1/api/agents", methods=["GET"])
@require_auth
@limiter.limit("30 per minute")
def get_user_agents():
    user_id = g.current_user["sub"]
    agents = elevenlabs_service.get_user_agents(user_id=user_id)
    json_response = build_response(agents, 200)
    return jsonify(json_response), 200


@agent_bp.route("/v1/api/agents/<string:agent_id>", methods=["DELETE"])
@require_auth
@limiter.limit("10 per minute")
def delete_agent(agent_id: str):
    user_id = g.current_user["sub"]
    result = elevenlabs_service.delete_agent(agent_id=agent_id, user_id=user_id)
    json_response = build_response(result, 200)
    return jsonify(json_response), 200


@agent_bp.route("/v1/api/agents/voices/preview", methods=["POST"])
@require_auth
@limiter.limit("20 per minute")
def preview_voice():
    data = request.get_json()
    result = elevenlabs_service.preview_voice(data=data)
    json_response = build_response(result, 200)
    return jsonify(json_response), 200


@agent_bp.route("/v1/api/agents/<string:agent_id>/name", methods=["PATCH"])
@require_auth
@limiter.limit("20 per minute")
def update_name(agent_id: str):
    user_id = g.current_user["sub"]
    data = request.get_json()
    result = elevenlabs_service.update_name(agent_id=agent_id, data=data, user_id=user_id)
    json_response = build_response(result, 200)
    return jsonify(json_response), 200


@agent_bp.route("/v1/api/agents/<string:agent_id>/specialty", methods=["PATCH"])
@require_auth
@limiter.limit("20 per minute")
def update_specialty(agent_id: str):
    user_id = g.current_user["sub"]
    data = request.get_json()
    result = elevenlabs_service.update_specialty(agent_id=agent_id, data=data, user_id=user_id)
    json_response = build_response(result, 200)
    return jsonify(json_response), 200

def _parse_date(value: str):
    if not value:
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        raise CopyException(f"Invalid date format: {value}. Use YYYY-MM-DD.", 400)


@agent_bp.route("/v1/api/agents/list", methods=["GET"])
@require_auth
def list_agents():
    user_id = g.current_user["sub"]

    filters = {
        "name": request.args.get("name"),
        "specialty": request.args.get("specialty"),
        "search": request.args.get("search"),
        "date_from": _parse_date(request.args.get("date_from")),
        "date_to": _parse_date(request.args.get("date_to")),
    }

    result = elevenlabs_service.get_user_agents_filtered(user_id=user_id, filters=filters)
    json_response = build_response(result, 200)
    return jsonify(json_response), 200

