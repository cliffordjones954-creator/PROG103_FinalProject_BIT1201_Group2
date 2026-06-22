"""
AuraClinic — Main Application
Pages: Register Patient · Book Appointment · Appointment Records · Search Patient
Launched by login_page.py as: RegisterPatientApp(master, username=...)

Place this file (and the "Logo and icons" folder) in the same directory as login_page.py.
Requires: pip install Pillow
"""

from pydoc import doc
import tkinter as tk
from tkinter import ttk, messagebox
import os, datetime, csv

try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except Exception:
    HAS_PIL = False

# ── Palette ────────────────────────────────────────────────────────────────────
TEAL        = "#1787AE"
BTN_BLUE    = "#5BBFDE"
BTN_HOVER   = "#3aa8cc"
WHITE       = "#FFFFFF"
SIDEBAR_BG  = "#eaf4f9"
CONTENT_BG  = "#f4f8fb"
TEXT_DARK   = "#1a2e44"
TEXT_MID    = "#4a6070"
INPUT_BG    = "#FFFFFF"
INPUT_BD    = "#D0DCE8"
ROW_ALT     = "#f0f7fb"
DEL_RED     = "#e74c3c"
DEL_HOVER   = "#c0392b"
UPD_BLUE    = "#5BBFDE"
SAVE_DARK   = "#1e3a5f"
CANCEL_RED  = "#e74c3c"
COMPLETE_GR = "#27ae60"
EDIT_ORANGE = "#e67e22"
TEAL_DARK   = "#0f6080"

HEADER_H   = 100
SIDEBAR_W  = 210

# ── Shared In-Memory Data ──────────────────────────────────────────────────────
PATIENTS = [
    {"id":"P1001","name":"John K. Koroma",  "age":28,"gender":"Male",  "phone":"076-123456","blood":"O+", "reg_date":"2025-05-29","email":"johnkoroma@email.com",    "address":"12 King Street, Freetown","condition":"None"},
    {"id":"P1002","name":"Mariama Bangura", "age":34,"gender":"Female","phone":"077-234567","blood":"A+", "reg_date":"2025-05-28","email":"mariama.bang@gmail.com",  "address":"45 Wilkinson Road",       "condition":"Hypertension"},
    {"id":"P1003","name":"Alhaji Kamara",   "age":45,"gender":"Male",  "phone":"078-345678","blood":"B+", "reg_date":"2025-05-27","email":"alhaji.kamara@gmail.com", "address":"7 Sanders Street",        "condition":"Diabetes"},
    {"id":"P1004","name":"Fatima Sesay",    "age":22,"gender":"Female","phone":"079-456789","blood":"AB+","reg_date":"2025-05-26","email":"fatima.sesay@gmail.com",   "address":"22 Pademba Road",         "condition":"None"},
    {"id":"P1005","name":"Mohamed Jalloh",  "age":37,"gender":"Male",  "phone":"076-567890","blood":"O-", "reg_date":"2025-05-25","email":"mohamed.jalloh@gmail.com","address":"3 Circular Road",         "condition":"Asthma"},
]

APPOINTMENTS = [
    {"appt_id":"A001","patient_id":"P1001","name":"John K. Koroma", "doctor":"Dr. Sarah Jallow","dept":"General Medicine","date":"2025-05-29","time":"10:30 AM","type":"Consultation","status":"Booked",   "notes":"Routine Consultation"},
    {"appt_id":"A002","patient_id":"P1002","name":"Mariama Bangura","doctor":"Dr. Kamara",      "dept":"Internal Medicine","date":"2025-05-29","time":"11:00 AM","type":"Follow-up",  "status":"Completed","notes":"Blood pressure check"},
    {"appt_id":"A003","patient_id":"P1003","name":"Alhaji Kamara",  "doctor":"Dr. Sesay",       "dept":"Endocrinology",   "date":"2025-05-30","time":"09:00 AM","type":"Consultation","status":"Cancelled","notes":"Diabetes review"},
    {"appt_id":"A004","patient_id":"P1004","name":"Fatima Sesay",   "doctor":"Dr. Bah",         "dept":"General Medicine","date":"2025-05-30","time":"02:00 PM","type":"Consultation","status":"Booked",   "notes":"General checkup"},
    {"appt_id":"A005","patient_id":"P1005","name":"Mohamed Jalloh", "doctor":"Dr. Jalloh",      "dept":"Pulmonology",     "date":"2025-05-31","time":"08:30 AM","type":"Consultation","status":"Completed","notes":"Asthma review"},
]

DOCTORS_BY_DEPT = {
    "General Medicine":  ["Dr. Sarah Jallow","Dr. Bah"],
    "Internal Medicine": ["Dr. Kamara"],
    "Endocrinology":     ["Dr. Sesay"],
    "Pulmonology":       ["Dr. Jalloh"],
    "Cardiology":        ["Dr. Conteh"],
    "Pediatrics":        ["Dr. Thomas"],
}
DEPARTMENTS  = list(DOCTORS_BY_DEPT.keys())
BLOOD_GROUPS = ["A+","A-","B+","B-","AB+","AB-","O+","O-"]
APPT_TYPES   = ["Consultation","Follow-up","Routine Check-up","Emergency","Specialist Referral"]
TIME_SLOTS   = ["08:00 AM","08:30 AM","09:00 AM","09:30 AM","10:00 AM","10:30 AM",
                "11:00 AM","11:30 AM","12:00 PM","01:00 PM","02:00 PM","03:00 PM","04:00 PM","04:30 PM"]

_pat_ctr  = [1006]
_appt_ctr = [6]

def _next_pid():
    v = f"P{_pat_ctr[0]}"; _pat_ctr[0] += 1; return v

def _peek_pid():
    return f"P{_pat_ctr[0]}"

def _next_aid():
    v = f"A{_appt_ctr[0]:03d}"; _appt_ctr[0] += 1; return v

def find_patient(pid):
    for p in PATIENTS:
        if p["id"] == pid: return p
    return None

# ── Icon / Image helpers ───────────────────────────────────────────────────────
_ICON_CACHE = {}

def _icon_dir():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "Logo and icons")

def load_icon(name, size=(20,20)):
    if not HAS_PIL: return None
    key = (name, size)
    if key in _ICON_CACHE: return _ICON_CACHE[key]
    path = os.path.join(_icon_dir(), name)
    if not os.path.exists(path): return None
    try:
        img = Image.open(path).convert("RGBA").resize(size, Image.LANCZOS)
        tk_img = ImageTk.PhotoImage(img)
        _ICON_CACHE[key] = tk_img
        return tk_img
    except Exception:
        return None

