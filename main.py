import streamlit as st
from pages.dashboard import show_dashboard
from app.auth import authenticate_user
from pathlib import Path
import base64
from pages.partners_choice import show_partners_choice
from pages.entry_panel import show_entry_panel
from pages.tables import show_tables
from pages.user_management import show_user_management
import textwrap



# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Service Analytics",
    page_icon="🚗",
    layout="wide"
)


# ============================================================
# SESSION STATE
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

# ============================================================
# LOGIN PAGE
# ============================================================

def login_page():
    # ========================================================
    # LOGIN PAGE BACKGROUND
    # ========================================================

    LOGIN_FERRARI_BG = r"C:\Users\lappify\Desktop\PowerBi\Notes\Servicing Datasets\ferrari - Copy.webp"

    login_background_base64 = image_to_base64(
        LOGIN_FERRARI_BG
    )

    st.markdown(
        f"""
            <style>

            .stApp {{
                background-image:
                    url("data:image/webp;base64,{login_background_base64}") !important;

                background-size: cover !important;
                background-position: center !important;
                background-attachment: fixed !important;
            }}

            </style>
            """,
        unsafe_allow_html=True
    )


    st.markdown(
        """
        <style>
        /* ====================================================
           HIDE SIDEBAR ON LOGIN PAGE
           ==================================================== */
        
        section[data-testid="stSidebar"] {
            display: none !important;
        }
        /* ====================================================
           TRANSPARENT TOP HEADER
           ==================================================== */
        
        header[data-testid="stHeader"] {
            background: transparent !important;
            box-shadow: none !important;
            border: none !important;
        }
        
        div[data-testid="stToolbar"] {
            background: transparent !important;
        }
        /* ====================================================
           LOGIN CARD
           ==================================================== */

        .login-card {
            width: 530px;
        
            margin-top: 180px;
            margin-left: auto;
            margin-right: 40px;
        
            padding: 28px 30px 18px 30px;
        
            background: rgba(20, 10, 10, 0.72);
        
            border: 4px solid #B22222;
            border-bottom: none;
        
            border-radius: 18px 18px 0 0;
        
            text-align: center;
        }
        div[data-testid="stForm"] {
            width: 530px !important;
        
            margin-left: auto !important;
            margin-right: 40px !important;
        
            padding: 10px 30px 30px 30px !important;
        
            background: rgba(20, 10, 10, 0.72) !important;
        
            border: 4px solid #B22222 !important;
        
            border-top: none !important;
        
            border-radius: 0 0 18px 18px !important;
        
            box-shadow:
                0px 8px 30px rgba(0, 0, 0, 0.45) !important;
        
            box-sizing: border-box !important;
        }


        /* ====================================================
           LOGIN BRAND
           ==================================================== */

        .login-brand {
            font-size: 55px;
            margin-bottom: 5px;
        }


        /* ====================================================
           LOGIN TITLE
           ==================================================== */

        .login-title {
            color: white !important;

            font-size: 32px;
            font-weight: 900;

            letter-spacing: 1px;

            line-height: 1.05;
        }


        /* ====================================================
           LOGIN SUBTITLE
           ==================================================== */

        .login-subtitle {
            color: #ffdddd !important;

            font-size: 13px;
            font-weight: 800;

            letter-spacing: 1.5px;

            margin-top: 12px;
        }


        /* ====================================================
           LOGIN INPUT LABELS
           ==================================================== */

        div[data-testid="stTextInput"] label {
            color: #8B0000 !important;

            font-size: 16px !important;

            font-weight: 800 !important;
        }


        /* ====================================================
           LOGIN INPUT BOX
           ==================================================== */

        div[data-testid="stTextInput"] input {

            border: 3px solid #B22222 !important;

            border-radius: 10px !important;

            background: rgba(255, 255, 255, 0.94) !important;

            color: #222222 !important;

            font-size: 16px !important;

            font-weight: 700 !important;

            padding: 10px 12px !important;
        }


        div[data-testid="stTextInput"] input:focus {

            border-color: #8B0000 !important;

            box-shadow:
                0px 0px 8px
                rgba(139, 0, 0, 0.35) !important;
        }


        /* ====================================================
           LOGIN BUTTON
           ==================================================== */

        div[data-testid="stFormSubmitButton"] button {

            background: #8B0000 !important;

            border: 4px solid #B22222 !important;

            border-radius: 12px !important;

            color: white !important;

            font-size: 18px !important;

            font-weight: 900 !important;

            min-height: 55px !important;

            box-shadow:
                0px 5px 12px
                rgba(120, 0, 0, 0.35) !important;
        }


        div[data-testid="stFormSubmitButton"] button:hover {

            background: #B22222 !important;

            border-color: #8B0000 !important;

            color: white !important;
        }


        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown("""
    <div class="login-card">
    <div class="login-brand">🚗</div>
    <div class="login-title">VERMA CAR</div>
    <div class="login-title">SERVICING CENTER</div>
    <div class="login-subtitle">SERVICE ANALYTICS & MANAGEMENT SYSTEM</div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("login_form"):

        username = st.text_input(
            "Username"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        login_button = st.form_submit_button(
            "LOGIN",
            use_container_width=True
        )

        if login_button:

            if not username or not password:

                st.error(
                    "Please enter username and password."
                )

            else:

                user = authenticate_user(
                    username,
                    password
                )

                if user:

                    st.session_state.logged_in = True
                    st.session_state.user = user

                    st.success(
                        "Login successful!"
                    )

                    st.rerun()

                else:

                    st.error(
                        "Invalid username or password."
                    )
# ============================================================
# GLOBAL THEME
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

FERRARI_BG = BASE_DIR / "assets" / "ferrari.webp"


def image_to_base64(image_path):

    with open(image_path, "rb") as image_file:
        return base64.b64encode(
            image_file.read()
        ).decode()


background_base64 = image_to_base64(FERRARI_BG)


def apply_global_theme():

    st.markdown(
        f"""
        <style>

        /* ====================================================
           GLOBAL PAGE BACKGROUND
           ==================================================== */

        .stApp {{
            background-image:
                linear-gradient(
                    rgba(255, 255, 255, 0.55),
                    rgba(255, 255, 255, 0.55)
                ),
                url("data:image/webp;base64,{background_base64}");

            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}


        /* ====================================================
           STREAMLIT HEADER
           ==================================================== */

        header[data-testid="stHeader"] {{
            background: transparent !important;
            box-shadow: none !important;
            border: none !important;
        }}

        div[data-testid="stToolbar"] {{
            background: transparent !important;
        }}


        /* ====================================================
           SIDEBAR THEME
           ==================================================== */

        section[data-testid="stSidebar"] {{
            background: rgba(245, 220, 220, 0.35) !important;
            border-right: 4px solid #8B0000 !important;
            color: #8B0000 !important;
        }}

        section[data-testid="stSidebar"] > div {{
            background: transparent !important;
        }}

        div[data-testid="stSidebarNav"] {{
            display: none !important;
        }}

        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] h4 {{
            color: #8B0000 !important;
        }}

        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] label {{
            color: #8B0000 !important;
        }}


        /* ====================================================
           SIDEBAR NAVIGATION TILES
           ==================================================== */

        section[data-testid="stSidebar"] button {{
            border: 2px solid #8B0000 !important;
            border-radius: 10px !important;

            background: rgba(224, 247, 250, 0.85) !important;

            color: #8B0000 !important;

            font-weight: 700 !important;
        }}

        section[data-testid="stSidebar"] button:hover {{
            background: rgba(139, 0, 0, 0.12) !important;
            color: #8B0000 !important;
        }}
        
        /* ====================================================
        GLOBAL KPI CARD
         ==================================================== */

        .kpi-card {{
            width: 100%;
            box-sizing: border-box;

            background: rgba(255, 235, 220, 0.94) !important;

            border: 5px solid #B22222 !important;
            border-radius: 12px !important;

            padding: 12px 8px !important;

            text-align: center !important;

            min-height: 85px;

            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;

            box-shadow:
                0px 3px 8px
                rgba(120, 0, 0, 0.20) !important;
        }}
        

        .kpi-title {{
            width: 100%;

            color: #B22222 !important;

            font-size: 13px !important;
            font-weight: 700 !important;

            text-align: center !important;

            margin-bottom: 5px !important;
        }}


        .kpi-value {{
            width: 100%;

            color: #8B0000 !important;

            font-size: 24px !important;
            font-weight: 800 !important;

            text-align: center !important;
        }}
        
        /* ====================================================
           PARTNERS' CHOICE HEADER
           ==================================================== */
        
        .partners-title {{
            color: #8B0000 !important;
            font-size: 38px !important;
            font-weight: 800 !important;
            text-align: left !important;
            margin-bottom: 10px;
        }}
        
        /* ====================================================
           CHART TITLE
           ==================================================== */
        
        .chart-title {{
            color: #8B0000 !important;
            font-size: 20px !important;
            font-weight: 800 !important;
            text-align: left !important;
        
            margin-top: 14px !important;
            margin-bottom: 8px !important;
        }}
        
        </style>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# MAIN APPLICATION
# ============================================================

def main_application():

    user = st.session_state.user
    apply_global_theme()

    st.sidebar.title("🚗 VERMA Servicing")

    st.sidebar.write(
        f"👤 {user['full_name']}"
    )

    st.sidebar.write(
        f"Role: {user['role']}"
    )

    st.sidebar.divider()

    st.sidebar.markdown(
        """
        <div style="
            color:white;
            font-size:18px;
            font-weight:700;
            margin: 5px 0 14px 4px;
        ">
            📂 Navigation
        </div>
        """,
        unsafe_allow_html=True
    )

    if "page" not in st.session_state:
        st.session_state.page = "Dashboard"

    # ==========================================
    # SIDEBAR TILE CSS
    # ==========================================

    st.markdown(
        """
        <style>

        /* Sidebar buttons */
        section[data-testid="stSidebar"]
        div.stButton > button {

            width: 100% !important;

            background-color: #E0F7FA !important;
            color: #145A32 !important;

            border: 2px solid #80CBC4 !important;
            border-radius: 12px !important;

            height: 48px !important;

            font-size: 16px !important;
            font-weight: 700 !important;

            text-align: left !important;

            padding-left: 16px !important;

            margin-bottom: 9px !important;

            box-shadow: 0 2px 5px rgba(0,0,0,0.20) !important;

            transition: all 0.2s ease !important;
        }


        /* Hover */
        section[data-testid="stSidebar"]
        div.stButton > button:hover {

            background-color: #B2EBF2 !important;

            border-color: #00ACC1 !important;

            color: #063D2A !important;

            transform: translateY(-1px);

            box-shadow: 0 4px 8px rgba(0,0,0,0.25) !important;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    # ==========================================
    # NAVIGATION TILES
    # ==========================================

    if st.sidebar.button(
            "📊   Dashboard",
            key="nav_dashboard",
            use_container_width=True
    ):
        st.session_state.page = "Dashboard"
        st.rerun()

    if st.sidebar.button(
            "👥   Partners' Choice",
            key="nav_customers",
            use_container_width=True
    ):
        st.session_state.page = "Partners' Choice"
        st.rerun()

    if st.sidebar.button(
            "🚗   Entry Panel",
            key="nav_vehicles",
            use_container_width=True
    ):
        st.session_state.page = "Entry Panel"
        st.rerun()

    if st.sidebar.button(
            "📋   Tables",
            key="nav_tables",
            use_container_width=True
    ):
        st.session_state.page = "Tables"
        st.rerun()

    if st.sidebar.button(
            "👤   User Management",
            key="nav_user_management",
            use_container_width=True
    ):
        st.session_state.page = "User Management"
        st.rerun()

    st.sidebar.divider()

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user = None

        st.rerun()
    # ==========================================
    # CURRENT PAGE
    # ==========================================

    if "page" not in st.session_state:
        st.session_state.page = "Dashboard"

    page = st.session_state.page

    if page == "Dashboard":

        show_dashboard()

    elif page == "Partners' Choice":

        show_partners_choice()

    elif page == "Entry Panel":

        if st.session_state.user["role"] in ["Admin", "Manager"]:

            show_entry_panel()

        else:

            st.error(
                "You do not have permission to access the Entry Panel."
            )
    elif page == "Tables":

        show_tables()


    elif page == "User Management":

        show_user_management()


# ============================================================
# APPLICATION ROUTING
# ============================================================

if st.session_state.logged_in:

    main_application()

else:

    login_page()