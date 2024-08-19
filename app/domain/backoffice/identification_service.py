import csv

from fastapi import UploadFile
from fastapi import status

from app.config.response import HTTPException
from app.data.backoffice import schemas
from app.data.models import IdentificationDetails
from app.data.backoffice.identification_repo import AbstractIdentificationRepo

def process_identification_file(file: UploadFile, identification_repo: AbstractIdentificationRepo):
    try:
        content = file.file.read().decode("utf-8").splitlines()
        reader = csv.DictReader(content)

        expected_headers = {"chassis_number", "plate_number", "type"}
        if set(reader.fieldnames) != expected_headers:
            raise HTTPException(
                title="Invalid headers",
                message=f"The headers in the file are invalid: Expected headers: ${expected_headers}",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        records_to_insert = []
        for row in reader:
            identification_detail = IdentificationDetails(
                chassis_number=row["chassis_number"],
                plate_number=row["plate_number"],
                type=row["type"],
            )
            records_to_insert.append(identification_detail)

        identification_repo.save_identification_details(records=records_to_insert)
        
    except Exception as e:
        raise HTTPException(
            title="Failed to process file",
            message=f"Failed to process file: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    finally:
        file.file.close()

    return schemas.IdentificationFileUploadResponseSchema(
        processed_records=len(records_to_insert)
    )
