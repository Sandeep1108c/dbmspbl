"""
Generate Review 1 Report Word Document
Library Circulation and Digital Resource Management System
"""

from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.style import WD_STYLE_TYPE
import os

doc = Document()

# ── Page Setup ──
for section in doc.sections:
    section.top_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.left_margin = Cm(2.54)
    section.right_margin = Cm(2.54)

# ── Styles ──
style = doc.styles['Normal']
font = style.font
font.name = 'Calibri'
font.size = Pt(11)
font.color.rgb = RGBColor(0x1A, 0x1A, 0x2E)

for i in range(1, 4):
    heading_style = doc.styles[f'Heading {i}']
    heading_style.font.name = 'Calibri'
    heading_style.font.color.rgb = RGBColor(0x0D, 0x47, 0xA1)
    if i == 1:
        heading_style.font.size = Pt(22)
    elif i == 2:
        heading_style.font.size = Pt(16)
    else:
        heading_style.font.size = Pt(13)

# ── Helper Functions ──
def add_styled_table(doc, headers, rows):
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = 'Light Grid Accent 1'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    # Header row
    for i, header in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = header
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.bold = True
                run.font.size = Pt(10)
                run.font.color.rgb = RGBColor(0x0D, 0x47, 0xA1)

    # Data rows
    for r, row_data in enumerate(rows):
        for c, val in enumerate(row_data):
            cell = table.rows[r + 1].cells[c]
            cell.text = str(val)
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.font.size = Pt(10)

    doc.add_paragraph()
    return table

def add_bullet(doc, text, bold_prefix=None, level=0):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.left_indent = Cm(1.27 + level * 0.63)
    if bold_prefix:
        run = p.add_run(bold_prefix)
        run.bold = True
        run.font.size = Pt(11)
        p.add_run(text)
    else:
        p.add_run(text)

# ═══════════════════════════════════════════════════
#                     TITLE PAGE
# ═══════════════════════════════════════════════════

doc.add_paragraph()
doc.add_paragraph()
doc.add_paragraph()

title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = title.add_run("DESIGN AND IMPLEMENTATION OF A\nDATABASE MANAGEMENT SYSTEM FOR")
run.bold = True
run.font.size = Pt(24)
run.font.color.rgb = RGBColor(0x0D, 0x47, 0xA1)

subtitle = doc.add_paragraph()
subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = subtitle.add_run("Library Circulation and\nDigital Resource Management System")
run.bold = True
run.font.size = Pt(20)
run.font.color.rgb = RGBColor(0x1B, 0x5E, 0x20)

doc.add_paragraph()

review = doc.add_paragraph()
review.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = review.add_run("REVIEW 1: PROJECT REPORT")
run.bold = True
run.font.size = Pt(16)
run.font.color.rgb = RGBColor(0x42, 0x42, 0x42)

doc.add_paragraph()
doc.add_paragraph()

info = doc.add_paragraph()
info.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = info.add_run("Database Management Systems: Project Based Learning")
run.font.size = Pt(12)
run.font.color.rgb = RGBColor(0x61, 0x61, 0x61)

doc.add_paragraph()

sep = doc.add_paragraph()
sep.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = sep.add_run("━" * 50)
run.font.color.rgb = RGBColor(0x0D, 0x47, 0xA1)

doc.add_page_break()

# ═══════════════════════════════════════════════════
#                  TABLE OF CONTENTS
# ═══════════════════════════════════════════════════

doc.add_heading('Table of Contents', level=1)
toc_items = [
    "1. Problem Identification",
    "2. Scope",
    "3. Objectives",
    "4. Users and User Roles",
    "5. Functional Requirements",
    "6. Non-Functional Requirements",
    "7. Business Rules",
    "8. ER Diagram",
    "9. Initial Relational Schema",
]
for item in toc_items:
    p = doc.add_paragraph(item)
    p.paragraph_format.space_after = Pt(4)
    p.runs[0].font.size = Pt(12)

doc.add_page_break()

# ═══════════════════════════════════════════════════
#           1. PROBLEM IDENTIFICATION
# ═══════════════════════════════════════════════════

doc.add_heading('1. Problem Identification', level=1)
doc.add_paragraph(
    "Traditional and manual library management systems often struggle with inefficiencies "
    "that hinder both staff productivity and patron experience. The primary problems identified "
    "in the current manual or disjointed systems include:"
)

problems = [
    ("Unreliable Tracking: ", "Manual ledgers and outdated systems lead to discrepancies in tracking book locations, availability, and member histories, increasing the risk of lost or misplaced items."),
    ("Lack of Digital Resource Management: ", "Modern libraries possess significant digital assets (e-books, journals, audiobooks), but older systems completely lack the infrastructure to track, log, or manage access to these digital resources."),
    ("Manual Fine Calculation: ", "Calculating overdue fines manually is prone to human error, inconsistencies, and disputes. It also creates unnecessary administrative overhead for librarians."),
    ("Inefficient Reservation Queuing: ", "Without an automated system, handling reservations for popular books becomes chaotic, leading to unfair distribution and frustrated patrons."),
    ("Data Redundancy and Inconsistency: ", "Information about members, books, and transactions is often duplicated across different registers, leading to data anomalies and making it difficult to generate accurate reports."),
]
for prefix, text in problems:
    add_bullet(doc, text, prefix)

# ═══════════════════════════════════════════════════
#                   2. SCOPE
# ═══════════════════════════════════════════════════

doc.add_heading('2. Scope', level=1)

doc.add_heading('In-Scope', level=2)
in_scope = [
    ("Physical Asset Management: ", "Cataloging and tracking printed books, journals, and physical media."),
    ("Digital Resource Management: ", "Managing metadata and access logs for digital assets such as e-books, e-journals, and audiobooks."),
    ("Member Management: ", "Registration, profiling, and tracking of various member types (Students, Faculty, External)."),
    ("Circulation Management: ", "Complete handling of issue, return, and renewal processes for physical copies."),
    ("Reservation System: ", "Automated queuing and notification for reserved items."),
    ("Fine Management: ", "Automated calculation, tracking, and settlement of overdue fines."),
    ("Digital Access Logging: ", "Monitoring and recording user interactions with digital resources for usage analytics."),
]
for prefix, text in in_scope:
    add_bullet(doc, text, prefix)

doc.add_heading('Out of Scope', level=2)
out_scope = [
    "Inter-library loan systems and networking with external library databases.",
    "E-commerce or financial payment gateway integration for purchasing books or paying fines online.",
    "Advanced AI-driven recommendation engines (e.g., collaborative filtering).",
]
for text in out_scope:
    add_bullet(doc, text)

# ═══════════════════════════════════════════════════
#                 3. OBJECTIVES
# ═══════════════════════════════════════════════════

doc.add_heading('3. Objectives', level=1)
doc.add_paragraph("The core objectives of developing this database system are:")

objectives = [
    ("Maintain a Comprehensive Catalogue: ", "Centralize and organize information for all physical and digital library assets."),
    ("Track Circulation Accurately: ", "Provide real-time status updates on issues, returns, and inventory levels."),
    ("Automate Fine Management: ", "Implement a flawless, rule-based system for calculating and tracking overdue fines."),
    ("Manage Reservations Efficiently: ", "Automate the reservation queue to ensure fair and organized distribution of requested materials."),
    ("Log Digital Resource Access: ", "Accurately record interactions with digital media to track usage and engagement."),
    ("Generate Insightful Reports: ", "Provide dynamic reporting capabilities on inventory, member history, popular items, and financial collections."),
    ("Enforce Data Integrity: ", "Utilize strict relational constraints (Primary Keys, Foreign Keys, Checks) to prevent data corruption."),
    ("Implement Role-Based Access Control: ", "Secure the system by restricting operations based on predefined user roles and permissions."),
    ("Improve Searchability: ", "Enable fast, multi-parameter searches across the entire library catalogue."),
    ("Streamline Administrative Tasks: ", "Reduce manual workloads for librarians, allowing them to focus on member services."),
]
for i, (prefix, text) in enumerate(objectives, 1):
    p = doc.add_paragraph(style='List Number')
    run = p.add_run(prefix)
    run.bold = True
    p.add_run(text)

# ═══════════════════════════════════════════════════
#            4. USERS AND USER ROLES
# ═══════════════════════════════════════════════════

