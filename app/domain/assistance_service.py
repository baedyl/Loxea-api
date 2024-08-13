from app.data.assistance_repo import AbstractAssistanceRepo
from app.data.models import IncidentType
from app.domain.storage import StorageBase


def request_assistance(
        user_id: int,
        latitude: str,
        longitude: str,
        address_complement: str,
        comment: str,
        type_: IncidentType,
        images: list[bytes] | None,
        image_extensions: list[str] | None,
        assistance_repo: AbstractAssistanceRepo,
        storage: StorageBase,
):
    record = {}
    match type_:
        case IncidentType.Assistance:
            record = assistance_repo.create_incidence_record(
                user_id=user_id,
                latitude=latitude,
                longitude=longitude,
                address_complement=address_complement,
                comment=comment,
                type_=type_,
                images=images
            )
        case IncidentType.Accident:
            ...
        # Call storage to store images and save record to db
    return record
