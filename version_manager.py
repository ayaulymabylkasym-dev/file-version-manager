
import os
import json
import difflib
import uuid
from datetime import datetime

STORAGE_FILE = "versions.json"

def load_versions():
    if not os.path.exists(STORAGE_FILE):
        return []
    with open(STORAGE_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

def save_version(document_text):
    versions = load_versions()
    version = {
        "id": str(uuid.uuid4())[:8],
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "content": document_text
    }
    versions.append(version)
    with open(STORAGE_FILE, "w", encoding="utf-8") as file:
        json.dump(versions, file, ensure_ascii=False, indent=4)
    return version["id"]

def list_versions():
    return load_versions()

def compare_versions(id1, id2):
    versions = load_versions()
    v1 = next((v for v in versions if v["id"] == id1), None)
    v2 = next((v for v in versions if v["id"] == id2), None)
    if v1 is None or v2 is None:
        raise ValueError("Нұсқа табылмады")
    return list(difflib.unified_diff(
        v1["content"].splitlines(),
        v2["content"].splitlines(),
        fromfile="1-нұсқа",
        tofile="2-нұсқа",
        lineterm=""
    ))

def restore_version(version_id):
    versions = load_versions()
    version = next((v for v in versions if v["id"] == version_id), None)
    if version is None:
        raise ValueError("Нұсқа табылмады")
    save_version(version["content"])
    return version["content"]


def compare_versions_as_text(id1, id2):
    """Return a readable text comparison of two document versions."""
    diff = compare_versions(id1, id2)

    if not diff:
        return "Нұсқалар арасында өзгеріс жоқ."

    return "\\n".join(diff)
