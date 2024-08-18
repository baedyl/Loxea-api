from abc import ABC
from abc import abstractmethod
from datetime import datetime
from datetime import timezone

from sqlmodel  import select, Session 

from app.data.models import IdentificationDetails


class AbstractIdentificationRepo(ABC):
    
    @abstractmethod
    def save_identification_details(self, records: list) -> None:...
    
    @abstractmethod
    def get_identification_from_chassis_number(self, chassis_number: str) -> IdentificationDetails | None:...
    
    @abstractmethod
    def get_identification_from_plate_number(self, plate_number: str) -> IdentificationDetails | None:...
    
    @abstractmethod
    def get_identification_from_id(self, id: int) -> IdentificationDetails | None:...
    
    @abstractmethod
    def update_identification(self, id: int, plate_number: str, chassis_number: str, type: str) -> IdentificationDetails | None:...
    
    @abstractmethod
    def soft_delete_identification(self, id: int) -> bool:...
    
    @abstractmethod
    def create_identification(self, plate_number: str, chassis_number: str, type: str) -> IdentificationDetails:...
    
    @abstractmethod
    def get_identification_details(self, offset: int, limit: int) -> list[IdentificationDetails]:...



class IdentificationRepo(AbstractIdentificationRepo):

    def __init__(self, session: Session) -> None:
        self._session = session

    
    def save_identification_details(self, records: list[IdentificationDetails]) -> int:
        """
        Saves a list of IdentificationDetails records to the database, ensuring no duplicates
        based on chassis_number or plate_number.

        Args:
            records (list[IdentificationDetails]): A list of IdentificationDetails objects to be saved.
        Returns:
            int: Number of records created.

        Raises:
            Exception: If there is an error during the database operation.
        """
        record_list = []
        for record in records:
            print(self.get_identification_from_chassis_number(chassis_number=record.chassis_number))
            print(self.get_identification_from_plate_number(plate_number=record.plate_number))

            if  (self.get_identification_from_chassis_number(chassis_number=record.chassis_number) is not None 
                or self.get_identification_from_plate_number(plate_number=record.plate_number) is not None):
                print("record exists")
                continue 
            
            record_list.append(record)
        
        if len(record_list) == 0:
            return 0
        
        try:
            self._session.bulk_save_objects(record_list)
            self._session.commit()
        except Exception as e:
            self._session.rollback()
            raise e 

        return len(record_list)

          
    def get_identification_from_chassis_number(self, chassis_number: str) -> IdentificationDetails | None:
        """
        Retrieves an IdentificationDetails record based on the chassis number.

        Args:
            chassis_number (str): The chassis number to search for.

        Returns:
            IdentificationDetails | None: The IdentificationDetails record if found, otherwise None.
        """
        record = self._session.exec(
            select(IdentificationDetails).where(
                (IdentificationDetails.chassis_number == chassis_number) & (IdentificationDetails.is_deleted == False)
            )
        ).one_or_none()
        return record 
    
    def get_identification_from_plate_number(self, plate_number: str) -> IdentificationDetails | None:
        """
        Retrieves an IdentificationDetails record based on the plate number.

        Args:
            plate_number (str): The plate number to search for.

        Returns:
            IdentificationDetails | None: The IdentificationDetails record if found, otherwise None.
        """
        record = self._session.exec(
            select(IdentificationDetails).where(
                (IdentificationDetails.plate_number == plate_number) & (IdentificationDetails.is_deleted == False)
            )
        ).one_or_none()
        return record 
    
    def get_identification_from_id(self, id: int) -> IdentificationDetails | None:
        """
        Retrieves an IdentificationDetails record based on the ID.

        Args:
            id (int): The ID of the identification detail to search for.

        Returns:
            IdentificationDetails | None: The IdentificationDetails record if found, otherwise None.
        """
        record = self._session.exec(
            select(IdentificationDetails).where(
                (IdentificationDetails.id == id) & (IdentificationDetails.is_deleted == False)
            )
        ).one_or_none()
        return record 

    def soft_delete_identification(self, id: int) -> bool:
        """
        Soft deletes an IdentificationDetails record by marking it as deleted.

        Args:
            id (int): The ID of the identification detail to soft delete.

        Returns:
            bool: True if the record was already deleted or successfully soft deleted, False if the record was not found.
        """
        record = self.get_identification_from_id(id)
        if not record:
            return False 
        if record.is_deleted:
            return True 

        record.is_deleted = True 
        record.deleted_at = datetime.now(timezone.utc)
        self._session.commit()
        return True 
    

    def get_identification_details(self, offset: int, limit: int) -> list[IdentificationDetails]:
        """
        Retrieves a paginated list of identification details that have not been soft-deleted.
        If limit is set to 0, all records starting from the offset will be returned.

        Args:
            offset (int): The starting position for the records to retrieve.
            limit (int): The maximum number of records to retrieve. If set to 0, all records are returned.

        Returns:
            list[IdentificationDetails]: A list of IdentificationDetails objects.
        """
        query = select(IdentificationDetails).where(IdentificationDetails.is_deleted == False).offset(offset)

        if limit > 0:
            query = query.limit(limit)

        records = self._session.exec(query).all()
        
        return records

    def update_identification(self, id: int, plate_number: str, chassis_number: str, type: str) -> IdentificationDetails | None:
        """
        Updates an existing IdentificationDetails record with new values, ensuring no duplicates 
        for chassis_number and plate_number.

        Args:
            id (int): The ID of the IdentificationDetails record to update.
            plate_number (str): The new plate number to set.
            chassis_number (str): The new chassis number to set.
            type (str): The new type to set.

        Returns:
            IdentificationDetails | None: The updated IdentificationDetails record if the update was successful, otherwise None.
        """
        record = self.get_identification_from_id(id)
        
        if record is None:
            return None 
        
        existing_records = self._session.exec(
            select(IdentificationDetails).where(
                (IdentificationDetails.id != id) &
                (IdentificationDetails.is_deleted == False) &
                ((IdentificationDetails.chassis_number == chassis_number) |
                (IdentificationDetails.plate_number == plate_number))
            )
        ).all()
        
        if existing_records:
            raise ValueError("A record with the same chassis number or plate number already exists.")
        
        record.plate_number = plate_number
        record.chassis_number = chassis_number
        record.type = type
        self._session.commit()
        
        return record

       

    def create_identification(self, plate_number: str, chassis_number: str, type: str) -> IdentificationDetails:
        """
        Creates a new IdentificationDetails record in the database.

        Args:
            plate_number (str): The plate number to set for the new record.
            chassis_number (str): The chassis number to set for the new record.
            type (str): The type to set for the new record.

        Returns:
            IdentificationDetails: The newly created IdentificationDetails record.
        """
        existing_record = self._session.exec(
            select(IdentificationDetails).where(
                (IdentificationDetails.is_deleted == False) &
                ((IdentificationDetails.chassis_number == chassis_number) |
                (IdentificationDetails.plate_number == plate_number))
            )
        ).one_or_none()

        if existing_record:
            raise ValueError("A record with the same chassis number or plate number already exists.")

        record = IdentificationDetails(
            plate_number=plate_number,
            chassis_number=chassis_number,
            type=type
        )
        self._session.add(record)
        self._session.commit()
        
        return record