"""
AuraClinic Login Page — Python tkinter
After successful login → opens the Register Patient Dashboard.
Only needs: pip install Pillow
Left panel loads from 'Login page1.png' placed in the same folder.
"""

import tkinter as tk
from tkinter import messagebox
import os

try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except Exception as e:
    HAS_PIL = False
    print(f"[WARN] Pillow not available: {e}")

# Import the dashboard (must be in the same folder)
try:
    from register_patient import RegisterPatientApp
    HAS_DASHBOARD = True
except Exception as ex:
    HAS_DASHBOARD = False
    print(f"[WARN] Could not import register_patient: {ex}")

# ── Palette ───────────────────────────────────────────────────────────────────
TEAL      = "#1787AE"
BTN_BLUE  = "#5BBFDE"
BTN_HOVER = "#3aa8cc"
WHITE     = "#FFFFFF"
INPUT_BD  = "#D0DCE8"
TEXT_DARK = "#1a2e44"
LEFT_BG   = "#daeef6"

WIN_W, WIN_H = 1100, 700
SPLIT        = 530
PNG_W        = 1440
CROP_AT      = 880

PNG_NAMES = ["Login page1.png"]

# ──  credentials (username → password) ────────────────────────────────────
VALID_USERS = {
    "admin":   "admin123",
    "doctor":  "doc2025",
    "nurse":   "nurse2025",}


# ── Load & crop left panel ────────────────────────────────────────────────────
def load_panel(w, h):
    if not HAS_PIL:
        return None
    script_dir = os.path.dirname(os.path.abspath(__file__))
    for name in PNG_NAMES:
        path = os.path.join(script_dir, name)
        if os.path.exists(path):
            try:
                img      = Image.open(path).convert("RGBA")
                crop_px  = int(img.width * CROP_AT / PNG_W)
                img      = img.crop((0, 0, crop_px, img.height))
                img      = img.resize((w, h), Image.LANCZOS)
                print(f"[OK] Loaded panel from: {name}")
                return ImageTk.PhotoImage(img)
            except Exception as exc:
                print(f"[WARN] Failed to load {name}: {exc}")
    print("[WARN] No image found — showing plain background.")
    return None


# ── Password entry with show/hide ─────────────────────────────────────────────
class PasswordEntry(tk.Frame):
    def __init__(self, parent, **kw):
        super().__init__(parent, bg=WHITE, **kw)
        self._showing = False

        self.entry = tk.Entry(
            self, show="\u2022",
            font=("Segoe UI", 11), bd=0, bg=WHITE,
            fg=TEXT_DARK, highlightthickness=0
        )
        self.entry.pack(side="left", fill="both", expand=True, padx=(12, 0), ipady=7)

        self._eye_btn = tk.Button(
            self, text="👁", bg=WHITE, fg="#999",
            font=("Segoe UI", 10), bd=0, cursor="hand2",
            activebackground=WHITE, relief="flat",
            command=self._toggle
        )
        self._eye_btn.pack(side="right", padx=6)

    def _toggle(self):
        self._showing = not self._showing
        self.entry.config(show="" if self._showing else "\u2022")

    def get(self):
        return self.entry.get()


