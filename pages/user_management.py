import streamlit as st
import pandas as pd
import bcrypt

from sqlalchemy import text
from database.connection import engine


# ============================================================
# USER MANAGEMENT PAGE
# ============================================================

def show_user_management():

    # ========================================================
    # PAGE HEADER
    # ========================================================

    st.markdown(
        """
        <div style="
            font-size:45px;
            font-weight:900;
            color:#8B0000;
            text-align:left;
            line-height:1.2;
            margin-top:-5px;
            margin-bottom:2px;
        ">
            👤 User Management
        </div>

        <div style="
            font-size:17px;
            font-weight:800;
            color:#555555;
            text-align:left;
            margin-bottom:20px;
        ">
            Create, manage and monitor application user accounts
        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # USER MANAGEMENT PAGE CSS
    # ========================================================

    st.markdown(
        """
        <style>

        /* ====================================================
           SECTION HEADINGS
           ==================================================== */

        .user-section-title {
            color:#8B0000;
            font-size:28px;
            font-weight:900;
            margin-top:18px;
            margin-bottom:10px;
        }


        /* ====================================================
           USER TABLE
           ==================================================== */

        .user-table-wrapper {
            width:100%;
            max-height:420px;
            overflow:auto;

            border:3px solid #8B0000;
            border-radius:10px;

            background:transparent;
        }

        .user-data-table {
            width:100%;
            border-collapse:collapse;

            font-size:15px;
            font-weight:700;

            color:#222222;
        }

        .user-data-table th {
            background-color:#8B0000 !important;
            color:white !important;

            font-size:16px !important;
            font-weight:900 !important;

            padding:11px 12px;

            border:1px solid #B22222;

            text-align:center;

            position:sticky;
            top:0;
            z-index:2;

            white-space:nowrap;
        }

        .user-data-table td {
            padding:10px 12px;

            border:1px solid #dddddd;

            font-size:15px;
            font-weight:700;

            white-space:nowrap;

            background-color:white;
        }

        .user-data-table tr:nth-child(even) td {
            background-color:#fff8f4;
        }

        .user-data-table tr:hover td {
            background-color:#ffe8dc;
        }


        /* ====================================================
           MANAGEMENT PANEL
           ==================================================== */

        .user-management-panel {
            border:3px solid #B22222;
            border-radius:12px;

            background:rgba(255,235,220,0.70);

            padding:18px 20px;

            margin-top:5px;
            margin-bottom:20px;
        }

        .user-panel-title {
            color:#8B0000;

            font-size:23px;
            font-weight:900;

            margin-bottom:12px;
        }


        /* ====================================================
           STREAMLIT INPUT LABELS
           ==================================================== */

        div[data-testid="stTextInput"] label,
        div[data-testid="stSelectbox"] label {
            color:#8B0000 !important;

            font-size:16px !important;
            font-weight:900 !important;
        }


        /* ====================================================
           INPUT BOXES
           ==================================================== */

        div[data-testid="stTextInput"] input {
            font-size:16px !important;
            font-weight:700 !important;
        }


        /* ====================================================
           USER MANAGEMENT BUTTONS
           ==================================================== */

        div[data-testid="stButton"] > button {
            background-color:rgba(255,235,220,0.98) !important;

            border:4px solid #B22222 !important;

            border-radius:10px !important;

            color:#8B0000 !important;

            font-size:16px !important;
            font-weight:900 !important;

            min-height:55px !important;

            box-shadow:
                0px 3px 8px
                rgba(120,0,0,0.20) !important;
        }

        div[data-testid="stButton"] > button:hover {
            background-color:rgba(139,0,0,0.10) !important;

            border-color:#8B0000 !important;

            color:#8B0000 !important;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # ACTIVE USERS
    # ========================================================

    st.markdown(
        """
        <div class="user-section-title">
            👥 Active Users
        </div>
        """,
        unsafe_allow_html=True
    )


    # Temporary placeholder
    # We will connect this to SQL Server next.

    # ========================================================
    # LOAD ACTIVE USERS FROM SQL SERVER
    # ========================================================

    query_active_users = text("""
        SELECT
            user_id AS [User ID],
            username AS [User Name],
            full_name AS [Full Name],
            role AS [Role],
            created_at AS [Created Date],
            CASE
                WHEN is_active = 1 THEN 'Active'
                ELSE 'Deactivated'
            END AS [Status]
        FROM app_users
        WHERE is_active = 1
        ORDER BY created_at DESC
    """)

    with engine.connect() as conn:
        active_users = pd.read_sql(
            query_active_users,
            conn
        )


    active_html = active_users.to_html(
        index=False,
        classes="user-data-table",
        escape=True
    )


    st.markdown(
        f"""
        <div class="user-table-wrapper">
            {active_html}
        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # USER ID CREATION & DELETION
    # ========================================================

    st.markdown(
        """
        <div class="user-section-title">
            ⚙️ User ID Creation & Deletion
        </div>
        """,
        unsafe_allow_html=True
    )


    col1, col2 = st.columns(2)


    # ========================================================
    # CREATE USER ID
    # ========================================================

    with col1:
        st.markdown(
            """
            <div class="user-panel-title">
                ➕ Create User ID
            </div>
            """,
            unsafe_allow_html=True
        )

        new_user_id = st.text_input(
            "User ID",
            key="new_user_id"
        )

        new_user_name = st.text_input(
            "User Name",
            key="new_user_name"
        )

        new_password = st.text_input(
            "Password",
            type="password",
            key="new_password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            key="confirm_password"
        )

        new_role = st.selectbox(
            "Role",
            [
                "Administrator",
                "Manager",
                "User"
            ],
            key="new_user_role"
        )

        create_user = st.button(
            "➕ CREATE USER ID",
            key="create_user",
            use_container_width=True
        )
        # ========================================================
        # CREATE USER
        # ========================================================

        if create_user:

            # ----------------------------------------------------
            # VALIDATION
            # ----------------------------------------------------

            if not new_user_id.strip():

                st.error("Please enter a User ID.")

            elif not new_user_name.strip():

                st.error("Please enter a User Name.")

            elif not new_password:

                st.error("Please enter a Password.")

            elif not confirm_password:

                st.error("Please confirm the Password.")

            elif new_password != confirm_password:

                st.error("Passwords do not match.")

            else:

                try:

                    # ------------------------------------------------
                    # CHECK WHETHER USERNAME ALREADY EXISTS
                    # ------------------------------------------------

                    check_query = text("""
                        SELECT COUNT(*)
                        FROM app_users
                        WHERE username = :username
                    """)

                    with engine.connect() as conn:

                        existing_user = conn.execute(
                            check_query,
                            {
                                "username": new_user_id.strip()
                            }
                        ).scalar()

                    if existing_user > 0:

                        st.error(
                            "This User ID already exists."
                        )

                    else:

                        # --------------------------------------------
                        # HASH PASSWORD USING BCRYPT
                        # --------------------------------------------

                        password_hash = bcrypt.hashpw(
                            new_password.encode("utf-8"),
                            bcrypt.gensalt()
                        ).decode("utf-8")

                        # --------------------------------------------
                        # INSERT NEW USER
                        # --------------------------------------------

                        insert_query = text("""
                            INSERT INTO app_users
                            (
                                username,
                                password_hash,
                                full_name,
                                role,
                                is_active
                            )
                            VALUES
                            (
                                :username,
                                :password_hash,
                                :full_name,
                                :role,
                                1
                            )
                        """)

                        with engine.begin() as conn:

                            conn.execute(
                                insert_query,
                                {
                                    "username": new_user_id.strip(),
                                    "password_hash": password_hash,
                                    "full_name": new_user_name.strip(),
                                    "role": new_role
                                }
                            )

                        st.success(
                            f"User '{new_user_id}' created successfully."
                        )

                        st.rerun()


                except Exception as e:

                    st.error(
                        f"Database error: {e}"
                    )


    # ========================================================
    # DELETE / DEACTIVATE USER
    # ========================================================

    with col2:
        st.markdown(
            """
            <div class="user-panel-title">
                🗑️ Delete / Deactivate User
            </div>
            """,
            unsafe_allow_html=True
        )

        selected_user = st.text_input(
            "User ID",
            key="selected_user_id"
        )

        user_action = st.selectbox(
            "Action",
            [
                "Activate User",
                "Deactivate User",
                "Delete User"
            ],
            key="user_action"
        )

        st.markdown(
            "<div style='height:27px;'></div>",
            unsafe_allow_html=True
        )
        apply_action = st.button(
            "⚠️ APPLY ACTION",
            key="apply_user_action",
            use_container_width=True
        )
        # ========================================================
        # APPLY ACTIVATE / DEACTIVATE ACTION
        # ========================================================

        if apply_action:

            if not selected_user.strip():

                st.error("Please enter a User ID.")

            else:

                try:

                    user_id_value = int(selected_user)

                    if user_action == "Activate User":

                        query = text("""
                            UPDATE app_users
                            SET is_active = 1
                            WHERE user_id = :user_id
                        """)

                    elif user_action == "Deactivate User":

                        query = text("""
                            UPDATE app_users
                            SET is_active = 0
                            WHERE user_id = :user_id
                        """)


                    else:

                        query = text("""

                            DELETE FROM app_users

                            WHERE user_id = :user_id

                        """)

                    if query is not None:

                        with engine.begin() as conn:

                            result = conn.execute(
                                query,
                                {
                                    "user_id": user_id_value
                                }
                            )

                        if result.rowcount == 0:

                            st.error(
                                "User ID was not found."
                            )

                        else:

                            st.success(
                                f"{user_action} completed successfully."
                            )

                            st.rerun()


                except ValueError:

                    st.error(
                        "User ID must be a numeric value."
                    )

                except Exception as e:

                    st.error(
                        f"Database error: {e}"
                    )


    # ========================================================
    # DELETED / DEACTIVATED USERS
    # ========================================================

    st.markdown(
        """
        <div class="user-section-title">
            🗑️ Deleted / Deactivated Users
        </div>
        """,
        unsafe_allow_html=True
    )


    # Temporary placeholder
    # We will connect this to SQL Server next.

    # ========================================================
    # LOAD DEACTIVATED USERS FROM SQL SERVER
    # ========================================================

    query_inactive_users = text("""
        SELECT
            user_id AS [User ID],
            username AS [User Name],
            full_name AS [Full Name],
            role AS [Role],
            created_at AS [Created Date],
            'Deactivated' AS [Status]
        FROM app_users
        WHERE is_active = 0
        ORDER BY created_at DESC
    """)

    with engine.connect() as conn:

        inactive_users = pd.read_sql(
            query_inactive_users,
            conn
        )


    inactive_html = inactive_users.to_html(
        index=False,
        classes="user-data-table",
        escape=True
    )


    st.markdown(
        f"""
        <div class="user-table-wrapper">
            {inactive_html}
        </div>
        """,
        unsafe_allow_html=True
    )