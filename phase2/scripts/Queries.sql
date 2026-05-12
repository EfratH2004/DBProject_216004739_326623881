SELECT e.eid,
       e.ename
FROM employee e
JOIN requests r ON e.eid = r.eid
GROUP BY e.eid, e.ename
HAVING COUNT(*) = (
    SELECT MAX(cnt)
    FROM (
        SELECT COUNT(*) AS cnt
        FROM requests
        GROUP BY eid
    ) x
);



SELECT e.eid,
       e.ename
FROM employee e
JOIN requests r ON e.eid = r.eid
GROUP BY e.eid, e.ename
HAVING COUNT(*) >= ALL (
    SELECT COUNT(*)
    FROM requests
    GROUP BY eid
);



SELECT r.rid
FROM requests r
WHERE r.priority_id = (
    SELECT p.priority_id
    FROM priority p
    WHERE LOWER(p.priority_name) = 'high'
);



SELECT r.rid,
       p.priority_name
FROM requests r
JOIN priority p ON r.priority_id = p.priority_id
WHERE LOWER(p.priority_name) = 'high';



SELECT r.rid,
       r.rnote_json,
       c.cid,
       r.open_date,
       CURRENT_DATE - r.open_date AS days_open
FROM requests r
JOIN customers c ON r.cid = c.cid
JOIN rstatus rs ON r.rs_id = rs.rs_id
WHERE LOWER(rs.rs_name) = 'open'
  AND r.open_date < CURRENT_DATE - INTERVAL '30 days'
ORDER BY days_open DESC;



SELECT r.rid,
       r.rnote_json,
       c.cid,
       r.open_date,
       CURRENT_DATE - r.open_date AS days_open
FROM requests r
JOIN customers c ON r.cid = c.cid
JOIN rstatus rs ON r.rs_id = rs.rs_id
WHERE LOWER(rs.rs_name) = 'open'
  AND (CURRENT_DATE - r.open_date) > 30
ORDER BY days_open DESC;



SELECT e.eid,
       e.ename,
       e.ephone
FROM employee e
WHERE e.eid NOT IN (
    SELECT r.eid
    FROM requests r
    WHERE r.eid IS NOT NULL
);



SELECT e.eid,
       e.ename,
       e.ephone
FROM employee e
WHERE NOT EXISTS (
    SELECT 1
    FROM requests r
    WHERE r.eid = e.eid
);



SELECT p.pid,
       p.pname
FROM products p
WHERE NOT EXISTS (
    SELECT 1
    FROM transactions t
    WHERE t.pid = p.pid
);



SELECT p.pid,
       p.pname
FROM products p
LEFT JOIN transactions t ON p.pid = t.pid
WHERE t.pid IS NULL;



BEGIN;
UPDATE products
SET price = price * 1.10
WHERE price > 0;



UPDATE requests
SET rs_id = (
    SELECT rs_id
    FROM rstatus
    WHERE LOWER(rs_name) = 'closed'
)
WHERE rid = 101;



BEGIN;
UPDATE requests
SET eid = 5
WHERE eid IS NULL;



BEGIN;
DELETE FROM products p
WHERE NOT EXISTS (
    SELECT 1
    FROM transactions t
    WHERE t.pid = p.pid
);

SELECT p.pid, p.pname
FROM products p
WHERE NOT EXISTS (
    SELECT 1
    FROM transactions t
    WHERE t.pid = p.pid
);



BEGIN;

DELETE FROM customers c
WHERE NOT EXISTS (
    SELECT 1
    FROM requests r
    WHERE r.cid = c.cid
)
AND NOT EXISTS (
    SELECT 1
    FROM transactions t
    WHERE t.cid = c.cid
);

SELECT c.cid
FROM customers c
WHERE NOT EXISTS (
    SELECT 1
    FROM requests r
    WHERE r.cid = c.cid
)
AND NOT EXISTS (
    SELECT 1
    FROM transactions t
    WHERE t.cid = c.cid
);



BEGIN;

DELETE FROM requests
WHERE open_date < CURRENT_DATE - INTERVAL '5 years';

SELECT rid, open_date
FROM requests
WHERE open_date < CURRENT_DATE - INTERVAL '5 years';