# ── Main Login App ────────────────────────────────────────────────────────────
class AuraClinicLogin(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("AuraClinic — Login")
        self.geometry(f"{WIN_W}x{WIN_H}")
        self.resizable(True, True)
        self.configure(bg=TEAL)
        self._img       = None
        self._last_size = (WIN_W, WIN_H)

        self.bind("<Configure>", self._on_resize)
        self._build_left()
        self._build_right()

    # ── Responsive resize ─────────────────────────────────────────────────────
    def _on_resize(self, event):
        w, h = self.winfo_width(), self.winfo_height()
        if (w, h) == self._last_size:
            return
        self._last_size = (w, h)
        split = max(200, int(w * (SPLIT / WIN_W)))

        cv = pnl = None
        for child in self.winfo_children():
            if isinstance(child, tk.Canvas):
                cv = child
            elif isinstance(child, tk.Frame):
                pnl = child

        if cv:
            cv.config(width=split, height=h)
            img = load_panel(split, h)
            if img:
                self._img = img
                cv.delete("all")
                cv.create_image(0, 0, anchor="nw", image=img)
            else:
                cv.delete("all")
                cv.create_text(split // 2, h // 2 - 30,
                               text="AuraClinic", fill=TEAL,
                               font=("Segoe UI", 32, "bold"), anchor="center")
        if pnl:
            pnl.place(x=split, y=0, width=max(w - split, 200), height=h)

    # ── Left illustration panel ───────────────────────────────────────────────
    def _build_left(self):
        cv = tk.Canvas(self, width=SPLIT, height=WIN_H,
                       bg=LEFT_BG, highlightthickness=0)
        cv.place(x=0, y=0)
        img = load_panel(SPLIT, WIN_H)
        if img:
            self._img = img
            cv.create_image(0, 0, anchor="nw", image=img)
        else:
            cv.create_text(SPLIT // 2, WIN_H // 2 - 30,
                           text="AuraClinic",
                           fill=TEAL, font=("Segoe UI", 32, "bold"), anchor="center")
            cv.create_text(SPLIT // 2, WIN_H // 2 + 20,
                           text="Place 'Login page1.png' here\nto show the illustration",
                           fill="#888", font=("Segoe UI", 11),
                           anchor="center", justify="center")

    # ── Right login form ──────────────────────────────────────────────────────
    def _build_right(self):
        pnl = tk.Frame(self, bg=TEAL, width=WIN_W - SPLIT, height=WIN_H)
        pnl.place(x=SPLIT, y=0)
        pnl.pack_propagate(False)

        # Vertical centring spacer
        tk.Frame(pnl, bg=TEAL,
                 height=max((WIN_H - 420) // 2, 30)).pack()

        tk.Label(pnl, text="Log In", bg=TEAL, fg=WHITE,
                 font=("Segoe UI", 28, "bold")).pack(pady=(0, 22))

        form = tk.Frame(pnl, bg=TEAL)
        form.pack(fill="x", padx=44)

        # ── Username ──────────────────────────────────────────────────────────
        tk.Label(form, text="Username*", bg=TEAL, fg=WHITE,
                 font=("Segoe UI", 11, "bold")).pack(anchor="w")
        tk.Frame(form, bg=TEAL, height=5).pack()

        u_box = tk.Frame(form, bg=WHITE,
                         highlightbackground=INPUT_BD, highlightthickness=1)
        u_box.pack(fill="x")
        self.u_entry = tk.Entry(u_box, fg="#aaa", bg=WHITE,
                                font=("Segoe UI", 11), bd=0,
                                highlightthickness=0)
        self.u_entry.insert(0, "Enter Your Username")
        self.u_entry.pack(fill="x", padx=12, ipady=9)

        def u_in(e):
            if self.u_entry.get() == "Enter Your Username":
                self.u_entry.delete(0, "end")
                self.u_entry.config(fg=TEXT_DARK)

        def u_out(e):
            if not self.u_entry.get().strip():
                self.u_entry.insert(0, "Enter Your Username")
                self.u_entry.config(fg="#aaa")

        self.u_entry.bind("<FocusIn>",  u_in)
        self.u_entry.bind("<FocusOut>", u_out)

        tk.Frame(form, bg=TEAL, height=16).pack()

        # ── Password ──────────────────────────────────────────────────────────
        tk.Label(form, text="Password*", bg=TEAL, fg=WHITE,
                 font=("Segoe UI", 11, "bold")).pack(anchor="w")
        tk.Frame(form, bg=TEAL, height=5).pack()

        p_box = tk.Frame(form, bg=WHITE,
                         highlightbackground=INPUT_BD, highlightthickness=1)
        p_box.pack(fill="x")
        self.pw = PasswordEntry(p_box)
        self.pw.pack(fill="x")
        self.pw.entry.config(show="", fg="#aaa")
        self.pw.entry.insert(0, "Enter Your Password")

        def p_in(e):
            if self.pw.entry.get() == "Enter Your Password":
                self.pw.entry.delete(0, "end")
                self.pw.entry.config(fg=TEXT_DARK, show="\u2022")

        def p_out(e):
            if not self.pw.entry.get().strip():
                self.pw.entry.config(show="", fg="#aaa")
                self.pw.entry.insert(0, "Enter Your Password")

        self.pw.entry.bind("<FocusIn>",  p_in)
        self.pw.entry.bind("<FocusOut>", p_out)

        # Allow Enter key to submit
        self.u_entry.bind("<Return>", lambda e: self._login())
        self.pw.entry.bind("<Return>", lambda e: self._login())

        tk.Frame(form, bg=TEAL, height=6).pack()

        # Forgot password link
        fp = tk.Label(form, text="Forget Password?",
                      bg=TEAL, fg="#c8eaf5",
                      font=("Segoe UI", 9, "underline"), cursor="hand2")
        fp.pack(anchor="e")
        fp.bind("<Button-1>", lambda e: messagebox.showinfo(
            "Forget Password",
            "A reset link will be sent to your registered email."))

        tk.Frame(form, bg=TEAL, height=22).pack()

        # Login button
        self.btn = tk.Button(
            form, text="Login", bg=BTN_BLUE, fg=WHITE,
            font=("Segoe UI", 12, "bold"),
            bd=0, relief="flat", cursor="hand2",
            activebackground=BTN_HOVER,
            command=self._login
        )
        self.btn.pack(fill="x", ipady=11)
        self.btn.bind("<Enter>", lambda e: self.btn.config(bg=BTN_HOVER))
        self.btn.bind("<Leave>", lambda e: self.btn.config(bg=BTN_BLUE))

        tk.Frame(form, bg=TEAL, height=20).pack()

        # Register row
        row = tk.Frame(form, bg=TEAL)
        row.pack()
        tk.Label(row, text="Don't have an account?  ",
                 bg=TEAL, fg=WHITE, font=("Segoe UI", 10)).pack(side="left")
        reg = tk.Label(row, text="Register Now", bg=TEAL, fg=WHITE,
                       font=("Segoe UI", 10, "bold", "underline"), cursor="hand2")
        reg.pack(side="left")
        reg.bind("<Button-1>", lambda e: messagebox.showinfo(
            "Register", "Please contact your system administrator\nto create an account."))

       
    # ── Login logic ───────────────────────────────────────────────────────────
    def _login(self):
        u = self.u_entry.get().strip()
        p = self.pw.get().strip()

        if not u or u == "Enter Your Username":
            messagebox.showwarning("Validation", "Please enter your username.")
            return
        if not p or p == "Enter Your Password":
            messagebox.showwarning("Validation", "Please enter your password.")
            return

        # Credential check
        if VALID_USERS.get(u.lower()) == p:
            self._open_dashboard(u)
        else:
            messagebox.showerror(
                "Login Failed",
                "Incorrect username or password.\nPlease try again.")
            # Clear password field on failure
            self.pw.entry.config(show="", fg="#aaa")
            self.pw.entry.delete(0, "end")
            self.pw.entry.insert(0, "Enter Your Password")

    def _open_dashboard(self, username):
        """Hide login window and launch the Register Patient dashboard."""
        self.withdraw()          # hide login (don't destroy — keeps mainloop alive)

        if HAS_DASHBOARD:
            dash = RegisterPatientApp(self, username=username.capitalize())
            # If dashboard is closed bring login back (or fully quit)
            dash.protocol("WM_DELETE_WINDOW", lambda: self._dashboard_closed(dash))
        else:
            messagebox.showerror(
                "Missing File",
                "register_patient.py not found.\n"
                "Place it in the same folder as login_page.py.")
            self.deiconify()    # show login again

    def _dashboard_closed(self, dash):
        """Called when the dashboard window is closed."""
        dash.destroy()
        self.destroy()          # quit the whole application


if __name__ == "__main__":
    app = AuraClinicLogin()
    app.mainloop()
