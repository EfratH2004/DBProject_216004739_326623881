CREATE INDEX idx_requests_eid_status
ON requests(eid, rs_id);



CREATE INDEX idx_transactions_cid_date
ON transactions(cid, transaction_date);



CREATE INDEX idx_requests_date
ON requests(open_date);