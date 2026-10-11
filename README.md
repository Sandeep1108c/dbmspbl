# Library Circulation and Digital Resource Management System (DBMS PBL)

An interactive, production-ready Database Management System designed for modern hybrid libraries managing physical assets (books, editions, copies) and electronic resources (e-books, audiobooks, journals).

Developed as part of the **Database Management Systems: Project-Based Learning (DBMS PBL)** curriculum.

---

## Key System Features

- **Executive Analytics Dashboard:** Real-time KPI counters, inventory breakdown donut chart, patron category demographics, and circulation velocity stats.
- **Full Catalog & Inventory Management:** Multi-edition book cataloging with authors, publishers, categories, and unique accession barcode tracking.
- **Member Directory & Quota Enforcement:** Categorized memberships (Student, Faculty, Staff, Public) with role-based borrowing limits and active status checks.
- **Circulation Desk (Check-in / Check-out):** One-click checkouts with live quota validation, plus automated check-in with dynamic overdue fine calculations.
- **First-In-First-Out (FIFO) Reservation Queue:** Priority-based waitlist system for high-demand titles when all physical copies are checked out.
- **Financial Settlement Desk:** Transparent tracking of overdue fines, cashier receipt settlements, and authorized waivers.
- **Digital Library & Access Audit Trail:** Searchable catalog for downloadable electronic assets with persistent logging of member ID, IP address, and access timestamps.
- **Interactive SQL Evaluation Console:** Live query execution interface with pre-loaded complex joins, subqueries, and group-by evaluations.

---

## Database Architecture

- **Normalization:** 14 normalized relational tables adhering to Third Normal Form (3NF) and Boyce-Codd Normal Form (BCNF).
- **Dual-Engine Persistence:**
  - **MySQL Server 8.4** on default port 3306 for enterprise client-server operation.
  - **Embedded SQLite 3** with automatic fallback for seamless cloud and standalone execution.

---

## Project Structure

```
.
├── app.py                      # Main Streamlit web application
├── database.py                 # Dual-engine database abstraction and seed data
├── requirements.txt            # Python dependencies for deployment
├── .streamlit/
│   └── config.toml             # Custom modern theme and UI settings
├── Final_Project_Report.docx   # Comprehensive project report document
├── Review1_Report.docx         # Review 1 submission report
├── Final_Presentation_5Slides.pptx # 5-slide project defense presentation
├── ER_Diagram.png              # Conceptual Entity-Relationship diagram
├── Relational_Schema.png       # Relational schema diagram
└── run_app.bat                 # One-click Windows launcher
```

---

## How to Run Locally

1. Clone this repository:
   ```bash
   git clone https://github.com/Sandeep1108c/dbmspbl.git
   cd dbmspbl
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Launch the application:
   ```bash
   streamlit run app.py
   ```

---

## Deploy on Streamlit Community Cloud

1. Fork or push this repository to your GitHub account (`https://github.com/Sandeep1108c/dbmspbl`).
2. Visit [share.streamlit.io](https://share.streamlit.io).
3. Connect your GitHub account and select repository `Sandeep1108c/dbmspbl`.
4. Set Main file path to `app.py`.
5. Click **Deploy!**
