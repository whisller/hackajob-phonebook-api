from flask_httpauth import HTTPBasicAuth
from hackajob_phone_book_api import API_AUTH

auth = HTTPBasicAuth()


@auth.get_password
def get_pw(username):
    if username == API_AUTH[0]:
        return API_AUTH[1]
    return None
