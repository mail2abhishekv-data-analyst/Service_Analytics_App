import streamlit as st
from sqlalchemy import text
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from database.connection import engine


def show_partners_choice():

    # ========================================================
    # PAGE TITLE
    # ========================================================

    st.markdown(
        """
        <div class="dashboard-header">
            <div class="partners-title">
                PARTNERS' CHOICE
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ========================================================
    # KPI QUERIES
    # ========================================================

    with engine.connect() as conn:

        partner_data = conn.execute(
            text("""
                SELECT
                    COUNT(DISTINCT customer_vehicle_id) AS total_partners,

                    SUM(
                        CASE
                            WHEN loyal_customer_flag = 1
                            THEN 1
                            ELSE 0
                        END
                    ) AS loyal_partners,

                    AVG(
                        CAST(lifetime_value AS FLOAT)
                    ) AS avg_lifetime_value,

                    AVG(
                        CAST(visit_count AS FLOAT)
                    ) AS avg_visits
                FROM sample_customers
            """)
        ).fetchone()

        vehicle_data = conn.execute(
            text("""
                SELECT
                    COUNT(DISTINCT vehicle_id) AS total_vehicles
                FROM sample_vehicles
            """)
        ).fetchone()

        location_data = conn.execute(
            text("""
                SELECT
                    COUNT(DISTINCT retail_location_id) AS total_locations
                FROM sample_retail_locations
            """)
        ).fetchone()

    total_partners = partner_data.total_partners
    loyal_partners = partner_data.loyal_partners
    avg_lifetime_value = partner_data.avg_lifetime_value
    avg_visits = partner_data.avg_visits

    total_vehicles = vehicle_data.total_vehicles
    total_locations = location_data.total_locations

    # ========================================================
    # KPI ROW
    # ========================================================

    col1, col2, col3, col4, col5, col6 = st.columns(
        6,
        gap="small"
    )

    with col1:
        st.html(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">
                    👥 Total Partners
                </div>

                <div class="kpi-value">
                    {total_partners:,}
                </div>
            </div>
            """
        )

    with col2:
        st.html(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">
                    ⭐ Loyal Partners
                </div>

                <div class="kpi-value">
                    {loyal_partners:,}
                </div>
            </div>
            """
        )

    with col3:
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

    with col4:
        st.html(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">
                    📍 Retail Locations
                </div>

                <div class="kpi-value">
                    {total_locations:,}
                </div>
            </div>
            """
        )

    with col5:
        st.html(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">
                    💰 Avg Lifetime Value
                </div>

                <div class="kpi-value">
                    ₹{avg_lifetime_value:,.2f}
                </div>
            </div>
            """
        )

    with col6:
        st.html(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">
                    🔄 Avg Visits / Partner
                </div>

                <div class="kpi-value">
                    {avg_visits:.2f}
                </div>
            </div>
            """
        )

    # ========================================================
    # PARTNER ANALYSIS QUERIES
    # ========================================================

    with engine.connect() as conn:
        # ----------------------------------------------------
        # PARTNERS BY REGION
        # ----------------------------------------------------

        region_data = pd.read_sql(
            text("""
                SELECT
                    CAST(region AS VARCHAR(20)) AS region,
                    COUNT(DISTINCT customer_vehicle_id) AS partner_count
                FROM sample_customers
                GROUP BY region
                ORDER BY partner_count DESC
            """),
            conn
        )

        # ----------------------------------------------------
        # LOYALTY & CHURN BY REGION
        # ----------------------------------------------------

        behavior_data = pd.read_sql(
            text("""
                SELECT
                    CAST(region AS VARCHAR(20)) AS region,

                    CASE
                        WHEN loyal_customer_flag = 1 AND churn_flag = 0
                            THEN 'Loyal & Active'

                        WHEN loyal_customer_flag = 1 AND churn_flag = 1
                            THEN 'Loyal & Churned'

                        WHEN loyal_customer_flag = 0 AND churn_flag = 0
                            THEN 'Non-Loyal & Active'

                        WHEN loyal_customer_flag = 0 AND churn_flag = 1
                            THEN 'Non-Loyal & Churned'
                    END AS partner_status,

                    COUNT(*) AS partner_count

                FROM sample_customers

                GROUP BY
                    region,
                    loyal_customer_flag,
                    churn_flag

                ORDER BY region
            """),
            conn
        )

        # ========================================================
        # TOP 10 VEHICLE MAKES
        # ========================================================

        vehicle_make_data = pd.read_sql(
            text("""
                SELECT TOP 10
                    vehicle_make,
                    COUNT(DISTINCT vehicle_id) AS vehicle_count
                FROM sample_vehicles
                GROUP BY vehicle_make
                ORDER BY vehicle_count DESC
            """),
            conn
        )

        # ========================================================
        #  Vehicle Type Distribution
        # ========================================================

        vehicle_type_data = pd.read_sql(
            text("""
                   SELECT
                       vehicle_type,
                       COUNT(DISTINCT vehicle_id) AS vehicle_count
                   FROM sample_vehicles
                   GROUP BY vehicle_type
                   ORDER BY vehicle_count DESC
               """),
            conn
        )

    # ========================================================
    # REGION CATEGORY ORDER
    # ========================================================

    behavior_data["region"] = behavior_data["region"].astype(str)

    region_order = sorted(
        behavior_data["region"].unique(),
        key=int
    )

    # ========================================================
    # VEHICLE TYPE FUNNEL
    # ========================================================

    fig_vehicle_type = go.Figure(
        go.Funnel(
            y=vehicle_type_data["vehicle_type"],
            x=vehicle_type_data["vehicle_count"],

            textinfo="label+value+percent initial",

            marker=dict(
                color=[
                    "#8B0000",
                    "#B22222",
                    "#CD5C5C"
                ]
            ),

            textfont=dict(
                color="white",
                size=13
            )
        )
    )
    fig_vehicle_type.update_layout(

        height=320,

        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",

        font=dict(
            family="Arial",
            color="#8B0000"
        ),

        margin=dict(
            l=30,
            r=30,
            t=20,
            b=20
        ),

        showlegend=False
    )

    # ========================================================
    # PARTNER ANALYSIS CHARTS
    # ========================================================

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.markdown(
            """
            <div class="chart-title">
                📍 Partners by Region
            </div>
            """,
            unsafe_allow_html=True
        )

        fig_region = px.bar(
            region_data,
            x="partner_count",
            y="region",
            orientation="h",
            text="partner_count"
        )

        fig_region.update_traces(
            textposition="outside",
            textfont=dict(
                size=12,
                color="#8B0000"
            )
        )

        fig_region.update_layout(
            yaxis=dict(
                title="Region",
                type="category",
                categoryorder="total descending"
            )
        )
        fig_region.update_traces(
            marker_color="#8B0000",

            textposition="outside",

            textfont=dict(
                size=13,
                color="#8B0000"
            )
        )

        fig_region.update_layout(
            height=320,

            # Transparent chart background
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",

            font=dict(
                family="Arial",
                color="#8B0000"
            ),

            xaxis=dict(
                title=dict(
                    text="Number of Partners",
                    font=dict(
                        color="#8B0000",
                        size=13
                    )
                ),

                tickfont=dict(
                    color="#8B0000",
                    size=12
                ),

                showgrid=False,
                zeroline=False
            ),

            yaxis=dict(
                title=dict(
                    text="Region",
                    font=dict(
                        color="#8B0000",
                        size=13
                    )
                ),

                tickfont=dict(
                    color="#8B0000",
                    size=12
                ),

                type="category",
                categoryorder="total descending"
            ),

            margin=dict(
                l=65,
                r=45,
                t=25,
                b=55
            ),

            showlegend=False
        )
        st.plotly_chart(
            fig_region,
            use_container_width=True
        )
    with chart_col2:
        st.markdown(
            """
            <div class="chart-title">
                🔄 Partner Loyalty & Churn by Region
            </div>
            """,
            unsafe_allow_html=True
        )

        fig_behavior = px.bar(
            behavior_data,
            x="partner_count",
            y="region",
            color="partner_status",
            orientation="h",
            text="partner_count",
            barmode="stack",

            category_orders={
                "region": region_order,

                "partner_status": [
                    "Loyal & Active",
                    "Loyal & Churned",
                    "Non-Loyal & Active",
                    "Non-Loyal & Churned"
                ]
            },

            color_discrete_map={
                "Loyal & Active": "#8B0000",
                "Loyal & Churned": "#B22222",
                "Non-Loyal & Active": "#CD5C5C",
                "Non-Loyal & Churned": "#F08080"
            }
        )
        fig_behavior.update_traces(
            textposition="inside",
            textfont=dict(
                size=11,
                color="white"
            )
        )

        fig_behavior.update_yaxes(
            type="category"
        )

        fig_behavior.update_layout(

            height=320,

            # ====================================================
            # TRANSPARENT BACKGROUND
            # ====================================================

            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",

            # ====================================================
            # GENERAL FONT
            # ====================================================

            font=dict(
                family="Arial",
                color="#8B0000"
            ),

            # ====================================================
            # X AXIS
            # ====================================================

            xaxis=dict(

                title=dict(
                    text="Number of Partners",
                    font=dict(
                        color="#8B0000",
                        size=13
                    )
                ),

                tickfont=dict(
                    color="#8B0000",
                    size=12
                ),

                showgrid=False,
                zeroline=False
            ),

            # ====================================================
            # Y AXIS
            # ====================================================

            yaxis=dict(

                title=dict(
                    text="Region",
                    font=dict(
                        color="#8B0000",
                        size=13
                    )
                ),

                tickfont=dict(
                    color="#8B0000",
                    size=12
                ),

                type="category"
            ),

            # ====================================================
            # LEGEND
            # ====================================================

            legend=dict(

                title=dict(
                    text="Partner Status",
                    font=dict(
                        color="#8B0000",
                        size=12
                    )
                ),

                font=dict(
                    color="#8B0000",
                    size=11
                )
            ),

            margin=dict(
                l=65,
                r=45,
                t=25,
                b=55
            )
        )

        st.plotly_chart(
            fig_behavior,
            use_container_width=True
        )
    # ========================================================
    # TOP 10 VEHICLE MAKES CHART
    # ========================================================
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div class="chart-title">
                🚗 Top 10 Vehicle Makes
            </div>
            """,
            unsafe_allow_html=True
        )

        fig_vehicle_make = px.bar(
            vehicle_make_data,
            x="vehicle_make",
            y="vehicle_count",
            text="vehicle_count"
        )
        fig_vehicle_make.update_traces(

            marker_color="#8B0000",

            textposition="outside",

            textfont=dict(
                size=13,
                color="#8B0000"
            )
        )
        fig_vehicle_make.update_layout(

            height=320,

            # Transparent background
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",

            font=dict(
                family="Arial",
                color="#8B0000"
            ),

            # X AXIS
            xaxis=dict(

                title=dict(
                    text="Vehicle Make",
                    font=dict(
                        color="#8B0000",
                        size=13
                    )
                ),

                tickfont=dict(
                    color="#8B0000",
                    size=11
                ),

                showgrid=False,
                zeroline=False
            ),

            # Y AXIS
            yaxis=dict(

                title=dict(
                    text="Number of Vehicles",
                    font=dict(
                        color="#8B0000",
                        size=13
                    )
                ),

                tickfont=dict(
                    color="#8B0000",
                    size=12
                ),

                showgrid=False,
                zeroline=False
            ),

            margin=dict(
                l=60,
                r=35,
                t=25,
                b=75
            ),

            showlegend=False
        )

        st.plotly_chart(
            fig_vehicle_make,
            use_container_width=True
        )
    with col2:
        st.markdown(
            """
            <div class="chart-title">
                🚘 Vehicle Type Distribution
            </div>
            """,
            unsafe_allow_html=True
        )

        st.plotly_chart(
            fig_vehicle_type,
            use_container_width=True
        )