ALTER TABLE products
ADD CONSTRAINT check_price_positive
CHECK (price > 0);



ALTER TABLE requests
ADD CONSTRAINT fk_requests_customer
FOREIGN KEY (cid)
REFERENCES customers(cid)
ON DELETE CASCADE;



ALTER TABLE transactions
ADD CONSTRAINT unique_transaction_customer_employee_product_date
UNIQUE (cid, eid, pid, transaction_date);