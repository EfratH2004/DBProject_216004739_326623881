# DBProject – Phase 1

## Team Members
Meitav Bin Nun  
Efrat Hourvitz  

---

## Introduction

The general topic of the project is an **online store system**.  
Each team was required to focus on a specific department within the store.

Our team chose to focus on the **Customer Service department**.  
Therefore, the system we designed manages the information required for customer support operations, including customers, service requests, employees, products, and transactions related to customer inquiries.

---

# System Description

The goal of the system is to help customer service employees track customer activity, handle service requests, and view purchase information in order to provide better support.

The system manages the following main entities:

- **Customers** – store customer contact information.
- **Products** – represent products available in the online store.
- **Transactions** – represent purchases completed by customers on the website.
- **Requests** – represent customer service requests opened through the website.
- **Employees** – represent customer service employees that handle requests and assist customers.

### System functionality

Customers can perform purchases on the website, which are stored as **transactions** in the system.  
Customers can also open **service requests** when they encounter issues or need assistance.

Customer service **employees** handle these requests and may also assist customers regarding previous transactions.

The system allows tracking:

- customer purchases  
- customer service requests  
- employee handling of requests  
- relationships between customers, products, and transactions  

This information enables the customer service team to provide efficient support.

---

# ERD Diagram

![ERD Diagram](phase1/images/ERD.png)

---

# DSD Diagram

![DSD Diagram](phase1/images/DSD.png)

---

# Data Population Documentation

### Data Generation – Customers
![Customers Data](phase1/images/customers_mockaroo.png)

### Data Generation – Employees
![Employees Data](phase1/images/employees_mockaroo.png)

### Data Generation – Products
![Products Data](phase1/images/products_mockaroo.png)

---

# Data Insertion Process

The data was inserted into the database in multiple stages:

1. Creation of tables using SQL scripts  
2. Generation of mock data using Mockaroo  
3. Importing CSV files into PostgreSQL  
4. Ensuring referential integrity using foreign keys  
5. Running validation queries to verify correctness  

---

# System Screens

### Login Screen
![Login](phase1/images/login.png)

---

### Dashboard
![Dashboard](phase1/images/dashboard.png)

---

### Customers Screen
![Customers](phase1/images/customers.png)

---

### Products Screen
![Products](phase1/images/products.png)

---

### Employees Screen
![Employees](phase1/images/employees.png)

---

### Requests Screen
![Requests](phase1/images/requests.png)

---

### Transactions Screen
![Transactions](phase1/images/transactions.png)

---

# Backup

A full backup of the database was created.

The backup includes:

- Database structure (tables, relationships, constraints)  
- All inserted data  

Backup file:
[Download backup](./phase1/customer_service_backup.backup)

# Phase 2

## Introduction

In this phase of the project, advanced SQL queries, transactions, constraints, and indexes were implemented in order to improve the functionality and performance of the database system.

The main goals of this phase were:

- Writing complex SELECT queries
- Comparing different implementations of the same query
- Performing UPDATE and DELETE operations
- Using transactions with COMMIT and ROLLBACK
- Adding constraints using ALTER TABLE
- Improving query efficiency using indexes
- Measuring query performance before and after indexing

The queries were designed according to the GUI screens of the system such as Requests, Employees, Products, Customers, Transactions, and Dashboard.

---

# SELECT Queries

## Query 1 – Open Requests Older Than 30 Days

### Version A – Using INTERVAL

This query displays all open customer requests that have been open for more than 30 days.

![openMoreThan30Days1.1](phase2/images/openMoreThan30Days1.1.jpeg)

---

### Version B – Using Date Difference Calculation

This query also displays open requests older than 30 days by directly calculating the number of days.

![openMoreThan30Days1.2](phase2/images/openMoreThan30Days1.2.jpeg)

---

### Efficiency Comparison

Version A is generally more efficient because PostgreSQL can optimize INTERVAL comparisons better than repeated arithmetic calculations on dates.

---

