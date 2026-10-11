# DBMS PBL Review 1 Document

## Project Title
**DESIGN AND IMPLEMENTATION OF A DATABASE MANAGEMENT SYSTEM FOR LIBRARY CIRCULATION AND DIGITAL RESOURCE MANAGEMENT SYSTEM**

## 1. Problem Identification
Traditional and manual library management systems often struggle with inefficiencies that hinder both staff productivity and patron experience. The primary problems identified in the current manual or disjointed systems include:
- **Unreliable Tracking:** Manual ledgers and outdated systems lead to discrepancies in tracking book locations, availability, and member histories, increasing the risk of lost or misplaced items.
- **Lack of Digital Resource Management:** Modern libraries possess significant digital assets (e-books, journals, audiobooks), but older systems completely lack the infrastructure to track, log, or manage access to these digital resources.
- **Manual Fine Calculation:** Calculating overdue fines manually is prone to human error, inconsistencies, and disputes. It also creates unnecessary administrative overhead for librarians.
- **Inefficient Reservation Queuing:** Without an automated system, handling reservations for popular books becomes chaotic, leading to unfair distribution and frustrated patrons.
- **Data Redundancy and Inconsistency:** Information about members, books, and transactions is often duplicated across different registers, leading to data anomalies and making it difficult to generate accurate reports.

## 2. Scope
### In-Scope
The proposed database management system will comprehensively cover the following areas:
- **Physical Asset Management:** Cataloging and tracking printed books, journals, and physical media.
- **Digital Resource Management:** Managing metadata and access logs for digital assets such as e-books, e-journals, and audiobooks.
- **Member Management:** Registration, profiling, and tracking of various member types (Students, Faculty, External).
- **Circulation Management:** Complete handling of issue, return, and renewal processes for physical copies.
- **Reservation System:** Automated queuing and notification for reserved items.
- **Fine Management:** Automated calculation, tracking, and settlement of overdue fines.
- **Digital Access Logging:** Monitoring and recording user interactions with digital resources for usage analytics.

### Out of Scope
The following features are explicitly excluded from the current project scope:
- Inter-library loan systems and networking with external library databases.
- E-commerce or financial payment gateway integration for purchasing books or paying fines online.
- Advanced AI-driven recommendation engines (e.g., collaborative filtering).

## 3. Objectives
The core objectives of developing this database system are to:
1. **Maintain a Comprehensive Catalogue:** Centralize and organize information for all physical and digital library assets.
2. **Track Circulation Accurately:** Provide real-time status updates on issues, returns, and inventory levels.
3. **Automate Fine Management:** Implement a flawless, rule-based system for calculating and tracking overdue fines.
4. **Manage Reservations Efficiently:** Automate the reservation queue to ensure fair and organized distribution of requested materials.
5. **Log Digital Resource Access:** Accurately record interactions with digital media to track usage and engagement.
6. **Generate Insightful Reports:** Provide dynamic reporting capabilities on inventory, member history, popular items, and financial collections.
7. **Enforce Data Integrity:** Utilize strict relational constraints (Primary Keys, Foreign Keys, Checks) to prevent data corruption.
8. **Implement Role-Based Access Control:** Secure the system by restricting operations based on predefined user roles and permissions.
9. **Improve Searchability:** Enable fast, multi-parameter searches across the entire library catalogue.
10. **Streamline Administrative Tasks:** Reduce manual workloads for librarians, allowing them to focus on member services.

## 4. Users and User Roles

| User Role | Description & Permissions |
| :--- | :--- |
| **Admin / Chief Librarian** | Has full CRUD (Create, Read, Update, Delete) access to the entire database. Can manage the catalogue, administer member accounts, process issues/returns, manually adjust fines, override system defaults, and generate all administrative reports. |
| **Assistant Librarian** | Has operational privileges. Can process day-to-day issues and returns, search the catalogue, manage member queries, and administer the reservation queues. Cannot modify system configurations or delete major records. |
| **Member (Student / Faculty / External)** | Has read-only access to the public catalogue. Can search for items, view real-time availability, place and cancel reservations, view their own borrowing history, check outstanding fines, and access digital resources. |
| **System / Automated Agent** | Background database processes (Triggers, Events, Jobs) responsible for automated tasks such as daily fine calculation, auto-expiring unfulfilled reservations, and managing the state of the reservation FIFO queue. |

