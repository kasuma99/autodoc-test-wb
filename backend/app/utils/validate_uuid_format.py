from uuid import UUID

from app.exceptions.uuid_exception import UUIDException


def validate_uuid_format(string: str | UUID) -> UUID:
    if not isinstance(string, UUID):
        try:
            uuid = UUID(string)
            return uuid
        except ValueError:
            raise UUIDException(
                message=f"Requested badly formed hexadecimal UUID string: {string}"
            )
    return string
