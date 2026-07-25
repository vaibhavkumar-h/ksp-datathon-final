import matplotlib.pyplot as plt


def dark_figure(figsize=(8, 5)):
    """Drop-in replacement for plt.subplots() that matches the app's dark theme.
    Usage:
        from chart_theme import dark_figure
        fig, ax = dark_figure(figsize=(8, 5))
        ax.scatter(...)
        st.pyplot(fig)
    """
    fig, ax = plt.subplots(figsize=figsize)

    fig.patch.set_facecolor("#0E1117")
    ax.set_facecolor("#1A1D24")

    ax.tick_params(colors="#E6E6E6")
    ax.xaxis.label.set_color("#E6E6E6")
    ax.yaxis.label.set_color("#E6E6E6")
    ax.title.set_color("#FFFFFF")

    for spine in ax.spines.values():
        spine.set_color("#2A2D36")

    ax.grid(color="#2A2D36", linewidth=0.5, alpha=0.6)

    return fig, ax