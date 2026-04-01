from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.core.config import settings


def ensure_upload_dir() -> Path:
    path = Path(settings.upload_dir)
    path.mkdir(parents=True, exist_ok=True)
    return path


def save_event_attachment(evento_id: str, upload: UploadFile) -> tuple[str, str]:
    upload_dir = ensure_upload_dir()
    original = upload.filename or "arquivo"
    suffix = Path(original).suffix
    stored_name = f"{evento_id}_{uuid4().hex}{suffix}"
    full_path = upload_dir / stored_name

    with full_path.open("wb") as out:
        out.write(upload.file.read())

    return str(full_path), original


def delete_file_if_exists(path: str | None) -> None:
    if not path:
        return
    file_path = Path(path)
    if file_path.exists() and file_path.is_file():
        file_path.unlink()

