# AuraClinic — Healthcare Management System

A desktop healthcare management application built with **Python** and **tkinter**, designed to help small to medium-sized clinics digitize patient registration, appointment scheduling, and record management — without requiring a database server or internet connection.


---

## 📋 Overview

AuraClinic replaces error-prone, paper-based clinic workflows with a clean, navigable desktop interface. After logging in, staff can register patients, book appointments with real-time slot availability, manage the full appointment lifecycle, and search patient records using multiple filters.

This project was built as a final project for **PROG103 — Principles of Structured Programming**.

---

## ✨ Features

- 🔐 **Secure Login** — Username/password authentication with a show/hide password toggle
- 🧑‍⚕️ **Register Patient** — Add, update, delete, and browse patient records
- 📅 **Book Appointment** — Department/doctor selection with a live, color-coded time-slot grid that blocks double-bookings
- 📋 **Appointment Records** — Search, filter, view, edit, cancel, and mark appointments as completed
- 🔎 **Search Patient** — Multi-filter search (ID, name, phone, gender, blood group, date range) with CSV export
- 🖥️ **Single-window navigation** — All pages load inside one persistent application shell with a live clock and sidebar menu

---

## 🗂️ Project Structure

```
AuraClinic/
├── login_page.py          # Login window (entry point of the application)
├── register_patient.py    # Main application shell + all 4 pages
├── Login page1.png         # Illustration shown on the login screen
└── Logo and icons/         # Icons and header image used throughout the app
    ├── image.png
    ├── Vector.png
    ├── Calender icon.png
    ├── appointment records icon.png
    ├── Search patient icon.png
    ├── log-out icon.png
    ├── home icon.png
    ├── Save patient icon.png
    ├── update icon.png
    ├── delete icon.png
    ├── clear icon.png
    ├── reseticon.png
    ├── export icon.png
    ├── View Details icon.png
    ├── Edit Appointment icon.png
    ├── Cancel Appointment icon.png
    └── Mark as completed icon.png
```

> ⚠️ All files and folders must stay in the **same directory** for the app to find the images correctly.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- [Pillow](https://pillow.readthedocs.io/) (the only external dependency)

### Installation

```bash
git clone https://github.com/<your-username>/AuraClinic.git
cd AuraClinic
pip install Pillow
```

### Run the app

```bash
python login_page.py
```

### Demo credentials

| Username | Password   |
|----------|------------|
| admin    | admin123   |
| doctor   | doc2025    |
| nurse    | nurse2025  |

---

## 🖥️ Pages

| Page | Description |
|------|-------------|
| **Login** | Validates credentials and launches the main dashboard |
| **Register Patient** | Form-based CRUD for patient records, with a live patient list table |
| **Book Appointment** | Patient lookup, department/doctor selection, and an interactive time-slot picker |
| **Appointment Records** | Search/filter appointments and manage their status (Booked / Completed / Cancelled) |
| **Search Patient** | Advanced multi-field patient search with CSV export |

---

## 🛠️ Built With

- **Python 3** — core application logic
- **tkinter** — GUI framework
- **Pillow (PIL)** — image and icon rendering
- **ttk.Treeview** — data tables for patients and appointments

---

## 🧱 Architecture Notes

- All patient and appointment data is held in shared in-memory lists (`PATIENTS`, `APPOINTMENTS`), making it easy to swap in a real database (e.g. SQLite) later.
- Each page is implemented as an independent `tk.Frame` subclass, keeping the codebase modular and easy to extend.
- Shared helper functions (`_btn`, `_form_entry`, `_form_combo`, `load_icon`) centralize styling so the UI stays consistent across all pages.

---

## 🌍 SDG Alignment

This project supports:
- **SDG 3 — Good Health and Well-Being**, by reducing administrative errors and improving patient record accuracy
- **SDG 9 — Industry, Innovation, and Infrastructure**, by demonstrating that meaningful digital infrastructure is achievable in low-resource clinic settings using free, open-source tools

---

## 👥 Authors

**BIT1201 — Group 2**
- Clifford Joshua Jones
- Jane Sarah Bangura
- Ismatu Kamara

---

## 📄 License

This project was created for academic purposes as part of the PROG103 course.
