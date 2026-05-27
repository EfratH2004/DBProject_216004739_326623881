BEGIN;

-- 1. חיבור זמני לבסיס של הזוג השני
CREATE EXTENSION IF NOT EXISTS postgres_fdw;

DROP SCHEMA IF EXISTS other_src CASCADE;
DROP SERVER IF EXISTS other_department_server CASCADE;

CREATE SCHEMA other_src;

CREATE SERVER other_department_server
FOREIGN DATA WRAPPER postgres_fdw
OPTIONS (
    host '127.0.0.1',
    dbname 'other_department_db',
    port '5432'
);

CREATE USER MAPPING FOR CURRENT_USER
SERVER other_department_server
OPTIONS (
    user 'meitav',
    password 'meitavandefrat'
);

IMPORT FOREIGN SCHEMA public
FROM SERVER other_department_server
INTO other_src;


-- 2. הוספת טבלאות חסרות מהמערכת השנייה

CREATE TABLE IF NOT EXISTS seasons (
    s_id INT PRIMARY KEY,
    s_name VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS paymentmethod (
    pm_id INT PRIMARY KEY,
    pm_name VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS transactionstatus (
    t_status_id INT PRIMARY KEY,
    t_status_name VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS contains (
    tid INT,
    pid INT,
    quantity INT,
    unit_price NUMERIC(6,2),
    PRIMARY KEY (tid, pid),
    FOREIGN KEY (tid) REFERENCES transactions(tid),
    FOREIGN KEY (pid) REFERENCES products(pid)
);


-- 3. הוספת עמודות חסרות לטבלאות קיימות

ALTER TABLE products
ADD COLUMN IF NOT EXISTS manufactured_in VARCHAR(50),
ADD COLUMN IF NOT EXISTS stock_qty INT,
ADD COLUMN IF NOT EXISTS s_id INT;

ALTER TABLE transactions
ADD COLUMN IF NOT EXISTS amount NUMERIC(6,2),
ADD COLUMN IF NOT EXISTS has_discount BOOLEAN,
ADD COLUMN IF NOT EXISTS shipping_details_json JSON,
ADD COLUMN IF NOT EXISTS pm_id INT,
ADD COLUMN IF NOT EXISTS t_status_id INT;

ALTER TABLE requests
ADD COLUMN IF NOT EXISTS subject VARCHAR(100),
ADD COLUMN IF NOT EXISTS interaction_log_json JSON,
ADD COLUMN IF NOT EXISTS resolved_at DATE;

ALTER TABLE customers
ADD COLUMN IF NOT EXISTS has_club_card BOOLEAN;


-- 4. הוספת נתוני lookup

INSERT INTO seasons (s_id, s_name)
SELECT s_id::INT, s_name
FROM other_src.seasons
ON CONFLICT (s_id) DO NOTHING;

INSERT INTO paymentmethod (pm_id, pm_name)
SELECT pm_id::INT, pm_name
FROM other_src.paymentmethod
ON CONFLICT (pm_id) DO NOTHING;

INSERT INTO transactionstatus (t_status_id, t_status_name)
SELECT t_status_id::INT, t_status_name
FROM other_src.transactionstatus
ON CONFLICT (t_status_id) DO NOTHING;

INSERT INTO rstatus (rs_id, rs_name)
SELECT i_status_id::INT + 1000000, i_status_name
FROM other_src.inquirystatus
ON CONFLICT (rs_id) DO NOTHING;

INSERT INTO priority (priority_id, priority_name)
SELECT DISTINCT priority + 1000000, 'Priority ' || priority
FROM other_src.inquiries
ON CONFLICT (priority_id) DO NOTHING;


-- 5. הכנסת לקוחות מהמערכת השנייה

INSERT INTO customers (
    cid,
    cphone,
    cemail,
    caddress,
    registration_date,
    cnote_json,
    cs_id,
    has_club_card
)
SELECT
    c_id::INT + 1000000,
    c_phone,
    NULL,
    address,
    CURRENT_DATE,
    NULL,
    (SELECT MIN(cs_id) FROM cstatus),
    has_club_card
FROM other_src.customers
ON CONFLICT (cid) DO NOTHING;


-- 6. הכנסת לקוחות המערכת השנייה כ-private

INSERT INTO private (
    cid,
    first_name,
    last_name,
    birthday,
    gender
)
SELECT
    c_id::INT + 1000000,
    split_part(c_name, ' ', 1),
    NULLIF(substring(c_name from position(' ' in c_name) + 1), ''),
    NULL,
    NULL
FROM other_src.customers
ON CONFLICT (cid) DO NOTHING;


-- 7. הכנסת עובדים

INSERT INTO employee (
    eid,
    ename,
    ephone,
    eaddress,
    start_date,
    end_date
)
SELECT
    e_id::INT + 1000000,
    e_name,
    e_phone,
    NULL,
    hire_date,
    NULL
FROM other_src.employees
ON CONFLICT (eid) DO NOTHING;


-- 8. הכנסת מוצרים

INSERT INTO products (
    pid,
    pname,
    price,
    warranty_period,
    category,
    manufactured_in,
    stock_qty,
    s_id
)
SELECT
    p_id::INT + 1000000,
    p_name,
    price::INT,
    NULL,
    NULL,
    manufactured_in,
    stock_qty,
    s_id::INT
FROM other_src.products
ON CONFLICT (pid) DO NOTHING;


-- 9. הכנסת עסקאות

INSERT INTO transactions (
    tid,
    transaction_date,
    cid,
    eid,
    pid,
    amount,
    has_discount,
    shipping_details_json,
    pm_id,
    t_status_id
)
SELECT
    t_id::INT + 1000000,
    transaction_datetime,
    c_id::INT + 1000000,
    NULL,
    NULL,
    amount,
    has_discount,
    shipping_details_json,
    pm_id::INT,
    t_status_id::INT
FROM other_src.transactions
ON CONFLICT (tid) DO NOTHING;


-- 10. הכנסת הקשר בין עסקאות למוצרים

INSERT INTO contains (
    tid,
    pid,
    quantity,
    unit_price
)
SELECT
    t_id::INT + 1000000,
    p_id::INT + 1000000,
    quantity,
    unit_price
FROM other_src.contains
ON CONFLICT (tid, pid) DO NOTHING;


-- 11. הכנסת פניות מהמערכת השנייה לתוך requests

INSERT INTO requests (
    rid,
    open_date,
    rnote_json,
    cid,
    eid,
    rs_id,
    priority_id,
    subject,
    interaction_log_json,
    resolved_at
)
SELECT
    i_id::INT + 1000000,
    created_at,
    NULL,
    c_id::INT + 1000000,
    e_id::INT + 1000000,
    i_status_id::INT + 1000000,
    priority + 1000000,
    subject,
    interaction_log_json,
    resolved_at
FROM other_src.inquiries
ON CONFLICT (rid) DO NOTHING;


-- 12. הוספת FK חדשים

ALTER TABLE products
DROP CONSTRAINT IF EXISTS fk_products_seasons;

ALTER TABLE products
ADD CONSTRAINT fk_products_seasons
FOREIGN KEY (s_id) REFERENCES seasons(s_id);

ALTER TABLE transactions
DROP CONSTRAINT IF EXISTS fk_transactions_paymentmethod;

ALTER TABLE transactions
ADD CONSTRAINT fk_transactions_paymentmethod
FOREIGN KEY (pm_id) REFERENCES paymentmethod(pm_id);

ALTER TABLE transactions
DROP CONSTRAINT IF EXISTS fk_transactions_transactionstatus;

ALTER TABLE transactions
ADD CONSTRAINT fk_transactions_transactionstatus
FOREIGN KEY (t_status_id) REFERENCES transactionstatus(t_status_id);


-- 13. ניקוי החיבור הזמני

DROP SCHEMA other_src CASCADE;
DROP SERVER other_department_server CASCADE;

COMMIT;