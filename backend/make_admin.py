# run this once to make the first admin
# usage: python make_admin.py youremail@gmail.com
# the user must be registered first
import sys
from models import get_db, create_tables

if len(sys.argv) != 2:
    print("Usage: python make_admin.py email")
    sys.exit()

email = sys.argv[1].strip().lower()

create_tables()
conn = get_db()
result = conn.execute("UPDATE users SET role = 'admin' WHERE email = ?", (email,))
conn.commit()
conn.close()

if result.rowcount == 0:
    print("No user found with this email. Register first.")
else:
    print(email + " is now an admin. Login again to see the admin page.")
