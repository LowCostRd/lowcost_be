import uuid
from datetime import datetime


class Agent:
    def __init__(
        self,
        user_id: str,
        agent_id: str,
        name: str,
        specialty: str = None,
        voice_id: str = None,
        image_url: str = None,
        roles: list = None,
        _id=None,
        created_at=None,
    ):
        self._id = _id or str(uuid.uuid4())
        self.user_id = user_id         
        self.agent_id = agent_id       
        self.name = name
        self.specialty = specialty     
        self.voice_id = voice_id
        self.image_url = image_url        
        self.roles = roles or []       
        self.created_at = created_at or datetime.now()
        self.updated_at = datetime.now()

    def to_dict(self):
        return {
            "_id": self._id,
            "user_id": self.user_id,
            "agent_id": self.agent_id,
            "name": self.name,
            "specialty": self.specialty,
            "voice_id": self.voice_id,
            "image_url": self.image_url,
            "roles": self.roles,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }