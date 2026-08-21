import streamlit as st
from sqlalchemy import text
from pathlib import Path
import base64
import pandas as pd
from database.connection import engine
import plotly.express as px


# ============================================================
# ASSET PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

FERRARI_BG = BASE_DIR / "assets" / "ferrari.webp"
FERRARI_LOGO = BASE_DIR / "assets" / "Ferrari_logo.avif"


def image_to_base64(image_path):

    with open(image_path, "rb") as image_file:
        return base64.b64encode(
            image_file.read()
        ).decode()


background_base64 = image_to_base64(FERRARI_BG)
logo_base64 = image_to_base64(FERRARI_LOGO)


# ============================================================
# DASHBOARD
# ============================================================

def show_dashboard():

    # ========================================================
    # FERRARI DASHBOARD STYLE
    # ========================================================

    st.markdown(
        f"""
        <style>

        

        /* ====================================================
           MAIN CONTENT
           ==================================================== */

        .block-container {{
            padding-top: 0.3rem;
            padding-left: 1.5rem;
            padding-right: 1.5rem;
        }}


        /* ====================================================
           FERRARI LOGO
           ==================================================== */

        .ferrari-logo {{
            width: 70px;
            height: 70px;
            object-fit: contain;
            display: block;
            margin: 0 auto 0 auto;
        }}


        /* ====================================================
           DASHBOARD TITLE
           ==================================================== */

        .dashboard-title {{
            color: #8B0000;
            font-size: 45px;
            font-weight: 800;
            text-align: left;
            margin-top: -5px;
            margin-bottom: 0px;
        }}
      
        /* ====================================================
           KPI AREA
           ==================================================== */

        div[data-testid="stHorizontalBlock"] {{
            gap: 10px;
        }}


        /* ====================================================
           KPI CARD
           ==================================================== */

        .kpi-card {{
            background: rgba(255, 235, 220, 0.94);
            border: 5px solid #B22222;
            border-radius: 12px;
            padding: 12px 8px;
            text-align: center;
            min-height: 85px;
            box-shadow:
                0px 3px 8px
                rgba(120, 0, 0, 0.20);
        }}


        .kpi-title {{
            color: #B22222;
            font-size: 13px;
            font-weight: 700;
            margin-bottom: 5px;
        }}


        .kpi-value {{
            color: #8B0000;
            font-size: 24px;
            font-weight: 800;
        }}
             
         
        /* ====================================================
           REMOVE STREAMLIT DEFAULT METRIC LOOK
           ==================================================== */

        [data-testid="stMetric"] {{
            background: transparent;
            border: none;
            padding: 0;
        }}


        [data-testid="stMetricLabel"] {{
            color: #B22222 !important;
            font-weight: 700 !important;
        }}


        [data-testid="stMetricValue"] {{
            color: #8B0000 !important;
            font-weight: 800 !important;
        }}
        
        div[data-testid="stDataFrame"] {{
            background: transparent !important;
            border-radius: 12px !important;
        }}

        div[data-testid="stDataFrame"] iframe {{
            background: transparent !important;
        }}
        .service-table-wrapper {{
            width: 100%;
            height: 360px;
            overflow-y: auto;
            overflow-x: auto;

            background: transparent !important;

            border: 2px solid #8B0000;
            border-radius: 12px;

            padding: 0;
        }}

        .service-data-table {{
            width: 100%;
            border-collapse: collapse;

            background: transparent !important;

            color: #8B0000;
            font-family: Arial, sans-serif;
            font-size: 13px;
        }}

        .service-data-table thead th {{
            background: transparent !important;
            color: #8B0000 !important;

            font-weight: 800;
            font-size: 14px;

            padding: 10px 12px;

            border-bottom: 2px solid #8B0000;

            text-align: left;

            position: sticky;
            top: 0;
            z-index: 2;
        }}

        .service-data-table tbody td {{
            background: transparent !important;
            color: #8B0000 !important;

            padding: 8px 12px;

            border-bottom: 1px solid rgba(139, 0, 0, 0.35);

            white-space: nowrap;
        }}

        .service-data-table tbody tr:hover td {{
            background: rgba(139, 0, 0, 0.08) !important;
        }}
              
         
            
        </style>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # TITLE
    # ========================================================

    st.html(
        f"""
        <div class="dashboard-header">

            <div class="dashboard-title">
                VERMA CAR SERVICING CENTER
            </div>

            <img
                src="data:image/avif;base64,{logo_base64}"
                class="ferrari-logo"
            >

        </div>
        """
    )


    # ========================================================
    # KPI QUERIES
    # ========================================================

    with engine.connect() as connection:

        total_customers = connection.execute(
            text("""
                SELECT COUNT(*)
                FROM sample_customers
            """)
        ).scalar()

        total_vehicles = connection.execute(
            text("""
                SELECT COUNT(*)
                FROM sample_vehicles
            """)
        ).scalar()

        total_invoices = connection.execute(
            text("""
                SELECT COUNT(*)
                FROM sample_invoices
            """)
        ).scalar()

        total_services = connection.execute(
            text("""
                SELECT COUNT(*)
                FROM sample_service_history
            """)
        ).scalar()

        total_locations = connection.execute(
            text("""
                SELECT COUNT(*)
                FROM sample_retail_locations
            """)
        ).scalar()

        total_revenue = connection.execute(
            text("""
                SELECT COALESCE(SUM(invoice_net_sales), 0)
                FROM sample_invoices
            """)
        ).scalar()


    # ========================================================
    # SIX KPI CARDS — SINGLE ROW
    # ========================================================

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        st.html(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">
                    👥 Total Customers
                </div>

                <div class="kpi-value">
                    {total_customers:,}
                </div>
            </div>
            """
        )
    with col2:
        st.html(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">
                    🚗 Total Vehicles
                </div>

                <div class="kpi-value">
                    {total_vehicles:,}
                </div>
            </div>
            """
        )

    with col3:
        st.html(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">
                    🧾 Total Invoices
                </div>

                <div class="kpi-value">
                    {total_invoices:,}
                </div>
            </div>
            """
        )

    with col4:
        st.html(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">
                    🔧 Total Services
                </div>

                <div class="kpi-value">
                    {total_services:,}
                </div>
            </div>
            """
        )

    with col5:
        st.html(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">
                    🏢 Retail Locations
                </div>

                <div class="kpi-value">
                    {total_locations:,}
                </div>
            </div>
            """
        )
    with col6:
        st.html(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">
                    💰 Net Revenue
                </div>

                <div class="kpi-value">
                    ₹{total_revenue:,.2f}
                </div>
            </div>
            """
        )


    # ========================================================
    # MONTHLY SERVICE REVENUE TREND
    # ========================================================

    monthly_revenue_query = text("""
        SELECT
            DATEFROMPARTS(
                YEAR(invoice_date),
                MONTH(invoice_date),
                1
            ) AS month_date,
            SUM(invoice_net_sales) AS total_revenue
        FROM sample_invoices
        GROUP BY
            YEAR(invoice_date),
            MONTH(invoice_date)
        ORDER BY
            month_date
    """)

    with engine.connect() as conn:
        monthly_revenue_df = pd.read_sql(
            monthly_revenue_query,
            conn
        )

    # ========================================================
    # SERVICE REVENUE BY CATEGORY
    # ========================================================

    category_revenue_query = text("""
        SELECT
            invoice_line_category_code AS category,
            SUM(invoice_line_total_amount) AS total_revenue
        FROM sample_service_history
        GROUP BY invoice_line_category_code
        ORDER BY total_revenue DESC
    """)

    with engine.connect() as conn:
        category_revenue_df = pd.read_sql(
            category_revenue_query,
            conn
        )

    # ========================================================
    # TOP 10 VEHICLES BY SERVICE REVENUE
    # ========================================================

    vehicle_revenue_query = text("""
        SELECT TOP 10
            sh.vehicle_id,
            v.vehicle_make,
            v.vehicle_model,
            SUM(sh.invoice_line_total_amount) AS total_revenue
        FROM sample_service_history sh
        INNER JOIN sample_vehicles v
            ON sh.vehicle_id = v.vehicle_id
        GROUP BY
            sh.vehicle_id,
            v.vehicle_make,
            v.vehicle_model
        ORDER BY
            total_revenue DESC
    """)

    with engine.connect() as conn:
        vehicle_revenue_df = pd.read_sql(
            vehicle_revenue_query,
            conn
        )
    vehicle_revenue_df["display_name"] = (
            vehicle_revenue_df["vehicle_make"]
            .str.replace(" TRUCKS", "", regex=False)
            + " • " +
            vehicle_revenue_df["vehicle_model"]
    )

    # ========================================================
    # PARTS VS LABOR REVENUE
    # ========================================================

    parts_labor_query = text("""
        SELECT
            SUM(invoice_parts_amount) AS parts_revenue,
            SUM(invoice_labor_amount) AS labor_revenue
        FROM sample_invoices
    """)

    with engine.connect() as conn:
        parts_labor_df = pd.read_sql(
            parts_labor_query,
            conn
        )

        parts_labor_chart_df = pd.DataFrame({
            "Revenue Type": [
                "Parts Revenue",
                "Labor Revenue"
            ],
            "Revenue": [
                parts_labor_df.loc[0, "parts_revenue"],
                parts_labor_df.loc[0, "labor_revenue"]
            ]
        })

    # ========================================================
    # RECENT SERVICE ACTIVITY
    # ========================================================

    recent_service_query = text("""
        SELECT TOP 10
            sh.invoice_date,
            sh.vehicle_id,
            sh.invoice_line_category_code,
            sh.invoice_line_type,
            sh.invoice_line_total_amount,
            sh.service_parts_amount,
            sh.service_labor_amount
        FROM sample_service_history sh
        ORDER BY
            sh.invoice_date DESC,
            sh.invoice_line_order DESC
    """)

    with engine.connect() as conn:
        recent_service_df = pd.read_sql(
            recent_service_query,
            conn
        )

    vehicle_lookup_query = text("""
        SELECT
            vehicle_id,
            vehicle_make,
            vehicle_model
        FROM sample_vehicles
    """)

    with engine.connect() as conn:
        vehicle_lookup_df = pd.read_sql(
            vehicle_lookup_query,
            conn
        )
    recent_service_df = recent_service_df.merge(
        vehicle_lookup_df,
        on="vehicle_id",
        how="left"
    )

    recent_service_df["Vehicle"] = (
            recent_service_df["vehicle_make"]
            .str.replace(" TRUCKS", "", regex=False)
            + " • " +
            recent_service_df["vehicle_model"]
    )

    recent_service_display = recent_service_df[
        [
            "invoice_date",
            "Vehicle",
            "invoice_line_category_code",
            "invoice_line_type",
            "invoice_line_total_amount",
            "service_parts_amount",
            "service_labor_amount"
        ]
    ].copy()

    recent_service_display.columns = [
        "Service Date",
        "Vehicle",
        "Category",
        "Service Type",
        "Total Amount",
        "Parts",
        "Labor"
    ]

    # ========================================================
    # SERVICE REVENUE TREND
    # ========================================================

    if not monthly_revenue_df.empty:

        monthly_revenue_df["month_date"] = pd.to_datetime(
            monthly_revenue_df["month_date"]
        )

        monthly_revenue_df["month_label"] = (
            monthly_revenue_df["month_date"]
            .dt.strftime("%b %Y")
        )

        fig = px.line(
            monthly_revenue_df,
            x="month_label",
            y="total_revenue",
            markers=True
        )

        fig.update_layout(
            height=280,

            margin=dict(
                l=20,
                r=20,
                t=55,
                b=35
            ),

            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",

            font=dict(
                family="Arial",
                size=13,
                color="#8B0000"
            ),

            title=dict(
                text=" Service Revenue Trend",
                x=0,
                xanchor="left",
                y=0.98,
                font=dict(
                    family="Arial",
                    size=20,
                    color="#8B0000"
                )
            ),

            xaxis=dict(
                title=dict(
                    text="Month",
                    font=dict(
                        family="Arial",
                        size=14,
                        color="#8B0000"
                    )
                ),
                tickfont=dict(
                    family="Arial",
                    size=13,
                    color="#8B0000"
                ),
                showgrid=False,
                zeroline=False,
                linecolor="#8B0000"
            ),

            yaxis=dict(
                title=dict(
                    text="Net Sales",
                    font=dict(
                        family="Arial",
                        size=14,
                        color="#8B0000"
                    )
                ),
                tickfont=dict(
                    family="Arial",
                    size=13,
                    color="#8B0000"
                ),
                showgrid=False,
                zeroline=False,
                linecolor="#8B0000"
            ),

            hovermode="x unified",

            showlegend=False
        )

        fig.update_traces(
            line=dict(
                color="#8B0000",
                width=4
            ),
            marker=dict(
                color="#8B0000",
                size=8
            )
        )
        col1, col2 = st.columns(2)

        with col1:
            st.plotly_chart(
                fig,
                use_container_width=True,
                config={
                    "displayModeBar": False
                }
            )

        with col2:

            fig2 = px.bar(
                category_revenue_df,
                x="category",
                y="total_revenue"
            )

            fig2.update_layout(
                height=280,

                margin=dict(
                    l=20,
                    r=20,
                    t=55,
                    b=35
                ),

                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",

                font=dict(
                    family="Arial",
                    size=13,
                    color="#8B0000"
                ),

                title=dict(
                    text=" Service Revenue by Category",
                    x=0,
                    xanchor="left",
                    y=0.98,
                    font=dict(
                        family="Arial",
                        size=20,
                        color="#8B0000"
                    )
                ),

                xaxis=dict(
                    title=dict(
                        text="Service Category",
                        font=dict(
                            family="Arial",
                            size=14,
                            color="#8B0000"
                        )
                    ),
                    tickfont=dict(
                        family="Arial",
                        size=13,
                        color="#8B0000"
                    ),
                    showgrid=False,
                    zeroline=False,
                    linecolor="#8B0000"
                ),

                yaxis=dict(
                    title=dict(
                        text="Revenue",
                        font=dict(
                            family="Arial",
                            size=14,
                            color="#8B0000"
                        )
                    ),
                    tickfont=dict(
                        family="Arial",
                        size=13,
                        color="#8B0000"
                    ),
                    showgrid=False,
                    zeroline=False,
                    linecolor="#8B0000"
                ),

                showlegend=False
            )

            fig2.update_traces(
                marker=dict(
                    color="#8B0000"
                )
            )

            st.plotly_chart(
                fig2,
                use_container_width=True,
                config={
                    "displayModeBar": False
                }
            )

        col3, col4 = st.columns(2)

        with col3:

            fig3 = px.bar(
                vehicle_revenue_df,
                x="total_revenue",
                y="display_name",
                orientation="h",
                custom_data=["vehicle_id", "vehicle_make", "vehicle_model"]
            )
            fig3.update_layout(
                height=280,

                margin=dict(
                    l=20,
                    r=20,
                    t=55,
                    b=35
                ),

                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",

                font=dict(
                    family="Arial",
                    size=13,
                    color="#8B0000"
                ),

                title=dict(
                    text="🚗 Top 10 Vehicles by Service Revenue",
                    x=0,
                    xanchor="left",
                    y=0.98,
                    font=dict(
                        family="Arial",
                        size=20,
                        color="#8B0000"
                    )
                ),

                xaxis=dict(
                    title=dict(
                        text="Service Revenue",
                        font=dict(
                            size=14,
                            color="#8B0000"
                        )
                    ),
                    tickfont=dict(
                        size=12,
                        color="#8B0000"
                    ),
                    showgrid=False,
                    zeroline=False,
                    linecolor="#8B0000"
                ),

                yaxis=dict(
                    title=None,
                    tickfont=dict(
                        size=11,
                        color="#8B0000"
                    ),
                    showgrid=False,
                    zeroline=False,
                    linecolor="#8B0000",
                    automargin=True
                ),

                showlegend=False
            )

            fig3.update_traces(
                marker=dict(
                    color="#8B0000"
                ),
                hovertemplate=(
                    "<b>%{y}</b><br>"
                    "Vehicle ID: %{customdata[0]}<br>"
                    "Make: %{customdata[1]}<br>"
                    "Model: %{customdata[2]}<br>"
                    "Service Revenue: ₹%{x:,.2f}"
                    "<extra></extra>"
                )
            )

            st.plotly_chart(
                fig3,
                use_container_width=True,
                config={"displayModeBar": False}
            )

        with col4:

            fig4 = px.bar(
                parts_labor_chart_df,
                x="Revenue Type",
                y="Revenue"
            )

            fig4.update_layout(
                height=280,

                margin=dict(
                    l=20,
                    r=20,
                    t=55,
                    b=35
                ),

                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",

                font=dict(
                    family="Arial",
                    size=13,
                    color="#8B0000"
                ),

                title=dict(
                    text="🔧 Parts vs Labor Revenue",
                    x=0,
                    xanchor="left",
                    y=0.98,
                    font=dict(
                        family="Arial",
                        size=20,
                        color="#8B0000"
                    )
                ),

                xaxis=dict(
                    title=None,
                    tickfont=dict(
                        size=13,
                        color="#8B0000"
                    ),
                    showgrid=False,
                    zeroline=False,
                    linecolor="#8B0000"
                ),

                yaxis=dict(
                    title=dict(
                        text="Revenue",
                        font=dict(
                            size=14,
                            color="#8B0000"
                        )
                    ),
                    tickfont=dict(
                        size=13,
                        color="#8B0000"
                    ),
                    showgrid=False,
                    zeroline=False,
                    linecolor="#8B0000"
                ),

                showlegend=False
            )

            fig4.update_traces(
                marker=dict(
                    color="#8B0000"
                )
            )

            st.plotly_chart(
                fig4,
                use_container_width=True,
                config={"displayModeBar": False}
            )

        st.markdown(
            """
            <div class="section-title">
                📋 Recent Service Activity
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="service-table">
            """,
            unsafe_allow_html=True
        )

        # ========================================================
        # STYLE RECENT SERVICE TABLE
        # ========================================================

        table_html = recent_service_display.to_html(
            index=False,
            classes="service-data-table",
            border=0
        )

        st.markdown(
            f"""
            <div class="service-table-wrapper">
                {table_html}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            </div>
            """,
            unsafe_allow_html=True
        )
    else:

        st.info("No invoice data available for the revenue trend.")