def load_header_image(w, h):
    if not HAS_PIL: return None
    path = os.path.join(_icon_dir(), "image.png")
    if not os.path.exists(path): return None
    try:
        img = Image.open(path).convert("RGBA").resize((w, h), Image.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception:
        return None

# ── Styled button helper ───────────────────────────────────────────────────────
def _btn(parent, text, bg, fg=WHITE, icon=None, cmd=None, padx=14, pady=8, font_size=10):
    b = tk.Button(parent, text=f"  {text}", bg=bg, fg=fg,
                  font=("Segoe UI", font_size, "bold"),
                  bd=0, relief="flat", cursor="hand2", padx=padx, pady=pady,
                  activebackground=bg, activeforeground=fg,
                  image=icon, compound="left" if icon else "none",
                  command=cmd)
    hover_color = {TEAL: TEAL_DARK, DEL_RED: DEL_HOVER, SAVE_DARK: "#162d4a",
                   BTN_BLUE: BTN_HOVER, COMPLETE_GR: "#1e8449",
                   EDIT_ORANGE: "#ca6f1e", "#6c757d": "#5a6268"}.get(bg, bg)
    b.bind("<Enter>", lambda e: b.config(bg=hover_color))
    b.bind("<Leave>", lambda e: b.config(bg=bg))
    return b

# ── Treeview style ─────────────────────────────────────────────────────────────
def _setup_tree_style():
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("AuraTree.Treeview",
                    background=WHITE, fieldbackground=WHITE,
                    foreground=TEXT_DARK, font=("Segoe UI", 9),
                    rowheight=28)
    style.configure("AuraTree.Treeview.Heading",
                    background=TEAL, foreground=WHITE,
                    font=("Segoe UI", 9, "bold"), relief="flat")
    style.map("AuraTree.Treeview",
              background=[("selected", BTN_BLUE)],
              foreground=[("selected", WHITE)])
    style.map("AuraTree.Treeview.Heading", background=[("active", TEAL_DARK)])

# ── Section title ──────────────────────────────────────────────────────────────
def _section_title(parent, text):
    f = tk.Frame(parent, bg=WHITE)
    f.pack(fill="x", padx=18, pady=(14, 6))
    tk.Label(f, text=text, bg=WHITE, fg=TEAL,
             font=("Segoe UI", 11, "bold")).pack(side="left")
    tk.Frame(f, bg=INPUT_BD, height=1).pack(side="left", fill="x", expand=True, padx=(10, 0), pady=7)

# ── Labeled form entry ─────────────────────────────────────────────────────────
def _form_entry(parent, label, row, col, colspan=1, width=22, state="normal"):
    c_off = col * 2
    tk.Label(parent, text=label, bg=WHITE, fg=TEXT_MID,
             font=("Segoe UI", 9)).grid(row=row, column=c_off, sticky="e", padx=(6, 4), pady=6)
    var = tk.StringVar()
    e = tk.Entry(parent, textvariable=var, font=("Segoe UI", 10),
                 bg=INPUT_BG, fg=TEXT_DARK, bd=1, relief="solid",
                 highlightthickness=0, width=width, state=state)
    e.grid(row=row, column=c_off+1, sticky="ew", padx=(0, 12), pady=6,
           columnspan=colspan)
    return var, e

def _form_combo(parent, label, row, col, values, width=20):
    c_off = col * 2
    tk.Label(parent, text=label, bg=WHITE, fg=TEXT_MID,
             font=("Segoe UI", 9)).grid(row=row, column=c_off, sticky="e", padx=(6, 4), pady=6)
    var = tk.StringVar()
    cb = ttk.Combobox(parent, textvariable=var, values=values,
                      font=("Segoe UI", 10), width=width, state="readonly")
    cb.grid(row=row, column=c_off+1, sticky="ew", padx=(0, 12), pady=6)
    return var, cb

# ══════════════════════════════════════════════════════════════════════════════
#  MAIN APP SHELL
# ══════════════════════════════════════════════════════════════════════════════
class RegisterPatientApp(tk.Toplevel):

    def __init__(self, master, username="Admin"):
        super().__init__(master)
        self.username    = username
        self._hdr_img    = None
        self._icon_store = {}   # keeps PhotoImage refs alive
        self._active_key = None

        self.title("AuraClinic — Healthcare Management System")
        self.geometry("1280x800")
        self.minsize(1100, 700)
        self.configure(bg=WHITE)
        _setup_tree_style()

        self._build_header()
        self._build_body()
        self._build_footer()
        self._show_page("register")

    # ── Header ──────────────────────────────────────────────────────────────────
    def _build_header(self):
        hdr = tk.Frame(self, bg=TEAL, height=HEADER_H)
        hdr.pack(fill="x"); hdr.pack_propagate(False)

        # Clinic image
        img = load_header_image(115, 90)
        if img:
            self._hdr_img = img
            tk.Label(hdr, image=img, bg=TEAL).pack(side="left", padx=(6, 0))
        else:
            tk.Frame(hdr, bg=TEAL, width=10).pack(side="left")

        # Title block
        tf = tk.Frame(hdr, bg=TEAL)
        tf.pack(side="left", fill="both", expand=True, padx=10)
        tk.Label(tf, text="Aura Clinic Healthcare Management System",
                 bg=TEAL, fg=WHITE,
                 font=("Segoe UI", 20, "bold")).pack(anchor="w", pady=(18, 2))
        tk.Label(tf, text="Better Care, Better Health, Better Life",
                 bg=TEAL, fg="#c8eaf5",
                 font=("Segoe UI", 11)).pack(anchor="w")

        # Clock
        self._clock_lbl = tk.Label(hdr, bg=TEAL, fg=WHITE,
                                    font=("Segoe UI", 10), justify="right")
        self._clock_lbl.pack(side="right", padx=20)
        self._tick()

    def _tick(self):
        n = datetime.datetime.now()
        self._clock_lbl.config(
            text=f"{n.strftime('%B %d, %Y')}\n{n.strftime('%I :%M :%S %p')}")
        self.after(1000, self._tick)

    # ── Body ────────────────────────────────────────────────────────────────────
    def _build_body(self):
        body = tk.Frame(self, bg=CONTENT_BG)
        body.pack(fill="both", expand=True)

        # Sidebar
        self._sb = tk.Frame(body, bg=SIDEBAR_BG, width=SIDEBAR_W)
        self._sb.pack(side="left", fill="y"); self._sb.pack_propagate(False)
        self._build_sidebar()

        # Vertical divider
        tk.Frame(body, bg=INPUT_BD, width=1).pack(side="left", fill="y")

        # Content pane
        self._content = tk.Frame(body, bg=WHITE)
        self._content.pack(side="left", fill="both", expand=True)

    def _build_sidebar(self):
        tk.Label(self._sb, text="MAIN MENU", bg=SIDEBAR_BG, fg=TEAL,
                 font=("Segoe UI", 11, "bold")).pack(pady=(18, 10))

        nav = [
            ("register",     "Register Patient",    "Vector.png"),
            ("book",         "Book Appointment",    "Calender icon.png"),
            ("appointments", "Appointment Records", "appointment records icon.png"),
            ("search",       "Search Patient",      "Search patient icon.png"),
        ]
        self._nav_btns = {}
        for key, label, iname in nav:
            ico = load_icon(iname, (22, 22))
            if ico: self._icon_store[f"nav_{key}"] = ico

            outer = tk.Frame(self._sb, bg=SIDEBAR_BG)
            outer.pack(fill="x", padx=10, pady=3)

            btn = tk.Button(outer, text=f"  {label}",
                            image=ico if ico else None,
                            compound="left" if ico else "none",
                            bg=SIDEBAR_BG, fg=TEXT_DARK,
                            font=("Segoe UI", 10), bd=0, relief="flat",
                            anchor="w", padx=8, pady=10,
                            cursor="hand2",
                            command=lambda k=key: self._show_page(k))
            btn.pack(fill="x")
            self._nav_btns[key] = btn
            btn.bind("<Enter>",
                     lambda e, b=btn, k=key: b.config(
                         bg=BTN_BLUE if self._active_key != k else BTN_HOVER,
                         fg=WHITE))
            btn.bind("<Leave>",
                     lambda e, b=btn, k=key: b.config(
                         bg=BTN_BLUE if self._active_key == k else SIDEBAR_BG,
                         fg=WHITE if self._active_key == k else TEXT_DARK))

        tk.Frame(self._sb, bg=INPUT_BD, height=1).pack(fill="x", padx=10, pady=12)

        # Logout
        lo_ico = load_icon("log-out icon.png", (20, 20))
        if lo_ico: self._icon_store["logout"] = lo_ico
        lo = tk.Button(self._sb, text="  Log-out",
                       image=lo_ico if lo_ico else None,
                       compound="left" if lo_ico else "none",
                       bg=DEL_RED, fg=WHITE,
                       font=("Segoe UI", 10, "bold"),
                       bd=0, relief="flat", padx=8, pady=10,
                       cursor="hand2", command=self._logout)
        lo.pack(fill="x", padx=10, pady=3)
        lo.bind("<Enter>", lambda e: lo.config(bg=DEL_HOVER))
        lo.bind("<Leave>", lambda e: lo.config(bg=DEL_RED))

    def _show_page(self, key):
        if self._active_key and self._active_key in self._nav_btns:
            self._nav_btns[self._active_key].config(bg=SIDEBAR_BG, fg=TEXT_DARK)
        self._active_key = key
        if key in self._nav_btns:
            self._nav_btns[key].config(bg=BTN_BLUE, fg=WHITE)

        for w in self._content.winfo_children():
            w.destroy()

        pages = {"register":     RegisterPatientPage,
                 "book":         BookAppointmentPage,
                 "appointments": AppointmentRecordsPage,
                 "search":       SearchPatientPage}
        if key in pages:
            pages[key](self._content, self).pack(fill="both", expand=True)

    # ── Footer ──────────────────────────────────────────────────────────────────
    def _build_footer(self):
        ft = tk.Frame(self, bg=TEAL, height=28)
        ft.pack(fill="x", side="bottom"); ft.pack_propagate(False)
        tk.Label(ft, text=f"User: {self.username}", bg=TEAL, fg=WHITE,
                 font=("Segoe UI", 8)).pack(side="left", padx=14)
        tk.Label(ft, text="Welcome to Aura Clinic Healthcare Management System",
                 bg=TEAL, fg=WHITE, font=("Segoe UI", 8)).pack(side="left", expand=True)
        tk.Label(ft, text="Version 1.0", bg=TEAL, fg=WHITE,
                 font=("Segoe UI", 8)).pack(side="right", padx=14)

    def _logout(self):
        if messagebox.askyesno("Log Out", "Are you sure you want to log out?"):
            self.master.deiconify()
            self.destroy()


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE — REGISTER PATIENT
# ══════════════════════════════════════════════════════════════════════════════
class RegisterPatientPage(tk.Frame):

    def __init__(self, parent, app):
        super().__init__(parent, bg=WHITE)
        self.app = app
        self._selected_id = None
        self._build()

    def _build(self):
    # Scrollable canvas
        canvas = tk.Canvas(self, bg=WHITE, highlightthickness=0)
        scroll = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        inner = tk.Frame(canvas, bg=WHITE)
        win_id = canvas.create_window((0, 0), window=inner, anchor="nw")

        def _on_frame_conf(e):
             canvas.configure(scrollregion=canvas.bbox("all"))
        def _on_canvas_conf(e):
             canvas.itemconfig(win_id, width=e.width)
        inner.bind("<Configure>", _on_frame_conf)
        canvas.bind("<Configure>", _on_canvas_conf)
        def _scroll(e):
             canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _scroll))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

        self._inner = inner
        self._build_form(inner)
        self._build_table(inner)
        
    def _build_form(self, parent):
        _section_title(parent, "PATIENT REGISTRATION")

        grid = tk.Frame(parent, bg=WHITE)
        grid.pack(fill="x", padx=18, pady=4)
        for c in range(4): grid.columnconfigure(c, weight=1 if c % 2 == 1 else 0)

        # Left column vars
        self.v_id,    _ = _form_entry(grid, "Patient ID:",        0, 0, state="readonly")
        self.v_name,  _ = _form_entry(grid, "Full Name:",         1, 0)
        self.v_age,   _ = _form_entry(grid, "Age:",               2, 0)
        self.v_gender, self._gender_cb = _form_combo(grid, "Gender:", 3, 0,
                                                     ["Male","Female","Other"])
        self.v_phone, _ = _form_entry(grid, "Phone Number:",      4, 0)

        # Right column vars
        self.v_address,   _ = _form_entry(grid, "Address:",          0, 2)
        self.v_email,     _ = _form_entry(grid, "Email:",            1, 2)
        self.v_blood, self._blood_cb = _form_combo(grid, "Blood Group:", 2, 2, BLOOD_GROUPS)
        self.v_condition, _ = _form_entry(grid, "Medical Condition:", 3, 2)
        self.v_regdate,   _ = _form_entry(grid, "Date Registered:",   4, 2)

        # Pre-fill new ID and today's date
        self._clear_form()

        # Buttons
        bf = tk.Frame(parent, bg=WHITE)
        bf.pack(fill="x", padx=18, pady=12)

        save_ico   = load_icon("Save patient icon.png",  (18,18))
        upd_ico    = load_icon("update icon.png",        (18,18))
        del_ico    = load_icon("delete icon.png",        (18,18))
        clear_ico  = load_icon("clear icon.png",         (18,18))
        for ico in [save_ico, upd_ico, del_ico, clear_ico]:
            if ico: self.app._icon_store[id(ico)] = ico

        _btn(bf, "Save Patient", SAVE_DARK, icon=save_ico,
             cmd=self._save).pack(side="left", padx=(0,10))
        _btn(bf, "Update",       BTN_BLUE,  icon=upd_ico,
             cmd=self._update).pack(side="left", padx=(0,10))
        _btn(bf, "Delete",       DEL_RED,   icon=del_ico,
             cmd=self._delete).pack(side="left", padx=(0,10))
        _btn(bf, "Clear",        "#6c757d", icon=clear_ico,
             cmd=self._clear_form).pack(side="left")

    def _build_table(self, parent):
        _section_title(parent, "PATIENT LIST")

        cols = ("Patient ID","Full Name","Age","Gender","Phone Number","Blood Group","Date Registered","Email")
        tf = tk.Frame(parent, bg=WHITE)
        tf.pack(fill="both", expand=True, padx=18, pady=(0,18))

        self._tree = ttk.Treeview(tf, columns=cols, show="headings",
                                   style="AuraTree.Treeview", height=10)
        widths = [80,160,50,80,110,90,110,190]
        for col, w in zip(cols, widths):
            self._tree.heading(col, text=col)
            self._tree.column(col, width=w, anchor="center" if col in ("Age","Gender","Blood Group") else "w",
                              minwidth=w)

        vsb = ttk.Scrollbar(tf, orient="vertical",   command=self._tree.yview)
        hsb = ttk.Scrollbar(tf, orient="horizontal", command=self._tree.xview)
        self._tree.configure(yscroll=vsb.set, xscroll=hsb.set)
        self._tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        tf.rowconfigure(0, weight=1); tf.columnconfigure(0, weight=1)

        self._tree.tag_configure("odd",  background=WHITE)
        self._tree.tag_configure("even", background=ROW_ALT)
        self._tree.bind("<<TreeviewSelect>>", self._on_select)
        self._refresh_table()

    def _refresh_table(self):
        for row in self._tree.get_children():
            self._tree.delete(row)
        for i, p in enumerate(PATIENTS):
            tag = "even" if i % 2 == 0 else "odd"
            self._tree.insert("", "end", iid=p["id"],
                              values=(p["id"], p["name"], p["age"], p["gender"],
                                      p["phone"], p["blood"], p["reg_date"], p["email"]),
                              tags=(tag,))

    def _on_select(self, _):
        sel = self._tree.selection()
        if not sel: return
        p = find_patient(sel[0])
        if not p: return
        self._selected_id = p["id"]
        self.v_id.set(p["id"]);          self.v_name.set(p["name"])
        self.v_age.set(p["age"]);        self.v_gender.set(p["gender"])
        self.v_phone.set(p["phone"]);    self.v_address.set(p["address"])
        self.v_email.set(p["email"]);    self.v_blood.set(p["blood"])
        self.v_condition.set(p["condition"]); self.v_regdate.set(p["reg_date"])

    def _save(self):
        vals = self._collect()
        if vals is None: return
        if find_patient(vals["id"]):                                              # ← new line
            messagebox.showwarning("Save", "Already registered — use Update.")    # ← new line
            return                                                                # ← new line
        PATIENTS.append(vals)
        _pat_ctr[0] += 1
        self._refresh_table()
        messagebox.showinfo("Saved", f"Patient {vals['id']} registered successfully.")
        self._clear_form()

    def _update(self):
        if not self._selected_id:
            messagebox.showwarning("Update", "Select a patient to update."); return
        vals = self._collect(existing_id=self._selected_id)
        if vals is None: return
        for i, p in enumerate(PATIENTS):
            if p["id"] == self._selected_id:
                PATIENTS[i] = vals; break
        self._refresh_table()
        messagebox.showinfo("Updated", f"Patient {self._selected_id} updated.")

    def _delete(self):
        if not self._selected_id:
            messagebox.showwarning("Delete", "Select a patient to delete."); return
        has_appts = any(a["patient_id"] == self._selected_id and a["status"] != "Cancelled"
                         for a in APPOINTMENTS)
        msg = (f"{self._selected_id} has active appointments. Delete patient anyway?"
               if has_appts else f"Delete patient {self._selected_id}?")
        if messagebox.askyesno("Delete", msg):
            global PATIENTS
            PATIENTS = [p for p in PATIENTS if p["id"] != self._selected_id]
            self._refresh_table()
            self._clear_form()

    def _collect(self, existing_id=None):
        name  = self.v_name.get().strip()
        age   = self.v_age.get().strip()
        phone = self.v_phone.get().strip()
        if not name:
            messagebox.showwarning("Validation", "Full Name is required."); return None
        if not age.isdigit():
            messagebox.showwarning("Validation", "Age must be a number."); return None
        if not phone:
            messagebox.showwarning("Validation", "Phone Number is required."); return None
        return {
            "id":        existing_id or self.v_id.get(),
            "name":      name,
            "age":       int(age),
            "gender":    self.v_gender.get() or "Male",
            "phone":     phone,
            "address":   self.v_address.get().strip(),
            "email":     self.v_email.get().strip(),
            "blood":     self.v_blood.get() or "",
            "condition": self.v_condition.get().strip(),
            "reg_date":  self.v_regdate.get().strip() or datetime.date.today().isoformat(),
        }

    def _clear_form(self, _=None):
        self._selected_id = None
        self.v_id.set(_peek_pid())
        for v in [self.v_name, self.v_age, self.v_address,
                  self.v_email, self.v_condition]:
            v.set("")
        self.v_gender.set("Male")
        self.v_blood.set("")
        self.v_regdate.set(datetime.date.today().isoformat())
        self.v_phone.set("")


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE — SEARCH PATIENT
# ══════════════════════════════════════════════════════════════════════════════
class SearchPatientPage(tk.Frame):

    def __init__(self, parent, app):
        super().__init__(parent, bg=WHITE)
        self.app = app
        self._build()

    def _build(self):
        # ── Page title bar ─────────────────────────────────────────────────────
        self._build_titlebar()
        # ── Filter panel ───────────────────────────────────────────────────────
        self._build_filters()
        # ── Results ────────────────────────────────────────────────────────────
        self._build_results()
        # Initial load
        self._do_search()

    def _build_titlebar(self):
        bar = tk.Frame(self, bg=WHITE)
        bar.pack(fill="x", padx=18, pady=(14, 4))
        ico = load_icon("Search patient icon.png", (28,28))
        if ico: self.app._icon_store["sp_title"] = ico
        if ico:
            tk.Label(bar, image=ico, bg=WHITE).pack(side="left", padx=(0,8))
        tk.Label(bar, text="SEARCH PATIENT", bg=WHITE, fg=TEXT_DARK,
                 font=("Segoe UI", 14, "bold")).pack(side="left")
        tk.Label(bar, text="Search and view patient information",
                 bg=WHITE, fg=TEXT_MID,
                 font=("Segoe UI", 9)).pack(side="left", padx=12, pady=4)

        # Breadcrumb right
        home_ico = load_icon("home icon.png", (16,16))
        if home_ico: self.app._icon_store["sp_home"] = home_ico
        bc = tk.Frame(bar, bg=WHITE)
        bc.pack(side="right")
        if home_ico: tk.Label(bc, image=home_ico, bg=WHITE).pack(side="left")
        tk.Label(bc, text=" / SEARCH PATIENT", bg=WHITE, fg=TEXT_MID,
                 font=("Segoe UI", 9)).pack(side="left")

    def _build_filters(self):
        box = tk.LabelFrame(self, text="  Search Filters", bg=WHITE,
                             fg=TEAL, font=("Segoe UI", 9, "bold"),
                             bd=1, relief="solid")
        box.pack(fill="x", padx=18, pady=(4, 8))

        row1 = tk.Frame(box, bg=WHITE); row1.pack(fill="x", padx=10, pady=(8,2))
        row2 = tk.Frame(box, bg=WHITE); row2.pack(fill="x", padx=10, pady=(2,4))
        row3 = tk.Frame(box, bg=WHITE); row3.pack(fill="x", padx=10, pady=(2,8))

        # Row 1
        tk.Label(row1, text="Search By:", bg=WHITE, fg=TEXT_MID,
                 font=("Segoe UI",9)).pack(side="left")
        self.sv_by = tk.StringVar(value="Patient ID")
        ttk.Combobox(row1, textvariable=self.sv_by,
                     values=["Patient ID","Full Name"], state="readonly",
                     font=("Segoe UI",9), width=14).pack(side="left", padx=(4,16))
        tk.Label(row1, text="Keyword:", bg=WHITE, fg=TEXT_MID,
                 font=("Segoe UI",9)).pack(side="left")
        self.sv_kw = tk.StringVar()
        tk.Entry(row1, textvariable=self.sv_kw, font=("Segoe UI",9),
                 bd=1, relief="solid", width=26).pack(side="left", padx=(4,16))

        s_ico = load_icon("Search patient icon.png",(16,16))
        r_ico = load_icon("reseticon.png",(16,16))
        if s_ico: self.app._icon_store["sf_s"] = s_ico
        if r_ico: self.app._icon_store["sf_r"] = r_ico
        _btn(row1, "Search", TEAL,    icon=s_ico, cmd=self._do_search, pady=5).pack(side="left", padx=(0,6))
        _btn(row1, "Reset",  "#6c757d", icon=r_ico, cmd=self._reset,  pady=5).pack(side="left")

        # Row 2
        tk.Label(row2, text="Full Name:", bg=WHITE, fg=TEXT_MID,
                 font=("Segoe UI",9)).pack(side="left")
        self.sv_name = tk.StringVar()
        tk.Entry(row2, textvariable=self.sv_name, font=("Segoe UI",9),
                 bd=1, relief="solid", width=22).pack(side="left", padx=(4,16))
        tk.Label(row2, text="Phone Number:", bg=WHITE, fg=TEXT_MID,
                 font=("Segoe UI",9)).pack(side="left")
        self.sv_phone = tk.StringVar()
        tk.Entry(row2, textvariable=self.sv_phone, font=("Segoe UI",9),
                 bd=1, relief="solid", width=22).pack(side="left", padx=4)

        # Row 3
        tk.Label(row3, text="Gender:", bg=WHITE, fg=TEXT_MID,
                 font=("Segoe UI",9)).pack(side="left")
        self.sv_gender = tk.StringVar(value="All")
        ttk.Combobox(row3, textvariable=self.sv_gender,
                     values=["All","Male","Female","Other"], state="readonly",
                     font=("Segoe UI",9), width=10).pack(side="left", padx=(4,16))
        tk.Label(row3, text="Blood Group:", bg=WHITE, fg=TEXT_MID,
                 font=("Segoe UI",9)).pack(side="left")
        self.sv_blood = tk.StringVar(value="All")
        ttk.Combobox(row3, textvariable=self.sv_blood,
                     values=["All"]+BLOOD_GROUPS, state="readonly",
                     font=("Segoe UI",9), width=8).pack(side="left", padx=(4,16))
        tk.Label(row3, text="Date Registered From:", bg=WHITE, fg=TEXT_MID,
                 font=("Segoe UI",9)).pack(side="left")
        self.sv_from = tk.StringVar()
        tk.Entry(row3, textvariable=self.sv_from, font=("Segoe UI",9),
                 bd=1, relief="solid", width=12).pack(side="left", padx=(4,8))
        tk.Label(row3, text="To:", bg=WHITE, fg=TEXT_MID,
                 font=("Segoe UI",9)).pack(side="left")
        self.sv_to = tk.StringVar()
        tk.Entry(row3, textvariable=self.sv_to, font=("Segoe UI",9),
                 bd=1, relief="solid", width=12).pack(side="left", padx=4)

    def _build_results(self):
        rf = tk.Frame(self, bg=WHITE)
        rf.pack(fill="both", expand=True, padx=18, pady=(0,10))

        # Header row
        hdr = tk.Frame(rf, bg=WHITE)
        hdr.pack(fill="x", pady=(4,4))
        self._count_lbl = tk.Label(hdr, text="Search Results\nTotal Records Found: 0",
                                    bg=WHITE, fg=TEAL, font=("Segoe UI",9,"bold"),
                                    justify="left")
        self._count_lbl.pack(side="left")

        exp_ico = load_icon("export icon.png",(16,16))
        if exp_ico: self.app._icon_store["exp"] = exp_ico
        _btn(hdr, "Export", BTN_BLUE, icon=exp_ico,
             cmd=self._export, pady=5).pack(side="right")

        cols = ("Patient ID","Full Name","Age","Gender","Phone Number","Blood Group","Date Registered")
        tf = tk.Frame(rf, bg=WHITE)
        tf.pack(fill="both", expand=True)

        self._tree = ttk.Treeview(tf, columns=cols, show="headings",
                                   style="AuraTree.Treeview", height=14)
        widths = [90,180,55,90,120,100,120]
        for col, w in zip(cols, widths):
            self._tree.heading(col, text=col)
            self._tree.column(col, width=w, anchor="center" if col in ("Age","Gender","Blood Group") else "w")
        self._tree.tag_configure("odd",  background=WHITE)
        self._tree.tag_configure("even", background=ROW_ALT)

        vsb = ttk.Scrollbar(tf, orient="vertical",   command=self._tree.yview)
        hsb = ttk.Scrollbar(tf, orient="horizontal", command=self._tree.xview)
        self._tree.configure(yscroll=vsb.set, xscroll=hsb.set)
        self._tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        tf.rowconfigure(0,weight=1); tf.columnconfigure(0,weight=1)

    def _do_search(self, _=None):
        kw     = self.sv_kw.get().strip().lower()
        by     = self.sv_by.get()
        name   = self.sv_name.get().strip().lower()
        phone  = self.sv_phone.get().strip()
        gender = self.sv_gender.get()
        blood  = self.sv_blood.get()
        d_from = self.sv_from.get().strip()
        d_to   = self.sv_to.get().strip()

        results = []
        for p in PATIENTS:
            if kw:
                target = p["id"].lower() if by == "Patient ID" else p["name"].lower()
                if kw not in target: continue
            if name   and name  not in p["name"].lower():  continue
            if phone  and phone not in p["phone"]:         continue
            if gender != "All" and p["gender"] != gender:  continue
            if blood  != "All" and p["blood"]  != blood:   continue
            if d_from and p["reg_date"] < d_from:          continue
            if d_to   and p["reg_date"] > d_to:            continue
            results.append(p)

        for row in self._tree.get_children():
            self._tree.delete(row)
        for i, p in enumerate(results):
            tag = "even" if i%2==0 else "odd"
            self._tree.insert("", "end",
                              values=(p["id"],p["name"],p["age"],p["gender"],
                                      p["phone"],p["blood"],p["reg_date"]),
                              tags=(tag,))
        self._count_lbl.config(
            text=f"Search Results\nTotal Records Found: {len(results)}")

    def _reset(self):
        for v in [self.sv_kw, self.sv_name, self.sv_phone, self.sv_from, self.sv_to]:
            v.set("")
        self.sv_by.set("Patient ID"); self.sv_gender.set("All"); self.sv_blood.set("All")
        self._do_search()

    def _export(self):
        try:
            import tkinter.filedialog as fd
            path = fd.asksaveasfilename(defaultextension=".csv",
                                        filetypes=[("CSV files","*.csv")],
                                        title="Export Patients")
            if not path: return
            with open(path, "w", newline="") as f:
                w = csv.writer(f)
                w.writerow(["Patient ID","Full Name","Age","Gender",
                            "Phone Number","Blood Group","Date Registered"])
                for row in self._tree.get_children():
                    w.writerow(self._tree.item(row)["values"])
            messagebox.showinfo("Exported", f"Saved to {path}")
        except Exception as ex:
            messagebox.showerror("Export Error", str(ex))


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE — BOOK APPOINTMENT
# ══════════════════════════════════════════════════════════════════════════════
class BookAppointmentPage(tk.Frame):

    def __init__(self, parent, app):
        super().__init__(parent, bg=WHITE)
        self.app = app
        self._sel_time = tk.StringVar()
        self._time_btns = {}
        self._build()

    def _build(self):
        self._build_titlebar()

        main = tk.Frame(self, bg=WHITE)
        main.pack(fill="both", expand=True, padx=18, pady=8)
        main.columnconfigure(0, weight=3)
        main.columnconfigure(1, weight=2)
        main.rowconfigure(0, weight=1)

        left  = tk.Frame(main, bg=WHITE); left.grid(row=0, column=0, sticky="nsew", padx=(0,10))
        right = tk.Frame(main, bg=WHITE); right.grid(row=0, column=1, sticky="nsew")

        self._build_left(left)
        self._build_right(right)

    def _build_titlebar(self):
        bar = tk.Frame(self, bg=WHITE)
        bar.pack(fill="x", padx=18, pady=(14,4))
        ico = load_icon("Calender icon.png",(28,28))
        if ico: self.app._icon_store["ba_title"] = ico
        if ico: tk.Label(bar, image=ico, bg=WHITE).pack(side="left", padx=(0,8))
        tk.Label(bar, text="BOOK APPOINTMENT", bg=WHITE, fg=TEXT_DARK,
                 font=("Segoe UI",14,"bold")).pack(side="left")
        tk.Label(bar, text="Schedule a new appointment for a patient",
                 bg=WHITE, fg=TEXT_MID, font=("Segoe UI",9)).pack(side="left", padx=12)

        home_ico = load_icon("home icon.png",(16,16))
        if home_ico: self.app._icon_store["ba_home"] = home_ico
        bc = tk.Frame(bar, bg=WHITE); bc.pack(side="right")
        if home_ico: tk.Label(bc, image=home_ico, bg=WHITE).pack(side="left")
        tk.Label(bc, text=" / Book Appointment", bg=WHITE, fg=TEXT_MID,
                 font=("Segoe UI",9)).pack(side="left")

    def _build_left(self, parent):
        # ── Patient Info ────────────────────────────────────────────────────────
        pi = tk.LabelFrame(parent, text="  PATIENT INFORMATION", bg=WHITE,
                           fg=TEAL, font=("Segoe UI",9,"bold"),
                           bd=1, relief="solid")
        pi.pack(fill="x", pady=(0,10))

        pf = tk.Frame(pi, bg=WHITE); pf.pack(fill="x", padx=10, pady=8)
        pf.columnconfigure(1, weight=1)

        tk.Label(pf, text="Patient ID:", bg=WHITE, fg=TEXT_MID,
                 font=("Segoe UI",9)).grid(row=0, column=0, sticky="e", padx=(0,6), pady=6)
        self.bv_pid = tk.StringVar()
        pid_row = tk.Frame(pf, bg=WHITE)
        pid_row.grid(row=0, column=1, sticky="ew", pady=6)
        pid_row.columnconfigure(0, weight=1)
        tk.Entry(pid_row, textvariable=self.bv_pid, font=("Segoe UI",10),
                 bd=1, relief="solid").grid(row=0,column=0,sticky="ew")
        s_ico = load_icon("Search patient icon.png",(16,16))
        if s_ico: self.app._icon_store["ba_s"] = s_ico
        _btn(pid_row, "Search", BTN_BLUE, icon=s_ico,
             cmd=self._lookup_patient, pady=4,
             padx=10).grid(row=0,column=1,padx=(6,0))

        tk.Label(pf, text="Full Name:", bg=WHITE, fg=TEXT_MID,
                 font=("Segoe UI",9)).grid(row=1, column=0, sticky="e", padx=(0,6), pady=6)
        self.bv_name = tk.StringVar()
        tk.Entry(pf, textvariable=self.bv_name, font=("Segoe UI",10),
                 bd=1, relief="solid", state="readonly").grid(row=1,column=1,sticky="ew",pady=6)

        tk.Label(pf, text="Phone Number:", bg=WHITE, fg=TEXT_MID,
                 font=("Segoe UI",9)).grid(row=2, column=0, sticky="e", padx=(0,6), pady=6)
        self.bv_phone = tk.StringVar()
        tk.Entry(pf, textvariable=self.bv_phone, font=("Segoe UI",10),
                 bd=1, relief="solid", state="readonly").grid(row=2,column=1,sticky="ew",pady=6)

        # ── Appointment Details ─────────────────────────────────────────────────
        ad = tk.LabelFrame(parent, text="  APPOINTMENT DETAILS", bg=WHITE,
                           fg=TEAL, font=("Segoe UI",9,"bold"),
                           bd=1, relief="solid")
        ad.pack(fill="x", pady=(0,10))

        af = tk.Frame(ad, bg=WHITE); af.pack(fill="x", padx=10, pady=8)
        af.columnconfigure(1, weight=1)

        def _lbl_entry(row, label, var, state="normal"):
            tk.Label(af, text=label, bg=WHITE, fg=TEXT_MID,
                     font=("Segoe UI",9)).grid(row=row, column=0, sticky="e", padx=(0,6), pady=5)
            e = tk.Entry(af, textvariable=var, font=("Segoe UI",10),
                         bd=1, relief="solid", state=state)
            e.grid(row=row, column=1, sticky="ew", pady=5)
            return e

        def _lbl_combo(row, label, var, values):
            tk.Label(af, text=label, bg=WHITE, fg=TEXT_MID,
                     font=("Segoe UI",9)).grid(row=row, column=0, sticky="e", padx=(0,6), pady=5)
            cb = ttk.Combobox(af, textvariable=var, values=values,
                              font=("Segoe UI",10), state="readonly")
            cb.grid(row=row, column=1, sticky="ew", pady=5)
            return cb

        self.bv_dept  = tk.StringVar(value=DEPARTMENTS[0])
        self.bv_doc   = tk.StringVar()
        self.bv_type  = tk.StringVar(value=APPT_TYPES[0])
        self.bv_date  = tk.StringVar(value=datetime.date.today().isoformat())
        self.bv_time  = tk.StringVar()
        self.bv_notes = tk.StringVar()

        self._dept_cb = _lbl_combo(0, "Department:", self.bv_dept, DEPARTMENTS)
        self._doc_cb  = _lbl_combo(1, "Doctor:",     self.bv_doc,  DOCTORS_BY_DEPT[DEPARTMENTS[0]])
        _lbl_combo    (2, "Appointment Type:", self.bv_type, APPT_TYPES)
        _lbl_entry    (3, "Date:",             self.bv_date)
        _lbl_combo    (4, "Time:",             self.bv_time, TIME_SLOTS)
        _lbl_entry    (5, "Reason (Optional):",self.bv_notes)

        self._dept_cb.bind("<<ComboboxSelected>>", self._on_dept_change)
        self.bv_date.trace_add("write", lambda *a: self._refresh_avail())
        self.bv_doc.trace_add ("write", lambda *a: self._refresh_summary())
        self.bv_time.trace_add("write", lambda *a: (self._refresh_summary(),
                                                     self._sync_timeslot()))
        self.bv_dept.trace_add("write", lambda *a: self._refresh_summary())
        self.bv_type.trace_add("write", lambda *a: self._refresh_summary())

        self._update_doctors()

        # Action buttons
        bf = tk.Frame(parent, bg=WHITE); bf.pack(fill="x", pady=6)
        bk_ico = load_icon("Calender icon.png",(16,16))
        rs_ico = load_icon("reseticon.png",(16,16))
        cl_ico = load_icon("clear icon.png",(16,16))
        for i in [bk_ico, rs_ico, cl_ico]:
            if i: self.app._icon_store[id(i)] = i
        _btn(bf, "Book Appointment", SAVE_DARK, icon=bk_ico,
             cmd=self._book).pack(side="left", padx=(0,8))
        _btn(bf, "Reset",  BTN_BLUE,    icon=rs_ico, cmd=self._reset, pady=8).pack(side="left", padx=(0,8))
        _btn(bf, "Cancel", "#6c757d",   icon=cl_ico, cmd=self._reset, pady=8).pack(side="left")

    def _build_right(self, parent):
        # ── Doctor Availability ─────────────────────────────────────────────────
        avail = tk.LabelFrame(parent, text="  DOCTOR AVAILABILITY", bg=WHITE,
                              fg=TEAL, font=("Segoe UI",9,"bold"),
                              bd=1, relief="solid")
        avail.pack(fill="x", pady=(0,10))

        df = tk.Frame(avail, bg=WHITE); df.pack(fill="x", padx=10, pady=(6,4))
        tk.Label(df, text="Doctor:", bg=WHITE, fg=TEXT_MID,
                 font=("Segoe UI",9,"bold")).pack(side="left")
        self._avail_doc_lbl = tk.Label(df, text="", bg=WHITE, fg=TEXT_DARK,
                                        font=("Segoe UI",9))
        self._avail_doc_lbl.pack(side="left", padx=6)

        df2 = tk.Frame(avail, bg=WHITE); df2.pack(fill="x", padx=10, pady=(0,6))
        tk.Label(df2, text="Date:", bg=WHITE, fg=TEXT_MID,
                 font=("Segoe UI",9,"bold")).pack(side="left")
        self._avail_date_lbl = tk.Label(df2, text="", bg=WHITE, fg=TEXT_DARK,
                                         font=("Segoe UI",9))
        self._avail_date_lbl.pack(side="left", padx=6)

        self._slot_frame = tk.Frame(avail, bg=WHITE)
        self._slot_frame.pack(fill="x", padx=10, pady=(0,8))
        self._refresh_avail()

        # ── Appointment Summary ─────────────────────────────────────────────────
        summ = tk.LabelFrame(parent, text="  APPOINTMENT SUMMARY", bg=WHITE,
                             fg=TEAL, font=("Segoe UI",9,"bold"),
                             bd=1, relief="solid")
        summ.pack(fill="x")

        self._summ_frame = tk.Frame(summ, bg=WHITE)
        self._summ_frame.pack(fill="x", padx=10, pady=8)
        self._refresh_summary()

    def _on_dept_change(self, _=None):
        self._update_doctors()
        self._refresh_avail()
        self._refresh_summary()

    def _update_doctors(self):
        dept  = self.bv_dept.get()
        docs  = DOCTORS_BY_DEPT.get(dept, [])
        self._doc_cb.configure(values=docs)
        if docs: self.bv_doc.set(docs[0])
        else: self.bv_doc.set("")

    def _refresh_avail(self, *_):
        self._avail_doc_lbl.config(text=self.bv_doc.get())
        self._avail_date_lbl.config(text=self.bv_date.get())

        for w in self._slot_frame.winfo_children():
            w.destroy()
        self._time_btns = {}

       # Get booked times for this doctor+date
        booked = {a["time"] for a in APPOINTMENTS
               if a["doctor"] == self.bv_doc.get()
               and a["date"]  == self.bv_date.get()
               and a["status"] != "Cancelled"}
         # Also get booked times for this patient+date to prevent double booking  # ← new
        booked |= {a["time"] for a in APPOINTMENTS                                # ← new
               if a["patient_id"] == self.bv_pid.get().strip().upper()               # ← new
               and a["date"]      == self.bv_date.get()                       # ← new
               and a["status"]    != "Cancelled"}                             # ← new

        for i, slot in enumerate(TIME_SLOTS):
            r, c = divmod(i, 2)
            is_booked   = slot in booked
            is_selected = slot == self.bv_time.get()
            bg  = BTN_BLUE if is_selected else ("#d9534f" if is_booked else "#e9f5fb")
            fg  = WHITE    if (is_selected or is_booked) else TEXT_DARK
            state = "disabled" if is_booked else "normal"
            btn = tk.Button(self._slot_frame, text=slot,
                            bg=bg, fg=fg,
                            font=("Segoe UI",9), bd=1, relief="solid",
                            width=9, pady=5, state=state,
                            cursor="hand2" if not is_booked else "arrow",
                            command=lambda s=slot: self._pick_slot(s))
            btn.grid(row=r, column=c, padx=3, pady=3)
            self._time_btns[slot] = btn

    def _pick_slot(self, slot):
        self.bv_time.set(slot)
        self._refresh_avail()

    def _sync_timeslot(self):
        # Keep slot buttons visually in sync when time changes via combobox
        sel = self.bv_time.get()
        for slot, btn in self._time_btns.items():
            if btn.winfo_exists():
                if slot == sel:
                    btn.config(bg=BTN_BLUE, fg=WHITE)
                elif btn.cget("state") != "disabled":
                    btn.config(bg="#e9f5fb", fg=TEXT_DARK)

    def _refresh_summary(self, *_):
        for w in self._summ_frame.winfo_children():
            w.destroy()
        rows = [
            ("Patient:",     f"{self.bv_name.get()} ({self.bv_pid.get()})"),
            ("Doctor:",      self.bv_doc.get()),
            ("Department:",  self.bv_dept.get()),
            ("Date:",        self.bv_date.get()),
            ("Time:",        self.bv_time.get()),
            ("Type:",        self.bv_type.get()),
            ("Reason:",      self.bv_notes.get()),
        ]
        for label, val in rows:
            r = tk.Frame(self._summ_frame, bg=WHITE); r.pack(fill="x", pady=1)
            tk.Label(r, text=label, bg=WHITE, fg=TEXT_MID,
                     font=("Segoe UI",9), width=12, anchor="e").pack(side="left")
            tk.Label(r, text=val, bg=WHITE, fg=TEXT_DARK,
                     font=("Segoe UI",9,"bold"), anchor="w").pack(side="left", padx=4)

    def _lookup_patient(self):
        pid = self.bv_pid.get().strip().upper()
        p   = find_patient(pid)
        if p:
            self.bv_name.set(p["name"]); self.bv_phone.set(p["phone"])
            self._refresh_summary()
        else:
            messagebox.showwarning("Not Found", f"Patient ID '{pid}' not found.")
            self.bv_name.set(""); self.bv_phone.set("")

    def _book(self):
        pid  = self.bv_pid.get().strip().upper()
        name = self.bv_name.get().strip()
        doc  = self.bv_doc.get().strip()
        date = self.bv_date.get().strip()
        time = self.bv_time.get().strip()

        if not pid:  messagebox.showwarning("Validation","Enter Patient ID."); return
        p = find_patient(pid)
        if not p:
            messagebox.showwarning("Validation","Look up a valid patient first."); return
        name = p["name"]
        if not doc:  messagebox.showwarning("Validation","Select a doctor."); return
        if not date: messagebox.showwarning("Validation","Enter appointment date."); return
        if not time: messagebox.showwarning("Validation","Select an appointment time."); return

    # Check for conflict
        for a in APPOINTMENTS:
         if (a["doctor"]==doc and a["date"]== date and
                a["time"]==time and a["status"]!="Cancelled"):
            messagebox.showerror("Conflict",
                f"{doc} already has an appointment at {time} on {date}.")
            return

        for a in APPOINTMENTS:                                                    # ← new
         if (a["patient_id"]==pid and a["date"]==date and                      # ← new
                a["time"]==time and a["status"]!="Cancelled"):                # ← new
            messagebox.showerror("Conflict",                                  # ← new
                f"{name} already has an appointment at {time} on {date}.")    # ← new
            return                                                            # ← new
        

        new_appt = {
            "appt_id":    _next_aid(),
            "patient_id": pid,
            "name":       name,
            "doctor":     doc,
            "dept":       self.bv_dept.get(),
            "date":       date,
            "time":       time,
            "type":       self.bv_type.get(),
            "status":     "Booked",
            "notes":      self.bv_notes.get().strip(),
        }
        APPOINTMENTS.append(new_appt)
        messagebox.showinfo("Success",
            f"Appointment {new_appt['appt_id']} booked successfully!")
        self._reset()

    def _reset(self):
        self.bv_pid.set(""); self.bv_name.set(""); self.bv_phone.set("")
        self.bv_dept.set(DEPARTMENTS[0]); self._update_doctors()
        self.bv_type.set(APPT_TYPES[0])
        self.bv_date.set(datetime.date.today().isoformat())
        self.bv_time.set(""); self.bv_notes.set("")
        self._refresh_avail(); self._refresh_summary()


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE — APPOINTMENT RECORDS
# ══════════════════════════════════════════════════════════════════════════════
STATUS_COLORS = {
    "Booked":    "#1787AE",
    "Completed": "#27ae60",
    "Cancelled": "#e74c3c",
}