## 5. Functional Requirements

### Catalogue Management
- **FR-001:** The system shall allow authorized staff to add, edit, or remove book records, authors, publishers, and categories.
- **FR-002:** The system shall support the management of multiple editions and physical copies for a single title.
- **FR-003:** The system must enforce unique ISBNs for book titles and unique Accession Numbers for physical copies.

### Member Management
- **FR-004:** The system shall allow the registration of new members and the updating of existing member profiles.
- **FR-005:** The system shall categorize members into types (e.g., Student, Faculty, External) to enforce type-specific borrowing rules.
- **FR-006:** The system shall track and enforce membership validity periods.

### Circulation (Issue/Return)
- **FR-007:** The system shall process the issuing of physical copies to registered, valid members.
- **FR-008:** The system shall enforce that a physical copy can only have one active issue transaction at any given time.
- **FR-009:** The system shall record return dates accurately and automatically calculate the number of overdue days.

### Reservation Management
- **FR-010:** The system shall allow members to place reservations on titles where all physical copies are currently issued.
- **FR-011:** The system shall maintain reservation requests in a strict First-In-First-Out (FIFO) queue.
- **FR-012:** The system shall automatically expire reservations if the item is not claimed within a defined timeframe.

### Fine Management
- **FR-013:** The system shall automatically calculate fines based on the number of overdue days and predefined fine rates.
- **FR-014:** The system shall track partial and full fine payments made by members.
- **FR-015:** The system shall ensure fine amounts are never recorded as negative values.

### Digital Resource Management
- **FR-016:** The system shall maintain records for non-physical resources like e-books, e-journals, and audiobooks.
- **FR-017:** The system shall securely log every member access (download/view) to a digital resource.

### Search & Reports
- **FR-018:** The system shall provide search functionality across the catalogue by Title, Author, ISBN, and Category.
- **FR-019:** The system shall generate comprehensive reports, including lists of available titles, overdue copies, member borrowing histories, highly demanded books, and total fine collections.

## 6. Non-Functional Requirements
- **Data Integrity and Consistency:** The database schema must strictly adhere to normalization principles (up to 3NF/BCNF) and enforce constraints to prevent orphaned records and anomalous states.
- **Performance:** Complex queries, especially catalogue searches and availability checks, must execute efficiently, utilizing proper indexing on frequently searched columns (e.g., ISBN, Title, Author).
- **Security:** The database must enforce strict Role-Based Access Control (RBAC), ensuring members cannot modify data and staff only have necessary permissions.
- **Scalability:** The architecture must be capable of handling thousands of active members, a catalogue of millions of items, and concurrent transaction processing without performance degradation.
- **Backup and Recovery:** The system must support scheduled automated backups and provide mechanisms for swift recovery in the event of hardware failure or data corruption.

## 7. Business Rules
The database design and application logic will be governed by the following core business rules:
- **BR-01:** The ISBN must be unique across all book records.
- **BR-02:** The Accession number must be completely unique across all physical copies in the library.
- **BR-03:** A physical copy can have at most one active issue transaction at a time.
- **BR-04:** The `Issue_Date` must always be chronologically prior to or exactly equal to the `Due_Date`.
- **BR-05:** If a book is returned, the `Return_Date` must be chronologically on or after the `Issue_Date`.
- **BR-06:** Reservations for a title must be fulfilled strictly according to the FIFO (First-In-First-Out) queue order.
- **BR-07:** Fine amounts (both calculated and outstanding) must always be non-negative values (≥ 0).
- **BR-08:** A member is restricted to a maximum of *N* concurrently active issues, where *N* is configurable based on their specific membership type (e.g., Faculty may have a higher limit than Students).
- **BR-09:** Digital access logs must persistently record the specific Member, the specific Digital Resource, and the exact Timestamp of access.
- **BR-10:** Every physical copy must be directly linked to a valid, existing book edition record in the catalogue.

---
*End of Review 1 Document*
