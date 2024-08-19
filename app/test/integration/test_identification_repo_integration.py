import unittest
from sqlmodel import create_engine, SQLModel, Session
from app.data.models import IdentificationDetails
from app.data.backoffice.identification_repo import IdentificationRepo

class TestIdentificationRepoIntegration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine("sqlite:///:memory:")
        SQLModel.metadata.create_all(cls.engine)

    def setUp(self):
        self.session = Session(self.engine)
        self.repo = IdentificationRepo(self.session)

    def tearDown(self):
        self.session.close()

    def test_save_identification_details(self):
        records = [IdentificationDetails(chassis_number="1234", plate_number="ABC123", type="Car")]
        self.repo.save_identification_details(records)
        result = self.repo.get_identification_details(offset=0, limit=5)
        self.assertGreaterEqual(len(result), 1)

    def test_get_identification_from_chassis_number(self):
        records = [IdentificationDetails(chassis_number="1234", plate_number="ABC123", type="Car")]
        self.repo.save_identification_details(records)
        result = self.repo.get_identification_from_chassis_number("1234")
        self.assertIsNotNone(result)

    def test_get_identification_from_plate_number(self):
        records = [IdentificationDetails(chassis_number="1234", plate_number="ABC123", type="Car")]
        self.repo.save_identification_details(records)
        result = self.repo.get_identification_from_plate_number("ABC123")
        self.assertIsNotNone(result)

    def test_get_identification_from_id(self):
        record = self.repo.create_identification(chassis_number="123456", plate_number = "LT 308 X", type="Truck")
        result = self.repo.get_identification_from_id(record.id)
        self.assertIsNotNone(result)

    def test_soft_delete_identification(self):
        record = self.repo.create_identification(chassis_number="1256358", plate_number="Z1235 W", type="Car")
        result = self.repo.soft_delete_identification(record.id)
        self.assertTrue(result)
        self.assertTrue(record.is_deleted)

    def test_get_identification_details(self):
        identification1 = IdentificationDetails(chassis_number="1234", plate_number="ABC123", type="Car")
        identification2 = IdentificationDetails(chassis_number="5678", plate_number="DEF456", type="Truck")
        self.repo.save_identification_details([identification1, identification2])
        result = self.repo.get_identification_details(offset=0, limit=0)
        self.assertGreaterEqual(len(result), 2)


if __name__ == '__main__':
    unittest.main()
