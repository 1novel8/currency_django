import uuid


def upload_to(instance: str, filename: str) -> str:  # pylint: disable=unused-argument
    return f"{uuid.uuid4()}_{filename}"
