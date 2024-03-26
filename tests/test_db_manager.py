import unittest
from unittest.mock import patch, MagicMock
from src.backend.database.db_manager import Database_Pool_Manager

class TestDatabasePoolManager(unittest.TestCase):
    @patch('src.backend.database.db_manager.PooledDB')
    def test_get_table_data(self, mock_pooled_db):

        mock_connection = MagicMock()
        mock_cursor = MagicMock()


        mock_cursor.fetchall.return_value = [
            {
                'KEYWORD': 'test',
                'TODAY_COUNT': 1,
                'SUBREDDIT': 'test_subreddit',
                'RATIO_24H': 1.00,
                'RATIO_1W': 1.00,
                'RATIO_1M': 1.00,
            }
        ]


        mock_connection.cursor.return_value = mock_cursor
        mock_connection.__enter__.return_value = mock_connection
        mock_connection.__exit__.return_value = None

        mock_pooled_db.return_value.connection.return_value = mock_connection

        db_pool_manager = Database_Pool_Manager()
        results = db_pool_manager.get_table_data()
        print("lol")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['KEYWORD'], 'test')
        self.assertEqual(results[0]['TODAY_COUNT'], 1)
        self.assertEqual(results[0]['SUBREDDIT'], 'test_subreddit')
        self.assertEqual(type(results), type([]))
        self.assertAlmostEqual(results[0]['RATIO_24H'], 1.00)
        self.assertAlmostEqual(results[0]['RATIO_1W'], 1.00)
        self.assertAlmostEqual(results[0]['RATIO_1M'], 1.00)

if __name__ == '__main__':
    unittest.main()
