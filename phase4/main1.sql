CREATE OR REPLACE FUNCTION calculate_employee_load_score(p_eid INT)
RETURNS TABLE (
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
    WHERE eid = p_eid;

    IF employee_name IS NULL THEN
        RAISE EXCEPTION 'Employee with id % does not exist', p_eid;
    END IF;

    SELECT COUNT(*)
    INTO open_requests
    FROM requests
    WHERE eid = p_eid
	  AND rs_id IN (1, 1000001);

    SELECT COUNT(*)
    INTO high_priority_requests
    FROM requests r
    JOIN priority p ON r.priority_id = p.priority_id
    WHERE r.eid = p_eid
      AND rs_id IN (1, 1000001)
      AND (
            LOWER(p.priority_name) LIKE '%high%'
            OR LOWER(p.priority_name) LIKE '%urgent%'
            OR p.priority_name LIKE '%Critical%'
            OR p.priority_name LIKE '%Severe%'
			OR p.priority_name LIKE '%Extreme%'
          );
		  

    SELECT COALESCE(AVG(CURRENT_DATE - open_date), 0)
    INTO avg_days_open
    FROM requests
    WHERE eid = p_eid
      AND rs_id IN (1,1000001);

    load_score := open_requests * 10 + high_priority_requests * 20 + avg_days_open * 0.5;

    IF load_score <= 50 THEN
        load_level := 'LOW';
    ELSIF load_score <= 120 THEN
        load_level := 'MEDIUM';
    ELSE
        load_level := 'HIGH';
    END IF;

    RETURN NEXT; -- מחזיר רשומה של טבלה (רק עובד אחד)
END;
$$ LANGUAGE plpgsql; -- סיום הפונקציה




CREATE OR REPLACE PROCEDURE reassign_requests_from_employee(
    p_source_eid INT,
    p_target_eid INT,
    p_max_requests INT DEFAULT 5
)
AS $$
DECLARE
    req_rec RECORD;
    v_counter INT := 0;
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
        WHERE eid = p_source_eid
          AND rs_id IN (1, 1000001)
        ORDER BY priority_id DESC, open_date ASC -- קודם עדיפות גבוהה, אח"כ בקשה ישנה יותר
        LIMIT p_max_requests -- כמות הבקשות
    LOOP
        UPDATE requests
        SET eid = p_target_eid,
            rnote_json = 'REASSIGNED on ' || CURRENT_DATE ||
                         ' from employee ' || p_source_eid ||
                         ' to employee ' || p_target_eid,
            last_updated = CURRENT_DATE
        WHERE rid = req_rec.rid;

        v_counter := v_counter + 1;

        RAISE NOTICE 'Request % reassigned from employee % to employee %',
            req_rec.rid, p_source_eid, p_target_eid;
    END LOOP;

    RAISE NOTICE 'Total reassigned requests: %', v_counter;

EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error in reassign_requests_from_employee: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION validate_request_reassignment()
RETURNS TRIGGER
AS $$
DECLARE
    v_open_requests INT;
BEGIN
    IF OLD.eid IS DISTINCT FROM NEW.eid THEN -- שונה כי שייכנו אותו לעובד אחר

        SELECT COUNT(*)
        INTO v_open_requests
        FROM requests
        WHERE eid = NEW.eid
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
BEFORE UPDATE OF eid ON requests
FOR EACH ROW
EXECUTE FUNCTION validate_request_reassignment();




DO $$
DECLARE
    emp_rec RECORD;
    load_rec RECORD;

    v_source_eid INT := NULL;
    v_source_score NUMERIC := -1;

    v_target_eid INT := NULL;
    v_target_score NUMERIC := 9999999;
BEGIN
    RAISE NOTICE 'Main employee process started';

    FOR emp_rec IN
        SELECT eid, ename
        FROM employee
        ORDER BY eid
    LOOP
        SELECT *
		INTO load_rec
		FROM calculate_employee_load_score(emp_rec.eid);
		RAISE NOTICE 'Employee %, score %, level %',
			load_rec.employee_name,
			load_rec.load_score,
			load_rec.load_level;

		IF load_rec.load_level = 'HIGH'
		   AND load_rec.load_score > v_source_score THEN
			v_source_eid := load_rec.employee_id;
			v_source_score := load_rec.load_score;
		END IF;

		IF load_rec.load_score < v_target_score THEN
			v_target_eid := load_rec.employee_id;
			v_target_score := load_rec.load_score;
		END IF;
    END LOOP;

    IF v_source_eid IS NULL THEN
        RAISE NOTICE 'No overloaded employee found. Procedure was not executed.';

    ELSIF v_target_eid IS NULL OR v_source_eid = v_target_eid THEN
        RAISE NOTICE 'No valid target employee found. Procedure was not executed.';

    ELSE
        RAISE NOTICE 'Reassigning requests from employee % to employee %',
            v_source_eid, v_target_eid;

        CALL reassign_requests_from_employee(v_source_eid, v_target_eid, 5);
    END IF;

    RAISE NOTICE 'Main employee process finished';

EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error in main employee process: %', SQLERRM;
END;
$$;