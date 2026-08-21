import streamlit as st
import pandas as pd
from sqlalchemy import text

from database.connection import engine


# ============================================================
# VEHICLE ENTRY
# ============================================================

def vehicle_entry():

    if "vehicle_form_version" not in st.session_state:
        st.session_state.vehicle_form_version = 0


    st.subheader("🚗 Vehicle Entry")

    col1, col2 = st.columns(2)

    with col1:

        vehicle_id = st.text_input(
            "Vehicle ID *",
            placeholder="Enter Vehicle ID",
            key=f"vehicle_id_{st.session_state.vehicle_form_version}",
            value=""
        )

        vehicle_year = st.number_input(
            "Vehicle Year",
            min_value=1900,
            max_value=2100,
            value=2020,
            step=1,
            key=f"vehicle_year_{st.session_state.vehicle_form_version}"
        )
        vehicle_make = st.text_input(
            "Vehicle Make",
            key=f"vehicle_make_{st.session_state.vehicle_form_version}"
        )

        vehicle_model = st.text_input(
            "Vehicle Model",
            key=f"vehicle_model_{st.session_state.vehicle_form_version}"
        )

        vehicle_engine = st.text_input(
            "Vehicle Engine",
            key=f"vehicle_engine_{st.session_state.vehicle_form_version}"
        )

        vehicle_type = st.selectbox(
            "Vehicle Type",
            ["Car", "SUV", "Truck"],
            key=f"vehicle_type_{st.session_state.vehicle_form_version}"
        )

    with col2:

        drive_type = st.selectbox(
            "Drive Type",
            ["FWD", "RWD", "AWD", "4WD"],
            key=f"drive_type_{st.session_state.vehicle_form_version}"
        )

        transmission_type = st.selectbox(
            "Transmission Type",
            ["Automatic", "Manual"],
            key=f"transmission_type_{st.session_state.vehicle_form_version}"
        )

        first_service_date = st.date_input(
            "First Service Date",
            key=f"first_service_date_{st.session_state.vehicle_form_version}"
        )

        last_service_date = st.date_input(
            "Last Service Date",
            key=f"last_service_date_{st.session_state.vehicle_form_version}"
        )

        mileage_first = st.number_input(
            "First Mileage",
            min_value=0,
            value=0,
            step=1,
            key=f"mileage_first_{st.session_state.vehicle_form_version}"
        )

        mileage_last = st.number_input(
            "Last Mileage",
            min_value=0,
            value=0,
            step=1,
            key=f"mileage_last_{st.session_state.vehicle_form_version}"
        )

        fleet_flag = st.checkbox(
            "Fleet Vehicle",
            key=f"fleet_flag_{st.session_state.vehicle_form_version}"
        )

    st.divider()

    if st.button(
        "💾 Save Vehicle",
        type="primary",
        use_container_width=True
    ):

        # ====================================================
        # VALIDATION
        # ====================================================

        if not vehicle_id.strip():

            st.error("Please enter a Vehicle ID.")

            return

        if mileage_last < mileage_first:

            st.error(
                "Last Mileage cannot be less than First Mileage."
            )

            return

        if last_service_date < first_service_date:

            st.error(
                "Last Service Date cannot be earlier than First Service Date."
            )

            return

        # ====================================================
        # DERIVED VALUES
        # ====================================================

        today = pd.Timestamp.today()

        vehicle_age_years = (
            today.year - vehicle_year
        )

        mileage_growth = (
            mileage_last - mileage_first
        )

        service_days = (
            last_service_date - first_service_date
        ).days

        if service_days > 0:

            annualized_mileage = int(
                mileage_growth
                / service_days
                * 365
            )

        else:

            annualized_mileage = mileage_growth

        visit_count = 0

        # ====================================================
        # DATABASE INSERT
        # ====================================================

        try:

            with engine.begin() as conn:

                existing_vehicle = conn.execute(
                    text("""
                        SELECT COUNT(*)
                        FROM sample_vehicles
                        WHERE vehicle_id = :vehicle_id
                    """),
                    {
                        "vehicle_id": vehicle_id.strip()
                    }
                ).scalar()

                if existing_vehicle > 0:

                    st.error(
                        f"Vehicle ID '{vehicle_id}' already exists."
                    )

                    return

                conn.execute(
                    text("""
                        INSERT INTO sample_vehicles
                        (
                            vehicle_id,
                            vehicle_year,
                            vehicle_make,
                            vehicle_model,
                            vehicle_engine,
                            vehicle_type,
                            drive_type,
                            transmission_type,
                            vehicle_age_years,
                            visit_count,
                            first_service_date,
                            last_service_date,
                            mileage_first,
                            mileage_last,
                            mileage_growth,
                            annualized_mileage,
                            fleet_flag
                        )
                        VALUES
                        (
                            :vehicle_id,
                            :vehicle_year,
                            :vehicle_make,
                            :vehicle_model,
                            :vehicle_engine,
                            :vehicle_type,
                            :drive_type,
                            :transmission_type,
                            :vehicle_age_years,
                            :visit_count,
                            :first_service_date,
                            :last_service_date,
                            :mileage_first,
                            :mileage_last,
                            :mileage_growth,
                            :annualized_mileage,
                            :fleet_flag
                        )
                    """),
                    {
                        "vehicle_id": vehicle_id.strip(),
                        "vehicle_year": vehicle_year,
                        "vehicle_make": vehicle_make.strip(),
                        "vehicle_model": vehicle_model.strip(),
                        "vehicle_engine": vehicle_engine.strip(),
                        "vehicle_type": vehicle_type,
                        "drive_type": drive_type,
                        "transmission_type": transmission_type,
                        "vehicle_age_years": vehicle_age_years,
                        "visit_count": visit_count,
                        "first_service_date": first_service_date,
                        "last_service_date": last_service_date,
                        "mileage_first": mileage_first,
                        "mileage_last": mileage_last,
                        "mileage_growth": mileage_growth,
                        "annualized_mileage": annualized_mileage,
                        "fleet_flag": fleet_flag
                    }
                )

            st.session_state.vehicle_form_version += 1

            st.success(
                f"Vehicle '{vehicle_id}' saved successfully!"
            )

            st.rerun()

        except Exception as e:

            st.error(
                f"Unable to save vehicle: {e}"
            )
