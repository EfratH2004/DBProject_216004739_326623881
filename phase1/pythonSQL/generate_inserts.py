import random
from datetime import datetime, timedelta

NUM_CUSTOMERS = 500
NUM_EMPLOYEES = 500
NUM_PRODUCTS = 500
NUM_REQUESTS = 20000
NUM_TRANSACTIONS = 20000

all_customers = list(range(1, NUM_CUSTOMERS + 1))
random.shuffle(all_customers)

private_customers = all_customers[:300]
business_customers = all_customers[300:]

allowed_transaction_customers = random.sample(all_customers, 250)

first_names = ["Noa", "Dana", "Maya", "Yael", "Lior", "Tomer"]
last_names = ["Levi", "Cohen", "Mizrahi", "Biton", "Shani"]

companies = ["Tech", "Global", "NextGen", "Smart", "Future"]
contact_names = ["Avi Cohen", "Gil Levi", "Dana Mor"]

request_notes = [
    '{"issue":"late"}',
    '{"issue":"broken"}',
    '{"issue":"refund"}',
    '{"issue":"support"}'
]

# =========================
# PRIVATE
# =========================
with open("private_inserts.sql", "w", encoding="utf-8") as f:
    for cid in private_customers:
        first = random.choice(first_names)
        last = random.choice(last_names)
        birthday = (datetime.now() - timedelta(days=random.randint(7000, 20000))).date()
        gender = random.choice(["Male", "Female"])

        f.write(f"""INSERT INTO PRIVATE VALUES ('{first}','{last}','{birthday}','{gender}',{cid});
""")

# =========================
# BUSINESS
# =========================
with open("business_inserts.sql", "w", encoding="utf-8") as f:
    for cid in business_customers:
        contact = random.choice(contact_names)
        company = random.choice(companies) + str(cid)
        site = f"www.{company.lower()}.com"

        f.write(f"""INSERT INTO BUSINESS VALUES ('{contact}','{company}','{site}',{cid});
""")

# =========================
# REQUESTS
# =========================
with open("requests_inserts.sql", "w", encoding="utf-8") as f:
    for rid in range(1, NUM_REQUESTS + 1):
        date = (datetime.now() - timedelta(days=random.randint(0, 1000))).date()
        note = random.choice(request_notes)
        cid = random.randint(1, NUM_CUSTOMERS)
        eid = random.randint(1, NUM_EMPLOYEES)
        rs = random.randint(1, 20)
        pr = random.randint(1, 20)

        f.write(f"""INSERT INTO REQUESTS VALUES ({rid},'{date}','{note}',{cid},{eid},{rs},{pr});
""")

# =========================
# TRANSACTIONS
# =========================
with open("transactions_inserts.sql", "w", encoding="utf-8") as f:
    for tid in range(1, NUM_TRANSACTIONS + 1):
        date = (datetime.now() - timedelta(days=random.randint(0, 1000))).date()
        cid = random.choice(allowed_transaction_customers)
        eid = random.randint(1, NUM_EMPLOYEES)
        pid = random.randint(1, NUM_PRODUCTS)

        f.write(f"""INSERT INTO TRANSACTIONS VALUES ({tid},'{date}',{cid},{eid},{pid});
""")

print("✅ All SQL files created!")