import unittest
from service import app, status
from service.models import db, Account

BASE_URL = "/accounts"

class TestAccountRoutes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
        with app.app_context():
            db.create_all()

    def setUp(self):
        with app.app_context():
            db.session.query(Account).delete()
            db.session.commit()
        self.client = app.test_client()

    def _create_accounts(self, count):
        accounts = []
        with app.app_context():
            for _ in range(count):
                account = Account(name="Test User")
                account.create()
                db.session.refresh(account)
                accounts.append(account)
                account.temp_id = account.id 
        return accounts

    # ----------------------------------------------------------
    # TEST CASES UNTUK INDEX (Tambahan biar Coverage naik)
    # ----------------------------------------------------------
    def test_index(self):
        """It should return the index page"""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"], "Account REST API Service")

    # ----------------------------------------------------------
    # TEST CASES UNTUK CREATE (Tambahan biar POST tercover)
    # ----------------------------------------------------------
    def test_create_account(self):
        """It should Create a new Account"""
        account_data = {"name": "John Doe"}
        resp = self.client.post(
            BASE_URL,
            json=account_data,
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        new_account = resp.get_json()
        self.assertEqual(new_account["name"], "John Doe")

    # ----------------------------------------------------------
    # TEST CASES UNTUK READ
    # ----------------------------------------------------------
    def test_get_account(self):
        """It should Read a single Account"""
        account = self._create_accounts(1)[0]
        resp = self.client.get(f"{BASE_URL}/{account.temp_id}")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"], account.name)

    def test_get_account_not_found(self):
        """It should not Read an Account that is not found"""
        resp = self.client.get(f"{BASE_URL}/0")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    # ----------------------------------------------------------
    # TEST CASES UNTUK UPDATE
    # ----------------------------------------------------------
    def test_update_account(self):
        """It should Update an existing Account"""
        account = self._create_accounts(1)[0]
        new_account = {"name": "Updated Name"}
        
        resp = self.client.put(
            f"{BASE_URL}/{account.temp_id}", 
            json=new_account, 
            content_type="application/json"
        )
        
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_account = resp.get_json()
        self.assertEqual(updated_account["name"], "Updated Name")

    def test_update_account_not_found(self):
        """It should not Update an Account that is not found"""
        resp = self.client.put(f"{BASE_URL}/0", json={"name": "test"})
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    # ----------------------------------------------------------
    # TEST CASES UNTUK DELETE
    # ----------------------------------------------------------
    def test_delete_account(self):
        """It should Delete an Account"""
        account = self._create_accounts(1)[0]
        resp = self.client.delete(f"{BASE_URL}/{account.temp_id}")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    # ----------------------------------------------------------
    # TEST CASES UNTUK LIST
    # ----------------------------------------------------------
    def test_get_account_list(self):
        """It should Get a list of Accounts"""
        self._create_accounts(5)
        resp = self.client.get(BASE_URL)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 5)