# ============================================================
# PARTNER ENTRY
# ============================================================

def partner_entry():

    if "partner_form_version" not in st.session_state:
        st.session_state.partner_form_version = 0

    st.subheader("👥 Partner Entry")

    customer_vehicle_id = st.text_input(
        "Customer Vehicle ID *",
        placeholder="Enter Customer Vehicle ID",
        key=f"customer_vehicle_id_{st.session_state.partner_form_version}"
    )
    vehicle_id = st.text_input(
        "Vehicle ID *",
        placeholder="Enter Vehicle ID",
        key=f"partner_vehicle_id_{st.session_state.partner_form_version}"
    )
    region = st.text_input(
        "Region",
        placeholder="Enter Region",
        key=f"region_{st.session_state.partner_form_version}"
    )
    first_visit_date = st.date_input(
        "First Visit Date",
        key=f"partner_first_visit_date_{st.session_state.partner_form_version}"
    )
    last_visit_date = st.date_input(
        "Last Visit Date",
        key=f"partner_last_visit_date_{st.session_state.partner_form_version}"
    )
    fleet_flag = st.checkbox(
        "Fleet Customer",
        key=f"partner_fleet_flag_{st.session_state.partner_form_version}"
    )
    loyal_customer_flag = st.checkbox(
        "Loyal Customer",
        key=f"loyal_customer_flag_{st.session_state.partner_form_version}"
    )
    churn_flag = st.checkbox(
        "Churn Customer",
        key=f"churn_flag_{st.session_state.partner_form_version}"
    )
    st.divider()

    if st.button(
            "💾 Save Partner",
            type="primary",
            use_container_width=True
    ):
        if not customer_vehicle_id.strip():
            st.error("Please enter a Customer Vehicle ID.")

            return

        if not vehicle_id.strip():
            st.error("Please enter a Vehicle ID.")

            return
        visit_count = 0

        today = pd.Timestamp.today().date()

        days_since_last_visit = (
                today - last_visit_date
        ).days

        customer_tenure_days = (
                last_visit_date - first_visit_date
        ).days

        avg_spend = 0

        lifetime_value = 0

        max_invoice_value = 0

        min_invoice_value = 0

        avg_days_between_visits = 0

        try:

            with engine.begin() as conn:

                existing_customer = conn.execute(
                    text("""
                                SELECT COUNT(*)
                                FROM sample_customers
                                WHERE customer_vehicle_id = :customer_vehicle_id
                            """),
                    {
                        "customer_vehicle_id": customer_vehicle_id.strip()
                    }
                ).scalar()

                if existing_customer > 0:
                    st.error(
                        f"Customer Vehicle ID '{customer_vehicle_id}' already exists."
                    )

                    return

                conn.execute(
                    text("""
                                INSERT INTO sample_customers
                                (
                                    customer_vehicle_id,
                                    vehicle_id,
                                    region,
                                    visit_count,
                                    first_visit_date,
                                    last_visit_date,
                                    days_since_last_visit,
                                    customer_tenure_days,
                                    avg_spend,
                                    lifetime_value,
                                    max_invoice_value,
                                    min_invoice_value,
                                    avg_days_between_visits,
                                    churn_flag,
                                    loyal_customer_flag,
                                    fleet_flag
                                )
                                VALUES
                                (
                                    :customer_vehicle_id,
                                    :vehicle_id,
                                    :region,
                                    :visit_count,
                                    :first_visit_date,
                                    :last_visit_date,
                                    :days_since_last_visit,
                                    :customer_tenure_days,
                                    :avg_spend,
                                    :lifetime_value,
                                    :max_invoice_value,
                                    :min_invoice_value,
                                    :avg_days_between_visits,
                                    :churn_flag,
                                    :loyal_customer_flag,
                                    :fleet_flag
                                )
                            """),
                    {
                        "customer_vehicle_id": customer_vehicle_id.strip(),
                        "vehicle_id": vehicle_id.strip(),
                        "region": region.strip(),
                        "visit_count": visit_count,
                        "first_visit_date": first_visit_date,
                        "last_visit_date": last_visit_date,
                        "days_since_last_visit": days_since_last_visit,
                        "customer_tenure_days": customer_tenure_days,
                        "avg_spend": avg_spend,
                        "lifetime_value": lifetime_value,
                        "max_invoice_value": max_invoice_value,
                        "min_invoice_value": min_invoice_value,
                        "avg_days_between_visits": avg_days_between_visits,
                        "churn_flag": churn_flag,
                        "loyal_customer_flag": loyal_customer_flag,
                        "fleet_flag": fleet_flag
                    }
                )
            st.session_state.partner_form_version += 1

            st.success(
                f"Partner '{customer_vehicle_id}' saved successfully!"
            )

            st.rerun()
        except Exception as e:

            st.error(
                f"Unable to save partner: {e}"
            )
