-- מוסיפים עמודה לשמירת תאריך העדכון האחרון של הפנייה
-- אם לא יוזן ערך, ברירת המחדל תהיה התאריך הנוכחי
ALTER TABLE requests
ADD COLUMN IF NOT EXISTS last_updated DATE DEFAULT CURRENT_DATE;

-- משנים את סוג העמודה rnote_json ל-TEXT
-- כדי לאפשר שמירת הערות ארוכות יותר
ALTER TABLE requests
ALTER COLUMN rnote_json TYPE TEXT;

-- מוסיפים עמודה לשמירת מספר הפניות הפתוחות הנוכחי של העובד
ALTER TABLE employee
ADD COLUMN IF NOT EXISTS current_open_requests INT DEFAULT 0;

-- מוסיפים עמודה לשמירת ציון העומס המחושב של העובד
ALTER TABLE employee
ADD COLUMN IF NOT EXISTS current_load_score NUMERIC DEFAULT 0;

-- מוסיפים עמודה לשמירת רמת העומס של העובד
-- LOW / MEDIUM / HIGH
ALTER TABLE employee
ADD COLUMN IF NOT EXISTS current_load_level TEXT DEFAULT 'LOW';

-- מוסיפים עמודה לשמירת התאריך שבו נתוני העומס עודכנו לאחרונה
-- ברירת המחדל היא NULL
ALTER TABLE employee
ADD COLUMN IF NOT EXISTS workload_updated_at DATE;