class AppointmentRecordsPage(tk.Frame):

    def __init__(self, parent, app):
        super().__init__(parent, bg=WHITE)
        self.app = app
        self._sel_appt = None
        self._build()

    # ── Scroll container (makes sure detail area is always reachable) ──────────
    def _build(self):
        canvas = tk.Canvas(self, bg=WHITE, highlightthickness=0)
        vsb    = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        inner   = tk.Frame(canvas, bg=WHITE)
        win_id  = canvas.create_window((0, 0), window=inner, anchor="nw")

        def _on_inner(e):
            canvas.configure(scrollregion=canvas.bbox("all"))
        def _on_canvas(e):
            canvas.itemconfig(win_id, width=e.width)
        inner.bind("<Configure>", _on_inner)
        canvas.bind("<Configure>", _on_canvas)

        # Bind mousewheel only while cursor is over this canvas
        def _scroll(e):
            canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
        canvas.bind("<Enter>",     lambda e: canvas.bind_all("<MouseWheel>", _scroll))
        canvas.bind("<Leave>",     lambda e: canvas.unbind_all("<MouseWheel>"))

        self._inner = inner
        self._build_titlebar(inner)
        self._build_filters(inner)
        self._build_table(inner)
        self._build_detail_area(inner)
        self._do_search()

    def _build_titlebar(self, parent=None):
        if parent is None: parent = self
        bar = tk.Frame(parent, bg=WHITE)
        bar.pack(fill="x", padx=18, pady=(14,4))
        ico = load_icon("appointment records icon.png",(28,28))
        if ico: self.app._icon_store["ar_title"] = ico
        if ico: tk.Label(bar, image=ico, bg=WHITE).pack(side="left", padx=(0,8))
        tk.Label(bar, text="APPOINTMENT RECORDS", bg=WHITE, fg=TEXT_DARK,
                 font=("Segoe UI",14,"bold")).pack(side="left")
        tk.Label(bar, text="View and manage all booked appointments",
                 bg=WHITE, fg=TEXT_MID,
                 font=("Segoe UI",9)).pack(side="left", padx=12)

        home_ico = load_icon("home icon.png",(16,16))
        if home_ico: self.app._icon_store["ar_home"] = home_ico
        bc = tk.Frame(bar, bg=WHITE); bc.pack(side="right")
        if home_ico: tk.Label(bc, image=home_ico, bg=WHITE).pack(side="left")
        tk.Label(bc, text=" / APPOINTMENT RECORDS", bg=WHITE, fg=TEXT_MID,
                 font=("Segoe UI",9)).pack(side="left")

    def _build_filters(self, parent=None):
        if parent is None: parent = self
        box = tk.LabelFrame(parent, text="  Search Filters", bg=WHITE,
                             fg=TEAL, font=("Segoe UI",9,"bold"),
                             bd=1, relief="solid")
        box.pack(fill="x", padx=18, pady=(4,8))

        r1 = tk.Frame(box, bg=WHITE); r1.pack(fill="x", padx=10, pady=(8,2))
        r2 = tk.Frame(box, bg=WHITE); r2.pack(fill="x", padx=10, pady=(2,8))

        # Row 1
        tk.Label(r1, text="Search By:", bg=WHITE, fg=TEXT_MID,
                 font=("Segoe UI",9)).pack(side="left")
        self.av_by = tk.StringVar(value="Patient ID / Full Name")
        ttk.Combobox(r1, textvariable=self.av_by,
                     values=["Patient ID / Full Name","Appointment ID"],
                     state="readonly", font=("Segoe UI",9), width=22).pack(side="left", padx=(4,16))
        tk.Label(r1, text="Keyword:", bg=WHITE, fg=TEXT_MID,
                 font=("Segoe UI",9)).pack(side="left")
        self.av_kw = tk.StringVar()
        tk.Entry(r1, textvariable=self.av_kw, font=("Segoe UI",9),
                 bd=1, relief="solid", width=30).pack(side="left", padx=(4,16))

        s_ico = load_icon("Search patient icon.png",(16,16))
        r_ico = load_icon("reseticon.png",(16,16))
        if s_ico: self.app._icon_store["ar_s"] = s_ico
        if r_ico: self.app._icon_store["ar_r"] = r_ico
        _btn(r1,"Search",TEAL,    icon=s_ico,cmd=self._do_search,pady=5).pack(side="left",padx=(0,6))
        _btn(r1,"Reset", "#6c757d",icon=r_ico,cmd=self._reset,   pady=5).pack(side="left")

        # Row 2
        tk.Label(r2, text="Appointment Date:", bg=WHITE, fg=TEXT_MID,
                 font=("Segoe UI",9)).pack(side="left")
        self.av_from = tk.StringVar()
        tk.Entry(r2, textvariable=self.av_from, font=("Segoe UI",9),
                 bd=1, relief="solid", width=12).pack(side="left", padx=(4,8))
        tk.Label(r2, text="To:", bg=WHITE, fg=TEXT_MID,
                 font=("Segoe UI",9)).pack(side="left")
        self.av_to = tk.StringVar()
        tk.Entry(r2, textvariable=self.av_to, font=("Segoe UI",9),
                 bd=1, relief="solid", width=12).pack(side="left", padx=(4,16))

        tk.Label(r2, text="Doctor:", bg=WHITE, fg=TEXT_MID,
                 font=("Segoe UI",9)).pack(side="left")
        all_docs = ["All"] + sorted({d for docs in DOCTORS_BY_DEPT.values() for d in docs})
        self.av_doc = tk.StringVar(value="All")
        ttk.Combobox(r2, textvariable=self.av_doc, values=all_docs,
                     state="readonly", font=("Segoe UI",9), width=18).pack(side="left", padx=(4,16))

        tk.Label(r2, text="Status:", bg=WHITE, fg=TEXT_MID,
                 font=("Segoe UI",9)).pack(side="left")
        self.av_status = tk.StringVar(value="All")
        ttk.Combobox(r2, textvariable=self.av_status,
                     values=["All","Booked","Completed","Cancelled"],
                     state="readonly", font=("Segoe UI",9), width=12).pack(side="left", padx=4)

    def _build_table(self, parent=None):
        if parent is None: parent = self
        tf = tk.Frame(parent, bg=WHITE)
        tf.pack(fill="x", padx=18, pady=(0,4))

        cols = ("Appointment ID","Patient ID","Full Name","Doctor","Date","Time","Status")
        self._tree = ttk.Treeview(tf, columns=cols, show="headings",
                                   style="AuraTree.Treeview", height=8)
        widths = [110,90,160,150,100,90,100]
        for col, w in zip(cols, widths):
            self._tree.heading(col, text=col)
            self._tree.column(col, width=w, anchor="center" if col in ("Date","Time","Status") else "w")

        self._tree.tag_configure("odd",      background=WHITE)
        self._tree.tag_configure("even",     background=ROW_ALT)

        vsb = ttk.Scrollbar(tf, orient="vertical",   command=self._tree.yview)
        hsb = ttk.Scrollbar(tf, orient="horizontal", command=self._tree.xview)
        self._tree.configure(yscroll=vsb.set, xscroll=hsb.set)
        self._tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        tf.rowconfigure(0, weight=1); tf.columnconfigure(0, weight=1)

        self._count_lbl = tk.Label(parent, text="Showing 0 entries",
                                    bg=WHITE, fg=TEXT_MID, font=("Segoe UI",8))
        self._count_lbl.pack(anchor="w", padx=18)

        self._tree.bind("<<TreeviewSelect>>", self._on_select)

    def _build_detail_area(self, parent=None):
        if parent is None: parent = self
        bot = tk.Frame(parent, bg=WHITE)
        bot.pack(fill="x", padx=18, pady=(6, 18))
        bot.columnconfigure(0, weight=2); bot.columnconfigure(1, weight=1)

        # Left: detail card
        dl = tk.LabelFrame(bot, text="  Appointment Details", bg=WHITE,
                           fg=TEAL, font=("Segoe UI",9,"bold"),
                           bd=1, relief="solid")
        dl.grid(row=0, column=0, sticky="nsew", padx=(0,10))

        self._detail_vars = {}
        detail_fields = [
            ("Appointment ID:",  "appt_id"),
            ("Patient ID:",      "patient_id"),
            ("Full Name:",       "name"),
            ("Doctor:",          "doctor"),
            ("Department:",      "dept"),
            ("Appointment Date:","date"),
            ("Appointment Time:","time"),
            ("Status:",          "status"),
            ("Notes:",           "notes"),
        ]
        df = tk.Frame(dl, bg=WHITE); df.pack(fill="x", padx=10, pady=6)
        for i, (label, key) in enumerate(detail_fields):
            r, c = divmod(i, 2)
            tk.Label(df, text=label, bg=WHITE, fg=TEXT_MID,
                     font=("Segoe UI",9), anchor="e", width=16).grid(
                         row=r, column=c*2, sticky="e", padx=(4,2), pady=3)
            var = tk.StringVar()
            self._detail_vars[key] = var
            if key == "status":
                self._status_lbl = tk.Label(df, textvariable=var,
                                             bg="#1787AE", fg=WHITE,
                                             font=("Segoe UI",8,"bold"),
                                             padx=8, pady=2, relief="flat")
                self._status_lbl.grid(row=r, column=c*2+1, sticky="w", padx=(0,12), pady=3)
            else:
                tk.Label(df, textvariable=var, bg=WHITE, fg=TEXT_DARK,
                         font=("Segoe UI",9,"bold"), anchor="w").grid(
                             row=r, column=c*2+1, sticky="ew", padx=(0,12), pady=3)

        df.columnconfigure(1, weight=1); df.columnconfigure(3, weight=1)

        # Action buttons below details
        bf = tk.Frame(dl, bg=WHITE); bf.pack(fill="x", padx=10, pady=(4,10))
        vd_ico  = load_icon("View Details icon.png",     (16,16))
        ea_ico  = load_icon("Edit Appointment icon.png", (16,16))
        ca_ico  = load_icon("Cancel Appointment icon.png",(16,16))
        mc_ico  = load_icon("Mark as completed icon.png",(16,16))
        for i in [vd_ico, ea_ico, ca_ico, mc_ico]:
            if i: self.app._icon_store[id(i)] = i

        _btn(bf,"View Details",    TEAL,        icon=vd_ico, cmd=self._view_details,  pady=6).pack(side="left",padx=(0,6))
        _btn(bf,"Edit Appointment",EDIT_ORANGE, icon=ea_ico, cmd=self._edit,          pady=6).pack(side="left",padx=(0,6))
        _btn(bf,"Cancel Appointment",CANCEL_RED,icon=ca_ico, cmd=self._cancel_appt,   pady=6).pack(side="left",padx=(0,6))
        _btn(bf,"Mark as Completed",COMPLETE_GR,icon=mc_ico, cmd=self._mark_complete, pady=6).pack(side="left")

        # Right: summary card
        sr = tk.LabelFrame(bot, text="  Appointment Summary", bg=WHITE,
                           fg=TEAL, font=("Segoe UI",9,"bold"),
                           bd=1, relief="solid")
        sr.grid(row=0, column=1, sticky="nsew")

        self._summ_labels = {}
        summ_rows = [
            ("Total Appointments", "total"),
            ("Booked",             "booked"),
            ("Completed (Seen)",   "completed"),
            ("Cancelled",          "cancelled"),
        ]
        sf = tk.Frame(sr, bg=WHITE); sf.pack(fill="x", padx=10, pady=8)
        sf.columnconfigure(0, weight=1)
        for i, (label, key) in enumerate(summ_rows):
            tk.Label(sf, text=label, bg=WHITE, fg=TEXT_MID,
                     font=("Segoe UI",9)).grid(row=i, column=0, sticky="w", pady=4)
            lbl = tk.Label(sf, text="0", bg=WHITE, fg=TEXT_DARK,
                           font=("Segoe UI",10,"bold"))
            lbl.grid(row=i, column=1, sticky="e", padx=6, pady=4)
            self._summ_labels[key] = lbl

        self._refresh_summary()

    def _do_search(self, _=None):
        kw     = self.av_kw.get().strip().lower()
        by     = self.av_by.get()
        doc    = self.av_doc.get()
        status = self.av_status.get()
        d_from = self.av_from.get().strip()
        d_to   = self.av_to.get().strip()

        results = []
        for a in APPOINTMENTS:
            if kw:
                if by == "Appointment ID":
                    if kw not in a["appt_id"].lower(): continue
                else:
                    if kw not in a["patient_id"].lower() and kw not in a["name"].lower():
                        continue
            if doc    != "All" and a["doctor"] != doc:      continue
            if status != "All" and a["status"] != status:   continue
            if d_from and a["date"] < d_from:               continue
            if d_to   and a["date"] > d_to:                 continue
            results.append(a)

        for row in self._tree.get_children():
            self._tree.delete(row)
        for i, a in enumerate(results):
            tag = "even" if i%2==0 else "odd"
            self._tree.insert("", "end", iid=a["appt_id"],
                              values=(a["appt_id"],a["patient_id"],a["name"],
                                      a["doctor"],a["date"],a["time"],a["status"]),
                              tags=(tag,))
        self._count_lbl.config(
            text=f"Showing 1 to {len(results)} of {len(results)} entries")
        self._refresh_summary()

    def _on_select(self, _):
        sel = self._tree.selection()
        if not sel: return
        aid = sel[0]
        for a in APPOINTMENTS:
            if a["appt_id"] == aid:
                self._sel_appt = a
                for key, var in self._detail_vars.items():
                    var.set(a.get(key,""))
                color = STATUS_COLORS.get(a["status"], TEAL)
                self._status_lbl.config(bg=color)
                return

    def _view_details(self):
        if not self._sel_appt:
            messagebox.showinfo("View Details","Select an appointment first."); return
        a = self._sel_appt
        info = "\n".join([f"Appointment ID : {a['appt_id']}",
                          f"Patient ID     : {a['patient_id']}",
                          f"Full Name      : {a['name']}",
                          f"Doctor         : {a['doctor']}",
                          f"Department     : {a['dept']}",
                          f"Date           : {a['date']}",
                          f"Time           : {a['time']}",
                          f"Type           : {a['type']}",
                          f"Status         : {a['status']}",
                          f"Notes          : {a['notes']}"])
        messagebox.showinfo("Appointment Details", info)

    def _edit(self):
        if not self._sel_appt:
            messagebox.showinfo("Edit","Select an appointment first."); return
        a = self._sel_appt
        if a["status"] == "Cancelled":
            messagebox.showwarning("Edit","Cannot edit a cancelled appointment."); return
        # Open a simple edit dialog
        EditAppointmentDialog(self, a, self._after_edit)

    def _after_edit(self, updated):
        conflict = any(a["doctor"] == updated["doctor"] and a["date"] == updated["date"]   # ← new
                       and a["time"] == updated["time"] and a["status"] != "Cancelled"     # ← new
                       and a["appt_id"] != updated["appt_id"] for a in APPOINTMENTS)        # ← new
        if conflict:                                                                       # ← new
            messagebox.showerror("Conflict",                                               # ← new
                f"{updated['doctor']} already has an appointment at {updated['time']} on {updated['date']}.")  # ← new
            return                                                                          # ← new
        for i, a in enumerate(APPOINTMENTS):
            if a["appt_id"] == updated["appt_id"]:
                APPOINTMENTS[i] = updated; break
        self._sel_appt = updated  
        self._do_search()
        self._on_select(None)   

    def _cancel_appt(self):
        if not self._sel_appt:
            messagebox.showinfo("Cancel","Select an appointment first."); return
        a = self._sel_appt
        if a["status"] == "Cancelled":
            messagebox.showinfo("Cancel","Already cancelled."); return
        if messagebox.askyesno("Cancel Appointment",
                               f"Cancel appointment {a['appt_id']} for {a['name']}?"):
            a["status"] = "Cancelled"
            self._do_search()
            self._detail_vars["status"].set("Cancelled")
            self._status_lbl.config(bg=STATUS_COLORS["Cancelled"])

    def _mark_complete(self):
        if not self._sel_appt:
            messagebox.showinfo("Mark Complete","Select an appointment first."); return
        a = self._sel_appt
        if a["status"] == "Completed":
            messagebox.showinfo("Mark Complete","Already completed."); return
        if a["status"] == "Cancelled":
            messagebox.showwarning("Mark Complete","Cannot complete a cancelled appointment."); return
        a["status"] = "Completed"
        self._do_search()
        self._detail_vars["status"].set("Completed")
        self._status_lbl.config(bg=STATUS_COLORS["Completed"])

    def _reset(self):
        self.av_kw.set(""); self.av_from.set(""); self.av_to.set("")
        self.av_by.set("Patient ID / Full Name")
        self.av_doc.set("All"); self.av_status.set("All")
        self._do_search()

    def _refresh_summary(self):
        total     = len(APPOINTMENTS)
        booked    = sum(1 for a in APPOINTMENTS if a["status"] == "Booked")
        completed = sum(1 for a in APPOINTMENTS if a["status"] == "Completed")
        cancelled = sum(1 for a in APPOINTMENTS if a["status"] == "Cancelled")
        self._summ_labels["total"].config(text=str(total))
        self._summ_labels["booked"].config(text=str(booked))
        self._summ_labels["completed"].config(text=str(completed))
        self._summ_labels["cancelled"].config(text=str(cancelled))