doc.add_heading('4. Users and User Roles', level=1)

user_roles = [
    ["Admin / Chief Librarian", "Has full CRUD (Create, Read, Update, Delete) access to the entire database. Can manage the catalogue, administer member accounts, process issues/returns, manually adjust fines, override system defaults, and generate all administrative reports."],
    ["Assistant Librarian", "Has operational privileges. Can process day-to-day issues and returns, search the catalogue, manage member queries, and administer the reservation queues. Cannot modify system configurations or delete major records."],
    ["Member (Student / Faculty / External)", "Has read-only access to the public catalogue. Can search for items, view real-time availability, place and cancel reservations, view their own borrowing history, check outstanding fines, and access digital resources."],
    ["System / Automated Agent", "Background database processes (Triggers, Events, Jobs) responsible for automated tasks such as daily fine calculation, auto-expiring unfulfilled reservations, and managing the state of the reservation FIFO queue."],
]
add_styled_table(doc, ["User Role", "Description & Permissions"], user_roles)

# ═══════════════════════════════════════════════════
#          5. FUNCTIONAL REQUIREMENTS
# ═══════════════════════════════════════════════════

doc.add_heading('5. Functional Requirements', level=1)

doc.add_heading('Catalogue Management', level=2)
fr_catalogue = [
    ["FR-001", "The system shall allow authorized staff to add, edit, or remove book records, authors, publishers, and categories."],
    ["FR-002", "The system shall support the management of multiple editions and physical copies for a single title."],
    ["FR-003", "The system must enforce unique ISBNs for book titles and unique Accession Numbers for physical copies."],
]
add_styled_table(doc, ["ID", "Requirement"], fr_catalogue)

doc.add_heading('Member Management', level=2)
fr_member = [
    ["FR-004", "The system shall allow the registration of new members and the updating of existing member profiles."],
    ["FR-005", "The system shall categorize members into types (Student, Faculty, External) to enforce type-specific borrowing rules."],
    ["FR-006", "The system shall track and enforce membership validity periods."],
]
add_styled_table(doc, ["ID", "Requirement"], fr_member)

doc.add_heading('Circulation (Issue/Return)', level=2)
fr_circ = [
    ["FR-007", "The system shall process the issuing of physical copies to registered, valid members."],
    ["FR-008", "The system shall enforce that a physical copy can only have one active issue transaction at any given time."],
    ["FR-009", "The system shall record return dates accurately and automatically calculate the number of overdue days."],
]
add_styled_table(doc, ["ID", "Requirement"], fr_circ)

doc.add_heading('Reservation Management', level=2)
fr_res = [
    ["FR-010", "The system shall allow members to place reservations on titles where all physical copies are currently issued."],
    ["FR-011", "The system shall maintain reservation requests in a strict First-In-First-Out (FIFO) queue."],
    ["FR-012", "The system shall automatically expire reservations if the item is not claimed within a defined timeframe."],
]
add_styled_table(doc, ["ID", "Requirement"], fr_res)

doc.add_heading('Fine Management', level=2)
fr_fine = [
    ["FR-013", "The system shall automatically calculate fines based on the number of overdue days and predefined fine rates."],
    ["FR-014", "The system shall track partial and full fine payments made by members."],
    ["FR-015", "The system shall ensure fine amounts are never recorded as negative values."],
]
add_styled_table(doc, ["ID", "Requirement"], fr_fine)

doc.add_heading('Digital Resource Management', level=2)
fr_digital = [
    ["FR-016", "The system shall maintain records for non-physical resources like e-books, e-journals, and audiobooks."],
    ["FR-017", "The system shall securely log every member access (download/view) to a digital resource."],
]
add_styled_table(doc, ["ID", "Requirement"], fr_digital)

doc.add_heading('Search & Reports', level=2)
fr_search = [
    ["FR-018", "The system shall provide search functionality across the catalogue by Title, Author, ISBN, and Category."],
    ["FR-019", "The system shall generate comprehensive reports: available titles, overdue copies, member histories, popular books, and fine collections."],
]
add_styled_table(doc, ["ID", "Requirement"], fr_search)

# ═══════════════════════════════════════════════════
#        6. NON-FUNCTIONAL REQUIREMENTS
# ═══════════════════════════════════════════════════

