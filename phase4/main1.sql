-- פונקציה שמחשבת את ציון העומס
CREATE OR REPLACE FUNCTION calculate_employee_load_score(p_eid INT)
RETURNS TABLE ( -- מכריז מה הפונקציה תחזיר
    employee_id INT,
    employee_name VARCHAR,
    open_requests INT,
    high_priority_requests INT,
    avg_days_open NUMERIC,
    load_score NUMERIC,
    load_level TEXT
)
AS $$
BEGIN

    SELECT eid, ename
    INTO employee_id, employee_name
    FROM employee
    WHERE eid = p_eid; -- העובד שמתאים לתעודת הזהות שהתקבלה כפרמטר

    IF employee_name IS NULL THEN
        RAISE EXCEPTION 'Employee with id % does not exist', p_eid;
    END IF;

    --מחשב את מספר הפניות הפתוחות של אותו עובד
    SELECT COUNT(*) 
    INTO open_requests
    FROM requests
    WHERE eid = p_eid -- הפניות של אותו עובד
	  AND rs_id IN (1, 1000001); -- rs_id = 'open'

    -- מחשב את מספר הפניות עם עדיפות גבוהה של אותו עובד
    SELECT COUNT(*)
    INTO high_priority_requests
    FROM requests r
    JOIN priority p ON r.priority_id = p.priority_id
    WHERE r.eid = p_eid
      AND rs_id IN (1, 1000001) -- rs_id = 'open'
      AND (
            LOWER(p.priority_name) LIKE '%high%'
            OR LOWER(p.priority_name) LIKE '%urgent%'
            OR p.priority_name LIKE '%Critical%'
            OR p.priority_name LIKE '%Severe%'
			OR p.priority_name LIKE '%Extreme%'
          );
		  
    -- מחשב את ממוצע הימים שפתוחות הפניות של אותו עובד
    SELECT COALESCE(AVG(CURRENT_DATE - open_date), 0)
    INTO avg_days_open
    FROM requests
    WHERE eid = p_eid
      AND rs_id IN (1,1000001);

    load_score := open_requests * 10 + high_priority_requests * 20 + avg_days_open * 0.5; -- נוסחת חישוב העומס

    IF load_score <= 50 THEN
        load_level := 'LOW';
    ELSIF load_score <= 120 THEN
        load_level := 'MEDIUM';
    ELSE
        load_level := 'HIGH';
    END IF;

    RETURN NEXT; -- מחזיר בפועל רשומה של טבלה (רק עובד אחד)
END;
$$ LANGUAGE plpgsql; -- סיום הפונקציה



-- פרוצדורה שמקבלת תעודת זהות של עובד עמוס, תעודת זהות של עובד פחות עמוס, ומספר מקסימלי של פניות להעברה
CREATE OR REPLACE PROCEDURE reassign_requests_from_employee(
    p_source_eid INT,
    p_target_eid INT,
    p_max_requests INT DEFAULT 5
)
AS $$
DECLARE
    req_rec RECORD; -- משתנה שיחזיק בכל סיבוב בלולאה פנייה אחת
    v_counter INT := 0; -- מונה שסופר כמה פניות הועברו בפועל
BEGIN
    IF p_source_eid = p_target_eid THEN
        RAISE EXCEPTION 'Source employee and target employee cannot be the same';
    END IF;

    IF p_max_requests <= 0 THEN
        RAISE EXCEPTION 'Max requests must be positive';
    END IF;

    FOR req_rec IN
        SELECT rid
        FROM requests
        WHERE eid = p_source_eid -- רק פניות פתוחות ששייכות לעובד המקור 
          AND rs_id IN (1, 1000001)
        ORDER BY priority_id DESC, open_date ASC -- קודם עדיפות גבוהה, אח"כ בקשה ישנה יותר
        LIMIT p_max_requests -- כמות הבקשות
    LOOP
        UPDATE requests -- מעדכנים את טבלת הפניות
        SET eid = p_target_eid, -- משנים את העובד שאחראי על הפנייה לעובד היעד
            rnote_json = 'REASSIGNED on ' || CURRENT_DATE ||
                         ' from employee ' || p_source_eid ||
                         ' to employee ' || p_target_eid,
            last_updated = CURRENT_DATE
        WHERE rid = req_rec.rid;

        v_counter := v_counter + 1; -- מגדילים את המונה של הפניות שהועברו בפועל

        RAISE NOTICE 'Request % reassigned from employee % to employee %',
            req_rec.rid, p_source_eid, p_target_eid;
    END LOOP;

    RAISE NOTICE 'Total reassigned requests: %', v_counter;

EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error in reassign_requests_from_employee: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;


