import streamlit as st
import pandas as pd

from database.connection import engine
from sqlalchemy import text

# ============================================================
# TABLES PAGE THEME
# ============================================================

st.markdown(
    '<div class="table-navigation">',
    unsafe_allow_html=True
)
# ============================================================
# TABLES PAGE
# ============================================================

def show_tables():
    st.markdown(
        '<div style="font-size:45px; font-weight:800; color:#8B0000; '
        'text-align:left; line-height:1.2; margin-top:-5px; margin-bottom:0px;">'
        '📋 Data Tables'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div style="font-size:15px; font-weight:400; color:#555555; '
        'text-align:left; line-height:1.4; margin-bottom:18px;">'
        'View application records from the Service Analytics database'
        '</div>',
        unsafe_allow_html=True
    )

    # ========================================================
    # TABLE NAVIGATION
    # ========================================================

    if "table_page" not in st.session_state:
        st.session_state.table_page = "Vehicle"

    st.markdown(
        '<div class="entry-navigation">',
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <style>

        /* ========================================================
           TABLE NAVIGATION BUTTONS
           ======================================================== */

        div[data-testid="stButton"] > button {

            background-color: rgba(255, 235, 220, 0.98) !important;

            border: 5px solid #B22222 !important;

            border-radius: 12px !important;

            color: #8B0000 !important;

            font-size: 14px !important;

            font-weight: 800 !important;

            min-height: 85px !important;

            width: 100% !important;

            box-shadow:
                0px 3px 8px
                rgba(120, 0, 0, 0.20) !important;
        }

        div[data-testid="stButton"] > button:hover {

            background-color: rgba(255, 235, 220, 0.94) !important;

            border-color: #8B0000 !important;

            color: #8B0000 !important;
        }

        </style>
        """,
        unsafe_allow_html=True
    )
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        if st.button(
                "🚗\nVEHICLE",
                key="table_vehicle",
                use_container_width=True
        ):
            st.session_state.table_page = "Vehicle"
            st.rerun()

    with col2:
        if st.button(
                "👥\nPARTNER",
                key="table_partner",
                use_container_width=True
        ):
            st.session_state.table_page = "Partner"
            st.rerun()

    with col3:
        if st.button(
                "🏢\nLOCATION",
                key="table_location",
                use_container_width=True
        ):
            st.session_state.table_page = "Location"
            st.rerun()

    with col4:
        if st.button(
                "🧾\nINVOICE",
                key="table_invoice",
                use_container_width=True
        ):
            st.session_state.table_page = "Invoice"
            st.rerun()

    with col5:
        if st.button(
                "🔧\nSERVICE",
                key="table_service",
                use_container_width=True
        ):
            st.session_state.table_page = "Service"
            st.rerun()

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

    # ========================================================
    # THEMED DATA TABLE
    # ========================================================

    def display_themed_table(df):

        html = df.to_html(
            index=False,
            classes="service-data-table",
            escape=True
        )

        # ====================================================
        # TABLE CSS
        # ====================================================

        st.markdown(
            """
            <style>

            .table-wrapper {
                width: 100%;
                max-height: 820px;
                overflow: auto;
                border: 2px solid #8B0000;
                border-radius: 8px;
                background: transparent;
            }

            .service-data-table {
                width: 100%;
                margin: 0;
                border-collapse: collapse;
                font-size: 13px;
                color: #222222;
            }

            .service-data-table th {
                background-color: #8B0000 !important;
                color: white !important;
                font-weight: 800;
                padding: 9px 10px;
                border: 1px solid #B22222;
                text-align: center;
                position: sticky;
                top: 0;
                z-index: 2;
                white-space: nowrap;
            }

            .service-data-table td {
                padding: 7px 10px;
                border: 1px solid #dddddd;
                white-space: nowrap;
                background-color: white;
            }

            .service-data-table tr:nth-child(even) td {
                background-color: #fff8f4;
            }

            .service-data-table tr:hover td {
                background-color: #ffe8dc;
            }

            </style>
            """,
            unsafe_allow_html=True
        )

        # ====================================================
        # TABLE HTML
        # ====================================================

        st.markdown(
            f"""
            <div class="table-wrapper">
                {html}
            </div>
            """,
            unsafe_allow_html=True
        )
    if st.session_state.table_page == "Vehicle":

        st.subheader("🚗 Vehicles")

        query = text("""
            SELECT *
            FROM sample_vehicles
            ORDER BY vehicle_id
        """)

        with engine.connect() as conn:

            df_vehicles = pd.read_sql(
                query,
                conn
            )

        display_themed_table(df_vehicles)


    elif st.session_state.table_page == "Partner":

        st.subheader("👥 Partners")

        query = text("""
            SELECT *
            FROM sample_customers
            ORDER BY customer_vehicle_id
        """)

        with engine.connect() as conn:

            df_partners = pd.read_sql(
                query,
                conn
            )

        display_themed_table(df_partners)


    elif st.session_state.table_page == "Location":

        st.subheader("🏢 Retail Locations")

        query = text("""
            SELECT *
            FROM sample_retail_locations
            ORDER BY retail_location_id
        """)

        with engine.connect() as conn:

            df_locations = pd.read_sql(
                query,
                conn
            )

        display_themed_table(df_locations)


    elif st.session_state.table_page == "Invoice":

        st.subheader("🧾 Invoices")

        query = text("""
            SELECT *
            FROM sample_invoices
            ORDER BY invoice_date DESC, invoice_id
        """)

        with engine.connect() as conn:

            df_invoices = pd.read_sql(
                query,
                conn
            )

        display_themed_table(df_invoices)


    elif st.session_state.table_page == "Service":

        st.subheader("🔧 Services")

        query = text("""
            SELECT *
            FROM sample_service_history
            ORDER BY invoice_date DESC, service_id
        """)

        with engine.connect() as conn:

            df_services = pd.read_sql(
                query,
                conn
            )

        display_themed_table(df_services)


