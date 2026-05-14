from flask import Flask, jsonify, request, abort
from service import app, status
from service.models import Account, db
from flask_cors import CORS 
from flask_talisman import Talisman

# Jika app sudah di-import dari 'service' di baris 2, 
# kita tidak perlu mendefinisikannya lagi di sini dengan Flask(__name__).
# Cukup gunakan app yang sudah ada.

CORS(app)
Talisman(app, force_https=False)

@app.route("/", methods=["GET"])
def index():
    """Halaman Utama"""
    return jsonify(name="Account REST API Service", version="1.0"), status.HTTP_200_OK


######################################################################
# CREATE A NEW ACCOUNT
######################################################################
@app.route("/accounts", methods=["POST"])
def create_accounts():
    """Membuat Akun baru"""
    app.logger.info("Request to create an Account")
    data = request.get_json()

    account = Account()
    account.name = data.get("name")
    account.create()

    return jsonify(account.serialize()), status.HTTP_201_CREATED


######################################################################
# LIST ALL ACCOUNTS
######################################################################
@app.route("/accounts", methods=["GET"])
def list_accounts():
    """List semua Akun"""
    app.logger.info("Request to list Accounts")
    accounts = Account.query.all()
    results = [account.serialize() for account in accounts]
    return jsonify(results), status.HTTP_200_OK


######################################################################
# READ AN ACCOUNT
######################################################################
@app.route("/accounts/<int:account_id>", methods=["GET"])
def get_accounts(account_id):
    """Read an Account"""
    app.logger.info("Request to read account with id: %s", account_id)
    account = Account.find(account_id)
    if not account:
        abort(status.HTTP_404_NOT_FOUND, f"Account with id [{account_id}] not found.")
    return jsonify(account.serialize()), status.HTTP_200_OK


######################################################################
# UPDATE AN EXISTING ACCOUNT
######################################################################
@app.route("/accounts/<int:account_id>", methods=["PUT"])
def update_accounts(account_id):
    """Update an Account"""
    app.logger.info("Request to update account with id: %s", account_id)
    account = Account.find(account_id)
    if not account:
        abort(status.HTTP_404_NOT_FOUND, f"Account with id [{account_id}] not found.")
    data = request.get_json()
    if "name" in data:
        account.name = data["name"]
    db.session.commit()
    return jsonify(account.serialize()), status.HTTP_200_OK


######################################################################
# DELETE AN ACCOUNT
######################################################################
@app.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_accounts(account_id):
    """Delete an Account"""
    app.logger.info("Request to delete account with id: %s", account_id)
    account = Account.find(account_id)
    if account:
        db.session.delete(account)
        db.session.commit()
    return "", status.HTTP_204_NO_CONTENT