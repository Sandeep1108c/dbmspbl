"""
Library Circulation and Digital Resource Management System
DBMS PBL Interactive Model Application
Enhanced Modern UI with Streamlit, Plotly, and Dual-Engine Persistence
STRICT REQUIREMENT: ZERO em dashes and ZERO en dashes in this file.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
import database
import time

st.set_page_config(
    page_title="Library DBMS - Circulation & Digital Asset Manager",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-End Modern CSS Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Top Hero Banner */
    .hero-container {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 50%, #1E1B4B 100%);
        border-radius: 16px;
        padding: 24px 30px;
        color: #FFFFFF;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.1);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .hero-title {
        font-size: 1.85rem;
        font-weight: 800;
        letter-spacing: -0.025em;
        margin-bottom: 4px;
        color: #F8FAFC;
    }
    .hero-subtitle {
        font-size: 0.95rem;
        color: #94A3B8;
        font-weight: 400;
    }
    .hero-badges {
        display: flex;
        gap: 8px;
        margin-top: 10px;
    }
    .badge-pill {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .badge-blue { background: rgba(59, 130, 246, 0.2); color: #93C5FD; border: 1px solid rgba(59, 130, 246, 0.4); }
    .badge-emerald { background: rgba(16, 185, 129, 0.2); color: #6EE7B7; border: 1px solid rgba(16, 185, 129, 0.4); }
    .badge-purple { background: rgba(168, 85, 247, 0.2); color: #D8B4FE; border: 1px solid rgba(168, 85, 247, 0.4); }

    /* Modern Card Container */
    .metric-card {
        background: #FFFFFF;
        border-radius: 14px;
        padding: 20px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.06);
    }
    .metric-label {
        font-size: 0.82rem;
        font-weight: 600;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 6px;
    }
    .metric-value {
        font-size: 1.9rem;
        font-weight: 800;
        color: #0F172A;
        line-height: 1.1;
    }
    .metric-subtext {
        font-size: 0.8rem;
        color: #94A3B8;
        margin-top: 6px;
    }

    /* Book Cards */
    .book-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 14px;
        transition: all 0.2s ease;
    }
    .book-card:hover {
        border-color: #3B82F6;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.08);
    }
    .book-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 4px;
    }
    .book-meta {
        font-size: 0.85rem;
        color: #64748B;
        margin-bottom: 10px;
    }
    
    /* Status Pills */
    .status-tag {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 600;
    }
    .status-available { background: #DCFCE7; color: #166534; }
    .status-issued { background: #FEE2E2; color: #991B1B; }
    .status-reserved { background: #FEF3C7; color: #92400E; }
    .status-active { background: #DBEAFE; color: #1E40AF; }

    /* Button Style Enhancements */
    div.stButton > button:first-child {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s ease;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Database Manager
db = database.get_db()

# Sidebar: System Branding, Status & Navigation
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 10px 0 16px 0;">
        <span style="font-size: 2.8rem;">📚</span>
        <h2 style="margin: 6px 0 0 0; font-size: 1.35rem; font-weight: 800; color: #1E293B;">LIBRARY DBMS</h2>
        <p style="margin: 0; font-size: 0.8rem; color: #64748B; font-weight: 500;">Circulation & Digital Asset Manager</p>
    </div>
    """, unsafe_allow_html=True)

    # Engine Badge Container
    engine_name = "MySQL 8.4 Server" if db.engine_type == "mysql" else "SQLite 3 Database"
    engine_icon = "🟢" if db.engine_type == "mysql" else "🔵"
    st.info(f"**Engine:** {engine_icon} {engine_name}")

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🔄 Sync", help="Re-check database connection", use_container_width=True):
            db = database.DatabaseManager(force_sqlite=(db.engine_type != "mysql"))
            st.rerun()
    with col_btn2:
        btn_label = "MySQL" if db.engine_type == "sqlite" else "SQLite"
        if st.button(btn_label, help=f"Toggle to {btn_label}", use_container_width=True):
            db.force_sqlite = not db.force_sqlite
            db._check_mysql()
            st.rerun()

    st.markdown("<hr style='margin: 14px 0; border: none; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)

    nav_option = st.radio(
        "MAIN NAVIGATION",
        [
            "📊 Dashboard & Analytics",
            "📚 Catalogue & Inventory",
            "👥 Member Management",
            "🔄 Circulation Desk (Issue/Return)",
            "⏳ Reservation Queue",
            "💰 Fines & Payments",
            "💻 Digital Library & Logs",
            "⚡ SQL Query Console"
        ],
        label_visibility="visible"
    )

    st.markdown("<hr style='margin: 14px 0; border: none; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)
    st.caption("Course: Database Management Systems (DBMS PBL)")
    st.caption("Release: Version 2.0 (Working Model)")


# Hero Banner Header on all pages
def render_hero(title, subtitle):
    engine_badge = '<span class="badge-pill badge-emerald">MySQL Active</span>' if db.engine_type == "mysql" else '<span class="badge-pill badge-blue">SQLite Standalone</span>'
    today_str = date.today().strftime("%B %d, %Y")
    st.markdown(f"""
    <div class="hero-container">
        <div>
            <div class="hero-title">{title}</div>
            <div class="hero-subtitle">{subtitle}</div>
            <div class="hero-badges">
                {engine_badge}
                <span class="badge-pill badge-purple">DBMS PBL 2025-2026</span>
                <span class="badge-pill badge-blue">{today_str}</span>
            </div>
        </div>
        <div style="font-size: 2.8rem; opacity: 0.85;">🏛️</div>
    </div>
    """, unsafe_allow_html=True)


# ==============================================================================
# 1. DASHBOARD & ANALYTICS
# ==============================================================================
if nav_option == "📊 Dashboard & Analytics":
    render_hero(
        "System Dashboard and Operational Analytics",
        "Overview of library holdings, active circulation, member enrollment, and revenue metrics."
    )

    # Summary Metrics
    total_books = db.execute_query("SELECT COUNT(*) AS c FROM Book")[0]['c']
    total_copies = db.execute_query("SELECT COUNT(*) AS c FROM Copy")[0]['c']
    issued_copies = db.execute_query("SELECT COUNT(*) AS c FROM Copy WHERE Status = 'Issued'")[0]['c']
    available_copies = db.execute_query("SELECT COUNT(*) AS c FROM Copy WHERE Status = 'Available'")[0]['c']
    total_members = db.execute_query("SELECT COUNT(*) AS c FROM Member WHERE IsActive = 1")[0]['c']
    pending_fines = db.execute_query("SELECT COALESCE(SUM(Amount), 0) AS s FROM Fine WHERE Status = 'Pending'")[0]['s']
    collected_fines = db.execute_query("SELECT COALESCE(SUM(Amount), 0) AS s FROM Fine WHERE Status = 'Paid'")[0]['s']
    overdue_issues = db.execute_query("SELECT COUNT(*) AS c FROM Issue WHERE Status = 'Overdue'")[0]['c']

    # Modern Metric Cards Grid
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid #4F46E5;">
            <div class="metric-label">Book Titles</div>
            <div class="metric-value">{total_books}</div>
            <div class="metric-subtext">📘 {total_copies} physical copies in stacks</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid #2563EB;">
            <div class="metric-label">Active Loans</div>
            <div class="metric-value">{issued_copies}</div>
            <div class="metric-subtext">⚠️ {overdue_issues} currently past due date</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid #059669;">
            <div class="metric-label">Registered Patrons</div>
            <div class="metric-value">{total_members}</div>
            <div class="metric-subtext">🎓 Students, faculty, and public</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid #E11D48;">
            <div class="metric-label">Pending Fines</div>
            <div class="metric-value">Rs. {float(pending_fines):.2f}</div>
            <div class="metric-subtext">💳 Rs. {float(collected_fines):.2f} settled revenue</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # Interactive Plots
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.markdown("#### 📦 Physical Inventory Distribution")
        status_df = db.query_df("SELECT Status, COUNT(*) AS Count FROM Copy GROUP BY Status")
        if not status_df.empty:
            fig1 = px.pie(
                status_df,
                names="Status",
                values="Count",
                hole=0.52,
                color="Status",
                color_discrete_map={
                    "Available": "#10B981",
                    "Issued": "#EF4444",
                    "Reserved": "#F59E0B",
                    "Lost": "#6B7280"
                }
            )
            fig1.update_layout(
                margin=dict(t=15, b=15, l=15, r=15),
                height=290,
                legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5)
            )
            st.plotly_chart(fig1, width="stretch")

    with col_chart2:
        st.markdown("#### 👥 Member Distribution by Role")
        mem_df = db.query_df("SELECT MembershipType, COUNT(*) AS Count FROM Member GROUP BY MembershipType")
        if not mem_df.empty:
            fig2 = px.bar(
                mem_df,
                x="MembershipType",
                y="Count",
                color="MembershipType",
                color_discrete_sequence=["#3B82F6", "#8B5CF6", "#10B981", "#F59E0B"],
                text_auto=True,
                labels={"MembershipType": "Category", "Count": "Count"}
            )
            fig2.update_layout(
                margin=dict(t=15, b=15, l=15, r=15),
                height=290,
                showlegend=False,
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig2, width="stretch")

    col_chart3, col_chart4 = st.columns(2)

    with col_chart3:
        st.markdown("#### 🏷️ Holdings by Academic Subject")
        cat_df = db.query_df("""
            SELECT c.Name AS Category, COUNT(bc.BookID) AS Titles
            FROM Category c
            LEFT JOIN BookCategory bc ON c.CategoryID = bc.CategoryID
            GROUP BY c.CategoryID, c.Name
            ORDER BY Titles DESC
        """)
        fig3 = px.bar(
            cat_df,
            x="Titles",
            y="Category",
            orientation="h",
            color="Titles",
            color_continuous_scale="Purples"
        )
        fig3.update_layout(
            margin=dict(t=15, b=15, l=15, r=15),
            height=280,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            coloraxis_showscale=False
        )
        st.plotly_chart(fig3, width="stretch")

    with col_chart4:
        st.markdown("#### 🔄 Recent Circulation Ledger")
        recent_tx = db.query_df("""
            SELECT i.IssueID AS ID, m.FirstName || ' ' || m.LastName AS Patron,
                   b.Title, i.DueDate, i.Status
            FROM Issue i
            JOIN Member m ON i.MemberID = m.MemberID
            JOIN Copy c ON i.CopyID = c.CopyID
            JOIN Edition e ON c.EditionID = e.EditionID
            JOIN Book b ON e.BookID = b.BookID
            ORDER BY i.IssueID DESC LIMIT 5
        """)
        st.dataframe(recent_tx, width="stretch", hide_index=True)


# ==============================================================================
# 2. CATALOGUE & INVENTORY
# ==============================================================================
elif nav_option == "📚 Catalogue & Inventory":
    render_hero(
        "Library Catalogue and Stacks Inventory",
        "Search titles, view shelf coordinates, add new volumes, and accession physical copies."
    )

    tab_cat1, tab_cat2, tab_cat3 = st.tabs(["🔍 Browse & Search", "➕ Add Title to Catalogue", "🏷️ Accession Physical Copy"])

    with tab_cat1:
        c_filter1, c_filter2, c_view = st.columns([3, 2, 1.2])
        with c_filter1:
            search_query = st.text_input("Quick Search:", "", placeholder="Filter by Title, Author, ISBN...")
        with c_filter2:
            all_cat_names = [c['Name'] for c in db.execute_query("SELECT Name FROM Category")]
            cat_filter = st.selectbox("Category Filter:", ["All Categories"] + all_cat_names)
        with c_view:
            view_mode = st.radio("Display Mode:", ["Card Grid", "Table View"], horizontal=True)

        sql_search = """
            SELECT b.BookID, b.ISBN, b.Title, b.Language, b.TotalPages, b.PublicationYear,
                   GROUP_CONCAT(DISTINCT a.FirstName || ' ' || a.LastName) AS Authors,
                   GROUP_CONCAT(DISTINCT c.Name) AS Categories,
                   COUNT(DISTINCT cp.CopyID) AS TotalCopies,
                   SUM(CASE WHEN cp.Status = 'Available' THEN 1 ELSE 0 END) AS AvailableCopies
            FROM Book b
            LEFT JOIN BookAuthor ba ON b.BookID = ba.BookID
            LEFT JOIN Author a ON ba.AuthorID = a.AuthorID
            LEFT JOIN BookCategory bc ON b.BookID = bc.BookID
            LEFT JOIN Category c ON bc.CategoryID = c.CategoryID
            LEFT JOIN Edition e ON b.BookID = e.BookID
            LEFT JOIN Copy cp ON e.EditionID = cp.EditionID
            WHERE 1=1
        """
        params = []
        if search_query:
            sql_search += """ AND (b.Title LIKE %s OR b.ISBN LIKE %s OR a.FirstName LIKE %s OR a.LastName LIKE %s)""" if db.engine_type == 'mysql' else """ AND (b.Title LIKE ? OR b.ISBN LIKE ? OR a.FirstName LIKE ? OR a.LastName LIKE ?)"""
            sq = f"%{search_query}%"
            params.extend([sq, sq, sq, sq])

        sql_search += " GROUP BY b.BookID, b.ISBN, b.Title, b.Language, b.TotalPages, b.PublicationYear"

        catalog_df = db.query_df(sql_search, params=params)
        if cat_filter != "All Categories":
            catalog_df = catalog_df[catalog_df['Categories'].str.contains(cat_filter, na=False)]

        st.markdown(f"**Found {len(catalog_df)} titles in catalog:**")

        if view_mode == "Card Grid":
            # Display responsive cards
            cols = st.columns(2)
            for idx, row in catalog_df.iterrows():
                col_target = cols[idx % 2]
                with col_target:
                    avail = int(row['AvailableCopies']) if pd.notnull(row['AvailableCopies']) else 0
                    total = int(row['TotalCopies']) if pd.notnull(row['TotalCopies']) else 0
                    avail_badge = f'<span class="status-tag status-available">{avail} of {total} Available</span>' if avail > 0 else f'<span class="status-tag status-issued">0 of {total} Available</span>'
                    st.markdown(f"""
                    <div class="book-card">
                        <div class="book-title">📘 {row['Title']}</div>
                        <div class="book-meta">
                            <strong>Authors:</strong> {row['Authors'] or 'Unknown'}<br>
                            <strong>ISBN:</strong> <code>{row['ISBN']}</code> | <strong>Year:</strong> {row['PublicationYear']} | <strong>Pages:</strong> {row['TotalPages']}
                        </div>
                        <div style="margin-top: 8px;">
                            {avail_badge}
                            <span class="status-tag status-active">{row['Categories'] or 'Uncategorized'}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.dataframe(catalog_df, width="stretch", hide_index=True)

        st.markdown("<hr style='margin: 20px 0; border: none; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)
        st.markdown("#### 🔍 Inspect Shelf Coordinates for Title")
        book_options = {row['Title']: row['BookID'] for idx, row in catalog_df.iterrows()}
        if book_options:
            selected_book_title = st.selectbox("Select Book to Locate Physical Copies:", list(book_options.keys()))
            selected_b_id = book_options[selected_book_title]

            copies_df = db.query_df("""
                SELECT cp.CopyID, cp.AccessionNumber AS Barcode, e.EditionNumber AS Edition,
                       p.Name AS Publisher, e.Format, cp.ShelfLocation, cp.Status, cp.DateAcquired
                FROM Copy cp
                JOIN Edition e ON cp.EditionID = e.EditionID
                JOIN Publisher p ON e.PublisherID = p.PublisherID
                WHERE e.BookID = ? OR e.BookID = %s
            """.replace("?", "%s" if db.engine_type == 'mysql' else "?"), (selected_b_id,))

            st.dataframe(copies_df, width="stretch", hide_index=True)

    with tab_cat2:
        st.markdown("#### Register New Book Title into Collection")
        with st.form("add_book_form", clear_on_submit=True):
            f_col1, f_col2 = st.columns(2)
            with f_col1:
                b_title = st.text_input("Title *", placeholder="e.g. Modern Operating Systems")
                b_isbn = st.text_input("ISBN-13 (Unique) *", placeholder="e.g. 978-0133591620")
                b_year = st.number_input("Publication Year *", min_value=1950, max_value=2030, value=2024)
            with f_col2:
                b_pages = st.number_input("Total Pages", min_value=1, max_value=10000, value=500)
                b_lang = st.selectbox("Language", ["English", "Hindi", "French", "German", "Spanish"])
                
            all_authors = db.execute_query("SELECT AuthorID, FirstName || ' ' || LastName AS Name FROM Author")
            author_choices = {a['Name']: a['AuthorID'] for a in all_authors}
            sel_authors = st.multiselect("Select Author(s) *", list(author_choices.keys()))

            all_publishers = db.execute_query("SELECT PublisherID, Name FROM Publisher")
            pub_choices = {p['Name']: p['PublisherID'] for p in all_publishers}
            sel_pub = st.selectbox("Select Publisher *", list(pub_choices.keys()))

            all_cats = db.execute_query("SELECT CategoryID, Name FROM Category")
            cat_choices = {c['Name']: c['CategoryID'] for c in all_cats}
            sel_cats = st.multiselect("Select Categories *", list(cat_choices.keys()))

            save_submitted = st.form_submit_button("💾 Save Book to Database", type="primary")
            if save_submitted:
                if not b_title or not b_isbn or not sel_authors or not sel_cats:
                    st.error("Please fill in all required fields.")
                else:
                    try:
                        q_ins = "INSERT INTO Book (ISBN, Title, Language, TotalPages, PublicationYear) VALUES (%s, %s, %s, %s, %s)" if db.engine_type == 'mysql' else "INSERT INTO Book (ISBN, Title, Language, TotalPages, PublicationYear) VALUES (?, ?, ?, ?, ?)"
                        new_book_id = db.execute_query(q_ins, (b_isbn, b_title, b_lang, b_pages, b_year))
                        
                        for a_name in sel_authors:
                            q_ba = "INSERT INTO BookAuthor (BookID, AuthorID) VALUES (%s, %s)" if db.engine_type == 'mysql' else "INSERT INTO BookAuthor (BookID, AuthorID) VALUES (?, ?)"
                            db.execute_query(q_ba, (new_book_id, author_choices[a_name]))

                        for c_name in sel_cats:
                            q_bc = "INSERT INTO BookCategory (BookID, CategoryID) VALUES (%s, %s)" if db.engine_type == 'mysql' else "INSERT INTO BookCategory (BookID, CategoryID) VALUES (?, ?)"
                            db.execute_query(q_bc, (new_book_id, cat_choices[c_name]))

                        q_ed = "INSERT INTO Edition (BookID, EditionNumber, PublisherID, PublicationDate, Format) VALUES (%s, %s, %s, %s, %s)" if db.engine_type == 'mysql' else "INSERT INTO Edition (BookID, EditionNumber, PublisherID, PublicationDate, Format) VALUES (?, ?, ?, ?, ?)"
                        db.execute_query(q_ed, (new_book_id, 1, pub_choices[sel_pub], str(date.today()), "Paperback"))

                        st.success(f"Title '{b_title}' added successfully with Book ID #{new_book_id}!")
                    except Exception as e:
                        st.error(f"Error saving book: {str(e)}")

    with tab_cat3:
        st.markdown("#### Accession Physical Copy to Stacks")
        with st.form("add_copy_form"):
            all_editions = db.query_df("""
                SELECT e.EditionID, b.Title, e.EditionNumber, p.Name AS Publisher
                FROM Edition e
                JOIN Book b ON e.BookID = b.BookID
                JOIN Publisher p ON e.PublisherID = p.PublisherID
            """)
            edition_map = {f"{r['Title']} (Ed {r['EditionNumber']} - {r['Publisher']})": r['EditionID'] for _, r in all_editions.iterrows()}
            
            sel_edition_str = st.selectbox("Select Target Edition:", list(edition_map.keys()))
            cp_acc = st.text_input("Accession Barcode Number *", value=f"ACC-2026-{datetime.now().strftime('%M%S')}")
            cp_shelf = st.text_input("Stack Shelf Location *", value="Shelf B2-01")
            
            submit_copy = st.form_submit_button("🏷️ Record Copy into Inventory", type="primary")
            if submit_copy:
                try:
                    q_cp = "INSERT INTO Copy (AccessionNumber, EditionID, Status, ShelfLocation, DateAcquired) VALUES (%s, %s, %s, %s, %s)" if db.engine_type == 'mysql' else "INSERT INTO Copy (AccessionNumber, EditionID, Status, ShelfLocation, DateAcquired) VALUES (?, ?, ?, ?, ?)"
                    db.execute_query(q_cp, (cp_acc, edition_map[sel_edition_str], "Available", cp_shelf, str(date.today())))
                    st.success(f"Barcode {cp_acc} cataloged into stacks at {cp_shelf}!")
                except Exception as e:
                    st.error(f"Error accessioning copy: {str(e)}")


# ==============================================================================
# 3. MEMBER MANAGEMENT
# ==============================================================================
elif nav_option == "👥 Member Management":
    render_hero(
        "Patron Directory and Account Administration",
        "Manage patron registrations, verify borrowing quotas, and inspect fine balances."
    )

    tab_m1, tab_m2 = st.tabs(["📋 Registered Patron Directory", "➕ New Member Registration"])

    with tab_m1:
        members_df = db.query_df("""
            SELECT m.MemberID, m.FirstName || ' ' || m.LastName AS Name,
                   m.Email, m.Phone, m.MembershipType AS Category, m.MaxBooksAllowed AS Quota,
                   COUNT(CASE WHEN i.Status IN ('Active', 'Overdue') THEN 1 END) AS ActiveLoans,
                   COALESCE(SUM(CASE WHEN f.Status = 'Pending' THEN f.Amount ELSE 0 END), 0) AS PendingFine,
                   m.MembershipStartDate AS JoinedDate,
                   CASE WHEN m.IsActive = 1 THEN 'Active' ELSE 'Inactive' END AS Status
            FROM Member m
            LEFT JOIN Issue i ON m.MemberID = i.MemberID
            LEFT JOIN Fine f ON m.MemberID = f.MemberID
            GROUP BY m.MemberID
            ORDER BY m.MemberID ASC
        """)
        st.dataframe(members_df, width="stretch", hide_index=True)

    with tab_m2:
        st.markdown("#### Register New Library Member")
        with st.form("register_member_form", clear_on_submit=True):
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                m_fn = st.text_input("First Name *")
                m_ln = st.text_input("Last Name *")
                m_em = st.text_input("Email *")
                m_ph = st.text_input("Phone Number *")
            with col_m2:
                m_type = st.selectbox("Patron Category *", ["Student", "Faculty", "Staff", "Public"])
                default_quota = 3 if m_type == "Student" else (10 if m_type == "Faculty" else 2)
                m_limit = st.number_input("Max Active Loans Allowed", min_value=1, max_value=20, value=default_quota)
                m_addr = st.text_area("Address", height=100)
                valid_months = 24 if m_type in ["Student", "Faculty"] else 12

            submit_mem = st.form_submit_button("👤 Complete Registration", type="primary")
            if submit_mem:
                if not m_fn or not m_ln or not m_em or not m_ph:
                    st.error("Please fill in required fields.")
                else:
                    try:
                        s_dt = date.today()
                        e_dt = s_dt + timedelta(days=valid_months * 30)
                        q_m = "INSERT INTO Member (FirstName, LastName, Email, Phone, Address, MembershipType, MembershipStartDate, MembershipEndDate, MaxBooksAllowed, IsActive) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" if db.engine_type == 'mysql' else "INSERT INTO Member (FirstName, LastName, Email, Phone, Address, MembershipType, MembershipStartDate, MembershipEndDate, MaxBooksAllowed, IsActive) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                        new_m_id = db.execute_query(q_m, (m_fn, m_ln, m_em, m_ph, m_addr, m_type, str(s_dt), str(e_dt), m_limit, 1))
                        st.success(f"Patron {m_fn} {m_ln} successfully registered as Member ID #{new_m_id}!")
                    except Exception as e:
                        st.error(f"Error registering patron: {str(e)}")


# ==============================================================================
# 4. CIRCULATION DESK (ISSUE & RETURN)
# ==============================================================================
elif nav_option == "🔄 Circulation Desk (Issue/Return)":
    render_hero(
        "Circulation Front Desk Operations",
        "Process fast book loans, track active borrowings, and compute overdue penalties upon return."
    )

    tab_circ1, tab_circ2, tab_circ3 = st.tabs(["📤 Issue Book Loan", "📥 Check-in (Return)", "📑 Open Transactions"])

    with tab_circ1:
        st.markdown("#### Issue a Book to Registered Patron")
        with st.form("issue_desk_form"):
            patrons = db.query_df("SELECT MemberID, FirstName || ' ' || LastName || ' (' || MembershipType || ')' AS Name, MaxBooksAllowed FROM Member WHERE IsActive = 1")
            patron_dict = {row['Name']: (row['MemberID'], row['MaxBooksAllowed']) for _, row in patrons.iterrows()}
            sel_patron_str = st.selectbox("Select Patron:", list(patron_dict.keys()))

            available_copies = db.query_df("""
                SELECT cp.CopyID, cp.AccessionNumber || ' : ' || b.Title || ' (' || cp.ShelfLocation || ')' AS CopyLabel
                FROM Copy cp
                JOIN Edition e ON cp.EditionID = e.EditionID
                JOIN Book b ON e.BookID = b.BookID
                WHERE cp.Status = 'Available'
            """)
            if available_copies.empty:
                st.warning("All physical copies are currently checked out or reserved.")
                copy_dict = {}
            else:
                copy_dict = {row['CopyLabel']: row['CopyID'] for _, row in available_copies.iterrows()}
            sel_copy_str = st.selectbox("Select Available Copy:", list(copy_dict.keys()) if copy_dict else ["None"])

            loan_days = st.slider("Loan Duration (Days):", min_value=7, max_value=30, value=14)

            submit_issue = st.form_submit_button("🚀 Confirm Book Issue", type="primary")
            if submit_issue:
                if not copy_dict:
                    st.error("No copy available to issue.")
                else:
                    m_id, m_limit = patron_dict[sel_patron_str]
                    c_id = copy_dict[sel_copy_str]

                    curr_loans = db.execute_query(f"SELECT COUNT(*) AS c FROM Issue WHERE MemberID = {m_id} AND Status IN ('Active', 'Overdue')")[0]['c']
                    if curr_loans >= m_limit:
                        st.error(f"Cannot issue: Patron has reached max quota of {m_limit} active loans.")
                    else:
                        iss_date = date.today()
                        due_date = iss_date + timedelta(days=loan_days)
                        
                        q_iss = "INSERT INTO Issue (CopyID, MemberID, IssueDate, DueDate, Status) VALUES (%s, %s, %s, %s, 'Active')" if db.engine_type == 'mysql' else "INSERT INTO Issue (CopyID, MemberID, IssueDate, DueDate, Status) VALUES (?, ?, ?, ?, 'Active')"
                        db.execute_query(q_iss, (c_id, m_id, str(iss_date), str(due_date)))

                        q_cp_up = "UPDATE Copy SET Status = 'Issued' WHERE CopyID = %s" if db.engine_type == 'mysql' else "UPDATE Copy SET Status = 'Issued' WHERE CopyID = ?"
                        db.execute_query(q_cp_up, (c_id,))

                        st.success(f"Book issued successfully! Due Date: {due_date.strftime('%d-%b-%Y')}")

    with tab_circ2:
        st.markdown("#### Return Book and Automated Overdue Penalty Check")
        active_issues = db.query_df("""
            SELECT i.IssueID, i.CopyID, i.MemberID,
                   '#' || i.IssueID || ' | ' || b.Title || ' (' || cp.AccessionNumber || ') - ' || m.FirstName || ' ' || m.LastName AS IssueLabel,
                   i.DueDate, i.Status
            FROM Issue i
            JOIN Copy cp ON i.CopyID = cp.CopyID
            JOIN Edition e ON cp.EditionID = e.EditionID
            JOIN Book b ON e.BookID = b.BookID
            JOIN Member m ON i.MemberID = m.MemberID
            WHERE i.Status IN ('Active', 'Overdue')
        """)

        if active_issues.empty:
            st.info("No loans currently awaiting return.")
        else:
            issue_map = {row['IssueLabel']: row for _, row in active_issues.iterrows()}
            selected_issue_label = st.selectbox("Select Active Issue:", list(issue_map.keys()))
            issue_row = issue_map[selected_issue_label]

            due_dt = datetime.strptime(str(issue_row['DueDate']), "%Y-%m-%d").date()
            ret_dt = date.today()
            overdue_days = max(0, (ret_dt - due_dt).days)
            fine_rate = 5.0
            total_fine = overdue_days * fine_rate

            col_due1, col_due2 = st.columns(2)
            with col_due1:
                st.info(f"📅 Due Date: **{due_dt.strftime('%d-%b-%Y')}** | Check-in Date: **{ret_dt.strftime('%d-%b-%Y')}**")
            with col_due2:
                if overdue_days > 0:
                    st.error(f"🚨 **{overdue_days} Days Overdue!** Calculated Fine: **Rs. {total_fine:.2f}** (at Rs 5.00/day)")
                else:
                    st.success("✅ **On-time Return!** Zero fine incurred.")

            if st.button("📥 Complete Check-in (Return Book)", type="primary", use_container_width=True):
                q_ret = "UPDATE Issue SET ReturnDate = %s, Status = 'Returned' WHERE IssueID = %s" if db.engine_type == 'mysql' else "UPDATE Issue SET ReturnDate = ?, Status = 'Returned' WHERE IssueID = ?"
                db.execute_query(q_ret, (str(ret_dt), issue_row['IssueID']))

                q_cp_ret = "UPDATE Copy SET Status = 'Available' WHERE CopyID = %s" if db.engine_type == 'mysql' else "UPDATE Copy SET Status = 'Available' WHERE CopyID = ?"
                db.execute_query(q_cp_ret, (issue_row['CopyID'],))

                if total_fine > 0:
                    q_fine = "INSERT INTO Fine (IssueID, MemberID, Amount, Reason, FineDate, Status) VALUES (%s, %s, %s, %s, %s, 'Pending')" if db.engine_type == 'mysql' else "INSERT INTO Fine (IssueID, MemberID, Amount, Reason, FineDate, Status) VALUES (?, ?, ?, ?, ?, 'Pending')"
                    db.execute_query(q_fine, (issue_row['IssueID'], issue_row['MemberID'], total_fine, f"Late Return: {overdue_days} days overdue at Rs 5/day", str(ret_dt)))
                    st.warning(f"Book returned. Fine record of Rs. {total_fine:.2f} recorded.")
                else:
                    st.success("Book returned on time with clean record!")
                st.rerun()

    with tab_circ3:
        st.markdown("#### All Currently Checked-out Items")
        all_loans = db.query_df("""
            SELECT i.IssueID, cp.AccessionNumber AS Barcode, b.Title,
                   m.FirstName || ' ' || m.LastName AS MemberName,
                   i.IssueDate, i.DueDate, i.Status
            FROM Issue i
            JOIN Copy cp ON i.CopyID = cp.CopyID
            JOIN Edition e ON cp.EditionID = e.EditionID
            JOIN Book b ON e.BookID = b.BookID
            JOIN Member m ON i.MemberID = m.MemberID
            WHERE i.Status IN ('Active', 'Overdue')
            ORDER BY i.DueDate ASC
        """)
        st.dataframe(all_loans, width="stretch", hide_index=True)


# ==============================================================================
# 5. RESERVATION QUEUE
# ==============================================================================
elif nav_option == "⏳ Reservation Queue":
    render_hero(
        "Reservation Waitlist (FIFO Queue)",
        "Automated First-In-First-Out queuing for titles with zero available physical copies."
    )

    col_q1, col_q2 = st.columns([1.6, 1])

    with col_q1:
        st.markdown("#### Active Reservation Waitlist")
        res_df = db.query_df("""
            SELECT r.ReservationID, b.Title,
                   m.FirstName || ' ' || m.LastName AS Member,
                   r.ReservationDate, r.QueuePosition AS Position, r.Status, r.ExpiryDate
            FROM Reservation r
            JOIN Book b ON r.BookID = b.BookID
            JOIN Member m ON r.MemberID = m.MemberID
            ORDER BY r.BookID, r.QueuePosition ASC
        """)
        st.dataframe(res_df, width="stretch", hide_index=True)

    with col_q2:
        st.markdown("#### Enqueue New Reservation")
        with st.form("reserve_form"):
            books = db.query_df("SELECT BookID, Title FROM Book")
            b_dict = {r['Title']: r['BookID'] for _, r in books.iterrows()}
            sel_b_title = st.selectbox("Select Title:", list(b_dict.keys()))

            patrons = db.query_df("SELECT MemberID, FirstName || ' ' || LastName AS Name FROM Member WHERE IsActive = 1")
            p_dict = {r['Name']: r['MemberID'] for _, r in patrons.iterrows()}
            sel_p_name = st.selectbox("Requesting Member:", list(p_dict.keys()))

            submit_res = st.form_submit_button("⏳ Add to Waitlist Queue", type="primary")
            if submit_res:
                b_id = b_dict[sel_b_title]
                m_id = p_dict[sel_p_name]

                curr_q = db.execute_query(f"SELECT COALESCE(MAX(QueuePosition), 0) AS max_q FROM Reservation WHERE BookID = {b_id} AND Status = 'Pending'")[0]['max_q']
                next_pos = curr_q + 1
                exp_dt = datetime.now() + timedelta(days=7)

                q_res = "INSERT INTO Reservation (BookID, MemberID, ReservationDate, QueuePosition, Status, ExpiryDate) VALUES (%s, %s, %s, %s, 'Pending', %s)" if db.engine_type == 'mysql' else "INSERT INTO Reservation (BookID, MemberID, ReservationDate, QueuePosition, Status, ExpiryDate) VALUES (?, ?, ?, ?, 'Pending', ?)"
                db.execute_query(q_res, (b_id, m_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), next_pos, exp_dt.strftime("%Y-%m-%d %H:%M:%S")))

                st.success(f"Waitlist token created! Assigned Position #{next_pos}.")
                st.rerun()


# ==============================================================================
# 6. FINES & PAYMENTS
# ==============================================================================
elif nav_option == "💰 Fines & Payments":
    render_hero(
        "Financial Penalties and Payment Settlement",
        "Track overdue liabilities, record receipt settlements, and process authorized waivers."
    )

    f_c1, f_c2, f_c3 = st.columns(3)
    p_sum = db.execute_query("SELECT COALESCE(SUM(Amount), 0) AS s FROM Fine WHERE Status = 'Pending'")[0]['s']
    pd_sum = db.execute_query("SELECT COALESCE(SUM(Amount), 0) AS s FROM Fine WHERE Status = 'Paid'")[0]['s']
    w_sum = db.execute_query("SELECT COALESCE(SUM(Amount), 0) AS s FROM Fine WHERE Status = 'Waived'")[0]['s']

    with f_c1:
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid #EF4444;">
            <div class="metric-label">Pending Dues</div>
            <div class="metric-value">Rs. {float(p_sum):.2f}</div>
            <div class="metric-subtext">Unsettled patron balances</div>
        </div>
        """, unsafe_allow_html=True)
    with f_c2:
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid #10B981;">
            <div class="metric-label">Settled Revenue</div>
            <div class="metric-value">Rs. {float(pd_sum):.2f}</div>
            <div class="metric-subtext">Cash and receipt deposits</div>
        </div>
        """, unsafe_allow_html=True)
    with f_c3:
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid #8B5CF6;">
            <div class="metric-label">Waived Penalties</div>
            <div class="metric-value">Rs. {float(w_sum):.2f}</div>
            <div class="metric-subtext">Authorized chief librarian waivers</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    fines_df = db.query_df("""
        SELECT f.FineID AS ID, m.FirstName || ' ' || m.LastName AS Patron,
               f.Amount, f.Reason, f.FineDate, f.PaidDate, f.Status
        FROM Fine f
        JOIN Member m ON f.MemberID = m.MemberID
        ORDER BY f.FineID DESC
    """)
    st.dataframe(fines_df, width="stretch", hide_index=True)

    st.markdown("#### Settle Outstanding Fine Voucher")
    pending_fines_df = fines_df[fines_df['Status'] == 'Pending']
    if pending_fines_df.empty:
        st.success("All accounts settled! No outstanding fines.")
    else:
        fine_choices = {f"Voucher #{r['ID']} | {r['Patron']} : Rs. {r['Amount']:.2f} ({r['Reason']})": r['ID'] for _, r in pending_fines_df.iterrows()}
        selected_fine_str = st.selectbox("Select Pending Voucher:", list(fine_choices.keys()))
        selected_fine_id = fine_choices[selected_fine_str]

        col_pay1, col_pay2 = st.columns(2)
        with col_pay1:
            if st.button("💳 Settle Payment (Mark Paid)", type="primary", use_container_width=True):
                q_p = "UPDATE Fine SET Status = 'Paid', PaidDate = %s WHERE FineID = %s" if db.engine_type == 'mysql' else "UPDATE Fine SET Status = 'Paid', PaidDate = ? WHERE FineID = ?"
                db.execute_query(q_p, (str(date.today()), selected_fine_id))
                st.success(f"Fine #{selected_fine_id} marked as PAID.")
                st.rerun()
        with col_pay2:
            if st.button("⚖️ Waive Penalty (Authorized Waiver)", use_container_width=True):
                q_w = "UPDATE Fine SET Status = 'Waived' WHERE FineID = %s" if db.engine_type == 'mysql' else "UPDATE Fine SET Status = 'Waived' WHERE FineID = ?"
                db.execute_query(q_w, (selected_fine_id,))
                st.info(f"Fine #{selected_fine_id} marked as WAIVED.")
                st.rerun()


# ==============================================================================
# 7. DIGITAL LIBRARY & LOGS
# ==============================================================================
elif nav_option == "💻 Digital Library & Logs":
    render_hero(
        "Digital Resource Repository and Audit Trail",
        "Catalog electronic textbooks, stream media, and monitor immutable security access logs."
    )

    tab_dig1, tab_dig2 = st.tabs(["📖 Electronic Asset Catalog", "🛡️ Real-Time Audit Logs"])

    with tab_dig1:
        resources = db.query_df("""
            SELECT dr.ResourceID, b.Title, dr.ResourceType, dr.FileFormat,
                   dr.FileSize, dr.URL, dr.UploadDate
            FROM DigitalResource dr
            JOIN Book b ON dr.BookID = b.BookID
        """)

        for _, res in resources.iterrows():
            with st.container():
                st.markdown(f"""
                <div class="book-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span style="font-size: 1.25rem; font-weight: 700; color: #1E293B;">📗 {res['Title']}</span><br>
                            <span style="font-size: 0.85rem; color: #64748B;">
                                Format: <strong>{res['FileFormat']}</strong> ({res['FileSize']}) | Type: <strong>{res['ResourceType']}</strong> | Uploaded: {res['UploadDate']}
                            </span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                col_btn_l, _ = st.columns([1.5, 4])
                with col_btn_l:
                    if st.button(f"📥 Download / Read Asset #{res['ResourceID']}", key=f"res_btn_{res['ResourceID']}"):
                        log_q = "INSERT INTO DigitalAccessLog (ResourceID, MemberID, AccessDate, AccessType, IPAddress) VALUES (%s, 1, %s, 'Download', '127.0.0.1')" if db.engine_type == 'mysql' else "INSERT INTO DigitalAccessLog (ResourceID, MemberID, AccessDate, AccessType, IPAddress) VALUES (?, 1, ?, 'Download', '127.0.0.1')"
                        db.execute_query(log_q, (res['ResourceID'], datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                        st.success(f"Access granted! Digital access audit event logged for asset #{res['ResourceID']}.")
                        time.sleep(0.5)
                        st.rerun()
                st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    with tab_dig2:
        st.markdown("#### Patron Digital Access Audit Trail")
        logs_df = db.query_df("""
            SELECT l.LogID AS AuditID, b.Title AS Asset, dr.ResourceType AS Type,
                   m.FirstName || ' ' || m.LastName AS Patron,
                   l.AccessDate, l.AccessType AS Mode, l.IPAddress AS ClientIP
            FROM DigitalAccessLog l
            JOIN DigitalResource dr ON l.ResourceID = dr.ResourceID
            JOIN Book b ON dr.BookID = b.BookID
            JOIN Member m ON l.MemberID = m.MemberID
            ORDER BY l.LogID DESC
        """)
        st.dataframe(logs_df, width="stretch", hide_index=True)


# ==============================================================================
# 8. SQL QUERY CONSOLE
# ==============================================================================
elif nav_option == "⚡ SQL Query Console":
    render_hero(
        "Interactive SQL Query Execution Console",
        "Test relational joins, nested subqueries, aggregations, and standard DBMS PBL evaluation queries."
    )

    preset_queries = {
        "Select a pre-configured query...": "",
        "Q1. 5-Table Join: Complete Book Circulation Ledger": """
SELECT i.IssueID, b.Title, cp.AccessionNumber,
       m.FirstName || ' ' || m.LastName AS MemberName,
       m.MembershipType, i.IssueDate, i.DueDate, i.Status
FROM Issue i
JOIN Copy cp ON i.CopyID = cp.CopyID
JOIN Edition e ON cp.EditionID = e.EditionID
JOIN Book b ON e.BookID = b.BookID
JOIN Member m ON i.MemberID = m.MemberID;
        """,
        "Q2. Group By with Having: Active Borrowers by Category": """
SELECT m.MembershipType, COUNT(i.IssueID) AS TotalLoans
FROM Member m
JOIN Issue i ON m.MemberID = i.MemberID
GROUP BY m.MembershipType
HAVING COUNT(i.IssueID) >= 1;
        """,
        "Q3. Subquery: Members with Outstanding Unpaid Fines": """
SELECT MemberID, FirstName || ' ' || LastName AS Name, Email, Phone
FROM Member
WHERE MemberID IN (
    SELECT MemberID FROM Fine WHERE Status = 'Pending'
);
        """,
        "Q4. System Aggregates: Combined Circulation and Revenue Snapshot": """
SELECT
    (SELECT COUNT(*) FROM Copy WHERE Status = 'Issued') AS TotalIssuedCopies,
    (SELECT COUNT(*) FROM Copy WHERE Status = 'Available') AS TotalAvailableCopies,
    (SELECT COALESCE(SUM(Amount), 0) FROM Fine WHERE Status = 'Pending') AS TotalPendingFine,
    (SELECT COUNT(*) FROM Member WHERE IsActive = 1) AS TotalActiveMembers;
        """,
        "Q5. Correlated Subquery: Books With No Physical Copies Currently Issued": """
SELECT BookID, Title, ISBN
FROM Book b
WHERE NOT EXISTS (
    SELECT 1 FROM Edition e
    JOIN Copy cp ON e.EditionID = cp.EditionID
    WHERE e.BookID = b.BookID AND cp.Status = 'Issued'
);
        """
    }

    selected_preset = st.selectbox("Load Standard Evaluation Query:", list(preset_queries.keys()))
    initial_text = preset_queries[selected_preset] if selected_preset != "Select a pre-configured query..." else "SELECT * FROM Book;"

    query_input = st.text_area("SQL Statement:", value=initial_text.strip(), height=160)

    if st.button("🚀 Execute SQL Statement", type="primary", use_container_width=True):
        t0 = time.time()
        try:
            result_df = db.query_df(query_input)
            elapsed = (time.time() - t0) * 1000
            st.success(f"Query returned {len(result_df)} rows in {elapsed:.1f} ms.")
            st.dataframe(result_df, width="stretch", hide_index=True)
            
            # Download query result as CSV
            csv = result_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "📥 Export Result as CSV",
                data=csv,
                file_name="query_result.csv",
                mime="text/csv"
            )
        except Exception as e:
            st.error(f"Execution Error: {str(e)}")