## Query 2 – High Priority Requests

### Version A – Using JOIN

This query displays all requests marked as high priority.

![highPriority1](phase2/images/highPriority1.jpeg)

---

### Version B – Using Subquery

This query retrieves high priority requests using a nested subquery.

![highPriority2](phase2/images/highPriority2.jpeg)

---

### Efficiency Comparison

The JOIN version is usually more efficient because PostgreSQL can optimize joins directly without recalculating subqueries.

---

## Query 3 – Products That Were Never Sold

### Version A – Using LEFT JOIN

This query displays products that do not appear in any transaction.

![unsoldProducts1](phase2/images/unsoldProducts1.jpeg)

---

### Version B – Using NOT EXISTS

This query also finds products that were never sold using NOT EXISTS.

![unsoldProducts2](phase2/images/unsoldProducts2.jpeg)

---

### Efficiency Comparison

NOT EXISTS is generally more efficient because it works better with indexes and avoids large join operations.

---

## Query 4 – Employees With No Requests

### Version A – Using NOT IN

This query displays employees who never handled any request.

![noRequestsEmployees1](phase2/images/noRequestsEmployees1.jpeg)

---

### Version B – Using NOT EXISTS

This query also finds employees who did not handle requests.

![noRequestsEmployees2](phase2/images/noRequestsEmployees2.jpeg)

---

### Efficiency Comparison

NOT EXISTS is usually safer and more efficient because it handles NULL values correctly and optimizes better with indexes.

---

## Query 5 – Employee With Most Closed Requests

### Version A – Using ALL

This query displays the employee who handled the highest number of closed requests.

![mostRequestsOfEmployee1](phase2/images/mostRequestsOfEmployee1.jpeg)

---

### Version B – Using MAX

This query also finds the employee with the highest number of closed requests.

![mostRequestsOfEmployee2](phase2/images/mostRequestsOfEmployee2.jpeg)

---

### Efficiency Comparison

The MAX version is usually clearer and more stable for optimization, while the ALL version demonstrates advanced SQL capabilities.

---

# Additional SELECT Queries

## Query 6 – Total Revenue Per Customer

This query calculates the total amount spent by each customer.

![totalPerClient](phase2/images/totalPerClient.jpeg)

---

## Query 7 – Products With Highest Revenue

This query displays the products that generated the highest revenue.

![mostMoneyProducts](phase2/images/mostMoneyProducts.jpeg)

---

## Query 8 – Open Requests Per Employee

This query displays the number of open requests assigned to each employee.

![openRequestsPerEmloyee](phase2/images/openRequestsPerEmloyee.jpeg)

---

## Query 9 – Employees With More Than 10 Years Experience

This query displays employees with more than 10 years of experience.

![10YearsExperience](phase2/images/10YearsExperience.jpeg)

---


## Query 10 – Closed Requests This Year

This query displays all requests that were closed during the current year.

![closedRequestThisYear](phase2/images/closedRequestThisYear.jpeg)

---

## Query 11 – Most Sold Products

This query displays the products with the highest number of sales.

![mostSoldProducts](phase2/images/mostSoldProducts.jpeg)

---

# UPDATE Queries

## UPDATE Query 1 – Transaction With COMMIT and ROLLBACK

The following transaction demonstrates the use of BEGIN, UPDATE, ROLLBACK, and COMMIT.

### Before Update

The database before the update operation.

![beforeUpdate](phase2/images/beforeUpdate.jpeg)

---

### Update Operation

The UPDATE query execution.

![update](phase2/images/update.png)

---

### After Update

The database after the update operation.

![afterUpdate](phase2/images/afterUpdate.jpeg)

---

### ROLLBACK

The transaction was rolled back and the database returned to its previous state.

![rollback](phase2/images/rollback.jpeg)

---

### COMMIT

The transaction was committed and the changes were saved permanently.

![commit](phase2/images/commit.jpeg)

---

## UPDATE Query 2 – Assign Requests Without Employee

This query assigns requests without an employee to a specific employee.

