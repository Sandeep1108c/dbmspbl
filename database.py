"""
Database management module for Library Circulation and Digital Resource Management System.
Configured for MySQL 8.4 Server with cloud secrets support and transparent fallback.
STRICT REQUIREMENT: ZERO em dashes and ZERO en dashes in this file.
"""

import os
import sqlite3
from datetime import datetime, date, timedelta
import pandas as pd

# Default MySQL configuration
MYSQL_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'Sandeep@123',
    'database': 'dbms_project'
}

# Check for Streamlit Cloud secrets if available
try:
    import streamlit as st
    if hasattr(st, 'secrets') and 'mysql' in st.secrets:
        sec = st.secrets['mysql']
        MYSQL_CONFIG['host'] = sec.get('host', MYSQL_CONFIG['host'])
        MYSQL_CONFIG['port'] = int(sec.get('port', MYSQL_CONFIG['port']))
        MYSQL_CONFIG['user'] = sec.get('user', MYSQL_CONFIG['user'])
        MYSQL_CONFIG['password'] = sec.get('password', MYSQL_CONFIG['password'])
        MYSQL_CONFIG['database'] = sec.get('database', MYSQL_CONFIG['database'])
except Exception:
    pass

SQLITE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'library_system.db')

class DatabaseManager:
    def __init__(self, force_sqlite=False):
        self.force_sqlite = force_sqlite
        self.engine_type = 'sqlite'
        self.mysql_available = False
        self._check_mysql()

    def _check_mysql(self):
        if self.force_sqlite:
            self.engine_type = 'sqlite'
            return

        try:
            import pymysql
            conn = pymysql.connect(
                host=MYSQL_CONFIG['host'],
                port=MYSQL_CONFIG['port'],
                user=MYSQL_CONFIG['user'],
                password=MYSQL_CONFIG['password'],
                connect_timeout=3
            )
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{MYSQL_CONFIG['database']}`;")
            conn.commit()
            cursor.close()
            conn.close()
            self.mysql_available = True
            self.engine_type = 'mysql'
        except Exception:
            self.mysql_available = False
            self.engine_type = 'sqlite'

    def get_connection(self):
        if self.engine_type == 'mysql' and self.mysql_available:
            try:
                import pymysql
                return pymysql.connect(
                    host=MYSQL_CONFIG['host'],
                    port=MYSQL_CONFIG['port'],
                    user=MYSQL_CONFIG['user'],
                    password=MYSQL_CONFIG['password'],
                    database=MYSQL_CONFIG['database'],
                    cursorclass=pymysql.cursors.DictCursor,
                    autocommit=True
                )
            except Exception:
                self.engine_type = 'sqlite'
                return sqlite3.connect(SQLITE_PATH)
        else:
            conn = sqlite3.connect(SQLITE_PATH)
            conn.row_factory = sqlite3.Row
            return conn

    def execute_query(self, query, params=None):
        conn = self.get_connection()
        try:
            if self.engine_type == 'mysql':
                with conn.cursor() as cursor:
                    cursor.execute(query, params or ())
                    if query.strip().upper().startswith(('SELECT', 'SHOW', 'DESCRIBE', 'PRAGMA')):
                        return cursor.fetchall()
                    conn.commit()
                    return cursor.lastrowid
            else:
                cursor = conn.cursor()
                # Adapt %s placeholder to ? for sqlite driver
                if params and '%s' in query:
                    query = query.replace('%s', '?')
                cursor.execute(query, params or ())
                if query.strip().upper().startswith(('SELECT', 'SHOW', 'DESCRIBE', 'PRAGMA')):
                    rows = cursor.fetchall()
                    return [dict(ix) for ix in rows]
                conn.commit()
                last_id = cursor.lastrowid
                return last_id
        finally:
            conn.close()

    def query_df(self, query, params=None):
        conn = self.get_connection()
        try:
            if self.engine_type != 'mysql' and params and '%s' in query:
                query = query.replace('%s', '?')
            return pd.read_sql_query(query, conn, params=params)
        finally:
            conn.close()

    def init_database(self):
        """Initializes all 14 relational tables."""
        conn = self.get_connection()
        cursor = conn.cursor()

        if self.engine_type == 'mysql':
            pk_auto = "INT AUTO_INCREMENT PRIMARY KEY"
            fk_bool = "BOOLEAN"
            datetime_type = "DATETIME"
        else:
            pk_auto = "INTEGER PRIMARY KEY AUTOINCREMENT"
            fk_bool = "INTEGER"
            datetime_type = "TEXT"

        tables = [
            f"""
            CREATE TABLE IF NOT EXISTS Author (
                AuthorID {pk_auto},
                FirstName VARCHAR(100) NOT NULL,
                LastName VARCHAR(100) NOT NULL,
                Bio TEXT
            );
            """,
            f"""
            CREATE TABLE IF NOT EXISTS Publisher (
                PublisherID {pk_auto},
                Name VARCHAR(150) NOT NULL UNIQUE,
                Address VARCHAR(255),
                Phone VARCHAR(20),
                Email VARCHAR(100)
            );
            """,
            f"""
            CREATE TABLE IF NOT EXISTS Category (
                CategoryID {pk_auto},
                Name VARCHAR(100) NOT NULL UNIQUE,
                Description TEXT
            );
            """,
            f"""
            CREATE TABLE IF NOT EXISTS Book (
                BookID {pk_auto},
                ISBN VARCHAR(20) NOT NULL UNIQUE,
                Title VARCHAR(255) NOT NULL,
                Language VARCHAR(50) NOT NULL DEFAULT 'English',
                TotalPages INT CHECK (TotalPages > 0),
                PublicationYear INT NOT NULL
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS BookAuthor (
                BookID INT NOT NULL,
                AuthorID INT NOT NULL,
                PRIMARY KEY (BookID, AuthorID),
                FOREIGN KEY (BookID) REFERENCES Book(BookID) ON DELETE CASCADE,
                FOREIGN KEY (AuthorID) REFERENCES Author(AuthorID) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS BookCategory (
                BookID INT NOT NULL,
                CategoryID INT NOT NULL,
                PRIMARY KEY (BookID, CategoryID),
                FOREIGN KEY (BookID) REFERENCES Book(BookID) ON DELETE CASCADE,
                FOREIGN KEY (CategoryID) REFERENCES Category(CategoryID) ON DELETE CASCADE
            );
            """,
            f"""
            CREATE TABLE IF NOT EXISTS Edition (
                EditionID {pk_auto},
                BookID INT NOT NULL,
                EditionNumber INT NOT NULL CHECK (EditionNumber > 0),
                PublisherID INT NOT NULL,
                PublicationDate DATE NOT NULL,
                Format VARCHAR(50) NOT NULL DEFAULT 'Paperback',
                FOREIGN KEY (BookID) REFERENCES Book(BookID) ON DELETE CASCADE,
                FOREIGN KEY (PublisherID) REFERENCES Publisher(PublisherID)
            );
            """,
            f"""
            CREATE TABLE IF NOT EXISTS Copy (
                CopyID {pk_auto},
                AccessionNumber VARCHAR(50) NOT NULL UNIQUE,
                EditionID INT NOT NULL,
                Status VARCHAR(20) NOT NULL DEFAULT 'Available',
                ShelfLocation VARCHAR(100),
                DateAcquired DATE NOT NULL,
                FOREIGN KEY (EditionID) REFERENCES Edition(EditionID)
            );
            """,
            f"""
            CREATE TABLE IF NOT EXISTS Member (
                MemberID {pk_auto},
                FirstName VARCHAR(100) NOT NULL,
                LastName VARCHAR(100) NOT NULL,
                Email VARCHAR(150) NOT NULL UNIQUE,
                Phone VARCHAR(20) NOT NULL,
                Address VARCHAR(255),
                MembershipType VARCHAR(20) NOT NULL DEFAULT 'Student',
                MembershipStartDate DATE NOT NULL,
                MembershipEndDate DATE,
                MaxBooksAllowed INT NOT NULL DEFAULT 3,
                IsActive {fk_bool} NOT NULL DEFAULT 1
            );
            """,
            f"""
            CREATE TABLE IF NOT EXISTS Issue (
                IssueID {pk_auto},
                CopyID INT NOT NULL,
                MemberID INT NOT NULL,
                IssueDate DATE NOT NULL,
                DueDate DATE NOT NULL,
                ReturnDate DATE,
                Status VARCHAR(20) NOT NULL DEFAULT 'Active',
                FOREIGN KEY (CopyID) REFERENCES Copy(CopyID),
                FOREIGN KEY (MemberID) REFERENCES Member(MemberID)
            );
            """,
            f"""
            CREATE TABLE IF NOT EXISTS Reservation (
                ReservationID {pk_auto},
                BookID INT NOT NULL,
                MemberID INT NOT NULL,
                ReservationDate {datetime_type} NOT NULL,
                QueuePosition INT NOT NULL DEFAULT 1,
                Status VARCHAR(20) NOT NULL DEFAULT 'Pending',
                ExpiryDate {datetime_type},
                FOREIGN KEY (BookID) REFERENCES Book(BookID),
                FOREIGN KEY (MemberID) REFERENCES Member(MemberID)
            );
            """,
            f"""
            CREATE TABLE IF NOT EXISTS Fine (
                FineID {pk_auto},
                IssueID INT NOT NULL,
                MemberID INT NOT NULL,
                Amount DECIMAL(10,2) NOT NULL CHECK (Amount >= 0),
                Reason VARCHAR(255) NOT NULL,
                FineDate DATE NOT NULL,
                PaidDate DATE,
                Status VARCHAR(20) NOT NULL DEFAULT 'Pending',
                FOREIGN KEY (IssueID) REFERENCES Issue(IssueID),
                FOREIGN KEY (MemberID) REFERENCES Member(MemberID)
            );
            """,
            f"""
            CREATE TABLE IF NOT EXISTS DigitalResource (
                ResourceID {pk_auto},
                BookID INT NOT NULL,
                ResourceType VARCHAR(50) NOT NULL DEFAULT 'EBook',
                FileFormat VARCHAR(20) NOT NULL DEFAULT 'PDF',
                FileSize VARCHAR(30) NOT NULL,
                URL VARCHAR(255) NOT NULL,
                UploadDate DATE NOT NULL,
                FOREIGN KEY (BookID) REFERENCES Book(BookID)
            );
            """,
            f"""
            CREATE TABLE IF NOT EXISTS DigitalAccessLog (
                LogID {pk_auto},
                ResourceID INT NOT NULL,
                MemberID INT NOT NULL,
                AccessDate {datetime_type} NOT NULL,
                AccessType VARCHAR(50) NOT NULL DEFAULT 'View',
                IPAddress VARCHAR(45) NOT NULL DEFAULT '127.0.0.1',
                FOREIGN KEY (ResourceID) REFERENCES DigitalResource(ResourceID),
                FOREIGN KEY (MemberID) REFERENCES Member(MemberID)
            );
            """
        ]

        for stmt in tables:
            cursor.execute(stmt)

        if self.engine_type == 'mysql':
            conn.commit()
        else:
            conn.commit()

        conn.close()

    def seed_data(self):
        """Populates test data across all tables."""
        try:
            res = self.execute_query("SELECT COUNT(*) AS c FROM Book")
            count = res[0]['c'] if res else 0
            if count > 0:
                return False
        except Exception:
            pass

        # Authors
        authors = [
            ("Abraham", "Silberschatz", "Professor and pioneer in database system concepts and operating systems."),
            ("Henry", "Korth", "Professor of Computer Science and Engineering at Lehigh University."),
            ("Ramez", "Elmasri", "Author of Fundamentals of Database Systems and faculty member at UT Arlington."),
            ("Shamkant", "Navathe", "Professor at Georgia Institute of Technology specializing in DBMS."),
            ("Robert", "Martin", "Software craftsman, author of Clean Code and Clean Architecture."),
            ("Martin", "Fowler", "Chief Scientist at ThoughtWorks, author of Refactoring and Patterns."),
            ("Andrew", "Tanenbaum", "Distinguished Professor Emeritus, author of Computer Networks."),
            ("Thomas", "Cormen", "Professor of Computer Science and co-author of Introduction to Algorithms.")
        ]
        for fn, ln, bio in authors:
            self.execute_query(
                "INSERT INTO Author (FirstName, LastName, Bio) VALUES (%s, %s, %s)",
                (fn, ln, bio)
            )

        # Publishers
        publishers = [
            ("McGraw-Hill Education", "New York, NY", "+1-800-338-3987", "contact@mheducation.com"),
            ("Pearson Education", "London, UK", "+44-20-7010-2000", "support@pearson.com"),
            ("Prentice Hall", "Upper Saddle River, NJ", "+1-201-236-7000", "info@prenticehall.com"),
            ("O'Reilly Media", "Sebastopol, CA", "+1-707-827-7000", "support@oreilly.com"),
            ("MIT Press", "Cambridge, MA", "+1-617-253-5646", "mitpress-orders@mit.edu")
        ]
        for name, addr, phone, email in publishers:
            self.execute_query(
                "INSERT INTO Publisher (Name, Address, Phone, Email) VALUES (%s, %s, %s, %s)",
                (name, addr, phone, email)
            )

        # Categories
        categories = [
            ("Database Systems", "Relational models, SQL, transactions, indexing and storage architecture."),
            ("Software Engineering", "Design patterns, architecture, agile methodologies, and clean code principles."),
            ("Computer Networks", "Network protocols, TCP/IP stack, routing algorithms, and network security."),
            ("Algorithms & Data Structures", "Computational complexity, sorting, trees, graphs, and dynamic programming."),
            ("Operating Systems", "Process management, memory virtualization, concurrency, and file systems."),
            ("Artificial Intelligence", "Machine learning, neural networks, computer vision, and expert systems.")
        ]
        for name, desc in categories:
            self.execute_query(
                "INSERT INTO Category (Name, Description) VALUES (%s, %s)",
                (name, desc)
            )

        # Books
        books = [
            ("978-0078022159", "Database System Concepts", "English", 1376, 2019),
            ("978-0133970777", "Fundamentals of Database Systems", "English", 1272, 2015),
            ("978-0132350884", "Clean Code: A Handbook of Agile Craftsmanship", "English", 464, 2008),
            ("978-0201485677", "Refactoring: Improving the Design of Existing Code", "English", 448, 1999),
            ("978-0132126953", "Computer Networks", "English", 960, 2010),
            ("978-0262033848", "Introduction to Algorithms", "English", 1312, 2009),
            ("978-1491950357", "Designing Data-Intensive Applications", "English", 616, 2017),
            ("978-0131103627", "The C Programming Language", "English", 272, 1988)
        ]
        for isbn, title, lang, pages, year in books:
            self.execute_query(
                "INSERT INTO Book (ISBN, Title, Language, TotalPages, PublicationYear) VALUES (%s, %s, %s, %s, %s)",
                (isbn, title, lang, pages, year)
            )

        # Book-Author mappings
        ba_map = [
            (1, 1), (1, 2),  # Silberschatz & Korth
            (2, 3), (2, 4),  # Elmasri & Navathe
            (3, 5),          # Martin
            (4, 6),          # Fowler
            (5, 7),          # Tanenbaum
            (6, 8),          # Cormen
            (7, 6),          # Fowler
            (8, 5)           # Martin
        ]
        for b_id, a_id in ba_map:
            self.execute_query(
                "INSERT INTO BookAuthor (BookID, AuthorID) VALUES (%s, %s)",
                (b_id, a_id)
            )

        # Book-Category mappings
        bc_map = [
            (1, 1), (2, 1),
            (3, 2), (4, 2),
            (5, 3),
            (6, 4),
            (7, 1), (7, 2),
            (8, 2)
        ]
        for b_id, c_id in bc_map:
            self.execute_query(
                "INSERT INTO BookCategory (BookID, CategoryID) VALUES (%s, %s)",
                (b_id, c_id)
            )

        # Editions
        editions = [
            (1, 7, 1, "2019-02-15", "Hardcover"),
            (1, 6, 1, "2010-01-27", "Paperback"),
            (2, 7, 2, "2015-06-18", "Hardcover"),
            (3, 1, 3, "2008-08-01", "Paperback"),
            (4, 2, 2, "2018-11-30", "Hardcover"),
            (5, 5, 2, "2010-10-07", "Paperback"),
            (6, 3, 5, "2009-07-31", "Hardcover"),
            (7, 1, 4, "2017-03-16", "Paperback")
        ]
        for b_id, ed_no, pub_id, p_date, fmt in editions:
            self.execute_query(
                "INSERT INTO Edition (BookID, EditionNumber, PublisherID, PublicationDate, Format) VALUES (%s, %s, %s, %s, %s)",
                (b_id, ed_no, pub_id, p_date, fmt)
            )

        # Physical Copies
        copies = [
            ("ACC-2026-001", 1, "Available", "Shelf A1-01", "2024-01-10"),
            ("ACC-2026-002", 1, "Issued", "Shelf A1-01", "2024-01-10"),
            ("ACC-2026-003", 1, "Available", "Shelf A1-02", "2024-02-15"),
            ("ACC-2026-004", 2, "Available", "Shelf A1-03", "2024-02-15"),
            ("ACC-2026-005", 3, "Available", "Shelf A2-01", "2024-03-01"),
            ("ACC-2026-006", 3, "Issued", "Shelf A2-01", "2024-03-01"),
            ("ACC-2026-007", 4, "Available", "Shelf B1-05", "2024-01-20"),
            ("ACC-2026-008", 4, "Issued", "Shelf B1-05", "2024-01-20"),
            ("ACC-2026-009", 5, "Available", "Shelf B2-02", "2024-04-10"),
            ("ACC-2026-010", 6, "Issued", "Shelf C1-03", "2024-02-25"),
            ("ACC-2026-011", 6, "Available", "Shelf C1-03", "2024-02-25"),
            ("ACC-2026-012", 7, "Available", "Shelf D1-01", "2024-05-12"),
            ("ACC-2026-013", 7, "Reserved", "Shelf D1-01", "2024-05-12"),
            ("ACC-2026-014", 8, "Available", "Shelf E1-04", "2024-06-01"),
            ("ACC-2026-015", 8, "Available", "Shelf E1-04", "2024-06-01")
        ]
        for acc, ed_id, status, shelf, dt in copies:
            self.execute_query(
                "INSERT INTO Copy (AccessionNumber, EditionID, Status, ShelfLocation, DateAcquired) VALUES (%s, %s, %s, %s, %s)",
                (acc, ed_id, status, shelf, dt)
            )

        # Members
        members = [
            ("Rahul", "Sharma", "rahul.sharma@college.edu", "9876543210", "Block A, Room 204", "Student", "2025-08-01", "2027-07-31", 3, 1),
            ("Priya", "Patel", "priya.patel@college.edu", "9876543211", "Block B, Room 112", "Student", "2025-08-01", "2027-07-31", 3, 1),
            ("Dr. Arjun", "Verma", "arjun.verma@college.edu", "9876543212", "Faculty Quarters C-3", "Faculty", "2023-01-01", "2030-12-31", 10, 1),
            ("Sneha", "Reddy", "sneha.reddy@college.edu", "9876543213", "Block A, Room 305", "Student", "2025-08-01", "2027-07-31", 3, 1),
            ("Prof. Kiran", "Nair", "kiran.nair@college.edu", "9876543214", "Faculty Quarters B-1", "Faculty", "2022-07-15", "2030-12-31", 10, 1),
            ("Vikram", "Singh", "vikram.singh@library.org", "9876543215", "Flat 402, Green Residency", "Public", "2026-01-10", "2027-01-09", 2, 1),
            ("Ananya", "Deshmukh", "ananya.d@college.edu", "9876543216", "Staff Colony S-12", "Staff", "2024-03-01", "2028-02-29", 5, 1)
        ]
        for fn, ln, em, ph, ad, mt, sd, ed, mb, ia in members:
            self.execute_query(
                "INSERT INTO Member (FirstName, LastName, Email, Phone, Address, MembershipType, MembershipStartDate, MembershipEndDate, MaxBooksAllowed, IsActive) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (fn, ln, em, ph, ad, mt, sd, ed, mb, ia)
            )

        # Issues
        today = date.today()
        issues = [
            (1, 1, str(today - timedelta(days=25)), str(today - timedelta(days=11)), str(today - timedelta(days=12)), "Returned"),
            (2, 2, str(today - timedelta(days=5)), str(today + timedelta(days=9)), None, "Active"),
            (6, 4, str(today - timedelta(days=22)), str(today - timedelta(days=8)), None, "Overdue"),
            (8, 1, str(today - timedelta(days=30)), str(today - timedelta(days=16)), None, "Overdue"),
            (10, 3, str(today - timedelta(days=10)), str(today + timedelta(days=20)), None, "Active")
        ]
        for c_id, m_id, idt, ddt, rdt, st in issues:
            self.execute_query(
                "INSERT INTO Issue (CopyID, MemberID, IssueDate, DueDate, ReturnDate, Status) VALUES (%s, %s, %s, %s, %s, %s)",
                (c_id, m_id, idt, ddt, rdt, st)
            )

        # Fines
        fines = [
            (3, 4, 40.00, "Late Return: 8 days overdue at Rs 5 per day", str(today - timedelta(days=8)), None, "Pending"),
            (4, 1, 80.00, "Late Return: 16 days overdue at Rs 5 per day", str(today - timedelta(days=16)), None, "Pending"),
            (1, 1, 15.00, "Late Return: 3 days overdue", str(today - timedelta(days=12)), str(today - timedelta(days=11)), "Paid")
        ]
        for i_id, m_id, amt, rsn, fdt, pdt, st in fines:
            self.execute_query(
                "INSERT INTO Fine (IssueID, MemberID, Amount, Reason, FineDate, PaidDate, Status) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (i_id, m_id, amt, rsn, fdt, pdt, st)
            )

        # Reservations
        reservations = [
            (7, 2, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 1, "Pending", (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")),
            (1, 4, (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S"), 1, "Fulfilled", (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d %H:%M:%S"))
        ]
        for b_id, m_id, rdt, qp, st, exp in reservations:
            self.execute_query(
                "INSERT INTO Reservation (BookID, MemberID, ReservationDate, QueuePosition, Status, ExpiryDate) VALUES (%s, %s, %s, %s, %s, %s)",
                (b_id, m_id, rdt, qp, st, exp)
            )

        # Digital Resources
        resources = [
            (1, "EBook", "PDF", "24.5 MB", "https://digital.library.edu/assets/db-concepts-7e.pdf", "2024-01-15"),
            (3, "EBook", "EPUB", "4.2 MB", "https://digital.library.edu/assets/clean-code.epub", "2024-02-10"),
            (5, "EBook", "PDF", "18.9 MB", "https://digital.library.edu/assets/comp-networks-5e.pdf", "2024-03-05"),
            (6, "Audiobook", "MP3", "320.0 MB", "https://digital.library.edu/assets/intro-algorithms-audio.mp3", "2024-04-01")
        ]
        for b_id, rt, ff, fs, url, udt in resources:
            self.execute_query(
                "INSERT INTO DigitalResource (BookID, ResourceType, FileFormat, FileSize, URL, UploadDate) VALUES (%s, %s, %s, %s, %s, %s)",
                (b_id, rt, ff, fs, url, udt)
            )

        # Digital Access Logs
        logs = [
            (1, 1, (datetime.now() - timedelta(days=2, hours=3)).strftime("%Y-%m-%d %H:%M:%S"), "View", "192.168.1.101"),
            (1, 2, (datetime.now() - timedelta(days=1, hours=5)).strftime("%Y-%m-%d %H:%M:%S"), "Download", "192.168.1.105"),
            (2, 3, (datetime.now() - timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S"), "View", "10.0.4.22"),
            (3, 4, (datetime.now() - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S"), "Download", "192.168.1.114")
        ]
        for r_id, m_id, adt, atp, ip in logs:
            self.execute_query(
                "INSERT INTO DigitalAccessLog (ResourceID, MemberID, AccessDate, AccessType, IPAddress) VALUES (%s, %s, %s, %s, %s)",
                (r_id, m_id, adt, atp, ip)
            )

        return True

_db_instance = None

def get_db():
    global _db_instance
    if _db_instance is None:
        _db_instance = DatabaseManager()
        _db_instance.init_database()
        _db_instance.seed_data()
    return _db_instance
