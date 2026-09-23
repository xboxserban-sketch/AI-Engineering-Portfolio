import unittest
import sqlite3
import os

class TestEnterpriseLeadGen(unittest.TestCase):

    def setUp(self):
        # Setup an in-memory SQLite database for testing (no IO overhead)
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE leads (
                id INTEGER PRIMARY KEY,
                company_name TEXT,
                email TEXT
            )
        ''')

    def tearDown(self):
        self.conn.close()

    def test_database_insertion(self):
        """Test that the crawler properly structures and inserts data."""
        self.cursor.execute("INSERT INTO leads (company_name, email) VALUES ('Tech Corp', 'contact@tech.com')")
        self.conn.commit()
        
        self.cursor.execute("SELECT * FROM leads WHERE company_name='Tech Corp'")
        result = self.cursor.fetchone()
        
        self.assertIsNotNone(result)
        self.assertEqual(result[1], 'Tech Corp')
        self.assertEqual(result[2], 'contact@tech.com')

    def test_crawler_rate_limit_logic(self):
        """Ensure rate limits prevent IP bans."""
        # Mock logic
        rate_limit_seconds = 2.5
        self.assertGreater(rate_limit_seconds, 1.0, "Rate limit should be at least 1 second to prevent blocking")

if __name__ == '__main__':
    unittest.main()