### Before Update

![update11](phase2/images/update11.jpeg)

---

### Update Query

![update12](phase2/images/update12.jpeg)

---

### After Update

![update13](phase2/images/update13.jpeg)

---

## UPDATE Query 3 – Change Request Status

This query changes the status of a request.

### Before Update

![update21](phase2/images/update21.jpeg)

---

### Update Query

![update22](phase2/images/update22.jpeg)

---

### After Update

![update23](phase2/images/update23.png)

---

# DELETE Queries

## DELETE Query 1 – Delete Old Requests

This query deletes very old requests from the database.

### Before Delete

![DELETE1_1](phase2/images/DELETE1_1.png)

---

### After Delete

![DELETE1_2](phase2/images/DELETE1_2.png)

---

## DELETE Query 2 – Delete Customers Without Activity

This query deletes customers that have no requests and no transactions.

### Before Delete

![DELETE2_1](phase2/images/DELETE2_1.png)

---

### After Delete

![DELETE2_2](phase2/images/DELETE2_2.png)

---

## DELETE Query 3 – Delete Unsold Products

This query deletes products that were never sold.

### Before Delete

![DELETE3_1](phase2/images/DELETE3_1.png)

---

### After Delete

![DELETE3_2](phase2/images/DELETE3_2.png)

---

# Constraints

## Constraint 1 – UNIQUE Constraint

This constraint ensures that duplicate requests from the same customer and employee on the same date cannot exist.

### Constraint Creation

![UNIQUE_CONSTRAIN1](phase2/images/UNIQUE_CONSTRAIN1.png)

---

### Constraint Validation

![UNIQUE_CONSTRAIN2](phase2/images/UNIQUE_CONSTRAIN2.png)

---

## Constraint 2 – CHECK Constraint

This constraint ensures that product prices must always be positive.

### Constraint Creation

![CHECK_CONSTRAIN1](phase2/images/CHECK_CONSTRAIN1.png)

---

### Constraint Validation

![CHECK_CONSTRAIN2](phase2/images/CHECK_CONSTRAIN2.png)

---

## Constraint 3 – FOREIGN KEY Constraint

This constraint ensures that every request belongs to an existing customer.

### Constraint Creation

![FOREIGN_KEY_CONSTRAIN1](phase2/images/FOREIGN_KEY_CONSTRAIN1.png)

---

### Constraint Validation

![FOREIGN_KEY_CONSTRAIN2](phase2/images/FOREIGN_KEY_CONSTRAIN2.png)

---

# Indexes

## Created Indexes

The following indexes were created in order to improve query performance.

![INDEXES](phase2/images/INDEXES.png)

---

## Index 1 – Requests Date Index

### Before Index

![INDEX1_1](phase2/images/INDEX1_1.png)

---

### After Index

![INDEX1_2](phase2/images/INDEX1_2.png)

---

### Explanation

The index improved filtering operations on request dates by reducing the number of scanned rows.

---

## Index 2 – Transactions Customer and Date Index

### Before Index

![INDEX2_1](phase2/images/INDEX2_1.png)

---

### After Index

![INDEX2_2](phase2/images/INDEX2_2.png)

---

### Explanation

The index improved searches involving customer transactions and transaction dates.

---

## Index 3 – Requests Employee and Status Index

### Before Index

![INDEX3_1](phase2/images/INDEX3_1.png)

---

### After Index

![INDEX3_2](phase2/images/INDEX3_2.png)

---

### Explanation

The index improved queries that filter requests by employee and request status.

---

# Backup

A full updated backup of the database was created after completing Phase 2.

The backup includes:

- Database structure
- Constraints
- Indexes
- All updated data
- Transactions and relationships

Backup file:

[Download backup](./phase2/backup2.backup)



# Phase 3 – Integration and Views

## Introduction

In this phase, we performed database integration between our original Customer Service system and an additional department database received from another team.