# ============================================================
# LOCATION ENTRY
# ============================================================

def location_entry():

    if "location_form_version" not in st.session_state:
        st.session_state.location_form_version = 0

    st.subheader("🏢 Retail Location Entry")
    retail_location_id = st.text_input(
        "Retail Location ID *",
        placeholder="Enter Retail Location ID",
        key=f"retail_location_id_{st.session_state.location_form_version}"
    )
    st.divider()

    if st.button(
            "💾 Save Location",
            type="primary",
            use_container_width=True
    ):
        if not retail_location_id.strip():
            st.error("Please enter a Retail Location ID.")

            return
        invoice_count = 0
        vehicle_count = 0
        total_revenue = 0
        avg_ticket = 0
        try:

            with engine.begin() as conn:

                existing_location = conn.execute(
                    text("""
                            SELECT COUNT(*)
                            FROM sample_retail_locations
                            WHERE retail_location_id = :retail_location_id
                        """),
                    {
                        "retail_location_id": retail_location_id.strip()
                    }
                ).scalar()

                if existing_location > 0:
                    st.error(
                        f"Retail Location ID '{retail_location_id}' already exists."
                    )

                    return

                conn.execute(
                    text("""
                            INSERT INTO sample_retail_locations
                            (
                                retail_location_id,
                                invoice_count,
                                vehicle_count,
                                total_revenue,
                                avg_ticket
                            )
                            VALUES
                            (
                                :retail_location_id,
                                :invoice_count,
                                :vehicle_count,
                                :total_revenue,
                                :avg_ticket
                            )
                        """),
                    {
                        "retail_location_id": retail_location_id.strip(),
                        "invoice_count": invoice_count,
                        "vehicle_count": vehicle_count,
                        "total_revenue": total_revenue,
                        "avg_ticket": avg_ticket
                    }
                )
            st.session_state.location_form_version += 1

            st.success(
                f"Retail Location '{retail_location_id}' saved successfully!"
            )

            st.rerun()

        except Exception as e:

            st.error(
                f"Unable to save location: {e}"
            )
