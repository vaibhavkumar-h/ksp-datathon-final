import streamlit as st

def inject_custom_css():
    st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* ==========================================================
   GLOBAL
========================================================== */

html,
body,
.stApp{
    font-family:'Inter',sans-serif !important;
    background:#F4F6F9 !important;
    color:#0F172A !important;
}

/* Hide Streamlit Branding */

#MainMenu{
    visibility:hidden;
}

footer{
    visibility:hidden;
}

/* ==========================================================
   PAGE
========================================================== */

.block-container{
    padding:2rem 2rem 2rem 2rem;
    max-width:100%;
}

/* ==========================================================
   HEADINGS
========================================================== */

h1{
    color:#0F172A !important;
    font-size:2.3rem;
    font-weight:700;
    letter-spacing:-0.5px;
    margin-bottom:.25rem;
}

h2{
    color:#1E293B !important;
    font-weight:600;
}

h3{
    color:#334155 !important;
    font-weight:600;
}

p,
label,
span{
    color:#475569;
}

/* ==========================================================
   SIDEBAR
========================================================== */

section[data-testid="stSidebar"]{
    background:#1E293B;
}

section[data-testid="stSidebar"] *{
    color:white !important;
}

section[data-testid="stSidebar"] .stButton>button{
    width:100%;
}

/* ==========================================================
   BUTTON
========================================================== */

.stButton>button{

    background:#2563EB;

    color:white;

    border:none;

    border-radius:10px;

    font-weight:600;

    padding:.55rem 1.1rem;

    transition:all .2s;

}

.stButton>button:hover{

    background:#1D4ED8;

    transform:translateY(-2px);

}

/* ==========================================================
   INPUTS
========================================================== */

.stTextInput input,
.stNumberInput input,
.stSelectbox div[data-baseweb="select"],
.stTextArea textarea{

    border-radius:10px !important;

    border:1px solid #CBD5E1 !important;

}

/* ==========================================================
   METRICS
========================================================== */

[data-testid="stMetric"]{

    background:white;

    border-radius:14px;

    border:1px solid #E2E8F0;

    padding:18px;

    box-shadow:0 4px 10px rgba(15,23,42,.05);

}

/* ==========================================================
   DATAFRAME
========================================================== */

[data-testid="stDataFrame"]{

    border:1px solid #E2E8F0;

    border-radius:12px;

    overflow:hidden;

}

/* ==========================================================
   EXPANDER
========================================================== */

details{

    border:1px solid #E2E8F0;

    border-radius:12px;

    background:white;

}

/* ==========================================================
   ALERTS
========================================================== */

[data-testid="stAlert"]{

    border-radius:12px;

}

/* ==========================================================
   TABS
========================================================== */

button[data-baseweb="tab"]{

    border-radius:10px;

}

/* ==========================================================
   SCROLLBAR
========================================================== */

::-webkit-scrollbar{
    width:10px;
}

::-webkit-scrollbar-thumb{
    background:#CBD5E1;
    border-radius:10px;
}

::-webkit-scrollbar-thumb:hover{
    background:#94A3B8;
}

</style>
""", unsafe_allow_html=True)