The goal of this phase was to create one integrated database while preserving the existing tables and data.  
The integration was performed according to option A, which requires changing the existing database schema using SQL commands, without recreating the entire database from scratch.

---

## New Department DSD

The DSD of the received department was created based on the restored backup database.

![DSD Other Department](phase3/images/DSD_OTHER.png)

---

## New Department ERD

After analyzing the DSD, we performed reverse engineering and created an ERD for the received department.

![ERD Other Department](phase3/images/ERD_OTHER.png)

---

## Integrated ERD

After comparing both systems, we designed a shared ERD that combines the original Customer Service department with the received department.

![Integrated ERD](phase3/images/ERD_INTEGRATION.png)

---

## Integrated DSD

The integrated DSD represents the final database structure after applying the integration changes.

![Integrated DSD](phase3/images/DSD_INTEGRATION.png)

---

## Reverse Engineering Algorithm

The reverse engineering process from DSD to ERD was performed as follows:

1. Each table in the received schema was examined.
2. Tables with an independent primary key and descriptive attributes were identified as entities.
3. Tables mainly composed of foreign keys were identified as relationship tables.
4. Primary keys were mapped as entity identifiers.
5. Foreign keys were used to identify relationships between entities.
6. The relationship cardinality was determined according to the location of the foreign key.
7. Lookup tables such as statuses, payment methods and seasons were identified as supporting entities.
8. Based on these rules, an ERD was created for the received department.

---

## Integration Decisions

During the integration process, several design decisions were made:

- The `customers` entities from both systems were merged into one customer structure.
- Customers from the received department were inserted into the existing `customers` table.
- Since our original system separates customers into `private` and `business`, customers from the received department were mapped into the `private` table.
- The `employees` entities were merged into the existing `employee` table.
- The `products` entities were merged into the existing `products` table.
- The received department’s `inquiries` were integrated into the existing `requests` table.
- Additional fields such as `subject`, `resolved_at`, and `interaction_log_json` were added to support the received department data.
- New supporting tables such as `seasons`, `paymentmethod`, and `transactionstatus` were added.
- ID offsets were used when inserting data from the received department in order to avoid primary key conflicts.
- Foreign key relationships were preserved after the integration.

---

## Integration Process

The integration was implemented in the file:

```text
Integrate.sql
```

The integration script:
- Added missing columns using ALTER TABLE
- Created new supporting tables
- Inserted data from the received department
- Preserved foreign key relationships
- Prevented primary key conflicts using ID offsets

---

# Views

Two views were created in the file:

```text
Views.sql
```

Each view represents one of the original departments and combines multiple tables using JOIN operations and filtering conditions.

---

## View 1 – Customer Service Active Requests View

This view represents our original Customer Service department.

The view combines:
- customers
- private/business
- requests
- employee
- rstatus
- priority

The view displays customer service requests together with:
- customer information
- employee information
- request status
- request priority

The view only displays valid and active requests.

---

## View Query

```sql
SELECT *
FROM customer_service_active_requests_view
LIMIT 10;
```

### Output

![Customer Service View](phase3/images/customer_service_view.png)

---

## Query 1 – Requests By Employee And Status

This query counts how many requests each employee handled for every request status.

```sql
SELECT
    employee_name,
    request_status,
    COUNT(*) AS total_requests
FROM customer_service_active_requests_view
GROUP BY employee_name, request_status
ORDER BY total_requests DESC;
```

### Output

![Customer Service Query 1](phase3/images/customer_service_query1.png)

---

## Query 2 – Customers With The Highest Number Of Requests

This query displays customers who opened the largest number of service requests.

```sql
SELECT
    customer_name,
    cphone,
    COUNT(*) AS total_requests
FROM customer_service_active_requests_view
GROUP BY customer_name, cphone
ORDER BY total_requests DESC
LIMIT 10;
```

### Output

![Customer Service Query 2](phase3/images/customer_service_query2.png)

---

## View 2 – Received Department Sales View

This view represents the department received from the other team.