# ── Edit Appointment Dialog ────────────────────────────────────────────────────
class EditAppointmentDialog(tk.Toplevel):

    def __init__(self, parent, appt, on_save):
        super().__init__(parent)
        self.appt    = dict(appt)
        self.on_save = on_save
        self.title(f"Edit Appointment — {appt['appt_id']}")
        self.geometry("480x400")
        self.resizable(False, False)
        self.configure(bg=WHITE)
        self.grab_set()
        self._build()

    def _build(self):
        tk.Label(self, text=f"Edit Appointment {self.appt['appt_id']}",
                 bg=WHITE, fg=TEAL, font=("Segoe UI",12,"bold")).pack(pady=(16,10))

        f = tk.Frame(self, bg=WHITE); f.pack(fill="x", padx=30)
        f.columnconfigure(1, weight=1)

        fields = [
            ("Doctor",    "doctor",   None),
            ("Date",      "date",     None),
            ("Time",      "time",     TIME_SLOTS),
            ("Type",      "type",     APPT_TYPES),
            ("Status",    "status",   ["Booked","Completed","Cancelled"]),
            ("Notes",     "notes",    None),
        ]
        self._vars = {}
        for i, (label, key, opts) in enumerate(fields):
            tk.Label(f, text=f"{label}:", bg=WHITE, fg=TEXT_MID,
                     font=("Segoe UI",9)).grid(row=i, column=0, sticky="e",
                                                padx=(0,8), pady=6)
            var = tk.StringVar(value=self.appt.get(key,""))
            self._vars[key] = var
            if opts:
                cb = ttk.Combobox(f, textvariable=var, values=opts,
                                  font=("Segoe UI",10), state="readonly")
                cb.grid(row=i, column=1, sticky="ew", pady=6)
            else:
                tk.Entry(f, textvariable=var, font=("Segoe UI",10),
                         bd=1, relief="solid").grid(row=i, column=1,
                                                     sticky="ew", pady=6)

        bf = tk.Frame(self, bg=WHITE); bf.pack(pady=16)
        _btn(bf, "Save",   SAVE_DARK, cmd=self._save,  pady=8).pack(side="left", padx=8)
        _btn(bf, "Cancel", "#6c757d", cmd=self.destroy,pady=8).pack(side="left", padx=8)

    def _save(self):
        for key, var in self._vars.items():
            self.appt[key] = var.get()
        self.on_save(self.appt)
        self.destroy()


# ── Stand-alone entry point (testing without login) ───────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app  = RegisterPatientApp(root, username="Admin")
    app.protocol("WM_DELETE_WINDOW", root.destroy)
    root.mainloop()