doc.add_heading('6. Non-Functional Requirements', level=1)

nfr = [
    ("Data Integrity and Consistency: ", "The database schema must strictly adhere to normalization principles (up to 3NF/BCNF) and enforce constraints to prevent orphaned records and anomalous states."),
    ("Performance: ", "Complex queries, especially catalogue searches and availability checks, must execute efficiently, utilizing proper indexing on frequently searched columns (e.g., ISBN, Title, Author)."),
    ("Security: ", "The database must enforce strict Role-Based Access Control (RBAC), ensuring members cannot modify data and staff only have necessary permissions."),
    ("Scalability: ", "The architecture must be capable of handling thousands of active members, a catalogue of millions of items, and concurrent transaction processing without performance degradation."),
    ("Backup and Recovery: ", "The system must support scheduled automated backups and provide mechanisms for swift recovery in the event of hardware failure or data corruption."),
]
for prefix, text in nfr:
    add_bullet(doc, text, prefix)

# ═══════════════════════════════════════════════════
#              7. BUSINESS RULES
# ═══════════════════════════════════════════════════

doc.add_heading('7. Business Rules', level=1)
doc.add_paragraph("The database design and application logic will be governed by the following core business rules:")

br_data = [
    ["BR-01", "The ISBN must be unique across all book records."],
    ["BR-02", "The Accession number must be completely unique across all physical copies in the library."],
    ["BR-03", "A physical copy can have at most one active issue transaction at a time."],
    ["BR-04", "The Issue_Date must always be chronologically prior to or exactly equal to the Due_Date."],
    ["BR-05", "If a book is returned, the Return_Date must be chronologically on or after the Issue_Date."],
    ["BR-06", "Reservations for a title must be fulfilled strictly according to the FIFO queue order."],
    ["BR-07", "Fine amounts (both calculated and outstanding) must always be non-negative values (≥ 0)."],
    ["BR-08", "A member is restricted to a maximum of N concurrently active issues, where N is configurable based on membership type."],
    ["BR-09", "Digital access logs must persistently record the specific Member, Digital Resource, and exact Timestamp of access."],
    ["BR-10", "Every physical copy must be directly linked to a valid, existing book edition record in the catalogue."],
]
add_styled_table(doc, ["Rule ID", "Business Rule"], br_data)

doc.add_page_break()

# ═══════════════════════════════════════════════════
#               8. ER DIAGRAM
# ═══════════════════════════════════════════════════

doc.add_heading('8. Entity-Relationship (ER) Diagram', level=1)
doc.add_paragraph(
    "The following ER Diagram illustrates the conceptual design of the Library Circulation and Digital Resource "
    "Management System, showing all principal entities, their attributes, and relationships with cardinality notation."
)

er_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ER_Diagram.png")
if os.path.exists(er_path):
    doc.add_picture(er_path, width=Inches(6.0))
    last_para = doc.paragraphs[-1]
    last_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    caption = doc.add_paragraph("Figure 1: Entity-Relationship Diagram")
    caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
    caption.runs[0].italic = True
    caption.runs[0].font.size = Pt(10)
    caption.runs[0].font.color.rgb = RGBColor(0x61, 0x61, 0x61)
else:
    doc.add_paragraph("[ER Diagram image not found: please place ER_Diagram.png in the same folder]")

doc.add_paragraph()

# Entity listing
doc.add_heading('Entities and Relationships Summary', level=2)