The view combines:
- transactions
- customers
- products
- contains
- paymentmethod
- transactionstatus

The view displays:
- customer information
- product information
- transaction details
- payment information

The view only displays valid transactions and products.

---

## View Query

```sql
SELECT *
FROM received_department_sales_view
LIMIT 10;
```

### Output

![Received Department View](phase3/images/received_department_view.png)

---

## Query 1 – Most Sold Products

This query displays the products that appeared in the largest number of transactions.

```sql
SELECT
    product_name,
    COUNT(*) AS total_sales
FROM received_department_sales_view
GROUP BY product_name
ORDER BY total_sales DESC
LIMIT 10;
```

### Output

![Received Department Query 1](phase3/images/received_department_query1.png)

---

## Query 2 – Customers With The Highest Number Of Transactions

This query displays customers who performed the highest number of transactions.

```sql
SELECT
    customer_name,
    COUNT(*) AS total_transactions
FROM received_department_sales_view
GROUP BY customer_name
ORDER BY total_transactions DESC
LIMIT 10;
```

### Output

![Received Department Query 2](phase3/images/received_department_query2.png)

---

# Backup

A full updated backup of the integrated database was created after completing Phase 3.

Backup file:

[Download backup](./phase3/backup3.backup)

# Phase 4 – PL/pgSQL Programming

## Introduction

In this phase, we extended the integrated database created in Phase 3 by implementing advanced business logic using PL/pgSQL.

The goal of this phase was to create non-trivial database programs that operate directly on the integrated database and automate business processes.

The implementation includes:

* 2 Functions
* 2 Procedures
* 2 Triggers
* 2 Main Programs

The programs focus on two main business processes:

1. Employee workload management and automatic request reassignment.
2. Low stock product management and automatic price updates.

The implementation demonstrates the use of:

* Cursors
* Ref Cursors
* DML statements
* Conditional statements
* Loops
* Records
* Exception handling
* Triggers

---

# Database Changes

Before implementing the PL/pgSQL programs, several schema modifications were required.

These changes were implemented in the file:

```text
AlterTable.sql
```

```sql
ALTER TABLE requests
ADD COLUMN IF NOT EXISTS last_updated DATE DEFAULT CURRENT_DATE;

ALTER TABLE requests
ALTER COLUMN rnote_json TYPE TEXT;

ALTER TABLE employee
ADD COLUMN IF NOT EXISTS current_open_requests INT DEFAULT 0;

ALTER TABLE employee
ADD COLUMN IF NOT EXISTS current_load_score NUMERIC DEFAULT 0;

ALTER TABLE employee
ADD COLUMN IF NOT EXISTS current_load_level TEXT DEFAULT 'LOW';

ALTER TABLE employee
ADD COLUMN IF NOT EXISTS workload_updated_at DATE;
```

The column `last_updated` was added to the `requests` table in order to store the date of the most recent update performed on a request.

The column `rnote_json` was converted to `TEXT` in order to allow storing longer automatically generated notes.

The columns added to the `employee` table are derived fields that store the current workload information of each employee.

---

## Function 1 – Calculate Employee Load Score

The implementation was created in the file:

```text
calculate_employee_load_score.sql
```

### Description

This function calculates the workload score of a specific employee.

The calculation is based on:

* Number of open requests.
* Number of high-priority requests.
* Average age of open requests.

The function returns:

* Employee ID
* Employee Name
* Number of Open Requests
* Number of High Priority Requests
* Average Days Open
* Load Score
* Load Level

The workload level is classified as:

* LOW
* MEDIUM
* HIGH

### Code

```sql
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

    RETURN NEXT;
END;
$$ LANGUAGE plpgsql;
```

### Output

![Employee Load Function Output](phase4/images/proof_main1.png)

---

## Procedure 1 – Reassign Requests From Employee

The implementation was created in the file:

```text
reassign_requests_from_employee.sql
```

### Description

This procedure automatically balances workloads between employees.

The procedure receives:

* Source employee ID
* Target employee ID
* Maximum number of requests to transfer

