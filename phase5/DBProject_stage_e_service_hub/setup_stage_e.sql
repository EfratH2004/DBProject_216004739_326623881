-- Stage E setup additions
-- Run this once before running the Python application.

ALTER TABLE employee
ADD COLUMN IF NOT EXISTS password VARCHAR(50);

ALTER TABLE employee
ADD COLUMN IF NOT EXISTS role VARCHAR(20) DEFAULT 'employee';

UPDATE employee
SET role = 'employee'
WHERE role IS NULL OR role = '';

UPDATE employee
SET password = COALESCE(password, '1234');

UPDATE employee
SET role = 'manager'
WHERE eid = 1;

ALTER TABLE products
ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE;

UPDATE products
SET is_active = TRUE
WHERE is_active IS NULL;