entity_summary = [
    ["Book", "BookID (PK), ISBN, Title, Language, TotalPages, PublicationYear"],
    ["Author", "AuthorID (PK), FirstName, LastName, Bio"],
    ["BookAuthor", "BookID (PK, FK), AuthorID (PK, FK)"],
    ["Publisher", "PublisherID (PK), Name, Address, Phone, Email"],
    ["Category", "CategoryID (PK), Name, Description"],
    ["BookCategory", "BookID (PK, FK), CategoryID (PK, FK)"],
    ["Edition", "EditionID (PK), BookID (FK), EditionNumber, PublisherID (FK), PublicationDate, Format"],
    ["Copy", "CopyID (PK), AccessionNumber, EditionID (FK), Status, ShelfLocation, DateAcquired"],
    ["Member", "MemberID (PK), FirstName, LastName, Email, Phone, Address, MembershipType, IsActive"],
    ["Issue", "IssueID (PK), CopyID (FK), MemberID (FK), IssueDate, DueDate, ReturnDate, Status"],
    ["Reservation", "ReservationID (PK), BookID (FK), MemberID (FK), ReservationDate, QueuePosition, Status, ExpiryDate"],
    ["Fine", "FineID (PK), IssueID (FK), MemberID (FK), Amount, Reason, FineDate, PaidDate, Status"],
    ["DigitalResource", "ResourceID (PK), BookID (FK), ResourceType, FileFormat, FileSize, URL, UploadDate"],
    ["DigitalAccessLog", "LogID (PK), ResourceID (FK), MemberID (FK), AccessDate, AccessType, IPAddress"],
]
add_styled_table(doc, ["Entity", "Key Attributes"], entity_summary)

# Relationships table
doc.add_heading('Relationships', level=2)
rel_data = [
    ["Book", "has", "Author", "M:N (via BookAuthor)", "A book can have multiple authors and vice versa"],
    ["Book", "belongs to", "Category", "M:N (via BookCategory)", "A book can belong to multiple categories"],
    ["Book", "has", "Edition", "1:N", "A single book can have multiple editions"],
    ["Edition", "published by", "Publisher", "N:1", "Multiple editions can be from the same publisher"],
    ["Edition", "has", "Copy", "1:N", "An edition can have multiple physical copies"],
    ["Copy", "issued in", "Issue", "1:N", "A copy can be issued multiple times (1 active)"],
    ["Member", "takes", "Issue", "1:N", "A member can borrow multiple copies over time"],
    ["Member", "places", "Reservation", "1:N", "A member can place multiple reservations"],
    ["Book", "has", "Reservation", "1:N", "A book can have multiple reservations"],
    ["Issue", "generates", "Fine", "1:N", "An issue can generate fines (overdue, damage)"],
    ["Member", "incurs", "Fine", "1:N", "A member can incur multiple fines"],
    ["Book", "has", "DigitalResource", "1:N", "A book can have multiple digital resources"],
    ["DigitalResource", "accessed in", "DigitalAccessLog", "1:N", "A resource can be accessed many times"],
    ["Member", "logs", "DigitalAccessLog", "1:N", "A member can have multiple access logs"],
]
add_styled_table(doc, ["Entity 1", "Relationship", "Entity 2", "Cardinality", "Description"], rel_data)

doc.add_page_break()

# ═══════════════════════════════════════════════════
#          9. INITIAL RELATIONAL SCHEMA
# ═══════════════════════════════════════════════════

doc.add_heading('9. Initial Relational Schema', level=1)
doc.add_paragraph(
    "The following relational schema diagram shows all 14 tables with their columns, data types, primary keys, "
    "and foreign key relationships."
)

schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Relational_Schema.png")
if os.path.exists(schema_path):
    doc.add_picture(schema_path, width=Inches(6.0))
    last_para = doc.paragraphs[-1]
    last_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    caption = doc.add_paragraph("Figure 2: Relational Schema Diagram")
    caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
    caption.runs[0].italic = True
    caption.runs[0].font.size = Pt(10)
    caption.runs[0].font.color.rgb = RGBColor(0x61, 0x61, 0x61)
else:
    doc.add_paragraph("[Schema Diagram image not found: please place Relational_Schema.png in the same folder]")

doc.add_paragraph()

# Relational Notation
doc.add_heading('Relational Notation', level=2)
doc.add_paragraph("Bold = Primary Key | Italic = Foreign Key | Bold+Italic = Both PK and FK")
doc.add_paragraph()

