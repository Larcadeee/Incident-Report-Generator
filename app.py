import streamlit as st
import pandas as pd
from datetime import datetime

# =========================
# PAGE CONFIGURATION
# =========================
st.set_page_config(
    page_title="Incident Report Viewer",
    page_icon="📋",
    layout="wide"
)

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>

    .dispatch-header {
        background-color: #1A5276;
        color: white;
        padding: 15px;
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        border-radius: 5px;
        margin-bottom: 15px;
    }

    .section-header {
        background-color: #2980B9;
        color: white;
        padding: 8px;
        font-weight: bold;
        border-radius: 4px;
        margin-top: 20px;
        margin-bottom: 10px;
    }

    div[data-testid="stTextInput"] input:disabled,
    div[data-testid="stTextArea"] textarea:disabled {
        color: #1A5276 !important;
        background-color: #F8F9FA !important;
        font-weight: 600 !important;
        -webkit-text-fill-color: #1A5276 !important;
    }

</style>
""", unsafe_allow_html=True)

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():

    try:

        df = pd.read_csv("data.csv")

        # CLEAN COLUMN NAMES
        df.columns = df.columns.str.strip()

        # CONVERT TIMESTAMP
        if "TIMESTAMP" in df.columns:

            df["TIMESTAMP"] = pd.to_datetime(
                df["TIMESTAMP"],
                errors="coerce"
            )

            # Filter out rows with invalid timestamps
            df = df[df["TIMESTAMP"].notna()].copy()

            if df.empty:
                st.error("No valid TIMESTAMP values found in data.csv.")
                st.stop()

            df["Filter Date"] = df["TIMESTAMP"].dt.date
            df["Filter Time"] = df["TIMESTAMP"].dt.strftime("%I:%M %p")

        else:
            st.error("TIMESTAMP column not found.")
            st.stop()

        return df

    except FileNotFoundError:
        st.error("data.csv not found.")
        st.stop()

df = load_data()

# =========================
# HEADER
# =========================
st.markdown(
    '<div class="dispatch-header">🔍 INCIDENT REPORT FINDER</div>',
    unsafe_allow_html=True
)

# =========================
# FILTER SECTION
# =========================
st.markdown("### Select an Incident")

col1, col2 = st.columns(2)

with col1:

    min_date = df["Filter Date"].min()
    max_date = df["Filter Date"].max()

    selected_date = st.date_input(
        "1. Select Date 📅",
        value=max_date,
        min_value=min_date,
        max_value=max_date
    )

with col2:

    filtered_by_date = df[
        df["Filter Date"] == selected_date
    ]

    if filtered_by_date.empty:

        st.warning("No incidents recorded on this date.")
        selected_time = None

    else:

        available_times = sorted(
            filtered_by_date["Filter Time"]
            .dropna()
            .unique()
        )

        selected_time = st.selectbox(
            "2. Select Time ⏰",
            options=available_times
        )

st.divider()

# =========================
# DISPLAY RECORD
# =========================
if selected_time:

    record = filtered_by_date[
        filtered_by_date["Filter Time"] == selected_time
    ]

    if not record.empty:

        data = record.iloc[0]

        # =========================
        # SAFE VALUE FUNCTION
        # =========================
        def get_val(column_name):

            if column_name in data:

                val = data[column_name]

                if pd.isna(val):
                    return "N/A"

                return str(val)

            return "N/A"

        # =========================
        # REPORT VIEWER
        # =========================
        st.markdown(
            '<div class="dispatch-header">RESOURCE DISPATCH REPORT</div>',
            unsafe_allow_html=True
        )

        # =========================
        # BASIC INFORMATION
        # =========================
        st.markdown(
            '<div class="section-header">Basic Information</div>',
            unsafe_allow_html=True
        )

        b1, b2, b3 = st.columns(3)

        with b1:
            st.text_input(
                "Incident ID",
                value=get_val("INCIDENT ID"),
                disabled=True
            )

        with b2:
            st.text_input(
                "Priority Dispatch",
                value=get_val("PRIORITY DISPATCH"),
                disabled=True
            )

        with b3:
            st.text_input(
                "User",
                value=get_val("USER"),
                disabled=True
            )

        # =========================
        # INCIDENT DETAILS
        # =========================
        st.markdown(
            '<div class="section-header">Incident Details</div>',
            unsafe_allow_html=True
        )

        i1, i2, i3 = st.columns(3)

        with i1:
            st.text_input(
                "Barangay",
                value=get_val("BARANGAY"),
                disabled=True
            )

        with i2:
            st.text_input(
                "Incident Type",
                value=get_val("INCIDENT TYPE"),
                disabled=True
            )

        with i3:
            st.text_input(
                "KM Radius",
                value=get_val("KM RADIUS"),
                disabled=True
            )

        st.text_input(
            "Based Location",
            value=get_val("BASED LOCATION"),
            disabled=True
        )

        st.text_input(
            "Resource Team",
            value=get_val("RESOURCE TEAM"),
            disabled=True
        )

        # =========================
        # DATE DETAILS
        # =========================
        st.markdown(
            '<div class="section-header">Date Information</div>',
            unsafe_allow_html=True
        )

        d1, d2, d3 = st.columns(3)

        with d1:
            st.text_input(
                "Date",
                value=get_val("DATE"),
                disabled=True
            )

        with d2:
            st.text_input(
                "Day",
                value=get_val("DAY"),
                disabled=True
            )

        with d3:
            st.text_input(
                "Month",
                value=get_val("MONTH"),
                disabled=True
            )

        # =========================
        # TIME TRACKING
        # =========================
        st.markdown(
            '<div class="section-header">Time Tracking</div>',
            unsafe_allow_html=True
        )

        t1, t2 = st.columns(2)

        with t1:

            st.text_input(
                "Notification Time",
                value=get_val("NOTIFICATION TIME"),
                disabled=True
            )

            st.text_input(
                "Dispatch Time",
                value=get_val("DISPATCH TIME"),
                disabled=True
            )

            st.text_input(
                "Run Time",
                value=get_val("RUN TIME"),
                disabled=True
            )

            st.text_input(
                "Scene Time",
                value=get_val("SCENE TIME"),
                disabled=True
            )

            st.text_input(
                "En Route To Higher Facility",
                value=get_val("EN ROUTE TO HIGHER FACILITY"),
                disabled=True
            )

        with t2:

            st.text_input(
                "Arrival To Higher Facility",
                value=get_val("ARRIVAL TO HIGHER FACILITY"),
                disabled=True
            )

            st.text_input(
                "Endorsement Time",
                value=get_val("ENDORSEMENT TIME"),
                disabled=True
            )

            st.text_input(
                "Arrival At Base Time",
                value=get_val("ARRIVAL AT BASE TIME"),
                disabled=True
            )

            st.text_input(
                "Computed Dispatch Time",
                value=get_val("COMPUTED DISPATCH TIME"),
                disabled=True
            )

            st.text_input(
                "Computed Response Time",
                value=get_val("COMPUTED RESPONSE TIME"),
                disabled=True
            )

        # =========================
        # GENERATE REPORT
        # =========================
        st.markdown(
            '<div class="section-header">Generate Report</div>',
            unsafe_allow_html=True
        )

        # =========================
        # CREATE REPORT HTML
        # =========================
        report_html = f"""
        <html>

        <head>

        <style>

            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
            }}

            h1 {{
                text-align: center;
                color: #1A5276;
            }}

            h2 {{
                background-color: #2980B9;
                color: white;
                padding: 8px;
                border-radius: 4px;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 20px;
            }}

            td {{
                border: 1px solid #ccc;
                padding: 10px;
            }}

            .label {{
                font-weight: bold;
                width: 35%;
                background-color: #F4F6F6;
            }}

        </style>

        </head>

        <body>

        <h1>RESOURCE DISPATCH REPORT</h1>

        <h2>Basic Information</h2>

        <table>

            <tr>
                <td class="label">Incident ID</td>
                <td>{get_val("INCIDENT ID")}</td>
            </tr>

            <tr>
                <td class="label">Priority Dispatch</td>
                <td>{get_val("PRIORITY DISPATCH")}</td>
            </tr>

            <tr>
                <td class="label">User</td>
                <td>{get_val("USER")}</td>
            </tr>

            <tr>
                <td class="label">Date</td>
                <td>{get_val("DATE")}</td>
            </tr>

            <tr>
                <td class="label">Day</td>
                <td>{get_val("DAY")}</td>
            </tr>

            <tr>
                <td class="label">Month</td>
                <td>{get_val("MONTH")}</td>
            </tr>

        </table>

        <h2>Incident Details</h2>

        <table>

            <tr>
                <td class="label">Barangay</td>
                <td>{get_val("BARANGAY")}</td>
            </tr>

            <tr>
                <td class="label">Incident Type</td>
                <td>{get_val("INCIDENT TYPE")}</td>
            </tr>

            <tr>
                <td class="label">KM Radius</td>
                <td>{get_val("KM RADIUS")}</td>
            </tr>

            <tr>
                <td class="label">Based Location</td>
                <td>{get_val("BASED LOCATION")}</td>
            </tr>

            <tr>
                <td class="label">Resource Team</td>
                <td>{get_val("RESOURCE TEAM")}</td>
            </tr>

        </table>

        <h2>Time Tracking</h2>

        <table>

            <tr>
                <td class="label">Notification Time</td>
                <td>{get_val("NOTIFICATION TIME")}</td>
            </tr>

            <tr>
                <td class="label">Dispatch Time</td>
                <td>{get_val("DISPATCH TIME")}</td>
            </tr>

            <tr>
                <td class="label">Run Time</td>
                <td>{get_val("RUN TIME")}</td>
            </tr>

            <tr>
                <td class="label">Scene Time</td>
                <td>{get_val("SCENE TIME")}</td>
            </tr>

            <tr>
                <td class="label">En Route To Higher Facility</td>
                <td>{get_val("EN ROUTE TO HIGHER FACILITY")}</td>
            </tr>

            <tr>
                <td class="label">Arrival To Higher Facility</td>
                <td>{get_val("ARRIVAL TO HIGHER FACILITY")}</td>
            </tr>

            <tr>
                <td class="label">Endorsement Time</td>
                <td>{get_val("ENDORSEMENT TIME")}</td>
            </tr>

            <tr>
                <td class="label">Arrival At Base Time</td>
                <td>{get_val("ARRIVAL AT BASE TIME")}</td>
            </tr>

            <tr>
                <td class="label">Computed Response Time</td>
                <td>{get_val("COMPUTED RESPONSE TIME")}</td>
            </tr>

        </table>

        </body>
        </html>
        """

        # =========================
        # MODAL
        # =========================
        @st.dialog("📄 Incident Report Preview", width="large")
        def show_report_modal():

            st.components.v1.html(
                report_html,
                height=700,
                scrolling=True
            )

            st.divider()

            colx1, colx2 = st.columns(2)

            with colx1:

                st.download_button(
                    label="📥 Download Report",
                    data=report_html,
                    file_name=f"Incident_Report_{get_val('INCIDENT ID')}.html",
                    mime="text/html",
                    use_container_width=True
                )

            with colx2:

                st.components.v1.html(
                    """
                    <button onclick="window.print()"
                    style="
                        width:100%;
                        background:#1A5276;
                        color:white;
                        padding:12px;
                        border:none;
                        border-radius:6px;
                        font-size:16px;
                        cursor:pointer;
                    ">
                        🖨️ Print Report
                    </button>
                    """,
                    height=60
                )

        # =========================
        # OPEN MODAL BUTTON
        # =========================
        if st.button(
            "📄 Generate Report Preview",
            use_container_width=True
        ):
            show_report_modal()