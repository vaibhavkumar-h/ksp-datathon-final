"""Shared session authentication helpers for Streamlit pages."""

import streamlit as st


def is_authenticated() -> bool:
    """Return whether the current browser session has completed login."""
    return st.session_state.get("logged_in", False) is True


def login_user(username: str) -> None:
    """Persist the authenticated user's identity for the current session."""
    st.session_state.logged_in = True
    st.session_state.user = username


def require_auth() -> None:
    """Redirect unauthenticated visitors to login and stop this page."""
    if not is_authenticated():
        st.switch_page("login.py")
        st.stop()


def logout() -> None:
    """Clear all session data and return the visitor to the login page."""
    st.session_state.clear()
    st.switch_page("login.py")
    st.stop()


def render_logout_button() -> None:
    """Render shared authenticated navigation controls in the sidebar."""
    with st.sidebar:
        user = st.session_state.get("user", "User")
        st.caption(f"Signed in as {user.title()}")
        if st.button("Logout", use_container_width=True):
            logout()
