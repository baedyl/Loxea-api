import unittest
from unittest.mock import MagicMock
from app.data.backoffice.identification_repo import IdentificationRepo
from app.data.models import IdentificationDetails

class TestIdentificationRepo(unittest.TestCase):

    def setUp(self):
        """Initialize mock session and repo for each test."""
        self.mock_session = MagicMock()
        self.repo = IdentificationRepo(self.mock_session)

    def test_save_identification_details(self):
        """
        Test saving identification details to the database.
        Verify that `bulk_save_objects` and `commit` are called.
        Verify that `rollback` is called if an exception occurs.
        """
        records = [
            IdentificationDetails(chassis_number="1234", plate_number="ABC123", type="Car"),
            IdentificationDetails(chassis_number="5678", plate_number="XYZ789", type="Truck"),
            IdentificationDetails(chassis_number="0000", plate_number="DEF456", type="Bike")
        ]

        # Configure mock methods
        # Mock get_identification_from_chassis_number and get_identification_from_plate_number to return None
        # indicating that no existing records are found
        self.repo.get_identification_from_chassis_number = MagicMock(return_value=None)
        self.repo.get_identification_from_plate_number = MagicMock(return_value=None)

        # Call method under test
        result = self.repo.save_identification_details(records)

        # Verify that `bulk_save_objects` was called with the correct arguments
        self.mock_session.bulk_save_objects.assert_called_once_with(records[:3])
        self.mock_session.commit.assert_called_once()
        self.mock_session.rollback.assert_not_called()

        # Check the number of records created
        self.assertEqual(result, 3)

        # Reset mock session for testing exception handling
        self.mock_session.reset_mock()
        self.repo.get_identification_from_chassis_number = MagicMock(side_effect=[None, None, None])
        self.repo.get_identification_from_plate_number = MagicMock(side_effect=[None, None, None])
        self.mock_session.bulk_save_objects.side_effect = Exception("Test Exception")

        with self.assertRaises(Exception) as context:
            self.repo.save_identification_details(records)
        
            # Verify rollback was called due to the exception
            self.mock_session.rollback.assert_called_once()
            self.mock_session.commit.assert_not_called()
            self.assertTrue("Test Exception" in str(context.exception))
    

    def test_get_identification_from_chassis_number(self):
        """
        Test retrieving identification details by chassis number.
        """
        self.mock_session.exec.return_value.one_or_none.return_value = IdentificationDetails(
            chassis_number="1234", plate_number="ABC123", type="Car"
        )
        result = self.repo.get_identification_from_chassis_number("1234")
        self.assertIsNotNone(result)
        self.assertEqual(result.chassis_number, "1234")
        self.mock_session.exec.assert_called_once()

    def test_get_identification_from_plate_number(self):
        """
        Test retrieving identification details by plate number.
        """
        self.mock_session.exec.return_value.one_or_none.return_value = IdentificationDetails(
            chassis_number="1234", plate_number="ABC123", type="Car"
        )
        result = self.repo.get_identification_from_plate_number("ABC123")
        self.assertIsNotNone(result)
        self.assertEqual(result.plate_number, "ABC123")
        self.mock_session.exec.assert_called_once()

    def test_get_identification_from_id(self):
        """
        Test retrieving identification details by ID.
        """
        self.mock_session.exec.return_value.one_or_none.return_value = IdentificationDetails(
            id=1, chassis_number="1234", plate_number="ABC123", type="Car"
        )
        result = self.repo.get_identification_from_id(1)
        self.assertIsNotNone(result)
        self.assertEqual(result.id, 1)
        self.mock_session.exec.assert_called_once()

    def test_soft_delete_identification(self):
        """
        Test soft deleting an identification detail.
        """
        identification = IdentificationDetails(id=1, is_deleted=False)
        self.repo.get_identification_from_id = MagicMock(return_value=identification)
        
        result = self.repo.soft_delete_identification(1)
        self.assertTrue(result)
        self.assertTrue(identification.is_deleted)
        self.assertIsNotNone(identification.deleted_at)
        self.mock_session.commit.assert_called_once()

    def test_get_identification_details(self):
        """
        Test retrieving identification details with pagination.
        """
        self.mock_session.exec.return_value.all.return_value = [
            IdentificationDetails(id=1), IdentificationDetails(id=2)
        ]
        result = self.repo.get_identification_details(offset=0, limit=10)
        self.assertEqual(len(result), 2)
        self.mock_session.exec.assert_called_once()
        
    def test_get_identification_details_no_limit(self):
        """
        Test retrieving all identification details when limit is set to 0.
        """
        self.mock_session.exec.return_value.all.return_value = [
            IdentificationDetails(id=1), IdentificationDetails(id=2)
        ]
        result = self.repo.get_identification_details(offset=0, limit=0)
        self.assertEqual(len(result), 2)
        self.mock_session.exec.assert_called_once()

    def test_get_identification_details_empty_result(self):
        """
        Test retrieving identification details when no records match the query.
        """
        self.mock_session.exec.return_value.all.return_value = []
        result = self.repo.get_identification_details(offset=0, limit=10)
        self.assertEqual(len(result), 0)
        self.mock_session.exec.assert_called_once()

if __name__ == '__main__':
    unittest.main()
