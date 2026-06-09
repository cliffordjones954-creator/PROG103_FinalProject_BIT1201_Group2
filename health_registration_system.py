import sqlite3, tkinter as tk
from tkinter import ttk, messagebox

#Database Setup 
def init_db():
    conn=sqlite3.connect("clinic.db"); c=conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS Doctors(" 
    "doctor_id INTEGER PRIMARY KEY AUTOINCREMENT," 
    "name TEXT,"
    "specialization TEXT," 
    "fee REAL)")
    c.execute("CREATE TABLE IF NOT EXISTS Patients("
    "patient_id INTEGER PRIMARY KEY AUTOINCREMENT," 
    "name TEXT," 
    "contact INTEGER(9)," 
    "age INTEGER)")
    c.execute("CREATE TABLE IF NOT EXISTS Appointments(" 
    "appointment_id INTEGER PRIMARY KEY AUTOINCREMENT," 
    "patient_id INTEGER," 
    "doctor_id INTEGER," 
    "date DATE," 
    "time TIME," 
    "status TEXT," 
    "FOREIGN KEY(patient_id) REFERENCES Patients(patient_id)," 
    "FOREIGN KEY(doctor_id) REFERENCES Doctors(doctor_id))")
    conn.commit(); conn.close()

def insert_sample_doctors():
    conn=sqlite3.connect("clinic.db"); c=conn.cursor()
    if c.execute("SELECT COUNT(*) FROM Doctors").fetchone()[0]==0:
        docs=[("Dr. Mariama Conteh","General Practitioner",150),
              ("Dr. Abdul Kamara","Pediatrics",200),
              ("Dr. Fatmata Sesay","Cardiology",300)]
        c.executemany("INSERT INTO Doctors(name,specialization,fee) VALUES(?,?,?)",docs)
    conn.commit(); conn.close()

#Functions 
def run_query(q,p=(),fetch=False):
    conn=sqlite3.connect("clinic.db"); c=conn.cursor()
    c.execute(q,p); r=c.fetchall() if fetch else None
    conn.commit(); conn.close(); return r

def search_patient(pid):
    return run_query("SELECT * FROM Patients WHERE patient_id=?", (pid,), True)

def book_appointment(patient_id, doctor_id, date, time):
    clash = run_query(
        "SELECT * FROM Appointments WHERE doctor_id=? AND date=? AND time=? AND status!='Cancelled'",
        (doctor_id, date, time),
        True
    )
    if clash:
        return False
    run_query(
        "INSERT INTO Appointments(patient_id, doctor_id, date, time, status) VALUES(?,?,?,?,?)",
        (patient_id, doctor_id, date, time, "Scheduled")
    )
    return True

def reschedule_appointment(aid, date, time):
    appt = run_query("SELECT doctor_id FROM Appointments WHERE appointment_id=?", (aid,), True)
    if not appt:
        return False
    doctor_id = appt[0][0]
    clash = run_query(
        "SELECT * FROM Appointments WHERE doctor_id=? AND date=? AND time=? AND status!='Cancelled' AND appointment_id!=?",
        (doctor_id, date, time, aid),
        True
    )
    if clash:
        return False
    run_query("UPDATE Appointments SET date=?, time=? WHERE appointment_id=?", (date, time, aid))
    return True

def cancel_appointment(aid):
    run_query("UPDATE Appointments SET status='Cancelled' WHERE appointment_id=?", (aid,))

def update_appt(aid,date,time,status): 
    run_query("UPDATE Appointments SET date=?,time=?,status=? WHERE appointment_id=?",(date,time,status,aid))
def get_appointments(): 
    return run_query("""SELECT a.appointment_id,p.name,d.name,a.date,a.time,a.status FROM Appointments a JOIN Patients p ON a.patient_id=p.patient_id JOIN Doctors d ON a.doctor_id=d.doctor_id""",fetch=True)
def get_total():
    return run_query("SELECT COUNT(*) FROM Appointments",fetch=True)[0][0]

# Login 
users={"admin":"1234","staff":"0000"}
def login_screen(root):
    win=tk.Toplevel(root); win.title("Login")
    u,p=tk.Entry(win),tk.Entry(win,show="*")
    tk.Label(win,text="Username").grid(row=0,column=0); u.grid(row=0,column=1)
    tk.Label(win,text="Password").grid(row=1,column=0); p.grid(row=1,column=1)
    def attempt():
        if users.get(u.get())==p.get(): win.destroy(); main_gui(root)
        else: messagebox.showerror("Error","Invalid credentials")
    tk.Button(win,text="Login",command=attempt).grid(row=2,column=0,columnspan=2)

# Tabs
def registration_tab(f):
    n,c,a=tk.Entry(f),tk.Entry(f),tk.Entry(f)
    for i,(lbl,e) in enumerate([("Name",n),("Contact",c),("Age",a)]): tk.Label(f,text=lbl).grid(row=i,column=0); e.grid(row=i,column=1)
    tk.Button(f,text="Register",command=lambda:[search_patient("0"),run_query("INSERT INTO Patients(name,contact,age) VALUES(?,?,?)",(n.get(),c.get(),a.get())),messagebox.showinfo("OK","Registered")]).grid(row=3,column=0,columnspan=2)
    s=tk.Entry(f); tk.Label(f,text="Patient ID").grid(row=4,column=0); s.grid(row=4,column=1)
    tk.Button(f,text="Search",command=lambda:messagebox.showinfo("Result",search_patient(s.get()) or "Not found")).grid(row=5,column=0,columnspan=2)