The procedure:

1. Finds open requests assigned to the overloaded employee.
2. Sorts requests according to priority and age.
3. Reassigns requests to a less loaded employee.
4. Updates the request notes.
5. Updates the request update date.

### Code

```sql
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
        ORDER BY priority_id DESC, open_date ASC
        LIMIT p_max_requests
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
```

### Output

![Request Reassignment Procedure Output](phase4/images/proof_main1.png)

---

## Trigger 1 – Validate Request Reassignment

The implementation was created in the file:

```text
validate_request_reassignment.sql
```

### Description

This trigger is executed before updating the employee assigned to a request.

The trigger verifies that the target employee is not already overloaded.

If the target employee already has 20 or more open requests, the reassignment is rejected and an exception is raised.

This business rule prevents assigning requests to employees that are already overloaded.

### Code

```sql
CREATE OR REPLACE FUNCTION validate_request_reassignment()
RETURNS TRIGGER
AS $$
DECLARE
    v_open_requests INT;
BEGIN
    IF OLD.eid IS DISTINCT FROM NEW.eid THEN

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
```

### Output

![Request Reassignment Trigger Output](phase4/images/proof_main1.png)

---

## Main Program 1 – Employee Workload Management

The implementation was created in the file:

```text
main_employee_process.sql
```

### Description

This main program controls the entire workload balancing process.

The program:

1. Iterates through all employees.
2. Calculates workload scores using Function 1.
3. Finds the employee with the highest workload.
4. Finds the employee with the lowest workload.
5. Calls Procedure 1 in order to transfer requests.

### Code

```sql
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
```

### Output

![Main Program 1 Output](phase4/images/proof_main1.png)

---

# Low Stock Product Management

The second business process focuses on inventory management.

The workflow is:

```text
Main Program
    ↓
Get Low Stock Products
    ↓
Return Ref Cursor
    ↓
Increase Product Prices
    ↓
Validate Price Increase Using Trigger
```

---

## Function 2 – Get Low Stock Products

The implementation was created in the file:

```text
get_low_stock_products.sql
```

### Description

This function receives a stock threshold and returns a Ref Cursor containing all products whose stock quantity is lower than or equal to the specified limit.

Only products with valid stock information are considered.

This is important because the original products from our system do not necessarily contain stock quantity values, while products from the received department include stock information.

The function demonstrates the use of Ref Cursor.

### Code

```sql
CREATE OR REPLACE FUNCTION get_low_stock_products(p_limit INT)
RETURNS REFCURSOR
AS $$
DECLARE
    ref REFCURSOR;
BEGIN
    OPEN ref FOR
        SELECT
            pid,
            pname,
            price,
            stock_qty,
            manufactured_in,
            s_id
        FROM products
        WHERE stock_qty IS NOT NULL
          AND stock_qty <= p_limit
        ORDER BY stock_qty ASC, pname ASC;

    RETURN ref;

EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error in get_low_stock_products: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;
```

### Output

![Low Stock Function Output](phase4/images/proof_main2.png)

---

## Procedure 2 – Increase Low Stock Prices From Cursor

The implementation was created in the file:

```text
increase_low_stock_prices_from_cursor.sql
```

### Description

This procedure receives:

* A Ref Cursor containing low stock products.
* A percentage value representing the desired price increase.

The procedure iterates through the same cursor returned by Function 2 and updates the prices of all products in the cursor.

This avoids scanning the same products again and connects the function and procedure directly.

### Code

