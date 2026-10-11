"""
Generate Comprehensive Word Project Report for DBMS PBL
Project: Design and Implementation of a Database Management System for
         Library Circulation and Digital Resource Management System
STRICT REQUIREMENT: ZERO em dashes and ZERO en dashes in the entire report.
"""

import os
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_cell_background(cell, fill_hex):
    """Sets the background color of a table cell."""
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tc_pr.append(shd)

def create_report():
    doc = Document()

    # Page Margins
    for section in doc.sections:
        section.top_margin = Cm(2.54)
        section.bottom_margin = Cm(2.54)
        section.left_margin = Cm(2.54)
        section.right_margin = Cm(2.54)

    # Styles
    normal_style = doc.styles['Normal']
    normal_font = normal_style.font
    normal_font.name = 'Calibri'
    normal_font.size = Pt(11)
    normal_font.color.rgb = RGBColor(0x21, 0x25, 0x29)

    # Helper function for adding paragraphs
    def add_p(text, bold=False, italic=False, size=11, color_rgb=(0x21, 0x25, 0x29), align=WD_ALIGN_PARAGRAPH.LEFT, space_after=6):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(text)
        run.bold = bold
        run.italic = italic
        run.font.name = 'Calibri'
        run.font.size = Pt(size)
        run.font.color.rgb = RGBColor(*color_rgb)
        return p

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Calibri'
        run.font.size = Pt(18)
        run.font.color.rgb = RGBColor(0x0F, 0x4C, 0x81) # Deep classic blue
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Calibri'
        run.font.size = Pt(14)
        run.font.color.rgb = RGBColor(0x1B, 0x6C, 0xA8)
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Calibri'
        run.font.size = Pt(12)
        run.font.color.rgb = RGBColor(0x2D, 0x37, 0x48)
        return p

    def add_bullet_point(title, text, level=0):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.left_indent = Cm(1.0 + level * 0.5)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        if title:
            r_title = p.add_run(title + ": ")
            r_title.bold = True
            r_title.font.name = 'Calibri'
            r_title.font.size = Pt(11)
            r_title.font.color.rgb = RGBColor(0x1A, 0x20, 0x2C)
        r_text = p.add_run(text)
        r_text.font.name = 'Calibri'
        r_text.font.size = Pt(11)
        r_text.font.color.rgb = RGBColor(0x2D, 0x37, 0x48)
        return p

    def add_custom_table(headers, rows, col_widths=None):
        table = doc.add_table(rows=1 + len(rows), cols=len(headers))
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False

        # Header Row
        hdr_row = table.rows[0]
        for idx, text in enumerate(headers):
            cell = hdr_row.cells[idx]
            cell.text = text
            set_cell_background(cell, "0F4C81") # Navy
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.space_before = Pt(4)
            for r in p.runs:
                r.bold = True
                r.font.name = 'Calibri'
                r.font.size = Pt(10)
                r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

        # Data Rows
        for r_idx, row_data in enumerate(rows):
            row = table.rows[r_idx + 1]
            bg_color = "F7FAFC" if r_idx % 2 == 1 else "FFFFFF"
            for c_idx, val in enumerate(row_data):
                cell = row.cells[c_idx]
                cell.text = str(val)
                set_cell_background(cell, bg_color)
                p = cell.paragraphs[0]
                p.paragraph_format.space_after = Pt(3)
                p.paragraph_format.space_before = Pt(3)
                p.paragraph_format.line_spacing = 1.1
                for r in p.runs:
                    r.font.name = 'Calibri'
                    r.font.size = Pt(9.5)
                    r.font.color.rgb = RGBColor(0x2D, 0x37, 0x48)

        # Apply Column Widths if supplied
        if col_widths:
            for row in table.rows:
                for c_idx, w in enumerate(col_widths):
                    row.cells[c_idx].width = Cm(w)

        doc.add_paragraph().paragraph_format.space_after = Pt(8)
        return table

    # =========================================================================
    # TITLE PAGE
    # =========================================================================
    add_p("", space_after=30)
    add_p("PROJECT BASED LEARNING REPORT", bold=True, size=15, color_rgb=(0x4A, 0x55, 0x68), align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)
    add_p("DESIGN AND IMPLEMENTATION OF A DATABASE MANAGEMENT SYSTEM FOR", bold=True, size=17, color_rgb=(0x0F, 0x4C, 0x81), align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)
    add_p("LIBRARY CIRCULATION AND DIGITAL RESOURCE MANAGEMENT SYSTEM", bold=True, size=21, color_rgb=(0x0F, 0x4C, 0x81), align=WD_ALIGN_PARAGRAPH.CENTER, space_after=30)

    # Divider bar
    add_p("____________________________________________________________________________", color_rgb=(0x1B, 0x6C, 0xA8), align=WD_ALIGN_PARAGRAPH.CENTER, space_after=30)

    add_p("Course: Database Management Systems (DBMS PBL)", bold=True, size=13, color_rgb=(0x2D, 0x37, 0x48), align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)
    add_p("Department of Computer Science and Engineering", size=12, color_rgb=(0x4A, 0x55, 0x68), align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)
    add_p("Academic Year: 2025-2026", size=12, color_rgb=(0x4A, 0x55, 0x68), align=WD_ALIGN_PARAGRAPH.CENTER, space_after=40)

    add_p("Submission Version: Fully Working Model and Complete Project Report", italic=True, size=11, color_rgb=(0x71, 0x80, 0x96), align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)

    doc.add_page_break()

    # =========================================================================
    # TABLE OF CONTENTS
    # =========================================================================
    add_h1("Table of Contents")
    toc_items = [
        ("1. Executive Summary and Problem Statement", "Page 3"),
        ("2. Project Scope and System Boundaries", "Page 4"),
        ("3. Project Objectives", "Page 5"),
        ("4. Users and Role-Based Access Control", "Page 6"),
        ("5. Detailed Requirements Specification", "Page 7"),
        ("6. Business Rules and Integrity Constraints", "Page 9"),
        ("7. System Architecture and Modular Design", "Page 10"),
        ("8. Conceptual Modeling (Entity-Relationship Model)", "Page 12"),
        ("9. Relational Schema and Normalization Analysis", "Page 13"),
        ("10. Comprehensive Data Dictionary (14 Tables)", "Page 15"),
        ("11. Fully Working Model Implementation", "Page 20"),
        ("12. Advanced SQL Queries and Evaluation Results", "Page 23"),
        ("13. System Verification and Test Matrix", "Page 26"),
        ("14. Conclusion and Future Roadmap", "Page 28")
    ]
    for section, pg in toc_items:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        run_sec = p.add_run(section)
        run_sec.font.name = 'Calibri'
        run_sec.font.size = Pt(11)
        run_sec.font.color.rgb = RGBColor(0x1A, 0x20, 0x2C)

        dots_count = max(5, 75 - len(section))
        run_dots = p.add_run(" " + "." * dots_count + " ")
        run_dots.font.name = 'Calibri'
        run_dots.font.size = Pt(10)
        run_dots.font.color.rgb = RGBColor(0xA0, 0xAE, 0xC0)

        run_pg = p.add_run(pg)
        run_pg.bold = True
        run_pg.font.name = 'Calibri'
        run_pg.font.size = Pt(11)
        run_pg.font.color.rgb = RGBColor(0x0F, 0x4C, 0x81)

    doc.add_page_break()

    # =========================================================================
    # SECTION 1: EXECUTIVE SUMMARY & PROBLEM STATEMENT
    # =========================================================================
    add_h1("1. Executive Summary and Problem Statement")

    add_h2("1.1 Executive Summary")
    add_p(
        "Modern academic and research libraries have expanded well beyond traditional paper repositories into hybrid resource centers. "
        "They oversee physical books, multi-volume reference editions, physical audio-visual media, and thousands of digital assets including e-books, research journals, and audio lectures. "
        "Managing this heterogeneous collection demands a unified, highly reliable, and normalized relational database system. "
        "This project presents the complete design, normalization, architectural specification, and working software model for the Library Circulation and Digital Resource Management System. "
        "The system incorporates automated issue and return tracking, rule-based overdue fine assessments, a strict First-In-First-Out (FIFO) reservation queue, "
        "and security audit logging for digital material access."
    )

    add_h2("1.2 Problem Statement")
    add_p(
        "Traditional library workflows that depend on physical paper ledgers, fragmented spreadsheets, or antiquated desktop databases suffer from critical systemic bottlenecks:"
    )
    add_bullet_point(
        "Unreliable Inventory and Copy Tracking",
        "Physical copies are frequently misplaced or incorrectly recorded. Multiple copies sharing a single accession identifier cause inventory discrepancies and administrative confusion."
    )
    add_bullet_point(
        "Absence of Digital Resource Management",
        "Legacy software systems cannot catalog digital assets or monitor electronic document access, leaving institutions unable to gauge electronic usage trends."
    )
    add_bullet_point(
        "Error-Prone Manual Fine Computations",
        "Calculating overdue fees by hand introduces human errors, inconsistent dispute settlements, and administrative delays."
    )
    add_bullet_point(
        "Unstructured Reservation Queues",
        "When all copies of high-demand textbooks are loaned out, informal waitlists lead to unfair copy reallocations and patron dissatisfaction."
    )
    add_bullet_point(
        "Data Redundancy and Relational Anomalies",
        "Duplicating author, publisher, and patron information across multiple files causes update, insertion, and deletion anomalies that undermine data integrity."
    )

    # =========================================================================
    # SECTION 2: SCOPE
    # =========================================================================
    add_h1("2. Project Scope and System Boundaries")

    add_h2("2.1 In-Scope Components")
    add_p("The implemented relational database system encompasses the following operational domains:")
    add_bullet_point("Physical Asset Cataloging", "Multi-edition cataloging of books, categories, publishers, and individual physical copies linked via unique accession numbers.")
    add_bullet_point("Digital Media Repository", "Metadata tracking, format classification (PDF, EPUB, MP3), resource URLs, and access timestamps for electronic materials.")
    add_bullet_point("Member Administration", "Profiling patrons across defined classifications (Student, Faculty, Staff, Public) with category-specific borrowing limits and validity intervals.")
    add_bullet_point("Circulation Lifecycle", "Comprehensive tracking of checkout, return, and renewal operations with automatic copy availability status changes.")
    add_bullet_point("FIFO Reservation Queue", "Automated waitlist ordering for titles whose physical copies are fully checked out.")
    add_bullet_point("Automated Fine Settlement", "Rule-based calculation of daily overdue penalties, tracking settled cash receipts, and authorized waivers.")
    add_bullet_point("Audit Access Logging", "Recording every digital resource view and download event with patron identifier, timestamp, and IP address.")

    add_h2("2.2 Out-of-Scope Components")
    add_p("The following external services remain outside the immediate boundaries of this project:")
    add_bullet_point("Inter-Library Loan Networks", "External protocols connecting third-party university consortia.")
    add_bullet_point("Third-Party Payment Gateways", "Direct credit card or payment API processing. The system records internal cashier receipts and payment status flags.")
    add_bullet_point("AI Recommendation Algorithms", "Predictive machine learning algorithms for speculative book recommendations.")

    # =========================================================================
    # SECTION 3: OBJECTIVES
    # =========================================================================
    add_h1("3. Project Objectives")
    add_p("The core technical and operational objectives of this system are summarized below:")
    objectives_data = [
        ("Obj-01", "Centralized Catalog", "Unify physical books, editions, and electronic assets under a single normalized database schema."),
        ("Obj-02", "Precise Circulation", "Maintain real-time status visibility across all accessioned copies (Available, Issued, Reserved, Damaged)."),
        ("Obj-03", "Automated Overdue Fines", "Eliminate manual computation by evaluating overdue days and applying fine rates automatically upon book check-in."),
        ("Obj-04", "FIFO Waitlist Management", "Implement transparent waitlist queuing that guarantees fair allocation to the earliest reserving patron."),
        ("Obj-05", "Digital Access Accountability", "Record an immutable audit log of patron interactions with downloadable digital resources."),
        ("Obj-06", "Enforce Strict Relational Integrity", "Guarantee zero orphaned records through primary keys, foreign keys, cascades, and check constraints."),
        ("Obj-07", "Role-Based Data Security", "Enforce privilege boundaries separating chief librarians, operational assistants, and library patrons."),
        ("Obj-08", "Analytical Reporting", "Provide instant reporting on circulation velocity, overdue items, fine revenues, and category popularity.")
    ]
    add_custom_table(["ID", "Objective", "Operational Target"], objectives_data, [2.5, 5.0, 9.0])

    # =========================================================================
    # SECTION 4: USERS AND ROLES
    # =========================================================================
    add_h1("4. Users and Role-Based Access Control")
    add_p(
        "To safeguard sensitive patron details and maintain transactional consistency, the database enforces role-based permissions across four primary user categories:"
    )
    roles_data = [
        ("Chief Librarian / Administrator", "Full CRUD authority over the catalog, member profiles, circulation parameters, and financial records. Can waive fines and generate administrative audits.", "ALL PRIVILEGES"),
        ("Assistant Librarian / Circulation Desk", "Executes day-to-day checkouts, returns, and renewals. Inspects inventory locations, issues receipt confirmations, and manages physical hold shelves.", "SELECT, INSERT, UPDATE on Issue, Copy, Fine, Reservation"),
        ("Library Patron (Student / Faculty / Public)", "Read-only access to public search catalogs, personal borrowing history, active fine balances, and authorized digital materials. Can enqueue book reservations.", "SELECT on Book, Edition, DigitalResource; INSERT on Reservation"),
        ("Automated Database Engine Agent", "Background triggers and stored procedures that calculate daily overdue penalties and expire uncollected reservations.", "EXECUTE on Triggers and Events")
    ]
    add_custom_table(["User Role", "System Description and Responsibilities", "Database Privileges"], roles_data, [4.0, 8.5, 4.0])

    # =========================================================================
    # SECTION 5: REQUIREMENTS SPECIFICATION
    # =========================================================================
    add_h1("5. Detailed Requirements Specification")

    add_h2("5.1 Functional Requirements")
    add_bullet_point("FR-01 (Catalog Management)", "System must permit authorized staff to record titles, ISBNs, authors, publishers, categories, and edition years.")
    add_bullet_point("FR-02 (Accession Control)", "Each individual physical book copy must receive a unique accession barcode identifier.")
    add_bullet_point("FR-03 (Patron Management)", "System must register members with start date, expiration date, contact info, and role-based loan quotas.")
    add_bullet_point("FR-04 (Circulation Validation)", "System must verify that a copy is currently Available and that the member has not exceeded their active loan quota prior to checkout.")
    add_bullet_point("FR-05 (Automatic Overdue Determination)", "Upon book return, the system must compute the difference between return date and due date, immediately recording a fine if overdue.")
    add_bullet_point("FR-06 (Waitlist Queueing)", "If all copies of a title are checked out, patrons may reserve the title; the system assigns incremental queue numbers.")
    add_bullet_point("FR-07 (Fine Settlement)", "Cashiers must be able to record partial or full fine settlements, updating fine status from Pending to Paid.")
    add_bullet_point("FR-08 (Digital Asset Tracking)", "Patrons can browse digital resources; every view or download must write an audit record with patron ID, asset ID, timestamp, and IP.")

    add_h2("5.2 Non-Functional Requirements")
    add_bullet_point("Data Integrity and Consistency", "All tables must adhere to Third Normal Form (3NF) to eliminate insertion, update, and deletion anomalies.")
    add_bullet_point("Performance and Indexing", "Search queries against Title, ISBN, Author, and Accession Number must execute within 100 milliseconds using B-Tree indexing.")
    add_bullet_point("Security and Privacy", "Member contact details and passwords must be protected against SQL injection and unauthorized external inspection.")
    add_bullet_point("Scalability", "The schema must scale efficiently to accommodate 100,000 catalog entries and 10,000 active members without schema revisions.")

    # =========================================================================
    # SECTION 6: BUSINESS RULES
    # =========================================================================
    add_h1("6. Business Rules and Integrity Constraints")
    add_p("The database schema enforces ten core business rules across all transactions:")
    rules_data = [
        ("BR-01", "ISBN Uniqueness", "The ISBN attribute must be strictly unique across all cataloged book titles."),
        ("BR-02", "Accession Barcode Uniqueness", "Each physical copy must possess a globally unique Accession Number."),
        ("BR-03", "Single Active Loan Constraint", "A physical copy can have at most one open issue record where Status is Active or Overdue."),
        ("BR-04", "Chronological Loan Dates", "The IssueDate must be chronologically earlier than or equal to the DueDate."),
        ("BR-05", "Valid Return Timestamp", "When a book is returned, ReturnDate must be greater than or equal to IssueDate."),
        ("BR-06", "FIFO Waitlist Fulfillment", "Available copies of reserved titles must be allocated strictly in ascending order of QueuePosition."),
        ("BR-07", "Non-Negative Fine Rule", "All calculated fine amounts must be greater than or equal to zero (Amount >= 0)."),
        ("BR-08", "Member Quota Enforcement", "A member cannot check out additional books once active loans equal MaxBooksAllowed (Students: 3, Faculty: 10)."),
        ("BR-09", "Digital Access Audit Trail", "Every digital asset download must record MemberID, ResourceID, AccessDate, and IPAddress."),
        ("BR-10", "Foreign Key Referential Integrity", "Every physical copy must link to a valid Edition, which must link to a valid Book and Publisher.")
    ]
    add_custom_table(["Rule ID", "Rule Name", "Enforcement Logic"], rules_data, [2.2, 4.8, 9.5])

    # =========================================================================
    # SECTION 7: ARCHITECTURE & MODULAR DESIGN
    # =========================================================================
    add_h1("7. System Architecture and Modular Design")
    add_p(
        "The system employs a three-tier architecture that decouples database persistence from application workflows and presentation interfaces."
    )
    add_bullet_point(
        "Tier 1: Presentation Layer",
        "A modern, responsive web application built with Streamlit and Plotly. Provides interactive dashboards, circulation check-in/check-out desks, catalogue search filters, fine collection desks, and real-time query consoles."
    )
    add_bullet_point(
        "Tier 2: Business Logic and Abstraction Layer",
        "Python application modules that enforce loan quota checks, compute overdue penalties, manage queue priority increments, and coordinate dual-engine database connectivity."
    )
    add_bullet_point(
        "Tier 3: Database Persistence Layer",
        "Dual-engine relational database architecture supporting enterprise MySQL Server (default on port 3306) and local SQLite embedded storage. Enables deployment in enterprise client-server configurations or standalone evaluation environments."
    )

    # =========================================================================
    # SECTION 8: CONCEPTUAL MODEL (ER MODEL)
    # =========================================================================
    add_h1("8. Conceptual Modeling (Entity-Relationship Model)")
    add_p(
        "The conceptual database model comprises 10 core entity sets and 4 associative relationship sets. "
        "The design cleanly models real-world library relationships including many-to-many book authorship, many-to-many topic classifications, and 1-to-many copy ownership."
    )
    er_entities = [
        ("Book", "Represents an abstract intellectual title.", "BookID (PK), ISBN, Title, Language, TotalPages, PublicationYear"),
        ("Author", "Represents creators of intellectual works.", "AuthorID (PK), FirstName, LastName, Bio"),
        ("Publisher", "Represents book publishing organizations.", "PublisherID (PK), Name, Address, Phone, Email"),
        ("Category", "Represents thematic subject classifications.", "CategoryID (PK), Name, Description"),
        ("Edition", "Represents specific published releases of a book.", "EditionID (PK), BookID (FK), EditionNumber, PublisherID (FK), PublicationDate, Format"),
        ("Copy", "Represents individual physical inventory items.", "CopyID (PK), AccessionNumber, EditionID (FK), Status, ShelfLocation, DateAcquired"),
        ("Member", "Represents library cardholders and patrons.", "MemberID (PK), FirstName, LastName, Email, Phone, MembershipType, MaxBooksAllowed"),
        ("Issue", "Captures physical copy borrowing transactions.", "IssueID (PK), CopyID (FK), MemberID (FK), IssueDate, DueDate, ReturnDate, Status"),
        ("Reservation", "Tracks waitlist requests for checked-out titles.", "ReservationID (PK), BookID (FK), MemberID (FK), ReservationDate, QueuePosition, Status"),
        ("Fine", "Tracks financial liabilities incurred from late returns.", "FineID (PK), IssueID (FK), MemberID (FK), Amount, Reason, FineDate, PaidDate, Status"),
        ("DigitalResource", "Metadata for electronic files and downloads.", "ResourceID (PK), BookID (FK), ResourceType, FileFormat, FileSize, URL"),
        ("DigitalAccessLog", "Immutable audit trail of digital downloads.", "LogID (PK), ResourceID (FK), MemberID (FK), AccessDate, AccessType, IPAddress")
    ]
    add_custom_table(["Entity Set", "Real-World Representation", "Key Attributes"], er_entities, [3.2, 5.0, 8.3])

    # =========================================================================
    # SECTION 9: RELATIONAL SCHEMA & NORMALIZATION
    # =========================================================================
    add_h1("9. Relational Schema and Normalization Analysis")

    add_h2("9.1 Relational Schema Notation")
    add_p("The normalized relational database schema is formally defined below. Primary keys are marked with PK and foreign keys with FK:")
    schema_definitions = [
        "1. Author (AuthorID [PK], FirstName, LastName, Bio)",
        "2. Publisher (PublisherID [PK], Name, Address, Phone, Email)",
        "3. Category (CategoryID [PK], Name, Description)",
        "4. Book (BookID [PK], ISBN, Title, Language, TotalPages, PublicationYear)",
        "5. BookAuthor (BookID [PK, FK], AuthorID [PK, FK])",
        "6. BookCategory (BookID [PK, FK], CategoryID [PK, FK])",
        "7. Edition (EditionID [PK], BookID [FK], EditionNumber, PublisherID [FK], PublicationDate, Format)",
        "8. Copy (CopyID [PK], AccessionNumber, EditionID [FK], Status, ShelfLocation, DateAcquired)",
        "9. Member (MemberID [PK], FirstName, LastName, Email, Phone, Address, MembershipType, MembershipStartDate, MembershipEndDate, MaxBooksAllowed, IsActive)",
        "10. Issue (IssueID [PK], CopyID [FK], MemberID [FK], IssueDate, DueDate, ReturnDate, Status)",
        "11. Reservation (ReservationID [PK], BookID [FK], MemberID [FK], ReservationDate, QueuePosition, Status, ExpiryDate)",
        "12. Fine (FineID [PK], IssueID [FK], MemberID [FK], Amount, Reason, FineDate, PaidDate, Status)",
        "13. DigitalResource (ResourceID [PK], BookID [FK], ResourceType, FileFormat, FileSize, URL, UploadDate)",
        "14. DigitalAccessLog (LogID [PK], ResourceID [FK], MemberID [FK], AccessDate, AccessType, IPAddress)"
    ]
    for s in schema_definitions:
        add_p(s, space_after=3)

    add_h2("9.2 Normalization Analysis")
    add_p(
        "The schema was decomposed systematically through First Normal Form (1NF), Second Normal Form (2NF), and Third Normal Form (3NF):"
    )
    add_bullet_point(
        "First Normal Form (1NF)",
        "Every attribute contains strictly atomic, indivisible values. Multi-valued attributes like authors and categories were extracted into separate junction tables (BookAuthor, BookCategory), eliminating repeating groups."
    )
    add_bullet_point(
        "Second Normal Form (2NF)",
        "The schema is in 1NF and contains no partial functional dependencies. In junction tables with composite primary keys (such as BookAuthor), there are no non-prime attributes dependent on only a subset of the candidate key."
    )
    add_bullet_point(
        "Third Normal Form (3NF)",
        "The schema is in 2NF and exhibits zero transitive dependencies. Non-key attributes depend exclusively and directly on the primary key. For example, publisher contact details are stored in Publisher rather than being duplicated in Edition or Book."
    )

    # =========================================================================
    # SECTION 10: COMPREHENSIVE DATA DICTIONARY
    # =========================================================================
    add_h1("10. Comprehensive Data Dictionary (All 14 Tables)")
    add_p("The complete technical specifications for all database attributes are documented in the tables below:")

    # Table 1: Book
    add_h2("Table 1: Book")
    t1 = [
        ("BookID", "INT", "PK, AUTO_INCREMENT", "Unique surrogate key for each book title"),
        ("ISBN", "VARCHAR(20)", "UNIQUE, NOT NULL", "International Standard Book Number"),
        ("Title", "VARCHAR(255)", "NOT NULL", "Full title of the intellectual work"),
        ("Language", "VARCHAR(50)", "NOT NULL, DEFAULT 'English'", "Primary language of publication"),
        ("TotalPages", "INT", "CHECK (TotalPages > 0)", "Total page count"),
        ("PublicationYear", "INT", "NOT NULL", "Original publication year")
    ]
    add_custom_table(["Column Name", "Data Type", "Constraints", "Description"], t1, [3.0, 3.0, 4.0, 6.5])

    # Table 2: Author
    add_h2("Table 2: Author")
    t2 = [
        ("AuthorID", "INT", "PK, AUTO_INCREMENT", "Unique author identifier"),
        ("FirstName", "VARCHAR(100)", "NOT NULL", "First name of author"),
        ("LastName", "VARCHAR(100)", "NOT NULL", "Last name or family name of author"),
        ("Bio", "TEXT", "NULLABLE", "Biographical background and credentials")
    ]
    add_custom_table(["Column Name", "Data Type", "Constraints", "Description"], t2, [3.0, 3.0, 4.0, 6.5])

    # Table 3: Publisher
    add_h2("Table 3: Publisher")
    t3 = [
        ("PublisherID", "INT", "PK, AUTO_INCREMENT", "Unique publisher identifier"),
        ("Name", "VARCHAR(150)", "UNIQUE, NOT NULL", "Corporate name of publishing house"),
        ("Address", "VARCHAR(255)", "NULLABLE", "Headquarters postal address"),
        ("Phone", "VARCHAR(20)", "NULLABLE", "Support contact number"),
        ("Email", "VARCHAR(100)", "NULLABLE", "Official contact email")
    ]
    add_custom_table(["Column Name", "Data Type", "Constraints", "Description"], t3, [3.0, 3.0, 4.0, 6.5])

    # Table 4: Category
    add_h2("Table 4: Category")
    t4 = [
        ("CategoryID", "INT", "PK, AUTO_INCREMENT", "Unique category identifier"),
        ("Name", "VARCHAR(100)", "UNIQUE, NOT NULL", "Thematic subject name"),
        ("Description", "TEXT", "NULLABLE", "Scope and classification notes")
    ]
    add_custom_table(["Column Name", "Data Type", "Constraints", "Description"], t4, [3.0, 3.0, 4.0, 6.5])

    # Table 5 & 6: Junction Tables
    add_h2("Table 5 & 6: BookAuthor and BookCategory (Junction Tables)")
    t5 = [
        ("BookAuthor.BookID", "INT", "PK, FK to Book", "References associated book"),
        ("BookAuthor.AuthorID", "INT", "PK, FK to Author", "References contributing author"),
        ("BookCategory.BookID", "INT", "PK, FK to Book", "References associated book"),
        ("BookCategory.CategoryID", "INT", "PK, FK to Category", "References assigned subject category")
    ]
    add_custom_table(["Column Name", "Data Type", "Constraints", "Description"], t5, [4.0, 2.5, 3.5, 6.5])

    # Table 7: Edition
    add_h2("Table 7: Edition")
    t7 = [
        ("EditionID", "INT", "PK, AUTO_INCREMENT", "Unique identifier for published edition"),
        ("BookID", "INT", "FK to Book, NOT NULL", "Parent book title"),
        ("EditionNumber", "INT", "CHECK (EditionNumber > 0)", "Ordinal edition number"),
        ("PublisherID", "INT", "FK to Publisher, NOT NULL", "Publishing agency"),
        ("PublicationDate", "DATE", "NOT NULL", "Official date of publication"),
        ("Format", "VARCHAR(50)", "NOT NULL", "Physical binding format (Paperback, Hardcover)")
    ]
    add_custom_table(["Column Name", "Data Type", "Constraints", "Description"], t7, [3.0, 3.0, 4.0, 6.5])

    # Table 8: Copy
    add_h2("Table 8: Copy")
    t8 = [
        ("CopyID", "INT", "PK, AUTO_INCREMENT", "Unique copy identifier"),
        ("AccessionNumber", "VARCHAR(50)", "UNIQUE, NOT NULL", "Physical barcode / inventory accession tag"),
        ("EditionID", "INT", "FK to Edition, NOT NULL", "Referenced book edition"),
        ("Status", "VARCHAR(20)", "DEFAULT 'Available'", "State (Available, Issued, Reserved, Damaged)"),
        ("ShelfLocation", "VARCHAR(100)", "NULLABLE", "Stack rack and shelf identifier"),
        ("DateAcquired", "DATE", "NOT NULL", "Inventory intake date")
    ]
    add_custom_table(["Column Name", "Data Type", "Constraints", "Description"], t8, [3.0, 3.0, 4.0, 6.5])

    # Table 9: Member
    add_h2("Table 9: Member")
    t9 = [
        ("MemberID", "INT", "PK, AUTO_INCREMENT", "Unique membership card identifier"),
        ("FirstName", "VARCHAR(100)", "NOT NULL", "Patron given name"),
        ("LastName", "VARCHAR(100)", "NOT NULL", "Patron family name"),
        ("Email", "VARCHAR(150)", "UNIQUE, NOT NULL", "Official email address"),
        ("Phone", "VARCHAR(20)", "NOT NULL", "Primary mobile phone contact"),
        ("MembershipType", "VARCHAR(20)", "NOT NULL", "Category (Student, Faculty, Staff, Public)"),
        ("MaxBooksAllowed", "INT", "CHECK (MaxBooksAllowed > 0)", "Maximum simultaneous checked-out copies"),
        ("IsActive", "BOOLEAN", "DEFAULT TRUE", "Account validity status flag")
    ]
    add_custom_table(["Column Name", "Data Type", "Constraints", "Description"], t9, [3.0, 3.0, 4.0, 6.5])

    # Table 10: Issue
    add_h2("Table 10: Issue")
    t10 = [
        ("IssueID", "INT", "PK, AUTO_INCREMENT", "Unique transaction receipt identifier"),
        ("CopyID", "INT", "FK to Copy, NOT NULL", "Physical copy on loan"),
        ("MemberID", "INT", "FK to Member, NOT NULL", "Borrowing cardholder"),
        ("IssueDate", "DATE", "NOT NULL", "Checkout transaction date"),
        ("DueDate", "DATE", "NOT NULL", "Scheduled deadline for item return"),
        ("ReturnDate", "DATE", "NULLABLE", "Actual check-in date"),
        ("Status", "VARCHAR(20)", "DEFAULT 'Active'", "State (Active, Returned, Overdue)")
    ]
    add_custom_table(["Column Name", "Data Type", "Constraints", "Description"], t10, [3.0, 3.0, 4.0, 6.5])

    # Table 11: Reservation
    add_h2("Table 11: Reservation")
    t11 = [
        ("ReservationID", "INT", "PK, AUTO_INCREMENT", "Unique waitlist token identifier"),
        ("BookID", "INT", "FK to Book, NOT NULL", "Requested book title"),
        ("MemberID", "INT", "FK to Member, NOT NULL", "Requesting cardholder"),
        ("ReservationDate", "DATETIME", "NOT NULL", "Waitlist submission timestamp"),
        ("QueuePosition", "INT", "CHECK (QueuePosition >= 1)", "FIFO waitlist ordinal index"),
        ("Status", "VARCHAR(20)", "DEFAULT 'Pending'", "State (Pending, Fulfilled, Expired, Cancelled)"),
        ("ExpiryDate", "DATETIME", "NULLABLE", "Pickup window expiration timestamp")
    ]
    add_custom_table(["Column Name", "Data Type", "Constraints", "Description"], t11, [3.0, 3.0, 4.0, 6.5])

    # Table 12: Fine
    add_h2("Table 12: Fine")
    t12 = [
        ("FineID", "INT", "PK, AUTO_INCREMENT", "Unique fine assessment voucher"),
        ("IssueID", "INT", "FK to Issue, NOT NULL", "Associated overdue loan transaction"),
        ("MemberID", "INT", "FK to Member, NOT NULL", "Liable cardholder"),
        ("Amount", "DECIMAL(10,2)", "CHECK (Amount >= 0)", "Financial penalty assessed"),
        ("Reason", "VARCHAR(255)", "NOT NULL", "Explanatory description of penalty"),
        ("FineDate", "DATE", "NOT NULL", "Assessment date"),
        ("PaidDate", "DATE", "NULLABLE", "Settlement timestamp"),
        ("Status", "VARCHAR(20)", "DEFAULT 'Pending'", "State (Pending, Paid, Waived)")
    ]
    add_custom_table(["Column Name", "Data Type", "Constraints", "Description"], t12, [3.0, 3.0, 4.0, 6.5])

    # Table 13: DigitalResource
    add_h2("Table 13: DigitalResource")
    t13 = [
        ("ResourceID", "INT", "PK, AUTO_INCREMENT", "Unique digital media asset identifier"),
        ("BookID", "INT", "FK to Book, NOT NULL", "Associated catalog title"),
        ("ResourceType", "VARCHAR(50)", "NOT NULL", "Category (EBook, Audiobook, Supplement)"),
        ("FileFormat", "VARCHAR(20)", "NOT NULL", "MIME/extension format (PDF, EPUB, MP3)"),
        ("FileSize", "VARCHAR(30)", "NOT NULL", "Asset storage footprint (e.g. 24.5 MB)"),
        ("URL", "VARCHAR(255)", "NOT NULL", "Secure asset storage URI")
    ]
    add_custom_table(["Column Name", "Data Type", "Constraints", "Description"], t13, [3.0, 3.0, 4.0, 6.5])

    # Table 14: DigitalAccessLog
    add_h2("Table 14: DigitalAccessLog")
    t14 = [
        ("LogID", "INT", "PK, AUTO_INCREMENT", "Immutable security audit record identifier"),
        ("ResourceID", "INT", "FK to DigitalResource", "Accessed digital asset"),
        ("MemberID", "INT", "FK to Member", "Accessing cardholder"),
        ("AccessDate", "DATETIME", "NOT NULL", "Exact access event timestamp"),
        ("AccessType", "VARCHAR(50)", "DEFAULT 'View'", "Interaction mode (View, Download, Stream)"),
        ("IPAddress", "VARCHAR(45)", "NOT NULL", "IPv4 or IPv6 client network address")
    ]
    add_custom_table(["Column Name", "Data Type", "Constraints", "Description"], t14, [3.0, 3.0, 4.0, 6.5])

    # =========================================================================
    # SECTION 11: FULLY WORKING MODEL IMPLEMENTATION
    # =========================================================================
    add_h1("11. Fully Working Model Implementation")
    add_p(
        "A fully functional software model was engineered to realize the database specifications. "
        "The model delivers an end-to-end user experience, supporting dual-engine persistence, transactional circulation desks, "
        "automated fine calculation, interactive analytics dashboards, and live SQL execution."
    )

    add_h2("11.1 Technology Stack")
    add_bullet_point("Frontend Framework", "Streamlit 1.53.1 providing responsive multi-tab layout, interactive state management, and real-time form inputs.")
    add_bullet_point("Visualization Engine", "Plotly 6.5.2 delivering interactive donut charts, category distribution bars, and inventory velocity plots.")
    add_bullet_point("Database Layer", "Dual-engine architecture utilizing MySQL 8.4 Server and embedded SQLite 3 with seamless automated failover.")
    add_bullet_point("Data Manipulation", "Pandas 2.3.3 for analytical joins, aggregation summaries, and tabular data presentation.")

    add_h2("11.2 Core Operational Workflows")
    add_p(
        "The model automates several critical library operations through well-defined algorithmic workflows:"
    )
    add_bullet_point(
        "Book Checkout Workflow",
        "The system queries Member active loans. If active loans are less than MaxBooksAllowed and the selected copy status is Available, the issue record is created, and copy status transitions immediately to Issued."
    )
    add_bullet_point(
        "Book Return and Overdue Fine Workflow",
        "Upon return, the system checks whether the current date exceeds DueDate. If overdue, overdue days are multiplied by the institutional rate (Rs 5.00 per day), copy status returns to Available, and a pending Fine record is automatically logged."
    )
    add_bullet_point(
        "FIFO Reservation Allocation",
        "When all copies are checked out, patrons place reservations. The system evaluates existing pending requests for that book and assigns the next incremental QueuePosition."
    )
    add_bullet_point(
        "Digital Access Auditing",
        "When an authenticated patron requests an e-book or audiobook download, the system generates an audit record capturing MemberID, ResourceID, current timestamp, and client IP address."
    )

    # =========================================================================
    # SECTION 12: ADVANCED SQL QUERIES & RESULTS
    # =========================================================================
    add_h1("12. Advanced SQL Queries and Evaluation Results")
    add_p("The database was validated against complex queries demonstrating advanced relational operations:")

    add_h2("12.1 Query 1: Comprehensive Multi-Table Circulation Ledger")
    add_p("Demonstrates 5-table inner joins across transactions, inventory copies, editions, titles, and patrons:")
    add_p(
        "SELECT i.IssueID, b.Title, cp.AccessionNumber, m.FirstName, m.LastName, m.MembershipType, i.DueDate, i.Status "
        "FROM Issue i "
        "JOIN Copy cp ON i.CopyID = cp.CopyID "
        "JOIN Edition e ON cp.EditionID = e.EditionID "
        "JOIN Book b ON e.BookID = b.BookID "
        "JOIN Member m ON i.MemberID = m.MemberID;",
        italic=True, space_after=6
    )

    add_h2("12.2 Query 2: Aggregate Group By with Having Filter")
    add_p("Identifies patron membership types with active borrowing volume exceeding minimum thresholds:")
    add_p(
        "SELECT m.MembershipType, COUNT(i.IssueID) AS TotalLoans "
        "FROM Member m "
        "JOIN Issue i ON m.MemberID = i.MemberID "
        "GROUP BY m.MembershipType "
        "HAVING COUNT(i.IssueID) >= 1;",
        italic=True, space_after=6
    )

    add_h2("12.3 Query 3: Correlated Subquery for Unissued Inventory")
    add_p("Retrieves all titles that have physical editions but zero currently checked-out copies:")
    add_p(
        "SELECT b.BookID, b.Title, b.ISBN "
        "FROM Book b "
        "WHERE NOT EXISTS ( "
        "    SELECT 1 FROM Edition e "
        "    JOIN Copy cp ON e.EditionID = cp.EditionID "
        "    WHERE e.BookID = b.BookID AND cp.Status = 'Issued' "
        ");",
        italic=True, space_after=6
    )

    # =========================================================================
    # SECTION 13: TEST MATRIX
    # =========================================================================
    add_h1("13. System Verification and Test Matrix")
    add_p("A rigorous suite of validation test cases was executed against the working model:")
    test_cases = [
        ("TC-01", "ISBN Uniqueness", "Insert duplicate ISBN '978-0078022159'", "Database rejects with unique constraint violation", "Passed"),
        ("TC-02", "Quota Enforcement", "Attempt 4th issue for student with max quota of 3", "System blocks checkout with limit error notification", "Passed"),
        ("TC-03", "Auto Fine Calculation", "Check in book 8 days past due date", "Fine record created for Rs 40.00 (8 days x Rs 5/day)", "Passed"),
        ("TC-04", "FIFO Reservation Queue", "Two members reserve same checked-out title", "First assigned QueuePosition 1; second assigned QueuePosition 2", "Passed"),
        ("TC-05", "Digital Access Log", "Patron clicks download on EBook asset", "New record generated in DigitalAccessLog with timestamp and IP", "Passed"),
        ("TC-06", "Fine Settlement", "Cashier marks pending fine as Paid", "Fine status transitions to Paid and sets PaidDate timestamp", "Passed")
    ]
    add_custom_table(["Test ID", "Scenario", "Input / Action", "Expected and Actual Result", "Status"], test_cases, [1.8, 3.2, 4.2, 5.3, 2.0])

    # =========================================================================
    # SECTION 14: CONCLUSION & ROADMAP
    # =========================================================================
    add_h1("14. Conclusion and Future Roadmap")

    add_h2("14.1 Conclusion")
    add_p(
        "The Library Circulation and Digital Resource Management System successfully fulfills all project-based learning objectives. "
        "The relational schema adheres strictly to Third Normal Form, ensuring complete data consistency across physical copies, multi-author books, "
        "patron memberships, circulation transactions, and digital media logs. "
        "The accompanying interactive model provides librarians with an intuitive control center, eliminating manual calculation errors and guaranteeing fair waitlist allocations."
    )

    add_h2("14.2 Future Roadmap")
    add_bullet_point("RFID Hardware Integration", "Linking physical book RFID antennas for automated self-checkout and shelf inventory scans.")
    add_bullet_point("Digital Rights Management (DRM)", "Implementing time-limited encryption for downloaded e-books to enforce automatic expiration.")
    add_bullet_point("SMS and Email Webhooks", "Automating instant reminders 48 hours prior to loan due dates to minimize overdue occurrences.")

    # Save Document
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Final_Project_Report.docx')
    doc.save(out_path)
    return out_path

if __name__ == '__main__':
    out_file = create_report()
    print("Report generated successfully at:", out_file)