schema_notation = [
    'Book(BookID, ISBN, Title, Language, TotalPages, PublicationYear)',
    'Author(AuthorID, FirstName, LastName, Bio)',
    'BookAuthor(BookID, AuthorID) (composite PK, both FK)',
    'Publisher(PublisherID, Name, Address, Phone, Email)',
    'Category(CategoryID, Name, Description)',
    'BookCategory(BookID, CategoryID) (composite PK, both FK)',
    'Edition(EditionID, BookID, EditionNumber, PublisherID, PublicationDate, Format)',
    'Copy(CopyID, AccessionNumber, EditionID, Status, ShelfLocation, DateAcquired)',
    'Member(MemberID, FirstName, LastName, Email, Phone, Address, MembershipType, MembershipStartDate, MembershipEndDate, MaxBooksAllowed, IsActive)',
    'Issue(IssueID, CopyID, MemberID, IssueDate, DueDate, ReturnDate, Status)',
    'Reservation(ReservationID, BookID, MemberID, ReservationDate, QueuePosition, Status, ExpiryDate)',
    'Fine(FineID, IssueID, MemberID, Amount, Reason, FineDate, PaidDate, Status)',
    'DigitalResource(ResourceID, BookID, ResourceType, FileFormat, FileSize, URL, UploadDate)',
    'DigitalAccessLog(LogID, ResourceID, MemberID, AccessDate, AccessType, IPAddress)',
]
for i, notation in enumerate(schema_notation, 1):
    p = doc.add_paragraph(f"{i}. {notation}")
    p.runs[0].font.size = Pt(10)
    p.runs[0].font.name = 'Consolas'

doc.add_paragraph()

# PK/FK Summary table
doc.add_heading('Primary Keys and Foreign Keys Summary', level=2)
pk_fk_data = [
    ["Book", "BookID", "None", "None"],
    ["Author", "AuthorID", "None", "None"],
    ["BookAuthor", "(BookID, AuthorID)", "BookID, AuthorID", "Book, Author"],
    ["Publisher", "PublisherID", "None", "None"],
    ["Category", "CategoryID", "None", "None"],
    ["BookCategory", "(BookID, CategoryID)", "BookID, CategoryID", "Book, Category"],
    ["Edition", "EditionID", "BookID, PublisherID", "Book, Publisher"],
    ["Copy", "CopyID", "EditionID", "Edition"],
    ["Member", "MemberID", "None", "None"],
    ["Issue", "IssueID", "CopyID, MemberID", "Copy, Member"],
    ["Reservation", "ReservationID", "BookID, MemberID", "Book, Member"],
    ["Fine", "FineID", "IssueID, MemberID", "Issue, Member"],
    ["DigitalResource", "ResourceID", "BookID", "Book"],
    ["DigitalAccessLog", "LogID", "ResourceID, MemberID", "DigitalResource, Member"],
]
add_styled_table(doc, ["Table", "Primary Key", "Foreign Keys", "References"], pk_fk_data)

# Integrity Constraints
doc.add_heading('Integrity Constraints', level=2)

doc.add_heading('UNIQUE Constraints', level=3)
unique_items = ["Book.ISBN", "Copy.AccessionNumber", "Member.Email", "Publisher.Name", "Category.Name"]
for item in unique_items:
    add_bullet(doc, item)

doc.add_heading('CHECK Constraints', level=3)
check_items = [
    "Fine.Amount >= 0",
    "Book.TotalPages > 0",
    "Edition.EditionNumber > 0",
    "Member.MaxBooksAllowed > 0",
    "Reservation.QueuePosition >= 1",
    "Issue.DueDate >= Issue.IssueDate",
    "Issue.ReturnDate >= Issue.IssueDate (when not NULL)",
]
for item in check_items:
    add_bullet(doc, item)

doc.add_heading('DEFAULT Constraints', level=3)
default_items = [
    "Copy.Status = 'Available'",
    "Issue.Status = 'Active'",
    "Reservation.Status = 'Pending'",
    "Fine.Status = 'Pending'",
    "Member.IsActive = TRUE",
]
for item in default_items:
    add_bullet(doc, item)

# ── Footer separator ──
doc.add_paragraph()
sep = doc.add_paragraph()
sep.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = sep.add_run("━" * 40)
run.font.color.rgb = RGBColor(0x0D, 0x47, 0xA1)

end = doc.add_paragraph()
end.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = end.add_run("End of Review 1 Report")
run.italic = True
run.font.color.rgb = RGBColor(0x61, 0x61, 0x61)

# ── Save ──
output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Review1_Report.docx")
doc.save(output_path)
print(f"SUCCESS: Word document saved successfully: {output_path}")
