import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import db


APP_TITLE = "Service Hub"
BG = "#F7F8FA"
CARD = "#FFFFFF"
PRIMARY = "#4F35F5"
TEXT = "#111827"


class ServiceHubApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("1250x760")
        self.configure(bg=BG)
        self.current_user = None
        self.show_login()

    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()

    def topbar(self, title, back_command=None):
        bar = tk.Frame(self, bg=CARD, height=70)
        bar.pack(fill="x")
        left = tk.Frame(bar, bg=CARD)
        left.pack(side="left", padx=24, pady=18)

        if back_command:
            tk.Button(left, text="← Back", command=back_command, bg=CARD, bd=0, font=("Arial", 12)).pack(side="left", padx=(0, 18))

        tk.Label(left, text=title, bg=CARD, fg=TEXT, font=("Arial", 20, "bold")).pack(side="left")

        tk.Label(bar, text="● System Online", bg="#F1F5F9", fg="#334155", font=("Arial", 11), padx=18, pady=8).pack(side="right", padx=24)

    def button(self, parent, text, command, width=28):
        return tk.Button(parent, text=text, command=command, bg=PRIMARY, fg="white",
                         activebackground=PRIMARY, activeforeground="white",
                         font=("Arial", 12, "bold"), relief="flat", padx=14, pady=12, width=width)

    def ghost_button(self, parent, text, command, width=24):
        return tk.Button(parent, text=text, command=command, bg="#EEF2FF", fg=PRIMARY,
                         font=("Arial", 11, "bold"), relief="flat", padx=12, pady=10, width=width)

    def show_login(self):
        self.clear()
        self.configure(bg=BG)

        card = tk.Frame(self, bg=CARD, padx=45, pady=45)
        card.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(card, text="Service Hub", bg=CARD, fg=TEXT, font=("Arial", 28, "bold")).pack(pady=(0, 8))
        tk.Label(card, text="Customer Service Management System", bg=CARD, fg="#64748B", font=("Arial", 14)).pack(pady=(0, 28))

        tk.Label(card, text="Employee ID", bg=CARD, fg=TEXT, font=("Arial", 11, "bold")).pack(anchor="w")
        eid_entry = tk.Entry(card, font=("Arial", 13), width=34)
        eid_entry.pack(pady=(5, 14), ipady=7)

        tk.Label(card, text="Password", bg=CARD, fg=TEXT, font=("Arial", 11, "bold")).pack(anchor="w")
        pass_entry = tk.Entry(card, show="*", font=("Arial", 13), width=34)
        pass_entry.pack(pady=(5, 22), ipady=7)

        def login():
            eid = eid_entry.get().strip()
            password = pass_entry.get().strip()
            if not eid or not password:
                messagebox.showwarning("Missing details", "Please enter employee ID and password.")
                return
            try:
                user = db.fetch_one("""
                    SELECT eid, ename, role
                    FROM employee
                    WHERE eid = %s AND password = %s
                """, (eid, password))
                if not user:
                    messagebox.showerror("Login failed", "Invalid employee ID or password.")
                    return
                self.current_user = dict(user)
                if self.current_user["role"] == "manager":
                    self.show_manager_dashboard()
                else:
                    self.show_employee_dashboard()
            except Exception as e:
                messagebox.showerror("Connection error", f"Could not connect to database.\n\n{e}")

        self.button(card, "Sign in", login, width=30).pack()

        tk.Label(card, text="Default password after setup: 1234", bg=CARD, fg="#94A3B8", font=("Arial", 10)).pack(pady=(18, 0))

    def show_manager_dashboard(self):
        self.clear()
        self.topbar("Manager Dashboard")
        body = tk.Frame(self, bg=BG, padx=28, pady=28)
        body.pack(fill="both", expand=True)

        info = tk.Frame(body, bg=CARD, padx=28, pady=22)
        info.pack(fill="x", pady=(0, 22))

        revenue = self.get_year_revenue()
        tk.Label(info, text="Revenue This Year", bg=CARD, fg="#64748B", font=("Arial", 13, "bold")).pack(anchor="w")
        tk.Label(info, text=f"${revenue:,.2f}", bg=CARD, fg=TEXT, font=("Arial", 30, "bold")).pack(anchor="w", pady=(8, 0))

        grid = tk.Frame(body, bg=BG)
        grid.pack(anchor="w")

        actions = [
            ("Open Requests Over 30 Days", self.show_old_open_requests_query),
            ("Product Sales & Revenue", self.show_product_sales_query),
            ("Customer Total Spending", self.show_customer_spending_query),
            ("Employees Table", self.show_employees_table),
            ("Run Workload Balance", self.run_workload_balance),
            ("Run Supply & Demand", self.run_supply_demand),
            ("Discount Products", self.show_discount_screen),
            ("Enter Employee Screens", self.show_employee_dashboard),
            ("Logout", self.show_login),
        ]

        for i, (txt, cmd) in enumerate(actions):
            btn = self.button(grid, txt, cmd)
            btn.grid(row=i // 3, column=i % 3, padx=12, pady=12, sticky="ew")

    def get_year_revenue(self):
        try:
            row = db.fetch_one("""
                SELECT COALESCE(SUM(payment), 0) AS revenue
                FROM transactions
                WHERE EXTRACT(YEAR FROM payment_date) = EXTRACT(YEAR FROM CURRENT_DATE)
            """)
            return float(row["revenue"] or 0)
        except Exception:
            try:
                row = db.fetch_one("SELECT COALESCE(SUM(payment), 0) AS revenue FROM transactions")
                return float(row["revenue"] or 0)
            except Exception:
                return 0.0

    def show_employee_dashboard(self):
        self.clear()
        self.topbar("Employee Dashboard", self.show_manager_dashboard if self.current_user and self.current_user.get("role") == "manager" else None)
        body = tk.Frame(self, bg=BG, padx=28, pady=28)
        body.pack(fill="both", expand=True)

        tk.Label(body, text=f"Welcome, {self.current_user.get('ename', '')}", bg=BG, fg=TEXT, font=("Arial", 18, "bold")).pack(anchor="w", pady=(0, 18))

        grid = tk.Frame(body, bg=BG)
        grid.pack(anchor="w")

        actions = [
            ("Customers", lambda: self.show_crud_table("customers")),
            ("My Requests", self.show_requests_screen),
            ("My Transactions", self.show_transactions_screen),
            ("Products", lambda: self.show_crud_table("products")),
            ("Logout", self.show_login),
        ]

        for i, (txt, cmd) in enumerate(actions):
            self.button(grid, txt, cmd).grid(row=i // 3, column=i % 3, padx=12, pady=12)

    def table_view(self, title, columns, rows, back_command, row_actions=None):
        self.clear()
        self.topbar(title, back_command)
        frame = tk.Frame(self, bg=BG, padx=24, pady=24)
        frame.pack(fill="both", expand=True)

        tree = ttk.Treeview(frame, columns=columns, show="headings", height=18)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor="w")
        tree.pack(fill="both", expand=True)

        for row in rows:
            values = [row.get(c) for c in columns]
            tree.insert("", "end", values=values)

        if row_actions:
            actions_frame = tk.Frame(frame, bg=BG)
            actions_frame.pack(fill="x", pady=14)
            for text, callback in row_actions:
                self.ghost_button(actions_frame, text, lambda cb=callback, tr=tree: cb(tr)).pack(side="left", padx=8)

    def show_crud_table(self, table_name):
        self.clear()
        self.topbar(table_name.title(), self.show_employee_dashboard)

        frame = tk.Frame(self, bg=BG, padx=24, pady=24)
        frame.pack(fill="both", expand=True)

        top = tk.Frame(frame, bg=BG)
        top.pack(fill="x", pady=(0, 14))

        search_var = tk.StringVar()
        tk.Entry(top, textvariable=search_var, font=("Arial", 12), width=42).pack(side="left", ipady=7)
        self.ghost_button(top, "Search / Refresh", lambda: load()).pack(side="left", padx=8)
        self.button(top, f"Add {table_name[:-1].title()}", lambda: self.open_form(table_name), width=18).pack(side="right")

        columns = self.get_display_columns(table_name)
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=18)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=140, anchor="w")
        tree.pack(fill="both", expand=True)

        actions = tk.Frame(frame, bg=BG)
        actions.pack(fill="x", pady=12)

        def selected_pk():
            item = tree.focus()
            if not item:
                messagebox.showwarning("No selection", "Please select a row first.")
                return None
            values = tree.item(item, "values")
            return values[0]

        self.ghost_button(actions, "Edit Selected", lambda: self.open_form(table_name, selected_pk())).pack(side="left", padx=6)
        self.ghost_button(actions, "Delete Selected", lambda: self.safe_delete(table_name, selected_pk(), load)).pack(side="left", padx=6)

        def load():
            for x in tree.get_children():
                tree.delete(x)
            try:
                rows = self.get_table_rows(table_name, search_var.get().strip())
                for row in rows:
                    tree.insert("", "end", values=[row.get(c) for c in columns])
            except Exception as e:
                messagebox.showerror("Error", str(e))

        load()

    def get_display_columns(self, table):
        if table == "customers":
            return ["cid", "customer_name", "cemail", "cphone", "caddress", "registration_date", "status_name"]
        if table == "products":
            return ["pid", "pname", "price", "stock_qty", "manufactured_in"]
        return db.get_columns(table)

    def get_table_rows(self, table, search=""):
        if table == "customers":
            return db.fetch_all("""
                SELECT c.cid,
                       COALESCE(pr.first_name || ' ' || pr.last_name, b.company_name, b.contact_name, c.cnote_json, c.cid::text) AS customer_name,
                       c.cemail, c.cphone, c.caddress, c.registration_date,
                       COALESCE(cs.cs_name, '') AS status_name
                FROM customers c
                LEFT JOIN cstatus cs ON c.cs_id = cs.cs_id
                LEFT JOIN private pr ON c.cid = pr.cid
                LEFT JOIN business b ON c.cid = b.cid
                WHERE %s = '' OR
                      LOWER(COALESCE(pr.first_name || ' ' || pr.last_name, b.company_name, b.contact_name, c.cnote_json, '')) LIKE LOWER(%s)
                ORDER BY c.cid
            """, (search, f"%{search}%"))
        if table == "products":
            extra = "AND (pname ILIKE %s OR pid::text ILIKE %s)" if search else ""
            params = (f"%{search}%", f"%{search}%") if search else ()
            return db.fetch_all(f"""
                SELECT pid, pname, price, stock_qty, manufactured_in
                FROM products
                WHERE COALESCE(is_active, TRUE) = TRUE
                {extra}
                ORDER BY pid
            """, params)
        extra = ""
        params = ()
        if search:
            cols = db.get_columns(table)
            conditions = [f"CAST({c} AS TEXT) ILIKE %s" for c in cols]
            extra = "WHERE " + " OR ".join(conditions)
            params = tuple([f"%{search}%"] * len(cols))
        return db.fetch_all(f"SELECT * FROM {table} {extra} ORDER BY 1", params)

    def open_form(self, table_name, pk_value=None):
        if pk_value is None and table_name in ("requests", "transactions"):
            if table_name == "requests":
                return self.open_request_form()
            return self.open_transaction_form()

        cols = db.get_columns(table_name)
        pk = db.get_pk_column(table_name) or cols[0]
        row = None
        if pk_value:
            row = db.fetch_one(f"SELECT * FROM {table_name} WHERE {pk} = %s", (pk_value,))
            if not row:
                messagebox.showerror("Error", "Record was not found.")
                return

        win = tk.Toplevel(self)
        win.title(("Edit " if pk_value else "Add ") + table_name)
        win.geometry("520x620")
        win.configure(bg=BG)

        entries = {}
        for col in cols:
            if col == "is_active":
                continue
            tk.Label(win, text=col, bg=BG, fg=TEXT, font=("Arial", 10, "bold")).pack(anchor="w", padx=22, pady=(10, 2))
            ent = tk.Entry(win, font=("Arial", 11), width=44)
            ent.pack(padx=22, ipady=5)
            if row and row.get(col) is not None:
                ent.insert(0, str(row.get(col)))
            if pk_value and col == pk:
                ent.config(state="disabled")
            entries[col] = ent

        def save():
            try:
                data = {c: e.get().strip() or None for c, e in entries.items()}
                if pk_value:
                    update_cols = [c for c in data.keys() if c != pk]
                    sql = f"UPDATE {table_name} SET " + ", ".join([f"{c} = %s" for c in update_cols]) + f" WHERE {pk} = %s"
                    db.execute(sql, tuple(data[c] for c in update_cols) + (pk_value,))
                    messagebox.showinfo("Updated", f"{table_name.title()} was updated successfully.")
                else:
                    insert_cols = list(data.keys())
                    sql = f"INSERT INTO {table_name} (" + ", ".join(insert_cols) + ") VALUES (" + ", ".join(["%s"] * len(insert_cols)) + ")"
                    db.execute(sql, tuple(data[c] for c in insert_cols))
                    messagebox.showinfo("Added", f"{table_name.title()} was added successfully.")
                win.destroy()
                self.show_crud_table(table_name)
            except Exception as e:
                messagebox.showerror("Error", str(e))

        self.button(win, "Save", save, width=18).pack(pady=22)

    def safe_delete(self, table_name, pk_value, refresh_callback):
        if not pk_value:
            return
        if not messagebox.askyesno("Confirm", f"Are you sure you want to delete this {table_name[:-1]}?"):
            return
        try:
            pk = db.get_pk_column(table_name) or db.get_columns(table_name)[0]
            if table_name == "products":
                db.execute("UPDATE products SET is_active = FALSE WHERE pid = %s", (pk_value,))
                messagebox.showinfo("Deleted", "Product was removed from the active products list.")
            else:
                db.execute(f"DELETE FROM {table_name} WHERE {pk} = %s", (pk_value,))
                messagebox.showinfo("Deleted", f"{table_name.title()} record was deleted successfully.")
            refresh_callback()
        except Exception as e:
            messagebox.showerror("Delete blocked", f"The record could not be deleted because it may be connected to other data.\n\n{e}")

    def show_requests_screen(self):
        self.clear()
        self.topbar("Requests", self.show_employee_dashboard)
        frame = tk.Frame(self, bg=BG, padx=24, pady=24)
        frame.pack(fill="both", expand=True)

        top = tk.Frame(frame, bg=BG)
        top.pack(fill="x", pady=(0, 14))
        self.button(top, "New Request", self.open_request_form, width=18).pack(side="left")
        self.ghost_button(top, "Clean Old Requests", self.clean_old_requests, width=20).pack(side="left", padx=8)

        columns = ["rid", "subject", "customer_name", "status_name", "priority_name", "employee_name", "open_date"]
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=20)
        for c in columns:
            tree.heading(c, text=c)
            tree.column(c, width=160)
        tree.pack(fill="both", expand=True)

        def load():
            for x in tree.get_children():
                tree.delete(x)
            if self.current_user.get("role") == "manager":
                rows = db.fetch_all("""
                    SELECT r.rid, r.rnote_json AS subject,
                           COALESCE(pr.first_name || ' ' || pr.last_name, b.company_name, b.contact_name, c.cnote_json, c.cid::text) AS customer_name,
                           rs.rs_name AS status_name, p.priority_name, e.ename AS employee_name, r.open_date
                    FROM requests r
                    JOIN customers c ON r.cid = c.cid
                    LEFT JOIN private pr ON c.cid = pr.cid
                    LEFT JOIN business b ON c.cid = b.cid
                    LEFT JOIN rstatus rs ON r.rs_id = rs.rs_id
                    LEFT JOIN priority p ON r.priority_id = p.priority_id
                    LEFT JOIN employee e ON r.eid = e.eid
                    ORDER BY r.open_date DESC
                """)
            else:
                rows = db.fetch_all("""
                    SELECT r.rid, r.rnote_json AS subject,
                           COALESCE(pr.first_name || ' ' || pr.last_name, b.company_name, b.contact_name, c.cnote_json, c.cid::text) AS customer_name,
                           rs.rs_name AS status_name, p.priority_name, e.ename AS employee_name, r.open_date
                    FROM requests r
                    JOIN customers c ON r.cid = c.cid
                    LEFT JOIN private pr ON c.cid = pr.cid
                    LEFT JOIN business b ON c.cid = b.cid
                    LEFT JOIN rstatus rs ON r.rs_id = rs.rs_id
                    LEFT JOIN priority p ON r.priority_id = p.priority_id
                    LEFT JOIN employee e ON r.eid = e.eid
                    WHERE r.eid = %s
                    ORDER BY r.open_date DESC
                """, (self.current_user["eid"],))
            for r in rows:
                tree.insert("", "end", values=[r.get(c) for c in columns])

        action = tk.Frame(frame, bg=BG)
        action.pack(fill="x", pady=12)

        def selected():
            item = tree.focus()
            if not item:
                messagebox.showwarning("No selection", "Please select a request first.")
                return None
            return tree.item(item, "values")[0]

        self.ghost_button(action, "Edit Selected", lambda: self.open_request_form(selected())).pack(side="left", padx=6)
        self.ghost_button(action, "Delete Selected", lambda: self.delete_request(selected(), load)).pack(side="left", padx=6)
        load()

    def open_request_form(self, rid=None):
        row = db.fetch_one("SELECT * FROM requests WHERE rid = %s", (rid,)) if rid else None
        if rid and not row:
            return

        win = tk.Toplevel(self)
        win.title("Request")
        win.geometry("520x620")
        win.configure(bg=BG)

        customers = db.fetch_all("""
            SELECT c.cid, COALESCE(pr.first_name || ' ' || pr.last_name, b.company_name, b.contact_name, c.cnote_json, c.cid::text) AS name
            FROM customers c
            LEFT JOIN private pr ON c.cid = pr.cid
            LEFT JOIN business b ON c.cid = b.cid
            ORDER BY c.cid
        """)
        statuses = db.fetch_all("SELECT rs_id, rs_name FROM rstatus ORDER BY rs_id")
        priorities = db.fetch_all("SELECT priority_id, priority_name FROM priority ORDER BY priority_id")
        employees = db.fetch_all("SELECT eid, ename FROM employee ORDER BY eid")

        def combo(label, items, id_key, name_key, selected_id=None):
            tk.Label(win, text=label, bg=BG, fg=TEXT, font=("Arial", 10, "bold")).pack(anchor="w", padx=22, pady=(10, 2))
            values = [f"{x[id_key]} - {x[name_key]}" for x in items]
            cb = ttk.Combobox(win, values=values, state="readonly", width=42)
            cb.pack(padx=22, ipady=4)
            if selected_id is not None:
                for i, x in enumerate(items):
                    if str(x[id_key]) == str(selected_id):
                        cb.current(i)
                        break
            elif values:
                cb.current(0)
            return cb

        tk.Label(win, text="Subject / note", bg=BG, fg=TEXT, font=("Arial", 10, "bold")).pack(anchor="w", padx=22, pady=(10, 2))
        subject = tk.Entry(win, font=("Arial", 11), width=44)
        subject.pack(padx=22, ipady=5)
        if row:
            subject.insert(0, str(row.get("rnote_json") or ""))

        c_cb = combo("Customer", customers, "cid", "name", row.get("cid") if row else None)
        s_cb = combo("Status", statuses, "rs_id", "rs_name", row.get("rs_id") if row else None)
        p_cb = combo("Priority", priorities, "priority_id", "priority_name", row.get("priority_id") if row else None)
        e_cb = combo("Assigned employee", employees, "eid", "ename", row.get("eid") if row else self.current_user["eid"])

        def id_from_cb(cb):
            return int(cb.get().split(" - ")[0])

        def save():
            try:
                if rid:
                    db.execute("""
                        UPDATE requests
                        SET rnote_json = %s, cid = %s, rs_id = %s, priority_id = %s, eid = %s, last_updated = CURRENT_DATE
                        WHERE rid = %s
                    """, (subject.get(), id_from_cb(c_cb), id_from_cb(s_cb), id_from_cb(p_cb), id_from_cb(e_cb), rid))
                    messagebox.showinfo("Updated", "Request was updated successfully.")
                else:
                    cols = db.get_columns("requests")
                    if "open_date" in cols:
                        db.execute("""
                            INSERT INTO requests (rnote_json, cid, rs_id, priority_id, eid, open_date)
                            VALUES (%s, %s, %s, %s, %s, CURRENT_DATE)
                        """, (subject.get(), id_from_cb(c_cb), id_from_cb(s_cb), id_from_cb(p_cb), id_from_cb(e_cb)))
                    else:
                        db.execute("""
                            INSERT INTO requests (rnote_json, cid, rs_id, priority_id, eid)
                            VALUES (%s, %s, %s, %s, %s)
                        """, (subject.get(), id_from_cb(c_cb), id_from_cb(s_cb), id_from_cb(p_cb), id_from_cb(e_cb)))
                    messagebox.showinfo("Added", "Request was added successfully.")
                win.destroy()
                self.show_requests_screen()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        self.button(win, "Save Request", save, width=18).pack(pady=22)

    def delete_request(self, rid, refresh):
        if not rid:
            return
        if not messagebox.askyesno("Confirm", "Are you sure you want to delete this request?"):
            return
        try:
            db.execute("DELETE FROM requests WHERE rid = %s", (rid,))
            messagebox.showinfo("Deleted", "Request was deleted successfully.")
            refresh()
        except Exception as e:
            messagebox.showerror("Delete blocked", str(e))

    def clean_old_requests(self):
        if not messagebox.askyesno("Confirm", "Are you sure you want to clean old requests?"):
            return
        try:
            db.execute("DELETE FROM requests WHERE open_date < CURRENT_DATE - INTERVAL '5 years'")
            messagebox.showinfo("Done", "Old requests cleanup finished successfully.")
            self.show_requests_screen()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_transactions_screen(self):
        self.clear()
        self.topbar("Transactions", self.show_employee_dashboard)

        columns = [
            "tid",
            "transaction_date",
            "customer_id",
            "product_name",
            "payment",
            "amount",
            "has_discount",
            "payment_method",
            "status",
            "employee_name"
        ]

        try:
            base_query = """
                SELECT
                    t.tid,
                    t.transaction_date,
                    t.cid AS customer_id,
                    p.pname AS product_name,
                    t.payment,
                    t.amount,
                    t.has_discount,
                    COALESCE(pm.pm_name, t.pm_id::TEXT) AS payment_method,
                    COALESCE(ts.t_status_name, t.t_status_id::TEXT) AS status,
                    e.ename AS employee_name
                FROM transactions t
                LEFT JOIN products p ON t.pid = p.pid
                LEFT JOIN employee e ON t.eid = e.eid
                LEFT JOIN paymentmethod pm ON t.pm_id = pm.pm_id
                LEFT JOIN transactionstatus ts ON t.t_status_id = ts.t_status_id
            """

            if self.current_user.get("role") == "manager":
                rows = db.fetch_all(base_query + " ORDER BY t.transaction_date DESC")
            else:
                rows = db.fetch_all(
                    base_query + " WHERE t.eid = %s ORDER BY t.transaction_date DESC",
                    (self.current_user["eid"],)
                )

        except Exception as e:
            messagebox.showerror("Error", str(e))
            rows = []

        self.table_view(
            "Transactions",
            columns,
            rows,
            self.show_employee_dashboard
        )
        
    def show_old_open_requests_query(self):
        rows = db.fetch_all("""
            SELECT r.rid,
                   r.rnote_json AS subject,
                   COALESCE(pr.first_name || ' ' || pr.last_name, b.company_name, b.contact_name, c.cnote_json, c.cid::text) AS customer_name,
                   r.open_date,
                   CURRENT_DATE - r.open_date AS days_open
            FROM requests r
            JOIN customers c ON r.cid = c.cid
            LEFT JOIN private pr ON c.cid = pr.cid
            LEFT JOIN business b ON c.cid = b.cid
            JOIN rstatus rs ON r.rs_id = rs.rs_id
            WHERE LOWER(rs.rs_name) = 'open'
              AND r.open_date < CURRENT_DATE - INTERVAL '30 days'
            ORDER BY days_open DESC
        """)
        messagebox.showinfo("Query finished", "Open requests over 30 days query finished successfully.")
        self.table_view("Open Requests Over 30 Days", ["rid", "subject", "customer_name", "open_date", "days_open"], rows, self.show_manager_dashboard)

    def show_product_sales_query(self):
        rows = db.fetch_all("""
            SELECT p.pid,
                   p.pname,
                   COUNT(t.tid) AS total_sales,
                   COALESCE(SUM(t.payment), 0) AS total_revenue
            FROM products p
            LEFT JOIN transactions t ON p.pid = t.pid
            WHERE COALESCE(p.is_active, TRUE) = TRUE
            GROUP BY p.pid, p.pname
            ORDER BY total_revenue DESC
        """)
        self.table_view("Product Sales & Revenue", ["pid", "pname", "total_sales", "total_revenue"], rows, self.show_manager_dashboard,
                        row_actions=[("Remove Selected Product", self.remove_product_from_query)])
        messagebox.showinfo("Query finished", "Product sales and revenue query finished successfully.")

    def remove_product_from_query(self, tree):
        item = tree.focus()
        if not item:
            messagebox.showwarning("No selection", "Please select a product.")
            return
        pid = tree.item(item, "values")[0]
        if messagebox.askyesno("Confirm", "Remove this product from active products?"):
            db.execute("UPDATE products SET is_active = FALSE WHERE pid = %s", (pid,))
            messagebox.showinfo("Removed", "Product was removed from the active products list.")
            self.show_product_sales_query()

    def show_customer_spending_query(self):
        rows = db.fetch_all("""
            SELECT c.cid,
                   COALESCE(pr.first_name || ' ' || pr.last_name, b.company_name, b.contact_name, c.cnote_json, c.cid::text) AS customer_name,
                   COALESCE(SUM(t.payment), 0) AS total_spent
            FROM customers c
            LEFT JOIN transactions t ON c.cid = t.cid
            LEFT JOIN private pr ON c.cid = pr.cid
            LEFT JOIN business b ON c.cid = b.cid
            GROUP BY c.cid, pr.first_name, pr.last_name, b.company_name, b.contact_name
            ORDER BY total_spent DESC
        """)
        messagebox.showinfo("Query finished", "Customer total spending query finished successfully.")
        self.table_view("Customer Total Spending", ["cid", "customer_name", "total_spent"], rows, self.show_manager_dashboard)

    def show_employees_table(self):
        rows = db.fetch_all("""
            SELECT eid, ename, ephone, eaddress, role, current_open_requests, current_load_score, current_load_level
            FROM employee
            ORDER BY eid
        """)
        self.table_view("Employees", ["eid", "ename", "ephone", "eaddress", "role", "current_open_requests", "current_load_score", "current_load_level"], rows, self.show_manager_dashboard)

    def run_workload_balance(self):
        if not messagebox.askyesno("Confirm", "Run workload balance process?"):
            return
        try:
            before = db.fetch_all("SELECT eid, ename FROM employee ORDER BY eid")
            db.callproc("""
                DO $$
                DECLARE
                    emp_rec RECORD;
                    load_rec RECORD;
                    v_source_eid INT := NULL;
                    v_source_score NUMERIC := -1;
                    v_target_eid INT := NULL;
                    v_target_score NUMERIC := 9999999;
                BEGIN
                    FOR emp_rec IN SELECT eid, ename FROM employee ORDER BY eid LOOP
                        SELECT * INTO load_rec FROM calculate_employee_load_score(emp_rec.eid);

                        IF load_rec.load_level = 'HIGH' AND load_rec.load_score > v_source_score THEN
                            v_source_eid := load_rec.employee_id;
                            v_source_score := load_rec.load_score;
                        END IF;

                        IF load_rec.load_score < v_target_score THEN
                            v_target_eid := load_rec.employee_id;
                            v_target_score := load_rec.load_score;
                        END IF;
                    END LOOP;

                    IF v_source_eid IS NOT NULL AND v_target_eid IS NOT NULL AND v_source_eid <> v_target_eid THEN
                        CALL reassign_requests_from_employee(v_source_eid, v_target_eid, 5);
                    END IF;
                END;
                $$;
            """)
            messagebox.showinfo("Workload Balance", "Workload balance finished successfully.\nRequests were reassigned if an overloaded employee was found.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def run_supply_demand(self):
        if not messagebox.askyesno("Confirm", "Run supply and demand process?"):
            return
        try:
            db.callproc("""
                BEGIN;
                DO $$
                DECLARE
                    c REFCURSOR;
                    v_stock_limit INT := 10;
                    v_price_update_percent NUMERIC := 5;
                BEGIN
                    c := get_low_stock_products(v_stock_limit);
                    CALL increase_low_stock_prices_from_cursor(c, v_price_update_percent);
                    CLOSE c;
                END;
                $$;
                COMMIT;
            """)
            messagebox.showinfo("Supply & Demand", "Supply and demand process finished successfully.\nLow-stock product prices were updated.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_discount_screen(self):
        self.clear()
        self.topbar("Discount Products", self.show_manager_dashboard)
        frame = tk.Frame(self, bg=BG, padx=24, pady=24)
        frame.pack(fill="both", expand=True)

        control = tk.Frame(frame, bg=BG)
        control.pack(fill="x", pady=(0, 14))

        tk.Label(control, text="Discount percent:", bg=BG, font=("Arial", 11, "bold")).pack(side="left")
        percent_entry = tk.Entry(control, width=10, font=("Arial", 11))
        percent_entry.insert(0, "10")
        percent_entry.pack(side="left", padx=8)

        columns = ["pid", "pname", "price", "stock_qty"]
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=18)
        for c in columns:
            tree.heading(c, text=c)
            tree.column(c, width=160)
        tree.pack(fill="both", expand=True)

        def load():
            for x in tree.get_children():
                tree.delete(x)
            rows = db.fetch_all("""
                SELECT pid, pname, price, stock_qty
                FROM products
                WHERE COALESCE(is_active, TRUE) = TRUE
                ORDER BY pname
            """)
            for r in rows:
                tree.insert("", "end", values=[r.get(c) for c in columns])

        def apply_discount():
            item = tree.focus()
            if not item:
                messagebox.showwarning("No selection", "Please select a product.")
                return
            try:
                percent = float(percent_entry.get())
                if percent <= 0 or percent >= 100:
                    messagebox.showwarning("Invalid percent", "Discount percent must be between 0 and 100.")
                    return
                pid = tree.item(item, "values")[0]
                db.execute("""
                    UPDATE products
                    SET price = ROUND(price - (price * %s / 100))
                    WHERE pid = %s
                """, (percent, pid))
                messagebox.showinfo("Discount applied", "Discount was applied successfully.")
                load()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        self.button(control, "Apply Discount To Selected", apply_discount, width=24).pack(side="left", padx=8)
        load()


if __name__ == "__main__":
    app = ServiceHubApp()
    app.mainloop()
