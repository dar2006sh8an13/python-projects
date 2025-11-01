import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json, os, hashlib
from datetime import datetime, timedelta
from collections import defaultdict

# -------------------------
# Helpers: file I/O & hashing
# -------------------------
def load_json(filename, default):
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return default
    return default

def save_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def hash_password(username, password):
    # simple salted hash using username as salt
    if password is None:
        return None
    salted = (username + password).encode('utf-8')
    return hashlib.sha256(salted).hexdigest()

# -------------------------
# App: single-file structure
# -------------------------
USERS_FILE = "users_credentials.json"

ROLE_CATEGORIES = {
    "Student": ["Food", "Transport", "Books", "Stationery", "Snacks", "Other"],
    "Working Professional": ["Food", "Transport", "Rent", "Bills", "Entertainment", "Groceries", "Other"],
    "Unemployed": ["Food", "Transport", "Healthcare", "Job Search", "Other"],
    "Older Human": ["Healthcare", "Medicines", "Groceries", "Utilities", "Other"]
}

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker — Complete (Tkinter)")
        self.root.geometry("950x620")
        self.root.config(bg="#f4f6fb")
        self.current_user = None
        self.current_role = None
        self.expenses = []  # in-memory list of dicts for current user

        # Ensure users file exists
        if not os.path.exists(USERS_FILE):
            save_json(USERS_FILE, {})

        self.show_login_screen()

    # -------------------
    # LOGIN / SIGNUP UI
    # -------------------
    def show_login_screen(self):
        self.clear_root()
        frame = tk.Frame(self.root, bg="#f4f6fb")
        frame.pack(pady=40)

        tk.Label(frame, text="Expense Tracker", font=("Helvetica", 22, "bold"), bg="#f4f6fb").grid(row=0, column=0, columnspan=3, pady=10)
        tk.Label(frame, text="Login", font=("Helvetica", 16), bg="#f4f6fb").grid(row=1, column=0, columnspan=3, pady=(0,10))

        tk.Label(frame, text="Username:", bg="#f4f6fb").grid(row=2, column=0, sticky="e", padx=6, pady=6)
        username_entry = tk.Entry(frame, width=28)
        username_entry.grid(row=2, column=1, pady=6, columnspan=2)
        username_entry.focus()

        tk.Label(frame, text="Password:", bg="#f4f6fb").grid(row=3, column=0, sticky="e", padx=6, pady=6)
        password_entry = tk.Entry(frame, width=28, show="*")
        password_entry.grid(row=3, column=1, pady=6, columnspan=2)

        def do_login():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            if not username or not password:
                messagebox.showwarning("Input required", "Please enter both username and password.")
                return
            users = load_json(USERS_FILE, {})
            if username in users and users[username]["password_hash"] == hash_password(username, password):
                self.current_user = username
                self.current_role = users[username]["role"]
                self.load_user_data()
                messagebox.showinfo("Login Successful", f"Welcome back, {users[username]['full_name']}!")
                self.show_dashboard()
            else:
                messagebox.showerror("Login Failed", "Invalid username or password. If you're new, please Sign Up.")

        tk.Button(frame, text="Login", bg="#007BFF", fg="white", width=12, command=do_login).grid(row=4, column=1, pady=12, sticky="e")
        tk.Button(frame, text="Sign Up", bg="#28A745", fg="white", width=12, command=self.show_signup_screen).grid(row=4, column=2, pady=12, sticky="w")
        tk.Button(frame, text="Exit", bg="#6c757d", fg="white", width=8, command=self.root.quit).grid(row=4, column=0, pady=12, sticky="w")

    def show_signup_screen(self):
        self.clear_root()
        frame = tk.Frame(self.root, bg="#f4f6fb")
        frame.pack(pady=10)

        tk.Label(frame, text="Create Account", font=("Helvetica", 20, "bold"), bg="#f4f6fb").grid(row=0, column=0, columnspan=3, pady=10)

        labels = ["Full Name:", "Phone:", "Email:", "Username:", "Password:", "Role:"]
        entries = {}

        for i, lab in enumerate(labels, start=1):
            tk.Label(frame, text=lab, bg="#f4f6fb").grid(row=i, column=0, sticky="e", padx=6, pady=6)
            if lab == "Role:":
                var = tk.StringVar()
                var.set("Student")
                combo = ttk.Combobox(frame, textvariable=var, values=list(ROLE_CATEGORIES.keys()), state="readonly", width=25)
                combo.grid(row=i, column=1, pady=6, columnspan=2)
                entries["role"] = var
            elif lab == "Password:":
                ent = tk.Entry(frame, show="*", width=28)
                ent.grid(row=i, column=1, pady=6, columnspan=2)
                entries["password"] = ent
            else:
                ent = tk.Entry(frame, width=28)
                ent.grid(row=i, column=1, pady=6, columnspan=2)
                key = lab.replace(" ", "_").replace(":", "").lower()
                entries[key] = ent

        def do_signup():
            full_name = entries["full_name"].get().strip()
            phone = entries["phone"].get().strip()
            email = entries["email"].get().strip()
            username = entries["username"].get().strip()
            password = entries["password"].get().strip()
            role = entries["role"].get()

            if not all([full_name, phone, email, username, password, role]):
                messagebox.showwarning("Missing data", "Please fill all fields.")
                return
            if len(password) < 6:
                messagebox.showwarning("Weak password", "Password must be at least 6 characters.")
                return

            users = load_json(USERS_FILE, {})
            if username in users:
                messagebox.showerror("Username taken", "That username already exists. Choose another.")
                return

            users[username] = {
                "full_name": full_name,
                "phone": phone,
                "email": email,
                "role": role,
                "password_hash": hash_password(username, password)
            }
            save_json(USERS_FILE, users)
            # create user's expense file
            user_file = f"{username}_expenses.json"
            if not os.path.exists(user_file):
                save_json(user_file, [])
            messagebox.showinfo("Account created", "Signup successful! You can now log in.")
            self.show_login_screen()

        tk.Button(frame, text="Create Account", bg="#28A745", fg="white", width=16, command=do_signup).grid(row=8, column=1, pady=12)
        tk.Button(frame, text="Back to Login", bg="#6c757d", fg="white", width=12, command=self.show_login_screen).grid(row=8, column=2, pady=12)

    # -------------------
    # Dashboard (role-based)
    # -------------------
    def show_dashboard(self):
        self.clear_root()
        users = load_json(USERS_FILE, {})
        user_info = users.get(self.current_user, {})
        title = f"{user_info.get('full_name','User')} — {self.current_user} ({user_info.get('role','')})"
        tk.Label(self.root, text="Expense Tracker Dashboard", font=("Helvetica", 20, "bold"), bg="#007BFF", fg="white").pack(fill="x")
        tk.Label(self.root, text=title, font=("Helvetica", 12), bg="#f4f6fb").pack(fill="x")

        top_frame = tk.Frame(self.root, bg="#f4f6fb")
        top_frame.pack(fill="x", pady=6, padx=6)

        tk.Button(top_frame, text="➕ Add Expense", bg="#28A745", fg="white", width=14, command=self.add_expense_popup).pack(side="left", padx=6)
        tk.Button(top_frame, text="✏️ Edit Selected", bg="#ffc107", fg="black", width=14, command=self.edit_selected).pack(side="left", padx=6)
        tk.Button(top_frame, text="🗑️ Delete Selected", bg="#dc3545", fg="white", width=14, command=self.delete_selected).pack(side="left", padx=6)
        tk.Button(top_frame, text="🔄 Refresh", bg="#007BFF", fg="white", width=12, command=self.refresh_expenses).pack(side="left", padx=6)
        tk.Button(top_frame, text="📊 Summary", bg="#17a2b8", fg="white", width=12, command=self.show_summary_popup).pack(side="left", padx=6)
        tk.Button(top_frame, text="🚪 Logout", bg="#6c757d", fg="white", width=10, command=self.logout).pack(side="right", padx=6)

        # Treeview for expenses
        cols = ("Date", "Category", "Amount", "Note")
        self.tree = ttk.Treeview(self.root, columns=cols, show="headings", height=18)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # bottom info
        self.status_var = tk.StringVar()
        tk.Label(self.root, textvariable=self.status_var, bg="#f4f6fb", font=("Helvetica", 12, "bold")).pack(pady=4)

        self.refresh_expenses()

    # -------------------
    # Data load/save
    # -------------------
    def load_user_data(self):
        self.expenses = load_json(f"{self.current_user}_expenses.json", [])
        # ensure dates parsed? we store as strings; keep as dicts

    def save_user_data(self):
        save_json(f"{self.current_user}_expenses.json", self.expenses)

    # -------------------
    # Add / Edit / Delete
    # -------------------
    def add_expense_popup(self):
        users = load_json(USERS_FILE, {})
        role = users.get(self.current_user, {}).get("role", "Student")
        categories = ROLE_CATEGORIES.get(role, ["Other"])

        popup = tk.Toplevel(self.root)
        popup.title("Add Expense")
        popup.geometry("380x380")
        popup.config(bg="#f4f6fb")

        tk.Label(popup, text=f"Add Expense — {role}", font=("Helvetica", 14, "bold"), bg="#f4f6fb").pack(pady=6)

        tk.Label(popup, text="Category:", bg="#f4f6fb").pack(pady=4)
        cat_var = tk.StringVar()
        cat_combo = ttk.Combobox(popup, textvariable=cat_var, values=categories + ["Other"], state="readonly", width=30)
        cat_combo.pack()
        cat_combo.set(categories[0])

        tk.Label(popup, text="Amount (₹):", bg="#f4f6fb").pack(pady=4)
        amount_entry = tk.Entry(popup, width=30)
        amount_entry.pack()

        tk.Label(popup, text="Note (optional):", bg="#f4f6fb").pack(pady=4)
        note_entry = tk.Entry(popup, width=30)
        note_entry.pack()

        def save():
            cat = cat_var.get().strip() or "Other"
            amt = amount_entry.get().strip()
            note = note_entry.get().strip()
            if not amt:
                messagebox.showwarning("Required", "Please enter amount.")
                return
            try:
                amount = float(amt)
                if amount <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showwarning("Invalid", "Please enter a valid positive number for amount.")
                return
            entry = {
                "date": datetime.now().strftime(DATE_FORMAT),
                "category": cat,
                "amount": amount,
                "note": note
            }
            self.expenses.append(entry)
            self.save_user_data()
            messagebox.showinfo("Saved", "Expense added.")
            popup.destroy()
            self.refresh_expenses()

        tk.Button(popup, text="Save Expense", bg="#28A745", fg="white", width=15, command=save).pack(pady=10)
        tk.Button(popup, text="Cancel", bg="#6c757d", fg="white", width=10, command=popup.destroy).pack()

    def edit_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Select", "Please select an expense row to edit.")
            return
        idx = self.tree.index(sel[0])
        original = self.expenses[idx]

        popup = tk.Toplevel(self.root)
        popup.title("Edit Expense")
        popup.geometry("380x380")
        popup.config(bg="#f4f6fb")

        tk.Label(popup, text="Edit Expense", font=("Helvetica", 14, "bold"), bg="#f4f6fb").pack(pady=6)

        tk.Label(popup, text="Category:", bg="#f4f6fb").pack(pady=4)
        cat_entry = tk.Entry(popup, width=30)
        cat_entry.pack()
        cat_entry.insert(0, original.get("category",""))

        tk.Label(popup, text="Amount (₹):", bg="#f4f6fb").pack(pady=4)
        amount_entry = tk.Entry(popup, width=30)
        amount_entry.pack()
        amount_entry.insert(0, str(original.get("amount","")))

        tk.Label(popup, text="Note:", bg="#f4f6fb").pack(pady=4)
        note_entry = tk.Entry(popup, width=30)
        note_entry.pack()
        note_entry.insert(0, original.get("note",""))

        def save_edit():
            cat = cat_entry.get().strip() or "Other"
            amt = amount_entry.get().strip()
            note = note_entry.get().strip()
            try:
                amount = float(amt)
                if amount <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showwarning("Invalid", "Enter a valid amount.")
                return
            # update
            original["category"] = cat
            original["amount"] = amount
            original["note"] = note
            self.save_user_data()
            messagebox.showinfo("Updated", "Expense updated.")
            popup.destroy()
            self.refresh_expenses()

        tk.Button(popup, text="Save Changes", bg="#007BFF", fg="white", width=15, command=save_edit).pack(pady=10)
        tk.Button(popup, text="Cancel", bg="#6c757d", fg="white", width=10, command=popup.destroy).pack()

    def delete_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Select", "Please select an expense to delete.")
            return
        idx = self.tree.index(sel[0])
        confirm = messagebox.askyesno("Confirm", "Delete selected expense permanently?")
        if not confirm:
            return
        self.expenses.pop(idx)
        self.save_user_data()
        self.refresh_expenses()
        messagebox.showinfo("Deleted", "Expense removed.")

    # -------------------
    # Refresh and status
    # -------------------
    def refresh_expenses(self):
        # reload from file in case externally changed
        self.load_user_data()
        for i in self.tree.get_children():
            self.tree.delete(i)
        total = 0.0
        for e in self.expenses:
            self.tree.insert("", "end", values=(e["date"], e["category"], f"{e['amount']:.2f}", e.get("note","")))
            total += float(e["amount"])
        self.status_var.set(f"Total expenses: ₹{total:.2f} — Entries: {len(self.expenses)}")

    # -------------------
    # Summary computations
    # -------------------
    def show_summary_popup(self):
        if not self.expenses:
            messagebox.showinfo("No Data", "No expenses to summarize.")
            return
        popup = tk.Toplevel(self.root)
        popup.title("Expense Summary")
        popup.geometry("500x500")
        popup.config(bg="#f4f6fb")

        tk.Label(popup, text="Choose Summary", font=("Helvetica", 14, "bold"), bg="#f4f6fb").pack(pady=6)

        # buttons for daily/weekly/monthly/yearly
        btn_frame = tk.Frame(popup, bg="#f4f6fb")
        btn_frame.pack(pady=8)
        tk.Button(btn_frame, text="Daily", width=10, command=lambda: self.show_summary("daily", popup)).pack(side="left", padx=6)
        tk.Button(btn_frame, text="Weekly", width=10, command=lambda: self.show_summary("weekly", popup)).pack(side="left", padx=6)
        tk.Button(btn_frame, text="Monthly", width=10, command=lambda: self.show_summary("monthly", popup)).pack(side="left", padx=6)
        tk.Button(btn_frame, text="Yearly", width=10, command=lambda: self.show_summary("yearly", popup)).pack(side="left", padx=6)

        # container for results
        self.summary_text = tk.Text(popup, height=20, width=60)
        self.summary_text.pack(pady=8)
        self.summary_text.insert(tk.END, "Click a period button to load summary...")
        self.summary_text.configure(state="disabled")

    def show_summary(self, period, popup_window=None):
        # compute totals grouped by date / category depending on period
        # parse dates
        entries = []
        for e in self.expenses:
            try:
                dt = datetime.strptime(e["date"], DATE_FORMAT)
            except Exception:
                # if older format, try fallback
                dt = datetime.now()
            entries.append({"dt": dt, "category": e["category"], "amount": float(e["amount"])})

        now = datetime.now()
        group = defaultdict(float)  # grouping label -> total
        category_group = defaultdict(float)

        if period == "daily":
            # group by date (YYYY-MM-DD)
            for it in entries:
                if it["dt"].date() == now.date():
                    label = it["dt"].strftime("%Y-%m-%d")
                    group[label] += it["amount"]
                    category_group[it["category"]] += it["amount"]
        elif period == "weekly":
            # this week (Mon-Sun)
            start_week = now - timedelta(days=now.weekday())  # Monday
            for it in entries:
                if it["dt"].date() >= start_week.date():
                    label = it["dt"].strftime("%Y-%m-%d")
                    group[label] += it["amount"]
                    category_group[it["category"]] += it["amount"]
        elif period == "monthly":
            for it in entries:
                if it["dt"].year == now.year and it["dt"].month == now.month:
                    label = it["dt"].strftime("%Y-%m-%d")
                    group[label] += it["amount"]
                    category_group[it["category"]] += it["amount"]
        elif period == "yearly":
            for it in entries:
                if it["dt"].year == now.year:
                    label = it["dt"].strftime("%Y-%m-%d")
                    group[label] += it["amount"]
                    category_group[it["category"]] += it["amount"]
        else:
            messagebox.showerror("Error", "Unknown period.")
            return

        # prepare text
        total = sum(group.values())
        text_lines = [f"Summary ({period.title()})", "-"*40, f"Total: ₹{total:.2f}\n"]
        if not group:
            text_lines.append("No entries found in this period.")
        else:
            text_lines.append("By Date:")
            # order by date
            for k in sorted(group.keys()):
                text_lines.append(f"  {k}: ₹{group[k]:.2f}")
            text_lines.append("\nBy Category:")
            # sort categories by amount desc
            for cat, amt in sorted(category_group.items(), key=lambda x: -x[1]):
                text_lines.append(f"  {cat}: ₹{amt:.2f}")

        # show into popup's text widget
        if hasattr(self, 'summary_text'):
            self.summary_text.configure(state="normal")
            self.summary_text.delete(1.0, tk.END)
            self.summary_text.insert(tk.END, "\n".join(text_lines))
            self.summary_text.configure(state="disabled")

    # -------------------
    # Logout / clear
    # -------------------
    def logout(self):
        confirm = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if confirm:
            self.current_user = None
            self.current_role = None
            self.expenses = []
            self.show_login_screen()

    def clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# -------------------
# Run the app
# -------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()