# ============================================================
# INVOICE ENTRY
# ============================================================

def invoice_entry():

    if "invoice_form_version" not in st.session_state:
        st.session_state.invoice_form_version = 0

    st.subheader("🧾 Invoice Entry")
    col1, col2 = st.columns(2)

    with col1:
        invoice_id = st.text_input(
            "Invoice ID *",
            placeholder="Enter Invoice ID",
            key=f"invoice_id_{st.session_state.invoice_form_version}"
        )
        vehicle_id = st.text_input(
            "Vehicle ID *",
            placeholder="Enter Vehicle ID",
            key=f"invoice_vehicle_id_{st.session_state.invoice_form_version}"
        )
        retail_location_id = st.text_input(
            "Retail Location ID *",
            placeholder="Enter Retail Location ID",
            key=f"invoice_retail_location_id_{st.session_state.invoice_form_version}"
        )
        invoice_date = st.date_input(
            "Invoice Date",
            key=f"invoice_date_{st.session_state.invoice_form_version}"
        )


        vehicle_mileage = st.number_input(
            "Vehicle Mileage",
            min_value=0,
            value=0,
            step=1000,
            key=f"vehicle_mileage_{st.session_state.invoice_form_version}"
        )
        line_count = st.number_input(
            "Line Count",
            min_value=0,
            value=1,
            step=1,
            key=f"line_count_{st.session_state.invoice_form_version}"
        )
        fleet_flag = st.checkbox(
            "Fleet Invoice",
            key=f"invoice_fleet_flag_{st.session_state.invoice_form_version}"
        )
    st.divider()
    with col2:

        invoice_gross_sales = st.number_input(
            "Invoice Gross Sales",
            min_value=0.0,
            value=0.0,
            step=100.0,
            key=f"invoice_gross_sales_{st.session_state.invoice_form_version}"
        )

        invoice_net_sales = st.number_input(
            "Invoice Net Sales",
            min_value=0.0,
            value=0.0,
            step=100.0,
            key=f"invoice_net_sales_{st.session_state.invoice_form_version}"
        )

        invoice_parts_amount = st.number_input(
            "Parts Amount",
            min_value=0.0,
            value=0.0,
            step=100.0,
            key=f"invoice_parts_amount_{st.session_state.invoice_form_version}"
        )

        invoice_labor_amount = st.number_input(
            "Labor Amount",
            min_value=0.0,
            value=0.0,
            step=100.0,
            key=f"invoice_labor_amount_{st.session_state.invoice_form_version}"
        )

        tax_total = st.number_input(
            "Tax Total",
            min_value=0.0,
            value=0.0,
            step=10.0,
            key=f"tax_total_{st.session_state.invoice_form_version}"
        )

        promotion_total = st.number_input(
            "Promotion Total",
            min_value=0.0,
            value=0.0,
            step=10.0,
            key=f"promotion_total_{st.session_state.invoice_form_version}"
        )

    if st.button(
            "💾 Save Invoice",
            type="primary",
            use_container_width=True
    ):
        if not invoice_id.strip():
            st.error("Please enter an Invoice ID.")

            return

        if not vehicle_id.strip():
            st.error("Please enter a Vehicle ID.")

            return

        if not retail_location_id.strip():
            st.error("Please enter a Retail Location ID.")

            return

        if invoice_net_sales > invoice_gross_sales:
            st.error(
                "Invoice Net Sales cannot be greater than Gross Sales."
            )

            return
        invoice_year = invoice_date.year

        invoice_month = invoice_date.month

        invoice_quarter = (
                                  (invoice_month - 1) // 3
                          ) + 1

        if invoice_net_sales > 0:

            parts_ratio = (
                    invoice_parts_amount / invoice_net_sales
            )

            labor_ratio = (
                    invoice_labor_amount / invoice_net_sales
            )

        else:

            parts_ratio = 0

            labor_ratio = 0
        try:

            with engine.begin() as conn:

                existing_invoice = conn.execute(
                    text("""
                            SELECT COUNT(*)
                            FROM sample_invoices
                            WHERE invoice_id = :invoice_id
                        """),
                    {
                        "invoice_id": invoice_id.strip()
                    }
                ).scalar()

                if existing_invoice > 0:
                    st.error(
                        f"Invoice ID '{invoice_id}' already exists."
                    )

                    return

                conn.execute(
                    text("""
                            INSERT INTO sample_invoices
                            (
                                invoice_id,
                                vehicle_id,
                                retail_location_id,
                                invoice_date,
                                invoice_year,
                                invoice_month,
                                invoice_quarter,
                                invoice_gross_sales,
                                invoice_net_sales,
                                invoice_parts_amount,
                                invoice_labor_amount,
                                tax_total,
                                promotion_total,
                                vehicle_mileage,
                                line_count,
                                parts_ratio,
                                labor_ratio,
                                fleet_flag
                            )
                            VALUES
                            (
                                :invoice_id,
                                :vehicle_id,
                                :retail_location_id,
                                :invoice_date,
                                :invoice_year,
                                :invoice_month,
                                :invoice_quarter,
                                :invoice_gross_sales,
                                :invoice_net_sales,
                                :invoice_parts_amount,
                                :invoice_labor_amount,
                                :tax_total,
                                :promotion_total,
                                :vehicle_mileage,
                                :line_count,
                                :parts_ratio,
                                :labor_ratio,
                                :fleet_flag
                            )
                        """),
                    {
                        "invoice_id": invoice_id.strip(),
                        "vehicle_id": vehicle_id.strip(),
                        "retail_location_id": retail_location_id.strip(),
                        "invoice_date": invoice_date,
                        "invoice_year": invoice_year,
                        "invoice_month": invoice_month,
                        "invoice_quarter": invoice_quarter,
                        "invoice_gross_sales": invoice_gross_sales,
                        "invoice_net_sales": invoice_net_sales,
                        "invoice_parts_amount": invoice_parts_amount,
                        "invoice_labor_amount": invoice_labor_amount,
                        "tax_total": tax_total,
                        "promotion_total": promotion_total,
                        "vehicle_mileage": vehicle_mileage,
                        "line_count": line_count,
                        "parts_ratio": parts_ratio,
                        "labor_ratio": labor_ratio,
                        "fleet_flag": fleet_flag
                    }
                )
            st.session_state.invoice_form_version += 1

            st.success(
                f"Invoice '{invoice_id}' saved successfully!"
            )

            st.rerun()

        except Exception as e:

            st.error(
                f"Unable to save invoice: {e}"
            )