def booking_tab(frame_booking):
    # Patient ID
    tk.Label(frame_booking, text="Patient ID").grid(row=0, column=0, padx=5, pady=5)
    entry_patient = tk.Entry(frame_booking)
    entry_patient.grid(row=0, column=1, padx=5, pady=5)

    # Doctor Dropdown
    tk.Label(frame_booking, text="Select Doctor").grid(row=1, column=0, padx=5, pady=5)
    conn = sqlite3.connect("clinic.db")
    cursor = conn.cursor()
    cursor.execute("SELECT doctor_id, name, fee FROM Doctors")
    doctors = cursor.fetchall()
    conn.close()

    doctor_dict = {name: (doc_id, fee) for doc_id, name, fee in doctors}
    doctor_names = list(doctor_dict.keys())

    combo_doctor = ttk.Combobox(frame_booking, values=doctor_names, state="readonly")
    combo_doctor.grid(row=1, column=1, padx=5, pady=5)

    # Fee display
    label_fee = tk.Label(frame_booking, text="Fee: ")
    label_fee.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    def update_fee(event):
        doctor_name = combo_doctor.get()
        if doctor_name in doctor_dict:
            fee = doctor_dict[doctor_name][1]
            label_fee.config(text=f"Fee: {fee} Leones")

    combo_doctor.bind("<<ComboboxSelected>>", update_fee)

    # Date entry
    tk.Label(frame_booking, text="Date (YYYY-MM-DD)").grid(row=3, column=0, padx=5, pady=5)
    entry_date = tk.Entry(frame_booking)
    entry_date.grid(row=3, column=1, padx=5, pady=5)

    # Time entry
    tk.Label(frame_booking, text="Time (HH:MM)").grid(row=4, column=0, padx=5, pady=5)
    entry_time = tk.Entry(frame_booking)
    entry_time.grid(row=4, column=1, padx=5, pady=5)

    # patient validation
    def handle_booking():
        patient_id = entry_patient.get()
        doctor_name = combo_doctor.get()
        doctor_info = doctor_dict.get(doctor_name)
        doctor_id = doctor_info[0] if doctor_info else None
        date = entry_date.get()
        time = entry_time.get()

        if not patient_id or not doctor_id or not date or not time:
            messagebox.showerror("Error", "Please fill all fields.")
            return

        if not search_patient(patient_id):
            messagebox.showerror("Error", "Patient ID not found.")
            return

        ok = book_appointment(patient_id, doctor_id, date, time)
        if ok:
            messagebox.showinfo("Success", f"Appointment booked with {doctor_name}!")
        else:
            messagebox.showerror("Error", "Doctor already booked at that time.")

    tk.Button(frame_booking, text="Book Appointment", command=handle_booking).grid(row=5, column=0, columnspan=2, pady=10)

    # Reschedule
    tk.Label(frame_booking, text="Appointment ID").grid(row=6, column=0, padx=5, pady=5)
    entry_appt_id = tk.Entry(frame_booking)
    entry_appt_id.grid(row=6, column=1, padx=5, pady=5)

    tk.Label(frame_booking, text="New Date").grid(row=7, column=0, padx=5, pady=5)
    entry_new_date = tk.Entry(frame_booking)
    entry_new_date.grid(row=7, column=1, padx=5, pady=5)

    tk.Label(frame_booking, text="New Time").grid(row=8, column=0, padx=5, pady=5)
    entry_new_time = tk.Entry(frame_booking)
    entry_new_time.grid(row=8, column=1, padx=5, pady=5)

    def handle_reschedule():
        appt_id = entry_appt_id.get()
        new_date = entry_new_date.get()
        new_time = entry_new_time.get()
        if appt_id and new_date and new_time:
            reschedule_appointment(appt_id, new_date, new_time)
            messagebox.showinfo("Success", "Appointment rescheduled successfully!")
        else:
            messagebox.showerror("Error", "Please fill all fields.")

    tk.Button(frame_booking, text="Reschedule Appointment", command=handle_reschedule).grid(row=9, column=0, columnspan=2, pady=10)

    # Cancel
    def handle_cancel():
        appt_id = entry_appt_id.get()
        if appt_id:
            cancel_appointment(appt_id)
            messagebox.showinfo("Success", "Appointment cancelled successfully!")
        else:
            messagebox.showerror("Error", "Enter Appointment ID to cancel.")

    tk.Button(frame_booking, text="Cancel Appointment", command=handle_cancel).grid(row=10, column=0, columnspan=2, pady=10)

def confirmation_tab(f):
    cols=("ID","Patient","Doctor","Date","Time","Status")
    tree=ttk.Treeview(f,columns=cols,show="headings"); [tree.heading(c,text=c) for c in cols]; tree.pack(expand=True,fill="both")
    def refresh():
        [tree.delete(i) for i in tree.get_children()]
        [tree.insert("", "end", values=r) for r in get_appointments()]
        messagebox.showinfo("Statistics",f"Total Appointments: {get_total()}")
    tk.Button(f,text="Refresh",command=refresh).pack()

# --- Main GUI ---
def main_gui(root):
    nb=ttk.Notebook(root)
    for tab,name,func in [(ttk.Frame(nb),"Register",registration_tab),(ttk.Frame(nb),"Appointments",booking_tab),(ttk.Frame(nb),"Confirmation",confirmation_tab)]:
        nb.add(tab,text=name); func(tab)
    nb.pack(expand=True,fill="both")

if __name__=="__main__":
    init_db(); insert_sample_doctors()
    root=tk.Tk(); root.title("Clinic System"); root.geometry("800x500")
    login_screen(root); root.mainloop()
