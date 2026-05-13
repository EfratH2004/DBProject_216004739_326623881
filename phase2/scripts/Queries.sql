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
-- קודם מוצאים את מספר הבקשות הגבוה ביותר ואז מחזירים את העובדים שהגיעו אליו
-- מבחינת יעילות: לרוב MAX יעיל יותר מ-ALL כי מחשבים מקסימום פעם אחת בלבד


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
-- מחזיר עובדים שכמות הבקשות שלהם גדולה או שווה לכל שאר העובדים
-- מבחינת יעילות: לרוב פחות יעיל מ-MAX כי צריך להשוות מול כל הערכים


SELECT r.rid
FROM requests r
WHERE r.priority_id = (
    SELECT p.priority_id
    FROM priority p
    WHERE LOWER(p.priority_name) = 'high'
);
-- מחפשים את ה-ID של עדיפות high ואז מחזירים את כל הבקשות עם ה-ID הזה
-- מבחינת יעילות: יעיל אם הטבלה priority קטנה ויש אינדקס על priority_id


SELECT r.rid,
       p.priority_name
FROM requests r
JOIN priority p ON r.priority_id = p.priority_id
WHERE LOWER(p.priority_name) = 'high';
-- מחברים בין requests ל-priority ומסננים רק בקשות בעדיפות גבוהה
-- מבחינת יעילות: JOIN לרוב יעיל יותר כשצריך גם מידע מהטבלה השנייה


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
-- מחזירה בקשות פתוחות שעברו יותר מ-30 יום מאז שנפתחו
-- מבחינת יעילות: לרוב עדיף כי ניתן להשתמש באינדקס על open_date


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
-- מחשבת כמה ימים עברו מאז פתיחת הבקשה ובודקת אם עברו יותר מ-30 יום
-- מבחינת יעילות: פחות טוב לאינדקסים כי מופעל חישוב על העמודה עצמה


SELECT e.eid,
       e.ename,
       e.ephone
FROM employee e
WHERE e.eid NOT IN (
    SELECT r.eid
    FROM requests r
    WHERE r.eid IS NOT NULL
);
-- מחזירה עובדים שלא מופיעים בטבלת requests
-- מבחינת יעילות: NOT IN יכול להיות פחות יעיל ובעייתי עם NULL


SELECT e.eid,
       e.ename,
       e.ephone
FROM employee e
WHERE NOT EXISTS (
    SELECT 1
    FROM requests r
    WHERE r.eid = e.eid
);
-- בודקת שאין אף בקשה ששייכת לעובד הזה
-- מבחינת יעילות: לרוב NOT EXISTS יעיל ובטוח יותר מ-NOT IN


SELECT p.pid,
       p.pname
FROM products p
WHERE NOT EXISTS (
    SELECT 1
    FROM transactions t
    WHERE t.pid = p.pid
);
-- מחזירה מוצרים שלא הופיעו באף עסקה
-- מבחינת יעילות: NOT EXISTS לרוב יעיל במיוחד עם אינדקסים


SELECT p.pid,
       p.pname
FROM products p
LEFT JOIN transactions t ON p.pid = t.pid
WHERE t.pid IS NULL;
-- מחברים את כל המוצרים לעסקאות ומחזירים רק כאלה בלי התאמה
-- מבחינת יעילות: LEFT JOIN טוב אך לעיתים NOT EXISTS מהיר יותר בטבלאות גדולות


SELECT c.cid,
       COALESCE(pr.first_name || ' ' || pr.last_name,
                b.company_name,
                b.contact_name) AS customer_name,
       SUM(t.payment) AS total_spent
FROM customers c
JOIN transactions t ON c.cid = t.cid
LEFT JOIN private pr ON c.cid = pr.cid
LEFT JOIN business b ON c.cid = b.cid
GROUP BY c.cid,
         pr.first_name,
         pr.last_name,
         b.company_name,
         b.contact_name