-- הטריגר בודק שלעובד החדש אליו מעבירים את הפנייה אין כבר 20 פניות פתוחות או יותר
-- או שכל ההעברה מצליחה או שהיא לא מתבצעת כלל
CREATE OR REPLACE FUNCTION validate_request_reassignment() 
RETURNS TRIGGER
AS $$
DECLARE
    v_open_requests INT; -- כמה פניות פתוחות יש לעובד החדש
BEGIN
    IF OLD.eid IS DISTINCT FROM NEW.eid THEN -- בודק אם באמת שייכנו את הפנייה לעובד אחר

        SELECT COUNT(*)
        INTO v_open_requests
        FROM requests
        WHERE eid = NEW.eid -- בודקים כמה פניות פתוחות יש לעובד החדש
          AND rs_id IN (1, 1000001);

        IF v_open_requests >= 20 THEN
            RAISE EXCEPTION
                'Cannot assign request to employee %. Employee already has % open requests',
                NEW.eid,
                v_open_requests;
        END IF;

        NEW.last_updated := CURRENT_DATE;

    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
DROP TRIGGER IF EXISTS trg_validate_request_reassignment ON requests;

CREATE TRIGGER trg_validate_request_reassignment
BEFORE UPDATE OF eid ON requests -- מופעל ברגע שהפרוצדורה עושה UPDATE לעובד שאחראי על הפנייה
FOR EACH ROW
EXECUTE FUNCTION validate_request_reassignment();


--מי העובד הכי עמוס
--ומי העובד הכי פחות עמוס
--ואם יש עובד עמוס — הוא מעביר ממנו עד חמש פניות לעובד הפחות עמוס
DO $$ 
DECLARE
    emp_rec RECORD; --שומר בכל סיבוב בלולאת העובדים את הנתונים של העובד הנוכחי, שם ותעודת זהות
    load_rec RECORD; -- מחזיק את כל העמודות שהפונקצייה החזירה עבור אותו עובד

    v_source_eid INT := NULL; -- העובד הכי עמוס
    v_source_score NUMERIC := -1; -- ציון העומס שלו

    v_target_eid INT := NULL; -- העובד הכי פחות עמוס
    v_target_score NUMERIC := 9999999; -- ציון העומס שלו
BEGIN
    RAISE NOTICE 'Main employee process started';

    --לולאה שעוברת על כל העובדים, כל פעם emp_rec מחזיק את הנתונים של עובד אחר
    FOR emp_rec IN
        SELECT eid, ename
        FROM employee
        ORDER BY eid
    LOOP
        SELECT *
		INTO load_rec
		FROM calculate_employee_load_score(emp_rec.eid);
		RAISE NOTICE 'Employee %, score %, level %', -- מדפיסים למסך את פרטי העובד, ציון העומס ודרגות העומס שלו
			load_rec.employee_name,
			load_rec.load_score,
			load_rec.load_level;

		IF load_rec.load_level = 'HIGH' -- אם דרגת העומס שלו גבוהה וגם גדולה יותר מההכי גבוה שמצאנו עד עכשיו
		   AND load_rec.load_score > v_source_score THEN
			v_source_eid := load_rec.employee_id; -- נשמור את תעודת הזהות שלו כעובד הכי עמוס
			v_source_score := load_rec.load_score; -- נשמור את ציון העומס שלו כציון העומס הכי גבוה שמצאנו עד עכשיו
		END IF;

		IF load_rec.load_score < v_target_score THEN -- האם העובד הנוכחי הוא הכי פחות עמוס שמצאנו עד עכשיו
			v_target_eid := load_rec.employee_id;
			v_target_score := load_rec.load_score;
		END IF;
    END LOOP;

    IF v_source_eid IS NULL THEN
        RAISE NOTICE 'No overloaded employee found. Procedure was not executed.'; -- אין עובד עמוס תקין

    ELSIF v_target_eid IS NULL OR v_source_eid = v_target_eid THEN
        RAISE NOTICE 'No valid target employee found. Procedure was not executed.'; -- אין עובד יעד תקין

    ELSE
        RAISE NOTICE 'Reassigning requests from employee % to employee %', -- שניהם תקינים, אפשר לעשות העברה - קוראים לפרוצדורה
            v_source_eid, v_target_eid;

        CALL reassign_requests_from_employee(v_source_eid, v_target_eid, 5); -- קריאה לפרוצדורה
    END IF;

    RAISE NOTICE 'Main employee process finished';

EXCEPTION -- אם קרתה שגיאה בכל מקם אחר בקוד, תדפיס
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error in main employee process: %', SQLERRM;
END;
$$;