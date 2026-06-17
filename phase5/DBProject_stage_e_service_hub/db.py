import psycopg2 # אנחנו משתמשים בספרייה שמאפשרת ל־Python להתחבר ל־PostgreSQL
from psycopg2.extras import RealDictCursor # כשנקבל שורה מהדטה בייס נקבל אותה כמו מילון
from config import DB_CONFIG #פרטי ההתחברות כתובים בקובץ השני config.py


#פונקציה שפותחת חיבור לבסיס הנתונים
def get_connection():
    return psycopg2.connect(**DB_CONFIG) # פותח חיבור לpostgres


#פונקציה שמיועדת בעיקר לSELECT שמחזיר כמה שורות
def fetch_all(query, params=None):
    with get_connection() as conn: # פותח חיבור לבסיס הנתונים
        with conn.cursor(cursor_factory=RealDictCursor) as cur: # יוצרים קורסור - זה שממש מריץ את השאילתה. והתוצאה תחזור כמילון
            cur.execute(query, params or ()) # פה השאילתה נשלחת באמת לדאטה בייס
            return cur.fetchall()


def fetch_one(query, params=None):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params or ())
            return cur.fetchone()


def execute(query, params=None):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params or ())
            conn.commit()


def callproc(query, params=None):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params or ())
            conn.commit()


def get_columns(table_name):
    rows = fetch_all("""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = 'public'
          AND table_name = %s
        ORDER BY ordinal_position
    """, (table_name,))
    return [r["column_name"] for r in rows]


def table_exists(table_name):
    row = fetch_one("""
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema = 'public'
              AND table_name = %s
        ) AS exists
    """, (table_name,))
    return bool(row and row["exists"])


def get_pk_column(table_name):
    row = fetch_one("""
        SELECT kcu.column_name
        FROM information_schema.table_constraints tc
        JOIN information_schema.key_column_usage kcu
          ON tc.constraint_name = kcu.constraint_name
         AND tc.table_schema = kcu.table_schema
        WHERE tc.constraint_type = 'PRIMARY KEY'
          AND tc.table_schema = 'public'
          AND tc.table_name = %s
        ORDER BY kcu.ordinal_position
        LIMIT 1
    """, (table_name,))
    return row["column_name"] if row else None
