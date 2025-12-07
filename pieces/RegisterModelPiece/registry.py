import json
import os
import uuid
import datetime

#_REGISTRY_PATH = os.getenv(
#    "LOCAL_MODEL_REGISTRY",
#    os.path.join(os.getcwd(), "model_registry.json")
#)
_REGISTRY_PATH = os.path.join("/home/shared_storage/data/", "model_registry.json")

def _load_db():
    try:
        with open(_REGISTRY_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"models": [], "versions": []}

def _save_db(db):
    dirpath = os.path.dirname(_REGISTRY_PATH)
    #if dirpath:
    #    os.makedirs(dirpath, exist_ok=True)
    with open(_REGISTRY_PATH, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2, ensure_ascii=False)

class Model:
    def __init__(self, id: str, name: str, description: str = ""):
        self.id = id
        self.name = name
        self.description = description

    @classmethod
    def get_or_create(cls, name: str, description: str = "") -> "Model":
        db = _load_db()
        for m in db["models"]:
            if m.get("name") == name:
                return cls(m["id"], m.get("name"), m.get("description", ""))
        new_id = str(uuid.uuid4())
        model = {"id": new_id, "name": name, "description": description}
        db["models"].append(model)
        _save_db(db)
        return cls(new_id, name, description)

class ModelVersion:
    def __init__(self, id: str, model_id: str, files: list, metadata: dict, description: str = ""):
        self.id = id
        self.model_id = model_id
        self.files = files
        self.metadata = metadata
        self.description = description

    @classmethod
    def create(cls, model: Model, files: list, metadata: dict = None, description: str = "") -> "ModelVersion":
        if metadata is None:
            metadata = {}
        db = _load_db()
        version_id = str(uuid.uuid4())
        now = datetime.datetime.utcnow().isoformat() + "Z"
        v = {
            "id": version_id,
            "model_id": model.id,
            "files": files,
            "metadata": metadata,
            "description": description,
            "created_at": now,
        }
        db["versions"].append(v)
        _save_db(db)
        return cls(version_id, model.id, files, metadata, description)