# ============================================================
# SERVICE ENTRY
# ============================================================

def service_entry():

    if "service_form_version" not in st.session_state:
        st.session_state.service_form_version = 0

    st.subheader("🔧 Service Entry")
    col1, col2 = st.columns(2)

    with col1:
        service_id = st.text_input(
            "Service ID *",
            placeholder="Enter Service ID",
            key=f"service_id_{st.session_state.service_form_version}"
        )

        vehicle_id = st.text_input(
            "Vehicle ID *",
            placeholder="Enter Vehicle ID",
            key=f"service_vehicle_id_{st.session_state.service_form_version}"
        )

        invoice_id = st.text_input(
            "Invoice ID *",
            placeholder="Enter Invoice ID",
            key=f"service_invoice_id_{st.session_state.service_form_version}"
        )

        retail_location_id = st.text_input(
            "Retail Location ID *",
            placeholder="Enter Retail Location ID",
            key=f"service_retail_location_id_{st.session_state.service_form_version}"
        )
        invoice_line_order = st.number_input(
            "Invoice Line Order",
            min_value=1,
            value=1,
            step=1,
            key=f"service_invoice_line_order_{st.session_state.service_form_version}"
        )

        invoice_line_category_code = st.text_input(
            "Invoice Line Category Code",
            placeholder="Enter Category Code",
            key=f"service_category_code_{st.session_state.service_form_version}"
        )

        invoice_line_type = st.text_input(
            "Invoice Line Type",
            placeholder="Enter Line Type",
            key=f"service_line_type_{st.session_state.service_form_version}"
        )

        item_service_flag = st.selectbox(
            "Item / Service",
            ["Service", "Item"],
            key=f"service_item_flag_{st.session_state.service_form_version}"
        )
        service_business_type_id = st.number_input(
            "Service Business Type ID",
            min_value=0,
            value=0,
            step=1,
            key=f"service_business_type_id_{st.session_state.service_form_version}"
        )

        service_domain_id = st.number_input(
            "Service Domain ID",
            min_value=0,
            value=0,
            step=1,
            key=f"service_domain_id_{st.session_state.service_form_version}"
        )

        service_complexity_level = st.selectbox(
            "Service Complexity Level",
            ["Low", "Medium", "High"],
            key=f"service_complexity_{st.session_state.service_form_version}"
        )
    with col2:
        invoice_line_total_amount = st.number_input(
            "Invoice Line Total Amount",
            min_value=0.0,
            value=0.0,
            step=100.0,
            key=f"service_line_total_{st.session_state.service_form_version}"
        )

        service_parts_amount = st.number_input(
            "Service Parts Amount",
            min_value=0.0,
            value=0.0,
            step=100.0,
            key=f"service_parts_amount_{st.session_state.service_form_version}"
        )

        service_labor_amount = st.number_input(
            "Service Labor Amount",
            min_value=0.0,
            value=0.0,
            step=100.0,
            key=f"service_labor_amount_{st.session_state.service_form_version}"
        )

        vehicle_mileage = st.number_input(
            "Vehicle Mileage",
            min_value=0,
            value=0,
            step=1000,
            key=f"service_vehicle_mileage_{st.session_state.service_form_version}"
        )
        invoice_date = st.date_input(
            "Invoice Date",
            key=f"service_invoice_date_{st.session_state.service_form_version}"
        )
        repeat_flag = st.selectbox(
            "Repeat Service",
            ["N", "Y"],
            key=f"service_repeat_flag_{st.session_state.service_form_version}"
        )
        fleet_flag = st.checkbox(
            "Fleet Service",
            key=f"service_fleet_flag_{st.session_state.service_form_version}"
        )
    st.divider()

    if st.button(
            "💾 Save Service",
            type="primary",
            use_container_width=True
    ):
        if not service_id.strip():
            st.error("Please enter a Service ID.")

            return

        if not vehicle_id.strip():
            st.error("Please enter a Vehicle ID.")

            return

        if not invoice_id.strip():
            st.error("Please enter an Invoice ID.")

            return

        if not retail_location_id.strip():
            st.error("Please enter a Retail Location ID.")

            return
        if service_parts_amount + service_labor_amount > invoice_line_total_amount:
            st.error(
                "Parts Amount + Labor Amount cannot be greater than Line Total Amount."
            )

            return
        try:

            with engine.begin() as conn:

                existing_service = conn.execute(
                    text("""
                            SELECT COUNT(*)
                            FROM sample_service_history
                            WHERE service_id = :service_id
                        """),
                    {
                        "service_id": service_id.strip()
                    }
                ).scalar()

                if existing_service > 0:
                    st.error(
                        f"Service ID '{service_id}' already exists."
                    )

                    return

                conn.execute(
                    text("""
                            INSERT INTO sample_service_history
                            (
                                service_id,
                                vehicle_id,
                                invoice_id,
                                retail_location_id,
                                invoice_line_order,
                                invoice_line_category_code,
                                invoice_line_type,
                                item_service_flag,
                                service_business_type_id,
                                service_domain_id,
                                service_complexity_level,
                                invoice_line_total_amount,
                                service_parts_amount,
                                service_labor_amount,
                                vehicle_mileage,
                                invoice_date,
                                repeat_flag,
                                fleet_flag
                            )
                            VALUES
                            (
                                :service_id,
                                :vehicle_id,
                                :invoice_id,
                                :retail_location_id,
                                :invoice_line_order,
                                :invoice_line_category_code,
                                :invoice_line_type,
                                :item_service_flag,
                                :service_business_type_id,
                                :service_domain_id,
                                :service_complexity_level,
                                :invoice_line_total_amount,
                                :service_parts_amount,
                                :service_labor_amount,
                                :vehicle_mileage,
                                :invoice_date,
                                :repeat_flag,
                                :fleet_flag
                            )
                        """),
                    {
                        "service_id": service_id.strip(),
                        "vehicle_id": vehicle_id.strip(),
                        "invoice_id": invoice_id.strip(),
                        "retail_location_id": retail_location_id.strip(),
                        "invoice_line_order": invoice_line_order,
                        "invoice_line_category_code": invoice_line_category_code.strip(),
                        "invoice_line_type": invoice_line_type.strip(),
                        "item_service_flag": item_service_flag,
                        "service_business_type_id": service_business_type_id,
                        "service_domain_id": service_domain_id,
                        "service_complexity_level": service_complexity_level,
                        "invoice_line_total_amount": invoice_line_total_amount,
                        "service_parts_amount": service_parts_amount,
                        "service_labor_amount": service_labor_amount,
                        "vehicle_mileage": vehicle_mileage,
                        "invoice_date": invoice_date,
                        "repeat_flag": repeat_flag,
                        "fleet_flag": fleet_flag
                    }
                )
            st.session_state.service_form_version += 1

            st.success(
            f"Service '{service_id}' saved successfully!"
            )

            st.rerun()

        except Exception as e:

            st.error(
                f"Unable to save service: {e}"
            )
