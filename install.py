from hackajob_phone_book_api import database
from hackajob_phone_book_api.models import Entry, Phone, Email, Address

tables = (Entry, Phone, Email, Address)

with database.execution_context():
    database.drop_tables(tables, safe=True)
    database.create_tables(tables, safe=True)
