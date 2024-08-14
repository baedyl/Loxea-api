import csv
from typing import List
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session

from app.data.models import IdentificationDetails
from app.data.backoffice import schemas


def process_identification_file(file: UploadFile, db: Session):
    try:
        content = file.file.read().decode("utf-8").splitlines()
        reader = csv.DictReader(content)

        expected_headers = {"chassis_number", "plate_number", "type"}
        if set(reader.fieldnames) != expected_headers:
            raise HTTPException(status_code=400, detail="Invalid CSV headers")

        records_to_insert = []
        for row in reader:
            identification_detail = IdentificationDetails(
                chassis_number=row["chassis_number"],
                plate_number=row["plate_number"],
                type=row["type"]
            )
            records_to_insert.append(identification_detail)

        db.bulk_save_objects(records_to_insert)
        db.commit()

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")
    finally:
        file.file.close()

    return schemas.IdentificationFileUploadResponseSchema(
        processed_records = len(records_to_insert)
    )