```sql
CREATE OR REPLACE PROCEDURE increase_low_stock_prices_from_cursor(
    p_products_cursor REFCURSOR,
    p_percent NUMERIC DEFAULT 5
)
AS $$
DECLARE
    rec RECORD;
    v_new_price NUMERIC;
    v_counter INT := 0;
BEGIN
    IF p_percent <= 0 THEN
        RAISE EXCEPTION 'Percent must be positive';
    END IF;

    LOOP
        FETCH p_products_cursor INTO rec;
        EXIT WHEN NOT FOUND;

        v_new_price := rec.price + (rec.price * p_percent / 100);

        UPDATE products
        SET price = ROUND(v_new_price)::INT
        WHERE pid = rec.pid;

        v_counter := v_counter + 1;

        RAISE NOTICE 'Product % price updated from % to % using % percent',
            rec.pname,
            rec.price,
            ROUND(v_new_price)::INT,
            p_percent;
    END LOOP;

    RAISE NOTICE 'Total products updated: %', v_counter;

EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error in increase_low_stock_prices_from_cursor: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;
```

### Output

![Low Stock Procedure Output](phase4/images/proof_main2.png)

---

## Trigger 2 – Validate Price Increase

The implementation was created in the file:

```text
validate_price_increase.sql
```

### Description

This trigger is executed before updating the price of a product.

The trigger prevents an excessive price increase in a single update operation.

If the new price is more than 20% higher than the old price, the update is rejected and an exception is raised.

This business rule protects the store from unreasonable automatic or manual price increases.

### Code

```sql
CREATE OR REPLACE FUNCTION validate_price_increase()
RETURNS TRIGGER
AS $$
BEGIN

    IF NEW.price > OLD.price * 1.20 THEN
        RAISE EXCEPTION
            'Price increase too high for product %. Old price: %, New price: %',
            NEW.pid,
            OLD.price,
            NEW.price;
    END IF;

    RETURN NEW;

END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_validate_price_increase ON products;

CREATE TRIGGER trg_validate_price_increase
BEFORE UPDATE OF price ON products
FOR EACH ROW
EXECUTE FUNCTION validate_price_increase();
```

### Output

![Price Increase Trigger Output](phase4/images/proof_main2.png)

---

## Main Program 2 – Stock Management Process

The implementation was created in the file:

```text
main_stock_process.sql
```

### Description

This main program controls the low-stock management process.

The program:

1. Opens a transaction.
2. Calls Function 2 and receives a Ref Cursor.
3. Passes the cursor to Procedure 2.
4. Updates the prices of low-stock products.
5. Closes the cursor.
6. Commits the transaction.

### Code

```sql
BEGIN;

DO $$
DECLARE
    c REFCURSOR;
    v_stock_limit INT := 10;
    v_price_update_percent NUMERIC := 5;
BEGIN
    RAISE NOTICE 'Main stock process started';

    c := get_low_stock_products(v_stock_limit);

    CALL increase_low_stock_prices_from_cursor(c, v_price_update_percent);

    CLOSE c;

    RAISE NOTICE 'Main stock process finished';
END;
$$;

COMMIT;
```

### Output

![Main Program 2 Output](phase4/images/proof_main2.png)

---

# Backup

A full updated backup of the database was created after completing Phase 4.


Backup file:

[Download backup](./phase4/backup4.backup)


# Phase 5 – Graphical User Interface (GUI)

## Introduction

In this phase, we developed a complete graphical user interface for our integrated Customer Service Management System.

The GUI was implemented using **Python** and **Tkinter**, while all data is stored and managed in a **PostgreSQL** database.

The application allows managers and employees to interact with the database through a user-friendly interface without executing SQL commands manually.

The system supports:

- Full CRUD operations
- Execution of analytical SQL queries
- Execution of PL/pgSQL functions and procedures
- Role-based access control
- Friendly graphical interface

---

# Technologies Used

- Python
- Tkinter
- PostgreSQL
- psycopg2
- Git & GitHub

---

# System Structure

The application contains two user roles:

## Manager

The manager can:

- View yearly revenue
- Execute analytical queries
- Run workload balancing
- Run supply & demand process
- Run discount products process
- View employee information
- Access employee screens

## Employee

Employees can manage:

- Customers
- Requests
- Transactions
- Products

---

# Login Screen

The application starts with a login screen.

Users enter:

- Employee ID
- Password

According to the employee role, the system opens either the Manager Dashboard or the Employee Dashboard.

