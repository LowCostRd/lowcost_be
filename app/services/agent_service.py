import os
import requests
import logging
from datetime import datetime

from ..models.agent import Agent
from ..exception.copy_exception import CopyException
from .. import mongo
from ..constant.error_message import *

logger = logging.getLogger(__name__)

ELEVENLABS_BASE_URL = os.getenv("ELEVENLABS_BASE_URL")

BASE_PROMPT = (
    "You are a professional AI assistant for a medical practice. "
    "Always be polite, empathetic, and concise. "
    "Never provide a medical diagnosis or clinical advice. "
    "If unsure about anything clinical, direct the patient to speak with a staff member.\n\n"
)


class ElevenLabsService:

    def __init__(self):
        self.api_key = os.getenv("ELEVENLABS_API_KEY")
        if not self.api_key:
            raise CopyException(key_not_set,400)
        self.headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json",
        }

    def create_agent(self, data: dict, user_id: str) -> dict:
        name = (data.get("name") or "").strip()
        specialty = (data.get("specialty") or "").strip()

        if not name:
            raise CopyException(name_required, 400)

        payload = {
            "name": name,
            "conversation_config": {
                "agent": {
                    "first_message": "Hello! How can I help you today?",
                    "language": "en",
                    "prompt": {
                        "prompt": BASE_PROMPT.strip(),
                        "llm": "qwen35-397b-a17b",
                    },
                }
            },
        }

        res = requests.post(
            f"{ELEVENLABS_BASE_URL}/convai/agents/create",
            headers=self.headers,
            json=payload,
        )

        if res.status_code != 200:
            logger.error("ElevenLabs create_agent failed: %s", res.text)
            raise CopyException(
                res.json().get("detail", "Failed to create agent"),
                res.status_code,
            )

        elevenlabs_agent_id = res.json().get("agent_id")

       
        agent = Agent(
            user_id=user_id,
            agent_id=elevenlabs_agent_id,
            name=name,
            specialty=specialty or None,
        )
        mongo.db.agents.insert_one(agent.to_dict())

        return {"agent_id": elevenlabs_agent_id}
    
    

   
    def update_voice(self, agent_id: str, data: dict, user_id: str) -> dict:
        voice_id = (data.get("voice_id") or "").strip()
        image_url = (data.get("image_url") or "").strip()
        
        if not voice_id:
            raise CopyException(voice_id_required, 400)

       
        self._verify_agent_ownership(agent_id, user_id)

        payload = {
            "conversation_config": {
                "tts": {"voice_id": voice_id}
            }
        }

        res = requests.patch(
            f"{ELEVENLABS_BASE_URL}/convai/agents/{agent_id}",
            headers=self.headers,
            json=payload,
        )

        if res.status_code != 200:
            logger.error("ElevenLabs update_voice failed: %s", res.text)
            raise CopyException(
                res.json().get("detail", "Failed to update voice"),
                res.status_code,
            )
        
        update_fields = {"voice_id": voice_id, "updated_at": datetime.now()}

        if image_url:
            update_fields["image_url"] = image_url

        mongo.db.agents.update_one(
            {"agent_id": agent_id},
            {"$set": update_fields},
        )

        return {"success": True, "agent_id": agent_id, "image_url": image_url}


    
    def update_name(self, agent_id: str, data: dict, user_id: str) -> dict:
        name = (data.get("name") or "").strip()
        if not name:
            raise CopyException(name_required, 400)

        self._verify_agent_ownership(agent_id, user_id)

        payload = {
            "name": name
        }

        res = requests.patch(
            f"{ELEVENLABS_BASE_URL}/convai/agents/{agent_id}",
            headers=self.headers,
            json=payload,
        )

        if res.status_code != 200:
            logger.error("ElevenLabs update_name failed: %s", res.text)
            raise CopyException(
                res.json().get("detail", "Failed to update name"),
                res.status_code,
            )

        mongo.db.agents.update_one(
            {"agent_id": agent_id},
            {"$set": {"name": name, "updated_at": datetime.now()}},
        )

        return {"success": True, "agent_id": agent_id}
    
    def update_specialty(self, agent_id: str, data: dict, user_id: str) -> dict:
        specialty = (data.get("specialty") or "").strip()
        if not specialty:
            raise CopyException(specialty_required, 400)

        self._verify_agent_ownership(agent_id, user_id)

        mongo.db.agents.update_one(
            {"agent_id": agent_id},
            {"$set": {"specialty": specialty, "updated_at": datetime.now()}},
        )

        return {"success": True, "agent_id": agent_id}


    def update_roles(self, agent_id: str, data: dict, user_id: str) -> dict:
        roles = data.get("roles", [])
        first_message = (data.get("first_message") or "").strip()

        if not roles:
            raise CopyException(role_required, 400)

      
        self._verify_agent_ownership(agent_id, user_id)

        merged_prompt = self._build_prompt(roles)

        agent_config = {
            "prompt": {
                "prompt": merged_prompt,
                "llm": "qwen35-397b-a17b",
            }
        }
        if first_message:
            agent_config["first_message"] = first_message

        payload = {
            "conversation_config": {
                "agent": agent_config
            }
        }

        res = requests.patch(
            f"{ELEVENLABS_BASE_URL}/convai/agents/{agent_id}",
            headers=self.headers,
            json=payload,
        )

        if res.status_code != 200:
            logger.error("ElevenLabs update_roles failed: %s", res.text)
            raise CopyException(
                res.json().get("detail", "Failed to update roles"),
                res.status_code,
            )

        role_ids = [r.get("id") for r in roles]

        mongo.db.agents.update_one(
            {"agent_id": agent_id},
            {"$set": {"roles": role_ids, "updated_at": datetime.now()}},
        )

        return {
            "success": True,
            "agent_id": agent_id,
            "roles_applied": role_ids,
        }


    def get_voices(self) -> list:
        res = requests.get(
            f"{ELEVENLABS_BASE_URL}/voices",
            headers=self.headers,
        )

        if res.status_code != 200:
            logger.error("ElevenLabs get_voices failed: %s", res.text)
            raise CopyException("Failed to fetch voices", res.status_code)

        return [
            {
                "voice_id": v["voice_id"],
                "name": v["name"],
                "preview_url": v.get("preview_url"),
                "labels": v.get("labels", {}),
            }
            for v in res.json().get("voices", [])
        ]


    def get_user_agents(self, user_id: str) -> list:
        agents = mongo.db.agents.find(
            {"user_id": user_id},
            {"_id": 0},  
        )
        return list(agents)
    
    def delete_agent(self, agent_id: str, user_id: str) -> dict:
        logger.info("Attempting delete — agent_id=%s, user_id=%s", agent_id, user_id)
        self._verify_agent_ownership(agent_id, user_id)

        res = requests.delete(
            f"{ELEVENLABS_BASE_URL}/convai/agents/{agent_id}",
            headers=self.headers,
        )

        if res.status_code not in (200, 204):
            logger.error("ElevenLabs delete_agent failed: %s", res.text)
            error_message = "Failed to delete agent"
            try:
                error_message = res.json().get("detail", error_message)
            except Exception:
                pass
            raise CopyException(error_message, res.status_code)

        result = mongo.db.agents.delete_one({"agent_id": agent_id})
        logger.info("deleted_count=%d", result.deleted_count)

        return {"message": "Agent deleted successfully"}

    def get_user_agents_filtered(self, user_id: str, filters: dict = None) -> list:
        query = {"user_id": user_id}
        filters = filters or {}

        name = filters.get("name")
        specialty = filters.get("specialty")
        search = filters.get("search")
        date_from = filters.get("date_from")
        date_to = filters.get("date_to")

        and_clauses = []

        if name:
            query["name"] = {"$regex": name, "$options": "i"}

        if specialty:
            # `specialty` arrives as a list[str] from list_agents() (it splits the
            # comma-separated query param before calling this method).
            specialties = specialty if isinstance(specialty, list) else [specialty]

            if len(specialties) == 1:
                query["specialty"] = {"$regex": re.escape(specialties[0]), "$options": "i"}
            else:
                # Match ANY of the selected specialties (case-insensitive, partial match).
                # Kept as its own $and clause (not query["$or"]) so it can't collide
                # with the search $or below when both filters are applied together.
                and_clauses.append({
                    "$or": [
                        {"specialty": {"$regex": re.escape(s), "$options": "i"}}
                        for s in specialties
                    ]
                })

        if search:
            and_clauses.append({
                "$or": [
                    {"name": {"$regex": search, "$options": "i"}},
                    {"specialty": {"$regex": search, "$options": "i"}},
                ]
            })

        if and_clauses:
            query["$and"] = and_clauses

        if date_from or date_to:
            date_query = {}
            if date_from:
                date_query["$gte"] = date_from
            if date_to:
                date_query["$lte"] = date_to
            query["created_at"] = date_query

        agents = mongo.db.agents.find(query, {"_id": 0}).sort("created_at", -1)
        return list(agents)

    def preview_voice(self, data: dict) -> dict:
        voice_id = (data.get("voice_id") or "").strip()
        hospital_name = (data.get("hospital_name") or "Your Hospital").strip()

        if not voice_id:
            raise CopyException(voice_id_required, 400)

        text = (
            f"Thank you for calling {hospital_name}. "
            "I'm here to help you book or manage your appointment. "
            "How can I help you today?"
        )

        res = requests.post(
            f"{ELEVENLABS_BASE_URL}/text-to-speech/{voice_id}",
            headers=self.headers,
            json={
                "text": text,
                "model_id": "eleven_turbo_v2",
            },
        )

        if res.status_code != 200:
            logger.error("ElevenLabs preview_voice failed: %s", res.text)
            raise CopyException("Failed to generate voice preview", res.status_code)

        import base64
        audio_base64 = base64.b64encode(res.content).decode("utf-8")

        return {
            "voice_id": voice_id,
            "hospital_name": hospital_name,
            "audio_base64": audio_base64,
            "content_type": "audio/mpeg",
        }
   
    def _verify_agent_ownership(self, agent_id: str, user_id: str) -> None:
        record = mongo.db.agents.find_one(
            {"agent_id": agent_id, "user_id": user_id}
        )
        if not record:
            raise CopyException(
                agent_not_found, 404
            )


    def _build_prompt(self, roles: list) -> str:
        role_lines = []
        for role in roles:
            title = (role.get("title") or "").strip()
            description = (role.get("description") or "").strip()
            if title and description:
                role_lines.append(f"- {title}: {description}")
            elif title:
                role_lines.append(f"- {title}")

        if not role_lines:
            return BASE_PROMPT.strip()

        return BASE_PROMPT + "You are responsible for the following tasks:\n" + "\n".join(role_lines)