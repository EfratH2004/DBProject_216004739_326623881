ALTER TABLE requests
ADD COLUMN IF NOT EXISTS last_updated DATE DEFAULT CURRENT_DATE;

ALTER TABLE requests
ALTER COLUMN rnote_json TYPE TEXT;

-- עמודות נגזרות בטבלת employee בשביל לשמור את מצב העומס הנוכחי של העובד
ALTER TABLE employee
ADD COLUMN IF NOT EXISTS current_open_requests INT DEFAULT 0;

ALTER TABLE employee
ADD COLUMN IF NOT EXISTS current_load_score NUMERIC DEFAULT 0;

ALTER TABLE employee
ADD COLUMN IF NOT EXISTS current_load_level TEXT DEFAULT 'LOW';

ALTER TABLE employee
ADD COLUMN IF NOT EXISTS workload_updated_at DATE;
