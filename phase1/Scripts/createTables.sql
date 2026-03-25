CREATE SEQUENCE cstatus_seq START 1;
CREATE SEQUENCE rstatus_seq START 1;
CREATE SEQUENCE priority_seq START 1;

CREATE TABLE CSTATUS
(
  CS_id INT DEFAULT nextval('cstatus_seq'),
  CS_name VARCHAR(20),
  PRIMARY KEY (CS_id)
);

CREATE TABLE CUSTOMERS
(
  Cid INT,
  Cphone VARCHAR(20),
  Cemail VARCHAR(50),
  Caddress VARCHAR(50),
  registration_date DATE,
  Cnote_json VARCHAR(50),
  CS_id INT,
  PRIMARY KEY (Cid),
  FOREIGN KEY (CS_id) REFERENCES CSTATUS(CS_id)
);

CREATE TABLE EMPLOYEE
(
  Eid INT,
  Ename VARCHAR(20),
  Ephone VARCHAR(20),
  Eaddress VARCHAR(50),
  start_date DATE,
  end_date DATE,
  PRIMARY KEY (Eid)
);

CREATE TABLE RSTATUS
(
  RS_id INT DEFAULT nextval('rstatus_seq'),
  RS_name VARCHAR(20),
  PRIMARY KEY (RS_id)
);

CREATE TABLE PRIORITY
(
  priority_id INT DEFAULT nextval('priority_seq'),
  priority_name VARCHAR(20),
  PRIMARY KEY (priority_id)
);

CREATE TABLE REQUESTS
(
  Rid INT,
  open_date DATE,
  Rnote_json VARCHAR(50),
  Cid INT,
  Eid INT,
  RS_id INT,
  priority_id INT,
  PRIMARY KEY (Rid),
  FOREIGN KEY (Cid) REFERENCES CUSTOMERS(Cid),
  FOREIGN KEY (Eid) REFERENCES EMPLOYEE(Eid),
  FOREIGN KEY (RS_id) REFERENCES RSTATUS(RS_id),
  FOREIGN KEY (priority_id) REFERENCES PRIORITY(priority_id)
);

CREATE TABLE PRODUCTS
(
  Pid INT,
  Pname VARCHAR(20),
  price INT,
  warranty_period INT,
  category VARCHAR(30),
  PRIMARY KEY (Pid)
);

CREATE TABLE TRANSACTIONS
(
  Tid INT,
  transaction_date DATE,
  Cid INT,
  Eid INT,
  Pid INT,
  PRIMARY KEY (Tid),
  FOREIGN KEY (Cid) REFERENCES CUSTOMERS(Cid),
  FOREIGN KEY (Eid) REFERENCES EMPLOYEE(Eid),
  FOREIGN KEY (Pid) REFERENCES PRODUCTS(Pid)
);

CREATE TABLE PRIVATE
(
  first_name VARCHAR(20),
  last_name VARCHAR(20),
  birthday DATE,
  gender VARCHAR(10),
  Cid INT,
  PRIMARY KEY (Cid),
  FOREIGN KEY (Cid) REFERENCES CUSTOMERS(Cid)
);

CREATE TABLE BUSINESS
(
  contact_name VARCHAR(20),
  company_name VARCHAR(20),
  website VARCHAR(40),
  Cid INT,
  PRIMARY KEY (Cid),
  FOREIGN KEY (Cid) REFERENCES CUSTOMERS(Cid)
);