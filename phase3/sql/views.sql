-- =========================================================
-- View 1: מבט של האגף המקורי שלנו - Customer Service
-- מציג פניות שירות פעילות/משמעותיות עם פרטי לקוח, עובד, סטטוס ועדיפות.
-- מקור המבט: האגף המקורי שלנו.
-- =========================================================

CREATE OR REPLACE VIEW customer_service_active_requests_view AS
SELECT
    r.rid,
    c.cid,
    COALESCE(
        p.first_name || ' ' || p.last_name,
        b.company_name,
        'Unknown Customer'
    ) AS customer_name,
    c.cphone,
    c.cemail,
    e.eid,
    e.ename AS employee_name,
    r.open_date,
    r.subject,
    rs.rs_name AS request_status,
    pr.priority_name,
    r.resolved_at
FROM requests r
JOIN customers c
    ON r.cid = c.cid
LEFT JOIN private p
    ON c.cid = p.cid
LEFT JOIN business b
    ON c.cid = b.cid
JOIN employee e
    ON r.eid = e.eid
JOIN rstatus rs
    ON r.rs_id = rs.rs_id
JOIN priority pr
    ON r.priority_id = pr.priority_id
WHERE r.open_date <= CURRENT_DATE
  AND (
        r.resolved_at IS NULL
        OR r.resolved_at >= r.open_date
      )
  AND pr.priority_name IS NOT NULL;


-- Query 1: הצגת 10 פניות פעילות/תקינות עם כל פרטי השירות
SELECT *
FROM customer_service_active_requests_view
LIMIT 10;


-- Query 2: כמות פניות לפי עובד וסטטוס
SELECT
    employee_name,
    request_status,
    COUNT(*) AS total_requests
FROM customer_service_active_requests_view
GROUP BY employee_name, request_status
ORDER BY total_requests DESC;


-- Query 3: לקוחות עם הכי הרבה פניות שירות
SELECT
    customer_name,
    cphone,
    COUNT(*) AS total_requests
FROM customer_service_active_requests_view
GROUP BY customer_name, cphone
ORDER BY total_requests DESC
LIMIT 10;









-- =========================================================
-- View 2: מבט של האגף שקיבלנו - Sales / Transactions
-- מציג עסקאות מכירה תקינות עם לקוח, מוצר, תשלום וסטטוס.
-- מקור המבט: האגף שקיבלנו מהזוג השני.
-- =========================================================

CREATE OR REPLACE VIEW received_department_sales_view AS
SELECT
    t.tid,
    t.transaction_date,
    c.cid,
    COALESCE(
        p.first_name || ' ' || p.last_name,
        b.company_name,
        'Unknown Customer'
    ) AS customer_name,
    c.cphone,
    pr.pid,
    pr.pname AS product_name,
    pr.category,
    pr.manufactured_in,
    pr.stock_qty,
    t.amount,
    t.has_discount,
    pm.pm_name AS payment_method,
    ts.t_status_name AS transaction_status
FROM transactions t
JOIN customers c
    ON t.cid = c.cid
LEFT JOIN private p
    ON c.cid = p.cid
LEFT JOIN business b
    ON c.cid = b.cid
JOIN products pr
    ON t.pid = pr.pid
LEFT JOIN paymentmethod pm
    ON t.pm_id = pm.pm_id
LEFT JOIN transactionstatus ts
    ON t.t_status_id = ts.t_status_id
WHERE t.transaction_date <= CURRENT_DATE
  AND pr.price > 0
  AND (
        t.amount IS NULL
        OR t.amount >= 0
      );


-- Query 1: הצגת 10 עסקאות תקינות עם פרטי לקוח, מוצר ותשלום
SELECT *
FROM received_department_sales_view
LIMIT 10;


-- Query 2: מוצרים שנמכרו הכי הרבה פעמים
SELECT
    product_name,
    COUNT(*) AS total_sales
FROM received_department_sales_view
GROUP BY product_name
ORDER BY total_sales DESC
LIMIT 10;

-- Query 3: לקוחות שביצעו הכי הרבה עסקאות
SELECT
    customer_name,
    COUNT(*) AS total_transactions
FROM received_department_sales_view
GROUP BY customer_name
ORDER BY total_transactions DESC
LIMIT 10;