# ============================================================
# ENTRY PANEL
# ============================================================
def show_entry_panel():
    st.markdown(
        """
        <style>

        /* ====================================================
           ENTRY PANEL HEADER
           ==================================================== */

        .entry-header {
            color: #8B0000;
            font-size: 45px;
            font-weight: 800;
            text-align: left;
            margin-top: -25px;
            margin-bottom: 18px;
        }
     
        
        /* ====================================================
           ENTRY NAVIGATION
           ==================================================== */
        
        div[data-testid="stHorizontalBlock"] div[data-testid="stColumn"] div[data-testid="stButton"] button {

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
        
        /* Hover */
        
        .entry-navigation div[data-testid="stButton"] > button:hover {
        
            background: rgba(255, 235, 220, 0.94) !important;
        
            border-color: #8B0000 !important;
        
            color: #8B0000 !important;
        }
        
        /* ====================================================
           SAVE VEHICLE BUTTON
           ==================================================== */
        
        div[data-testid="stButton"] button[kind="primary"] {
        
            background-color: #8B0000 !important;
        
            border: 5px solid #B22222 !important;
        
            border-radius: 12px !important;
        
            color: white !important;
        
            font-size: 15px !important;
        
            font-weight: 800 !important;
        
            min-height: 55px !important;
        
            box-shadow:
                0px 3px 8px
                rgba(120, 0, 0, 0.25) !important;
        }
        
        
        div[data-testid="stButton"] button[kind="primary"]:hover {
        
            background-color: #B22222 !important;
        
            border-color: #8B0000 !important;
        
            color: white !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="entry-header">📝 Entry Panel</div>',
        unsafe_allow_html=True
    )

    # ========================================================
    # ENTRY NAVIGATION
    # ========================================================

    if "entry_page" not in st.session_state:
        st.session_state.entry_page = "Vehicle"

    st.markdown(
        '<div class="entry-navigation">',
        unsafe_allow_html=True
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        if st.button(
                "🚗\nVEHICLE",
                key="entry_vehicle",
                use_container_width=True
        ):
            st.session_state.entry_page = "Vehicle"
            st.rerun()

    with col2:
        if st.button(
                "👥\nPARTNER",
                key="entry_partner",
                use_container_width=True
        ):
            st.session_state.entry_page = "Partner"
            st.rerun()

    with col3:
        if st.button(
                "🏢\nLOCATION",
                key="entry_location",
                use_container_width=True
        ):
            st.session_state.entry_page = "Location"
            st.rerun()

    with col4:
        if st.button(
                "🧾\nINVOICE",
                key="entry_invoice",
                use_container_width=True
        ):
            st.session_state.entry_page = "Invoice"
            st.rerun()

    with col5:
        if st.button(
                "🔧\nSERVICE",
                key="entry_service",
                use_container_width=True
        ):
            st.session_state.entry_page = "Service"
            st.rerun()
    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

    # ========================================================
    # ENTRY CONTENT
    # ========================================================

    if st.session_state.entry_page == "Vehicle":

        vehicle_entry()


    elif st.session_state.entry_page == "Partner":

        partner_entry()


    elif st.session_state.entry_page == "Location":

        location_entry()


    elif st.session_state.entry_page == "Invoice":

        invoice_entry()


    elif st.session_state.entry_page == "Service":

        service_entry()