ORDER BY total_spent DESC;
-- מחשבת כמה כל לקוח הוציא בסך הכל
-- COALESCE מחזיר את השם הראשון שאינו NULL


SELECT e.eid,
       e.ename,
       COUNT(r.rid) AS closed_requests_this_year
FROM employee e
JOIN requests r ON e.eid = r.eid
JOIN rstatus rs ON r.rs_id = rs.rs_id
WHERE LOWER(rs.rs_name) = 'closed'
  AND EXTRACT(YEAR FROM r.open_date) = EXTRACT(YEAR FROM CURRENT_DATE)
GROUP BY e.eid, e.ename
ORDER BY closed_requests_this_year DESC;
-- סופרת כמה בקשות סגורות טיפל כל עובד השנה
-- ORDER BY DESC מציג את העובדים הפעילים ביותר ראשונים


SELECT p.pid,
       p.pname,
       COUNT(t.tid) AS total_sales
FROM products p
JOIN transactions t ON p.pid = t.pid
GROUP BY p.pid, p.pname
ORDER BY total_sales DESC;
-- מחשבת כמה פעמים כל מוצר נמכר
-- COUNT סופר את מספר העסקאות לכל מוצר


SELECT e.eid,
       e.ename,
       COUNT(r.rid) AS open_requests
FROM employee e
LEFT JOIN requests r ON e.eid = r.eid
JOIN rstatus rs ON r.rs_id = rs.rs_id
WHERE LOWER(rs.rs_name) = 'open'
GROUP BY e.eid, e.ename
ORDER BY open_requests DESC;
-- מחשבת כמה בקשות פתוחות יש לכל עובד
-- משתמשים ב-LEFT JOIN כדי לאפשר גם עובדים בלי בקשות


SELECT p.pid,
       p.pname,
       COUNT(t.tid) AS total_sales,
       SUM(t.payment) AS total_revenue
FROM products p
JOIN transactions t ON p.pid = t.pid
GROUP BY p.pid, p.pname
ORDER BY total_revenue DESC;
-- מחשבת גם את כמות המכירות וגם את סך ההכנסות מכל מוצר
-- SUM מחבר את כל התשלומים של העסקאות


BEGIN;
UPDATE products
SET price = price * 1.10
WHERE price > 0;
-- מעלה את המחיר של כל המוצרים ב-10%
-- WHERE מוודא שלא מעדכנים מחירים לא תקינים


UPDATE requests
SET rs_id = (
    SELECT rs_id
    FROM rstatus
    WHERE LOWER(rs_name) = 'closed'
)
WHERE rid = 101;
-- משנה את הסטטוס של בקשה 101 ל-closed
-- משתמשים בתת-שאילתה כדי למצוא את ה-ID של הסטטוס


BEGIN;
UPDATE requests
SET eid = 5
WHERE eid IS NULL;
-- משייך בקשות בלי עובד לעובד מספר 5
-- IS NULL בודק שאין כרגע עובד משויך


BEGIN;
DELETE FROM products p
WHERE NOT EXISTS (
    SELECT 1
    FROM transactions t
    WHERE t.pid = p.pid
);
-- מוחק מוצרים שלא השתתפו באף עסקה


SELECT p.pid, p.pname
FROM products p
WHERE NOT EXISTS (
    SELECT 1
    FROM transactions t
    WHERE t.pid = p.pid
);
-- בודק אילו מוצרים עדיין לא נמכרו אחרי המחיקה


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
-- מוחק לקוחות שאין להם בקשות וגם לא עסקאות


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
-- בודק אילו לקוחות ללא פעילות נשארו במערכת


BEGIN;

DELETE FROM requests
WHERE open_date < CURRENT_DATE - INTERVAL '5 years';
-- מוחק בקשות ישנות יותר מ-5 שנים


SELECT rid, open_date
FROM requests
WHERE open_date < CURRENT_DATE - INTERVAL '5 years';
-- בודק אם נשארו בקשות ישנות אחרי המחיקה