### Screenshot

![Login](phase5/images/login.png)

---

# Manager Dashboard

The Manager Dashboard provides access to:

- Open Requests Over 30 Days
- Product Sales & Revenue
- Customer Total Spending
- Employees Table
- Workload Balance Process
- Supply & Demand Process
- Discount Products
- Employee Screens

### Screenshot

![Manager Dashboard](phase5/images/manager_dashboard.png)

---

# Employee Dashboard

The Employee Dashboard provides access to all operational screens.

### Screenshot

![Employee Dashboard](phase5/images/employee_dashboard.png)

---

# Customers Management

Features:

- Search customers
- Add customer
- Update customer
- Soft delete customer
- Status selection using ComboBox

Foreign keys are displayed as meaningful names instead of IDs.

### Screenshot

![Customers](phase5/images/customers.png)

---

# Requests Management

Features:

- Search requests
- Add request
- Update request
- Soft delete request
- Priority and status selection using ComboBoxes

### Screenshot

![Requests](phase5/images/requests.png)

---

# Transactions Management

Features:

- Search transactions
- Add transaction
- Update transaction
- Soft delete transaction

The system displays:

- Customer names
- Product names
- Employee names
- Payment method names
- Transaction status names

instead of foreign key IDs.

### Screenshot

![Transactions](phase5/images/transactions.png)

---

# Products Management

Features:

- Search products
- Add product
- Update product
- Soft delete product

Products are not physically deleted from the database.

Instead, a soft-delete mechanism is implemented using Active / Inactive status.

### Screenshot

![Products](phase5/images/products.png)

---

# SQL Queries From Phase 2

The GUI allows managers to execute analytical SQL queries directly.

## Open Requests Over 30 Days

Displays requests that remained open for longer than the selected period.

### Screenshot

![Open Requests](phase5/images/query_requests.png)

---

## Product Sales & Revenue

Displays:

- Product name
- Number of sales
- Total revenue

### Screenshot

![Product Revenue](phase5/images/product_revenue.png)

---

## Customer Total Spending

Displays the total amount spent by each customer.

### Screenshot

![Customer Revenue](phase5/images/customer_revenue.png)

---

# Employees Information

Displays employee workload information and management reports.

### Screenshot

![Employees](phase5/images/employees.png)

---

# PL/pgSQL Programs From Phase 4

The GUI supports execution of the business processes developed in Phase 4.

## Workload Balance

The manager selects the maximum number of requests to transfer.

The system:

1. Detects overloaded employees.
2. Detects less-loaded employees.
3. Executes the balancing procedure.
4. Displays a summary popup.

### Screenshot

![Workload Balance](phase5/images/workload_balance.png)

---

## Supply & Demand

The manager enters:

- Stock threshold
- Price increase percentage

The system:

1. Finds low-stock products.
2. Executes the function.
3. Executes the procedure.
4. Displays a summary popup.

### Screenshot

![Supply Demand](phase5/images/supply_demand.png)

---

## Discount Products

The manager can execute the discount process directly from the dashboard.

### Screenshot

![Discount Products](phase5/images/discount_product.png)

---

# User Interface Features

The GUI includes:

- Modern dashboard layout
- Sidebar navigation
- Color-coded action cards
- Popup notifications
- Search functionality
- ComboBoxes instead of foreign key IDs
- Soft-delete mechanisms
- Automatic refresh after updates
- Role-based access control

---

# Installation

Install the required package:

```bash
pip install psycopg2-binary
```

---

# Running the Application

```bash
python app.py
```

---

# Project Summary

The Phase 5 application provides a complete graphical interface for the integrated database system.

Implemented features:

- Full CRUD support
- Friendly user interface
- Role-based access control
- SQL query execution
- PL/pgSQL function and procedure execution
- Soft-delete mechanisms
- Foreign key name resolution
- PostgreSQL integration

The application satisfies all Phase 5 requirements and provides a practical and user-friendly way to manage the Customer Service system.