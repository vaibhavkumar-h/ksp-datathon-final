import streamlit as st

from auth import is_authenticated, login_user
from styles import inject_custom_css


st.set_page_config(
    page_title="VASU — Karnataka State Police",
    page_icon="🛡",
    layout="wide",
)

inject_custom_css()

USERS = {
    "admin": "1234",
    "police": "police123",
    "judge": "judge123",
}

# ---------------------------------------------------------
# Purple-accented, grouped sidebar nav styling
# ---------------------------------------------------------
st.markdown("""
<style>

/* section group headers that st.navigation renders automatically */
section[data-testid="stSidebar"] h3 {
    color: #A78BFA !important;
    font-size: 0.72rem !important;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    margin-top: 18px !important;
    margin-bottom: 4px !important;
}

section[data-testid="stSidebar"] a,
section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"] {
    border-radius: 10px;
    margin: 2px 8px;
    padding: 8px 12px !important;
    transition: transform .18s ease, box-shadow .18s ease, background-color .18s ease;
}

section[data-testid="stSidebar"] a:hover,
section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"]:hover {
    background-color: #2E1065;
    transform: translateX(4px) scale(1.04);
    box-shadow: 0 0 14px rgba(167, 139, 250, 0.55);
}

section[data-testid="stSidebar"] a[aria-current="page"],
section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"][aria-current="page"] {
    background-color: #2E1065;
    box-shadow: 0 0 10px rgba(167, 139, 250, 0.4);
    border-left: 3px solid #A78BFA;
}

section[data-testid="stSidebar"] a:hover svg {
    filter: drop-shadow(0 0 4px rgba(167, 139, 250, 0.9));
    transform: scale(1.1);
    transition: transform .18s ease, filter .18s ease;
}

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# Login-page-specific styling
# ---------------------------------------------------------
st.markdown("""
<style>

.vasu-header {
    text-align: center;
    margin-top: 10px;
    margin-bottom: 6px;
}
.vasu-header .badge {
    display: inline-block;
    background-color: #1A1D24;
    border: 1px solid #2A2D36;
    border-radius: 999px;
    padding: 5px 16px;
    font-size: 0.78rem;
    color: #9CA3AF;
    letter-spacing: 0.5px;
    margin-bottom: 14px;
}
.vasu-title {
    font-size: 2.6rem;
    font-weight: 800;
    letter-spacing: 2px;
    background: linear-gradient(90deg, #7C3AED, #A78BFA);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}
.vasu-subtitle {
    font-size: 0.95rem;
    color: #9CA3AF;
    margin-top: 4px;
    margin-bottom: 2px;
}
.vasu-org {
    font-size: 0.85rem;
    color: #6B7280;
    margin-bottom: 28px;
}

.login-card {
    background-color: #1A1D24;
    border: 1px solid #2A2D36;
    border-radius: 16px;
    padding: 32px 34px 24px 34px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.35);
}

div[data-testid="stTextInput"] input {
    background-color: #12141A !important;
    border: 1px solid #2A2D36 !important;
    border-radius: 8px !important;
    color: #E6E6E6 !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: #7C3AED !important;
    box-shadow: 0 0 0 1px #7C3AED !important;
}

div[data-testid="stButton"] button {
    background-color: #7C3AED;
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    width: 100%;
    padding: 10px 0;
    transition: box-shadow 0.18s ease, transform 0.18s ease;
}
div[data-testid="stButton"] button:hover {
    box-shadow: 0 0 16px rgba(124, 58, 237, 0.5);
    transform: translateY(-1px);
}

.demo-creds {
    text-align: center;
    font-size: 0.78rem;
    color: #6B7280;
    margin-top: 18px;
}

</style>
""", unsafe_allow_html=True)


def render_login_form() -> None:
    # hide the sidebar entirely while logged out
    st.markdown(
        "<style>[data-testid='stSidebarNav'] {display:none;} "
        "section[data-testid='stSidebar'] {display:none;}</style>",
        unsafe_allow_html=True,
    )

    st.markdown("""
    <div class="vasu-header">
        <div class="badge">🚔 KARNATAKA STATE POLICE</div>
        <div class="vasu-title">VASU</div>
        <div class="vasu-subtitle">Vigilant Analytics for Safety &amp; Urban intelligence</div>
        <div class="vasu-org">Crime Intelligence &amp; Decision Support Platform</div>
    </div>
    """, unsafe_allow_html=True)

    left, center, right = st.columns([1, 1.2, 1])

    with center:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)

        st.markdown("##### Secure Login")

        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")

        if st.button("Login"):
            if username in USERS and USERS[username] == password:
                login_user(username)
                st.rerun()
            else:
                st.error("Invalid Username or Password")

        st.markdown(
            '<div class="demo-creds">Demo access: admin / police / judge</div>',
            unsafe_allow_html=True
        )

        st.markdown('</div>', unsafe_allow_html=True)


# ---------------------------------------------------------
# ROUTING
# ---------------------------------------------------------
if not is_authenticated():
    render_login_form()
else:
    # pages = {
    #     "Operations": [
    #         st.Page("pages/app.py", title="Dashboard", icon="🏠"),
    #         st.Page("pages/report_crime.py", title="Report Crime", icon="📢"),
    #         st.Page("pages/alerts.py", title="Alerts", icon="🚨"),
    #     ],
    #     "Intelligence": [
    #         st.Page("pages/crime_prediction.py", title="Crime Prediction", icon="🔮"),
    #         st.Page("pages/crime_chatbot.py", title="Crime Chatbot", icon="💬"),
    #         st.Page("pages/geospatial_hotspot.py", title="Geospatial Hotspot", icon="🗺️"),
    #         st.Page("pages/heatmap.py", title="Heatmap", icon="🔥"),
    #         st.Page("pages/Socioeconomic.py", title="Socioeconomic", icon="🏙️"),
    #         st.Page("pages/comparison.py", title="District Comparison", icon="📊"),
    #     ],
    #     "Reports": [
    #         st.Page("pages/pdf_report.py", title="PDF Report", icon="📄"),
    #         st.Page("pages/leaderboard.py", title="Leaderboard", icon="🏆"),
    #     ],
    # }
    pages = {
        "Operations": [
            st.Page("app_pages/app.py", title="Dashboard", icon="🏠"),
            st.Page("app_pages/report_crime.py", title="Report Crime", icon="📢"),
            st.Page("app_pages/alerts.py", title="Alerts", icon="🚨"),
        ],
        "Intelligence": [
            st.Page("app_pages/crime_prediction.py", title="Crime Prediction", icon="🔮"),
            st.Page("app_pages/crime_chatbot.py", title="Crime Chatbot", icon="💬"),
            st.Page("app_pages/geospatial_hotspot.py", title="Geospatial Hotspot", icon="🗺️"),
            st.Page("app_pages/heatmap.py", title="Heatmap", icon="🔥"),
            st.Page("app_pages/Socioeconomic.py", title="Socioeconomic", icon="🏙️"),
            st.Page("app_pages/comparison.py", title="District Comparison", icon="📊"),
        ],
        "Reports": [
            st.Page("app_pages/pdf_report.py", title="PDF Report", icon="📄"),
            st.Page("app_pages/leaderboard.py", title="Leaderboard", icon="🏆"),
        ],
    }

    pg = st.navigation(pages)
    pg.run()