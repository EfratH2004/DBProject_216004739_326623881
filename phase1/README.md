# DBProject – Phase 1

## Team Members
Meitav Bin Nun
Efrat Hourvitz
---
# DBProject – Phase 1

## Introduction

The general topic of the project is an **online store system**.  
Each team was required to focus on a specific department within the store.

Our team chose to focus on the **Customer Service department**.  
Therefore, the system we designed manages the information required for customer support operations, including customers, service requests, employees, products, and transactions related to customer inquiries.

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

![ERD Diagram](Phase1/images/ERD.png)

---

# DSD Diagram

![DSD Diagram](Phase1/images/DSD.png)

---

# Design Decisions

### Weak Entities Design

In the current ERD design, entities that conceptually behave like weak entities are modeled as **regular entities**.

This design decision was made intentionally in order to simplify the ERD structure.

In future phases of the project, database constraints will be applied to enforce the intended structure.  
Specifically, **foreign keys will be constrained with UNIQUE constraints**, allowing them to participate as part of the primary key when needed.

This approach keeps the conceptual model clean while allowing flexibility in the database implementation.
