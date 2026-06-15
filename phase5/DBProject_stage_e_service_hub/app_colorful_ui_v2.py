import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import db


APP_TITLE = "Service Hub"

# Colorful modern UI theme
BG = "#F5F7FF"
CARD = "#FFFFFF"
PRIMARY = "#6D5DFB"
PRIMARY_DARK = "#5145CD"
PRIMARY_LIGHT = "#EEF2FF"
TEXT = "#0F172A"
SUBTEXT = "#64748B"
BORDER = "#E0E7FF"

SIDEBAR = "#2D1B9A"
SIDEBAR_TEXT = "#EEF2FF"
SIDEBAR_ACTIVE = "#3B2DB8"

DANGER = "#F43F5E"
SUCCESS = "#10B981"
WARNING = "#F59E0B"
INFO = "#0EA5E9"
TEAL = "#14B8A6"
PINK = "#EC4899"
ORANGE = "#F97316"
PURPLE = "#8B5CF6"


class ServiceHubApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("1280x780")
        self.minsize(1120, 700)
        self.configure(bg=BG)
        self.current_user = None
        self.setup_styles()
        self.show_login()

    def setup_styles(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure("Treeview", background=CARD, foreground=TEXT, fieldbackground=CARD,
                        borderwidth=0, rowheight=34, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", background="#F8FAFC", foreground="#334155",
                        borderwidth=0, font=("Segoe UI", 10, "bold"))
        style.map("Treeview", background=[("selected", "#E0E7FF")], foreground=[("selected", TEXT)])
        style.configure("TCombobox", fieldbackground=CARD, background=CARD, foreground=TEXT, padding=6)

    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()

    def topbar(self, title, back_command=None):
        bar = tk.Frame(self, bg=CARD, height=76, highlightbackground=BORDER, highlightthickness=1)
        bar.pack(fill="x")
        bar.pack_propagate(False)

        left = tk.Frame(bar, bg=CARD)
        left.pack(side="left", padx=26, pady=17)

        if back_command:
            tk.Button(left, text="← Back", command=back_command, bg=PRIMARY_LIGHT, fg=PRIMARY,
                      activebackground="#E0E7FF", activeforeground=PRIMARY, bd=0,
                      font=("Segoe UI", 10, "bold"), padx=14, pady=8, cursor="hand2").pack(side="left", padx=(0, 16))

        tk.Label(left, text=title, bg=CARD, fg=TEXT, font=("Segoe UI", 22, "bold")).pack(side="left")

        user_name = self.current_user.get("ename", "Guest") if self.current_user else "Guest"
        tk.Label(bar, text=f"● Online   {user_name}", bg="#F8FAFC", fg="#334155",
                 font=("Segoe UI", 10, "bold"), padx=18, pady=9).pack(side="right", padx=24)

    def button(self, parent, text, command, width=28):
        return tk.Button(parent, text=text, command=command, bg=PRIMARY, fg="white",
                         activebackground=PRIMARY_DARK, activeforeground="white",
                         font=("Segoe UI", 11, "bold"), relief="flat", padx=14,
                         pady=12, width=width, cursor="hand2", bd=0)

    def ghost_button(self, parent, text, command, width=24):
        return tk.Button(parent, text=text, command=command, bg=PRIMARY_LIGHT, fg=PRIMARY,
                         activebackground="#E0E7FF", activeforeground=PRIMARY,
                         font=("Segoe UI", 10, "bold"), relief="flat", padx=12,
                         pady=10, width=width, cursor="hand2", bd=0)

    def danger_button(self, parent, text, command, width=20):
        return tk.Button(parent, text=text, command=command, bg="#FEE2E2", fg=DANGER,
                         activebackground="#FECACA", activeforeground=DANGER,
                         font=("Segoe UI", 10, "bold"), relief="flat", padx=12,
                         pady=10, width=width, cursor="hand2", bd=0)

    def card(self, parent, padx=24, pady=20):
        return tk.Frame(parent, bg=CARD, padx=padx, pady=pady,
                        highlightbackground=BORDER, highlightthickness=1)

    def section_title(self, parent, title, subtitle=None):
        tk.Label(parent, text=title, bg=parent["bg"], fg=TEXT,
                 font=("Segoe UI", 17, "bold")).pack(anchor="w")
        if subtitle:
            tk.Label(parent, text=subtitle, bg=parent["bg"], fg=SUBTEXT,
                     font=("Segoe UI", 10)).pack(anchor="w", pady=(2, 14))

    def action_card(self, parent, title, subtitle, command, accent=PRIMARY, icon="•", button_text="Open"):
        box = tk.Frame(parent, bg=CARD, padx=20, pady=18,
                       highlightbackground=BORDER, highlightthickness=1)

        icon_box = tk.Frame(box, bg=accent, width=54, height=54)
        icon_box.pack(side="left", padx=(0, 16), anchor="n")
        icon_box.pack_propagate(False)
        tk.Label(icon_box, text=icon, bg=accent, fg="white",
                 font=("Segoe UI", 21, "bold")).pack(expand=True)

        text_area = tk.Frame(box, bg=CARD)
        text_area.pack(side="left", fill="both", expand=True)

        tk.Label(text_area, text=title, bg=CARD, fg=accent,
                 font=("Segoe UI", 12, "bold"),
                 wraplength=310, justify="left").pack(anchor="w")

        tk.Label(text_area, text=subtitle, bg=CARD, fg=SUBTEXT,
                 font=("Segoe UI", 9),
                 wraplength=310, justify="left").pack(anchor="w", pady=(6, 14))

        tk.Button(text_area, text=f"{button_text}  ›", command=command, bg=accent, fg="white",
                  activebackground=accent, activeforeground="white",
                  font=("Segoe UI", 10, "bold"), relief="flat",
                  padx=16, pady=7, cursor="hand2", bd=0).pack(anchor="w")

        return box

    def sidebar_layout(self, title, items):
        self.clear()
        shell = tk.Frame(self, bg=BG)
        shell.pack(fill="both", expand=True)

        side = tk.Frame(shell, bg=SIDEBAR, width=250)
        side.pack(side="left", fill="y")
        side.pack_propagate(False)

        brand = tk.Frame(side, bg=SIDEBAR)
        brand.pack(fill="x", padx=18, pady=(28, 28))

        logo = tk.Frame(brand, bg="#7C3AED", width=52, height=52)
        logo.pack(side="left")
        logo.pack_propagate(False)
        tk.Label(logo, text="✦", bg="#7C3AED", fg="white",
                 font=("Segoe UI", 22, "bold")).pack(expand=True)

        brand_text = tk.Frame(brand, bg=SIDEBAR)
        brand_text.pack(side="left", padx=13)
        tk.Label(brand_text, text="Service Hub", bg=SIDEBAR, fg="white",
                 font=("Segoe UI", 18, "bold")).pack(anchor="w")
        tk.Label(brand_text, text="Management System", bg=SIDEBAR, fg="#C4B5FD",
                 font=("Segoe UI", 9)).pack(anchor="w")

        for label, command in items:
            is_logout = "Logout" in label
            fg = "#FDA4AF" if is_logout else SIDEBAR_TEXT
            active = "#7F1D1D" if is_logout else SIDEBAR_ACTIVE
            tk.Button(side, text=label, command=command, anchor="w",
                      bg=SIDEBAR, fg=fg,
                      activebackground=active, activeforeground="white",
                      font=("Segoe UI", 11, "bold"), relief="flat",
                      padx=22, pady=14, cursor="hand2", bd=0).pack(fill="x", padx=12, pady=4)

        decoration = tk.Frame(side, bg=SIDEBAR)
        decoration.pack(side="bottom", fill="x", padx=22, pady=26)
        tk.Label(decoration, text="● ● ●", bg=SIDEBAR, fg="#A78BFA",
                 font=("Segoe UI", 16, "bold")).pack(anchor="w")
        tk.Label(decoration, text="Stage E GUI", bg=SIDEBAR, fg="#C4B5FD",
                 font=("Segoe UI", 9)).pack(anchor="w", pady=(6, 0))

        content = tk.Frame(shell, bg=BG)
        content.pack(side="left", fill="both", expand=True)
        self.topbar_in(content, title)
        body = tk.Frame(content, bg=BG, padx=30, pady=26)
        body.pack(fill="both", expand=True)
        return body

    def topbar_in(self, parent, title):
        bar = tk.Frame(parent, bg=CARD, height=78, highlightbackground=BORDER, highlightthickness=1)
        bar.pack(fill="x")
        bar.pack_propagate(False)

        left = tk.Frame(bar, bg=CARD)
        left.pack(side="left", padx=28)
        tk.Label(left, text=title, bg=CARD, fg=TEXT,
                 font=("Segoe UI", 22, "bold")).pack(anchor="w")
        tk.Label(left, text="Overview & System Management", bg=CARD, fg=SUBTEXT,
                 font=("Segoe UI", 9)).pack(anchor="w", pady=(2, 0))

        user_name = self.current_user.get("ename", "Guest") if self.current_user else "Guest"
        right = tk.Frame(bar, bg=CARD)
        right.pack(side="right", padx=24)

        tk.Label(right, text="● Online", bg=CARD, fg=SUCCESS,
                 font=("Segoe UI", 10, "bold")).pack(side="left", padx=(0, 18))

        initials = "".join([part[0].upper() for part in user_name.split()[:2]]) or "U"
        avatar = tk.Frame(right, bg=PRIMARY, width=38, height=38)
        avatar.pack(side="left", padx=(0, 10))
        avatar.pack_propagate(False)
        tk.Label(avatar, text=initials, bg=PRIMARY, fg="white",
                 font=("Segoe UI", 11, "bold")).pack(expand=True)

        user_box = tk.Frame(right, bg=CARD)
        user_box.pack(side="left")
        tk.Label(user_box, text=user_name, bg=CARD, fg=TEXT,
                 font=("Segoe UI", 10, "bold")).pack(anchor="w")
        tk.Label(user_box, text=self.current_user.get("role", "user").title() if self.current_user else "User",
                 bg=CARD, fg=SUBTEXT, font=("Segoe UI", 9)).pack(anchor="w")

    def show_login(self):
        self.clear()
        self.configure(bg=BG)

        wrapper = tk.Frame(self, bg=BG)
        wrapper.pack(fill="both", expand=True)

        left = tk.Frame(wrapper, bg=SIDEBAR, width=470)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        tk.Label(left, text="Service Hub", bg=SIDEBAR, fg="white",
                 font=("Segoe UI", 34, "bold")).pack(anchor="w", padx=48, pady=(90, 8))
        tk.Label(left, text="A smart customer service\nmanagement system.",
                 bg=SIDEBAR, fg="#C4B5FD", font=("Segoe UI", 16),
                 justify="left").pack(anchor="w", padx=50, pady=(4, 40))

        for line in ["✓ Manage requests", "✓ Track products and transactions", "✓ Run manager reports"]:
            tk.Label(left, text=line, bg=SIDEBAR, fg="white",
                     font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=54, pady=8)

        right = tk.Frame(wrapper, bg=BG)
        right.pack(side="left", fill="both", expand=True)

        card = tk.Frame(right, bg=CARD, padx=48, pady=44,
                        highlightbackground=BORDER, highlightthickness=1)
        card.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(card, text="Welcome back", bg=CARD, fg=TEXT,
                 font=("Segoe UI", 28, "bold")).pack(anchor="w", pady=(0, 5))
        tk.Label(card, text="Sign in with your employee details", bg=CARD, fg=SUBTEXT,
                 font=("Segoe UI", 12)).pack(anchor="w", pady=(0, 28))

        tk.Label(card, text="Employee ID", bg=CARD, fg=TEXT,
                 font=("Segoe UI", 10, "bold")).pack(anchor="w")
        eid_entry = tk.Entry(card, font=("Segoe UI", 13), width=34, relief="flat",
                             bg="#F8FAFC", fg=TEXT, highlightbackground=BORDER, highlightthickness=1)
        eid_entry.pack(pady=(7, 16), ipady=10)

        tk.Label(card, text="Password", bg=CARD, fg=TEXT,
                 font=("Segoe UI", 10, "bold")).pack(anchor="w")
        pass_entry = tk.Entry(card, show="*", font=("Segoe UI", 13), width=34,
                              relief="flat", bg="#F8FAFC", fg=TEXT,
                              highlightbackground=BORDER, highlightthickness=1)
        pass_entry.pack(pady=(7, 24), ipady=10)

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

        self.button(card, "Sign in", login, width=30).pack(fill="x")
        tk.Label(card, text="Default password after setup: 1234", bg=CARD, fg="#94A3B8",
                 font=("Segoe UI", 9)).pack(pady=(18, 0))

    def show_manager_dashboard(self):
        body = self.sidebar_layout("Manager Dashboard", [
            ("🏠  Dashboard", self.show_manager_dashboard),
            ("🖥  Employee Screens", self.show_employee_dashboard),
            ("🚪  Logout", self.show_login),
        ])

        revenue = self.get_year_revenue()

        hero = tk.Frame(body, bg="#F5F3FF", padx=30, pady=24,
                        highlightbackground="#DDD6FE", highlightthickness=1)
        hero.pack(fill="x", pady=(0, 22))

        hero_left = tk.Frame(hero, bg="#F5F3FF")
        hero_left.pack(side="left", fill="both", expand=True)

        money = tk.Frame(hero_left, bg=PRIMARY, width=72, height=72)
        money.pack(side="left", padx=(0, 24))
        money.pack_propagate(False)
        tk.Label(money, text="$", bg=PRIMARY, fg="white",
                 font=("Segoe UI", 34, "bold")).pack(expand=True)

        text_box = tk.Frame(hero_left, bg="#F5F3FF")
        text_box.pack(side="left", fill="both", expand=True)
        tk.Label(text_box, text="Revenue This Year", bg="#F5F3FF", fg=PRIMARY,
                 font=("Segoe UI", 15, "bold")).pack(anchor="w")
        tk.Label(text_box, text=f"${revenue:,.2f}", bg="#F5F3FF", fg=TEXT,
                 font=("Segoe UI", 34, "bold")).pack(anchor="w", pady=(4, 0))
        tk.Label(text_box, text="Manager-only financial overview", bg="#F5F3FF", fg=SUBTEXT,
                 font=("Segoe UI", 10)).pack(anchor="w", pady=(2, 0))

        chart = tk.Frame(hero, bg="#F5F3FF")
        chart.pack(side="right", padx=18)
        tk.Label(chart, text="📈", bg="#F5F3FF", fg=SUCCESS,
                 font=("Segoe UI", 48, "bold")).pack()
        tk.Label(chart, text="Live reports", bg="#F5F3FF", fg=SUBTEXT,
                 font=("Segoe UI", 9, "bold")).pack()

        self.section_title(body, "Quick Access", "Run reports, view data and manage the system")

        grid = tk.Frame(body, bg=BG)
        grid.pack(fill="x", pady=(6, 0))

        cards = [
            ("Open Requests Over 30 Days", "View all requests that have been open for more than 30 days.", self.show_old_open_requests_query, INFO, "📋", "View Report"),
            ("Product Sales & Revenue", "See total sales count and revenue for each product.", self.show_product_sales_query, SUCCESS, "📊", "View Report"),
            ("Customer Total Spending", "View total amount spent by each customer.", self.show_customer_spending_query, ORANGE, "👥", "View Report"),
            ("Employees Table", "View all employees and workload information.", self.show_employees_table, PURPLE, "👤", "Open"),
            ("Run Workload Balance", "Distribute requests evenly among employees.", self.run_workload_balance, TEAL, "⚖", "Run Process"),
            ("Run Supply & Demand", "Run full supply and demand analysis.", self.run_supply_demand, PINK, "🛒", "Run Process"),
            ("Discount Products", "Apply discounts to products based on rules.", self.show_discount_screen, WARNING, "%", "Open"),
        ]

        for i, (title, sub, cmd, color, icon, btn_text) in enumerate(cards):
            c = self.action_card(grid, title, sub, cmd, accent=color, icon=icon, button_text=btn_text)
            c.grid(row=i // 2, column=i % 2, sticky="nsew", padx=10, pady=10)

        for col in range(2):
            grid.columnconfigure(col, weight=1)

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
        back_items = [("🏠  Manager Dashboard", self.show_manager_dashboard)] if self.current_user and self.current_user.get("role") == "manager" else [("🏠  Dashboard", self.show_employee_dashboard)]
        body = self.sidebar_layout("Employee Dashboard", [
            *back_items,
            ("🚪  Logout", self.show_login),
        ])

        welcome = tk.Frame(body, bg="#EEF2FF", padx=30, pady=24,
                           highlightbackground="#C7D2FE", highlightthickness=1)
        welcome.pack(fill="x", pady=(0, 24))

        tk.Label(welcome, text=f"Welcome, {self.current_user.get('ename', '')}", bg="#EEF2FF", fg=PRIMARY,
                 font=("Segoe UI", 28, "bold")).pack(anchor="w")
        tk.Label(welcome, text="Choose a workspace to manage daily customer service operations.",
                 bg="#EEF2FF", fg=SUBTEXT, font=("Segoe UI", 11)).pack(anchor="w", pady=(6, 0))

        self.section_title(body, "Workspaces", "CRUD screens for employees")

        grid = tk.Frame(body, bg=BG)
        grid.pack(fill="x", pady=(6, 0))

        actions = [
            ("Customers", "View, search, add and update customers.", lambda: self.show_crud_table("customers"), ORANGE, "👥"),
            ("Requests", "Manage your assigned service requests.", self.show_requests_screen, INFO, "📋"),
            ("Transactions", "View your transactions with friendly names.", self.show_transactions_screen, SUCCESS, "💳"),
            ("Products", "Manage active products and inventory.", lambda: self.show_crud_table("products"), PURPLE, "📦"),
        ]

        for i, (title, sub, cmd, color, icon) in enumerate(actions):
            c = self.action_card(grid, title, sub, cmd, accent=color, icon=icon)
            c.grid(row=i // 2, column=i % 2, sticky="nsew", padx=10, pady=10)
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)

    def table_view(self, title, columns, rows, back_command, row_actions=None):
        self.clear()
        self.topbar(title, back_command)
        frame = tk.Frame(self, bg=BG, padx=28, pady=24)
        frame.pack(fill="both", expand=True)

        table_card = self.card(frame, padx=18, pady=18)
        table_card.pack(fill="both", expand=True)

        tk.Label(table_card, text=f"{len(rows)} records", bg=CARD, fg=SUBTEXT,
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 10))

        table_frame = tk.Frame(table_card, bg=CARD)
        table_frame.pack(fill="both", expand=True)

        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=18)
        y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        x_scroll = ttk.Scrollbar(table_card, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

        for col in columns:
            tree.heading(col, text=col.replace("_", " ").title())
            tree.column(col, width=155, anchor="w")

        tree.pack(side="left", fill="both", expand=True)
        y_scroll.pack(side="right", fill="y")
        x_scroll.pack(fill="x")

        for i, row in enumerate(rows):
            values = [row.get(c) for c in columns]
            tree.insert("", "end", values=values, tags=("even" if i % 2 == 0 else "odd",))
        tree.tag_configure("even", background="#FFFFFF")
        tree.tag_configure("odd", background="#F8FAFC")

        if row_actions:
            actions_frame = tk.Frame(frame, bg=BG)
            actions_frame.pack(fill="x", pady=14)
            for text, callback in row_actions:
                self.ghost_button(actions_frame, text, lambda cb=callback, tr=tree: cb(tr)).pack(side="left", padx=8)

    def show_crud_table(self, table_name):
        self.clear()
        self.topbar(table_name.title(), self.show_employee_dashboard)

        frame = tk.Frame(self, bg=BG, padx=28, pady=24)
        frame.pack(fill="both", expand=True)

        toolbar = self.card(frame, padx=18, pady=16)
        toolbar.pack(fill="x", pady=(0, 16))

        search_var = tk.StringVar()
        tk.Label(toolbar, text="Search", bg=CARD, fg=TEXT,
                 font=("Segoe UI", 10, "bold")).pack(side="left", padx=(0, 8))
        search_entry = tk.Entry(toolbar, textvariable=search_var, font=("Segoe UI", 11),
                                width=42, relief="flat", bg="#F8FAFC", fg=TEXT,
                                highlightbackground=BORDER, highlightthickness=1)
        search_entry.pack(side="left", ipady=8)

        self.ghost_button(toolbar, "Search / Refresh", lambda: load(), width=18).pack(side="left", padx=10)
        self.button(toolbar, f"Add {table_name[:-1].title()}", lambda: self.open_form(table_name), width=18).pack(side="right")

        table_card = self.card(frame, padx=18, pady=18)
        table_card.pack(fill="both", expand=True)

        columns = self.get_display_columns(table_name)

        table_frame = tk.Frame(table_card, bg=CARD)
        table_frame.pack(fill="both", expand=True)

        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=18)
        y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        x_scroll = ttk.Scrollbar(table_card, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

        for col in columns:
            tree.heading(col, text=col.replace("_", " ").title())
            tree.column(col, width=145, anchor="w")
        tree.pack(side="left", fill="both", expand=True)
        y_scroll.pack(side="right", fill="y")
        x_scroll.pack(fill="x")

        actions = tk.Frame(frame, bg=BG)
        actions.pack(fill="x", pady=12)

        def selected_pk():
            item = tree.focus()
            if not item:
                messagebox.showwarning("No selection", "Please select a row first.")
                return None
            values = tree.item(item, "values")
            return values[0]

        self.ghost_button(actions, "Edit Selected", lambda: self.open_form(table_name, selected_pk()), width=18).pack(side="left", padx=6)
        self.danger_button(actions, "Delete Selected", lambda: self.safe_delete(table_name, selected_pk(), load), width=18).pack(side="left", padx=6)

        def load():
            for x in tree.get_children():
                tree.delete(x)
            try:
                rows = self.get_table_rows(table_name, search_var.get().strip())
                for i, row in enumerate(rows):
                    tree.insert("", "end", values=[row.get(c) for c in columns], tags=("even" if i % 2 == 0 else "odd",))
                tree.tag_configure("even", background="#FFFFFF")
                tree.tag_configure("odd", background="#F8FAFC")
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
            tk.Label(win, text=col, bg=BG, fg=TEXT, font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=22, pady=(10, 2))
            ent = tk.Entry(win, font=("Segoe UI", 11), width=44)
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
        self.danger_button(action, "Delete Selected", lambda: self.delete_request(selected(), load), width=18).pack(side="left", padx=6)
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
            tk.Label(win, text=label, bg=BG, fg=TEXT, font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=22, pady=(10, 2))
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

        tk.Label(win, text="Subject / note", bg=BG, fg=TEXT, font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=22, pady=(10, 2))
        subject = tk.Entry(win, font=("Segoe UI", 11), width=44)
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

        tk.Label(control, text="Discount percent:", bg=BG, font=("Segoe UI", 11, "bold")).pack(side="left")
        percent_entry = tk.Entry(control, width=10, font=("Segoe UI", 11))
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
