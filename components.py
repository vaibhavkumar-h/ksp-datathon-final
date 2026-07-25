import streamlit as st


def kpi_card(title, value, icon, color="#2563EB"):
    html = (
        f'<div style="background:#FFFFFF;border:1px solid #E2E8F0;'
        f'border-radius:16px;padding:22px;box-shadow:0 4px 12px rgba(15,23,42,0.08);'
        f'min-height:140px;transition:0.3s;">'
        f'<div style="display:flex;justify-content:space-between;'
        f'align-items:center;margin-bottom:20px;">'
        f'<div style="color:#64748B;font-size:15px;font-weight:600;">{title}</div>'
        f'<div style="width:44px;height:44px;border-radius:12px;background:{color};'
        f'display:flex;align-items:center;justify-content:center;color:white;'
        f'font-size:20px;font-weight:bold;">{icon}</div>'
        f'</div>'
        f'<div style="color:#0F172A;font-size:34px;font-weight:700;'
        f'line-height:1.2;word-break:break-word;">{value}</div>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)