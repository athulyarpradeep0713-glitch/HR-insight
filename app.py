
import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import date

st.set_page_config(
    page_title="HR Insight",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp { background: #f4f8ff; }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0b5ed7 0%, #1976d2 55%, #2589df 100%);
    }
    [data-testid="stSidebar"] * { color: white !important; }
    [data-testid="stSidebar"] [data-testid="stRadio"] label {
        padding: 7px 10px;
        border-radius: 9px;
    }
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
    .hero {
        background: linear-gradient(110deg, #0b5ed7, #2589df);
        padding: 22px 25px;
        border-radius: 16px;
        color: white;
        margin-bottom: 18px;
    }
    .hero h1 { color: white; margin: 0; }
    .hero p { color: #eaf4ff; margin: 6px 0 0 0; }
    .kpi {
        background: white;
        border: 1px solid #d8e8fb;
        border-radius: 14px;
        padding: 17px 18px;
        min-height: 112px;
        box-shadow: 0 3px 12px rgba(25, 90, 160, .05);
    }
    .kpi-label { color: #62758b; font-size: 13px; margin-bottom: 8px; }
    .kpi-value { color: #1458a6; font-size: 27px; font-weight: 750; }
    .section-title {
        color: #174f91;
        font-size: 19px;
        font-weight: 700;
        margin: 8px 0 12px;
    }
    div.stButton > button, div.stDownloadButton > button {
        border-radius: 9px;
        border: 1px solid #b9d8fb;
    }
    div.stButton > button[kind="primary"] {
        background: #1265c8;
        color: white;
        border: 0;
    }
    [data-testid="stDataFrame"] {
        border: 1px solid #c7def7;
        border-radius: 10px;
    }
    .login-wrap {
        max-width: 540px;
        margin: 45px auto;
        background: white;
        border: 1px solid #d7e7fa;
        border-radius: 18px;
        padding: 32px;
        box-shadow: 0 10px 35px rgba(20, 75, 140, .10);
    }
    .muted { color: #62758b; font-size: 13px; }
</style>
""", unsafe_allow_html=True)

DEFAULT_ROWS = [
    {
        "Employee_ID": 1001, "Name": "Aarav", "Department": "HR",
        "Job_Role": "HR Executive", "Gender": "Male", "Age": 28,
        "Salary": 45000, "Joining_Date": "2023-02-15", "Status": "Active"
    },
    {
        "Employee_ID": 1002, "Name": "Diya", "Department": "IT",
        "Job_Role": "Developer", "Gender": "Female", "Age": 26,
        "Salary": 65000, "Joining_Date": "2022-07-10", "Status": "Active"
    },
    {
        "Employee_ID": 1003, "Name": "Rohan", "Department": "Finance",
        "Job_Role": "Analyst", "Gender": "Male", "Age": 30,
        "Salary": 58000, "Joining_Date": "2021-11-20", "Status": "Active"
    },
    {
        "Employee_ID": 1004, "Name": "Meera", "Department": "IT",
        "Job_Role": "Tester", "Gender": "Female", "Age": 27,
        "Salary": 62000, "Joining_Date": "2023-05-08", "Status": "Active"
    },
    {
        "Employee_ID": 1005, "Name": "Kavin", "Department": "Marketing",
        "Job_Role": "Marketing Executive", "Gender": "Male", "Age": 29,
        "Salary": 48000, "Joining_Date": "2024-01-12", "Status": "Active"
    }
]

COLUMNS = [
    "Employee_ID", "Name", "Department", "Job_Role", "Gender",
    "Age", "Salary", "Joining_Date", "Status"
]

if "employees" not in st.session_state:
    st.session_state.employees = pd.DataFrame(DEFAULT_ROWS, columns=COLUMNS)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "notifications" not in st.session_state:
    st.session_state.notifications = True

if "theme" not in st.session_state:
    st.session_state.theme = "Blue"

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"


def format_salary(value):
    return f"₹{float(value):,.0f}"


def header(title, subtitle=""):
    st.markdown(
        f'<div class="hero"><h1>{title}</h1><p>{subtitle}</p></div>',
        unsafe_allow_html=True
    )


def kpi(label, value):
    st.markdown(
        f'<div class="kpi"><div class="kpi-label">{label}</div>'
        f'<div class="kpi-value">{value}</div></div>',
        unsafe_allow_html=True
    )


def get_data():
    return st.session_state.employees.copy()


def set_data(df):
    st.session_state.employees = df[COLUMNS].copy().reset_index(drop=True)


def csv_bytes(df):
    return df.to_csv(index=False).encode("utf-8")


def excel_bytes(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="HR Report")
    return output.getvalue()


if not st.session_state.logged_in:
    st.markdown('<div class="login-wrap">', unsafe_allow_html=True)
    st.markdown("## 👥 HR Insight")
    st.markdown("A simple employee management and analytics dashboard.")

    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Enter username")
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter password"
        )
        submitted = st.form_submit_button(
            "Sign in",
            type="primary",
            use_container_width=True
        )

    if submitted:
        if username == "hrman" and password == "hrman123":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Incorrect username or password. Please try again.")

    st.markdown(
        '<p class="muted">Demo login: username <b>hrman</b> · '
        'password <b>hrman123</b></p>',
        unsafe_allow_html=True
    )
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()


with st.sidebar:
    st.markdown("# HR INSIGHT")
    st.caption("PEOPLE MANAGEMENT")

    pages = [
        "Dashboard", "Employees", "Add Employee", "Departments",
        "Job Roles", "Search", "Analytics", "Reports", "Settings"
    ]

    page = st.radio(
        "NAVIGATION",
        pages,
        index=pages.index(st.session_state.page)
        if st.session_state.page in pages else 0
    )

    st.session_state.page = page
    st.divider()
    st.markdown("**Admin account**")
    st.caption("HR Manager")

    if st.button("Log out", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()


df = get_data()
departments = sorted(df["Department"].dropna().astype(str).unique().tolist())
roles = sorted(df["Job_Role"].dropna().astype(str).unique().tolist())


if page == "Dashboard":
    header("HR Insight Dashboard", "A clear overview of your employee data.")

    df = get_data()
    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        kpi("TOTAL EMPLOYEES", f"{len(df)}")
    with c2:
        kpi("DEPARTMENTS", f"{df['Department'].nunique()}")
    with c3:
        kpi("JOB ROLES", f"{df['Job_Role'].nunique()}")
    with c4:
        kpi(
            "AVERAGE SALARY",
            format_salary(df["Salary"].mean()) if len(df) else "₹0"
        )
    with c5:
        kpi(
            "TOTAL SALARY",
            format_salary(df["Salary"].sum()) if len(df) else "₹0"
        )

    st.write("")
    left, right = st.columns(2)

    with left:
        st.markdown(
            '<div class="section-title">Employees by Department</div>',
            unsafe_allow_html=True
        )
        if len(df):
            st.bar_chart(
                df.groupby("Department")["Employee_ID"]
                .count().sort_values(ascending=False)
            )
        else:
            st.info("Add employees to see department data.")

    with right:
        st.markdown(
            '<div class="section-title">Salary by Employee</div>',
            unsafe_allow_html=True
        )
        if len(df):
            chart_df = df.set_index("Name")[["Salary"]]
            st.bar_chart(chart_df)
        else:
            st.info("Add employees to see salary data.")

    st.markdown(
        '<div class="section-title">Recent Employee Records</div>',
        unsafe_allow_html=True
    )

    if len(df):
        recent = df.copy()
        recent["Joining_Date"] = pd.to_datetime(
            recent["Joining_Date"], errors="coerce"
        )
        st.dataframe(
            recent.sort_values("Joining_Date", ascending=False).head(5),
            use_container_width=True,
            hide_index=True
        )


elif page == "Employees":
    header("Employees", "View, edit, and remove employee records.")
    df = get_data()

    if df.empty:
        st.info("No employee records yet. Use Add Employee to create one.")
    else:
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.markdown(
            '<div class="section-title">Edit or delete an employee</div>',
            unsafe_allow_html=True
        )

        ids = df["Employee_ID"].astype(int).tolist()
        selected_id = st.selectbox("Choose Employee ID", ids)
        row = df[df["Employee_ID"] == selected_id].iloc[0]

        with st.form("edit_employee_form"):
            a, b = st.columns(2)

            name = a.text_input("Name", str(row["Name"]))
            department = b.text_input("Department", str(row["Department"]))
            role = a.text_input("Job role", str(row["Job_Role"]))

            gender_options = ["Female", "Male", "Other"]
            current_gender = (
                gender_options.index(row["Gender"])
                if row["Gender"] in gender_options else 0
            )
            gender = b.selectbox(
                "Gender", gender_options, index=current_gender
            )

            age = a.number_input(
                "Age", min_value=18, max_value=100, value=int(row["Age"])
            )
            salary = b.number_input(
                "Salary (₹)", min_value=0,
                value=int(row["Salary"]), step=1000
            )

            try:
                join_date = pd.to_datetime(row["Joining_Date"]).date()
            except Exception:
                join_date = date.today()

            joining = a.date_input("Joining date", value=join_date)
            status_options = ["Active", "Inactive"]
            current_status = (
                0 if row["Status"] == "Active" else 1
            )
            status = b.selectbox(
                "Status", status_options, index=current_status
            )

            save = st.form_submit_button("Save changes", type="primary")

        if save:
            df.loc[df["Employee_ID"] == selected_id, COLUMNS] = [
                selected_id, name.strip(), department.strip(), role.strip(),
                gender, int(age), int(salary), str(joining), status
            ]
            set_data(df)
            st.success("Employee updated.")
            st.rerun()

        if st.button("Delete selected employee", type="secondary"):
            set_data(df[df["Employee_ID"] != selected_id])
            st.success("Employee deleted.")
            st.rerun()

    st.download_button(
        "Download employee CSV",
        csv_bytes(get_data()),
        "employees.csv",
        "text/csv"
    )


elif page == "Add Employee":
    header("Add Employee", "Enter employee details and save the new record.")

    with st.form("add_employee_form", clear_on_submit=True):
        a, b = st.columns(2)

        name = a.text_input("Full name *")
        department = b.text_input("Department *")
        role = a.text_input("Job role *")
        gender = b.selectbox("Gender", ["Female", "Male", "Other"])
        age = a.number_input("Age", min_value=18, max_value=100, value=22)
        salary = b.number_input(
            "Salary (₹)", min_value=0, value=25000, step=1000
        )
        joining = a.date_input("Joining date", value=date.today())
        status = b.selectbox("Status", ["Active", "Inactive"])

        submitted = st.form_submit_button("Save Employee", type="primary")

    if submitted:
        if not name.strip() or not department.strip() or not role.strip():
            st.error("Please fill in the name, department, and job role.")
        else:
            current = get_data()
            next_id = (
                int(current["Employee_ID"].max()) + 1
                if len(current) else 1001
            )

            new_row = {
                "Employee_ID": next_id,
                "Name": name.strip(),
                "Department": department.strip(),
                "Job_Role": role.strip(),
                "Gender": gender,
                "Age": int(age),
                "Salary": int(salary),
                "Joining_Date": str(joining),
                "Status": status
            }

            set_data(
                pd.concat(
                    [current, pd.DataFrame([new_row])],
                    ignore_index=True
                )
            )
            st.success(f"Employee added successfully. Employee ID: {next_id}")
            st.rerun()


elif page == "Departments":
    header("Departments", "Explore your team distribution.")
    df = get_data()

    if df.empty:
        st.info("No department data available yet.")
    else:
        summary = df.groupby("Department").agg(
            Employees=("Employee_ID", "count"),
            Average_Salary=("Salary", "mean"),
            Total_Salary=("Salary", "sum")
        ).reset_index()

        summary["Average_Salary"] = summary["Average_Salary"].round(2)
        st.bar_chart(summary.set_index("Department")[["Employees"]])
        st.dataframe(summary, use_container_width=True, hide_index=True)

    with st.expander("Add a department"):
        new_department = st.text_input("Department name", key="new_department")

        if st.button("Add department"):
            if new_department.strip() and new_department.strip() not in departments:
                st.info(
                    "Department created. It will appear in employee records "
                    "when assigned to an employee."
                )
            elif new_department.strip() in departments:
                st.warning("That department already exists.")
            else:
                st.error("Enter a department name.")


elif page == "Job Roles":
    header("Job Roles", "See roles and the number of employees in each.")
    df = get_data()

    if df.empty:
        st.info("No job role data available yet.")
    else:
        summary = df.groupby("Job_Role").agg(
            Employees=("Employee_ID", "count"),
            Average_Salary=("Salary", "mean")
        ).reset_index().rename(columns={"Job_Role": "Job Role"})

        summary["Average_Salary"] = summary["Average_Salary"].round(2)
        st.bar_chart(summary.set_index("Job Role")[["Employees"]])
        st.dataframe(summary, use_container_width=True, hide_index=True)


elif page == "Search":
    header("Search & Filters", "Find employees using keywords and filters.")
    df = get_data()

    query = st.text_input("Search by name, ID, department, or job role")
    a, b, c = st.columns(3)

    dep_options = ["All"] + sorted(
        df["Department"].dropna().astype(str).unique().tolist()
    )
    role_options = ["All"] + sorted(
        df["Job_Role"].dropna().astype(str).unique().tolist()
    )
    status_options = ["All"] + sorted(
        df["Status"].dropna().astype(str).unique().tolist()
    )

    dep_filter = a.selectbox("Department", dep_options)
    role_filter = b.selectbox("Job role", role_options)
    status_filter = c.selectbox("Status", status_options)

    filtered = df.copy()

    if query.strip():
        mask = filtered[COLUMNS].astype(str).apply(
            lambda col: col.str.contains(
                query.strip(), case=False, na=False
            )
        ).any(axis=1)
        filtered = filtered[mask]

    if dep_filter != "All":
        filtered = filtered[filtered["Department"] == dep_filter]
    if role_filter != "All":
        filtered = filtered[filtered["Job_Role"] == role_filter]
    if status_filter != "All":
        filtered = filtered[filtered["Status"] == status_filter]

    st.caption(f"{len(filtered)} matching employee(s)")
    st.dataframe(filtered, use_container_width=True, hide_index=True)

    st.download_button(
        "Download search results",
        csv_bytes(filtered),
        "search_results.csv",
        "text/csv"
    )


elif page == "Analytics":
    header("HR Analytics", "Explore workforce, salary, and hiring patterns.")
    df = get_data()

    if df.empty:
        st.info("Add employees to see analytics.")
    else:
        a, b = st.columns(2)

        with a:
            st.markdown(
                '<div class="section-title">Department Distribution</div>',
                unsafe_allow_html=True
            )
            st.bar_chart(df.groupby("Department")["Employee_ID"].count())

        with b:
            st.markdown(
                '<div class="section-title">Average Salary by Department</div>',
                unsafe_allow_html=True
            )
            st.bar_chart(df.groupby("Department")["Salary"].mean())

        st.markdown(
            '<div class="section-title">Employees by Job Role</div>',
            unsafe_allow_html=True
        )
        st.bar_chart(df.groupby("Job_Role")["Employee_ID"].count())

        salary_stats = pd.DataFrame({
            "Metric": [
                "Average salary", "Highest salary",
                "Lowest salary", "Total salary expense"
            ],
            "Value (₹)": [
                round(df["Salary"].mean(), 2),
                int(df["Salary"].max()),
                int(df["Salary"].min()),
                int(df["Salary"].sum())
            ]
        })

        st.dataframe(
            salary_stats,
            use_container_width=True,
            hide_index=True
        )


elif page == "Reports":
    header("Reports", "Filter employee data and export reports.")
    df = get_data()

    a, b = st.columns(2)
    report_type = a.selectbox(
        "Report type",
        [
            "All employees", "Salary report",
            "Department report", "Inactive employees"
        ]
    )

    dep_options = ["All"] + sorted(
        df["Department"].dropna().astype(str).unique().tolist()
    )
    dep_filter = b.selectbox("Department filter", dep_options)

    report = df.copy()

    if dep_filter != "All":
        report = report[report["Department"] == dep_filter]

    if report_type == "Salary report":
        report = report[
            [
                "Employee_ID", "Name", "Department",
                "Job_Role", "Salary", "Status"
            ]
        ].sort_values("Salary", ascending=False)

    elif report_type == "Department report":
        report = report.groupby("Department").agg(
            Employee_Count=("Employee_ID", "count"),
            Average_Salary=("Salary", "mean"),
            Total_Salary=("Salary", "sum")
        ).reset_index()

    elif report_type == "Inactive employees":
        report = report[report["Status"] == "Inactive"]

    st.markdown(
        '<div class="section-title">Report Preview</div>',
        unsafe_allow_html=True
    )
    st.dataframe(report, use_container_width=True, hide_index=True)

    x, y = st.columns(2)

    with x:
        st.download_button(
            "Export CSV",
            csv_bytes(report),
            "hr_report.csv",
            "text/csv",
            use_container_width=True
        )

    with y:
        try:
            st.download_button(
                "Export Excel",
                excel_bytes(report),
                "hr_report.xlsx",
                "application/vnd.openxmlformats-officedocument."
                "spreadsheetml.sheet",
                use_container_width=True
            )
        except Exception:
            st.info(
                "Install openpyxl to enable Excel export: "
                "pip install openpyxl"
            )


elif page == "Settings":
    header("Settings", "Manage your preferences and application data.")

    st.markdown(
        '<div class="section-title">Admin Profile</div>',
        unsafe_allow_html=True
    )
    st.write("**Role:** HR Manager")
    st.write("**Username:** hrman")
    st.write("**Application:** HR Insight")

    st.divider()

    st.markdown(
        '<div class="section-title">Preferences</div>',
        unsafe_allow_html=True
    )

    theme = st.selectbox(
        "Dashboard theme",
        ["Blue", "Light"],
        index=0 if st.session_state.theme == "Blue" else 1
    )
    notifications = st.toggle(
        "Enable notifications",
        value=st.session_state.notifications
    )

    if st.button("Save settings", type="primary"):
        st.session_state.theme = theme
        st.session_state.notifications = notifications
        st.success("Settings saved.")

    st.divider()

    st.markdown(
        '<div class="section-title">Data Management</div>',
        unsafe_allow_html=True
    )
    st.caption(
        "Resetting restores the five sample employee records and removes "
        "changes made during this session."
    )

    confirm_reset = st.checkbox(
        "I understand that resetting will discard my current changes."
    )

    if st.button("Reset sample data", disabled=not confirm_reset):
        st.session_state.employees = pd.DataFrame(
            DEFAULT_ROWS, columns=COLUMNS
        )
        st.success("Sample data restored.")
        st.rerun()

    st.download_button(
        "Back up employee data (CSV)",
        csv_bytes(get_data()),
        "hr_insight_backup.csv",
        "text/csv"
    )
