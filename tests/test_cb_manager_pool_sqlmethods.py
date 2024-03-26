import unittest
from src.backend.database.db_manager import Database_Pool_Manager  # Adjust the import as necessary

class TestDatabasePoolManager(unittest.TestCase):
    def setUp(self):
        self.db_manager = Database_Pool_Manager()

    def test_get_table_data(self):
        """Test the get_table_data method for SQL syntax correctness and execution."""
        try:
            results = self.db_manager.get_table_data()
            self.assertIsInstance(results, list)
            self.assertNotEqual(len(results), 0)
        except Exception as e:
            self.fail(f"Execution of get_table_data failed: {e}")

if __name__ == '__main__':
    unittest.main()
