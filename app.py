
import streamlit as st
import pandas as pd
import plotly.express as px

from salary_calculator import calculate_salary

# Page configuration
st.set_page_config(
    page_title="Paymetrics",
    page_icon="💰",
    layout="wide"
)

# Custom styling
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
}

[data-testid="stMetric"] {
    border: 1px solid #64748b55;
    padding: 20px;
    border-radius: 12px;
}

.stDownloadButton button {
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# Application title
st.title("💰 Paymetrics")
st.caption("Employee Compensation & Salary Analytics")

st.divider()

# Sidebar
with st.sidebar:

    st.header("Employee Details")

    company_name = st.text_input(
        "Company Name",
        placeholder="Enter company name"
    )

    employee_name = st.text_input(
        "Employee Name",
        placeholder="Enter employee name"
    )

    department = st.selectbox(
        "Department",
        [
            "IT",
            "HR",
            "Finance",
            "Marketing",
            "Operations",
            "Data Analytics"
        ]
    )

    experience = st.number_input(
        "Years of Experience",
        min_value=0,
        max_value=50,
        value=1
    )

    basic_salary = st.number_input(
        "Monthly Basic Salary (₹)",
        min_value=0,
        value=30000,
        step=1000
    )

    st.subheader("Salary Components")

    hra_percent = st.slider(
        "HRA (%)", 0, 50, 20
    )

    bonus_percent = st.slider(
        "Bonus (%)", 0, 50, 10
    )

    deduction_percent = st.slider(
        "Deductions (%)", 0, 50, 5
    )

# Calculate salary
result = calculate_salary(
    basic_salary,
    hra_percent,
    bonus_percent,
    deduction_percent
)

# Employee overview
st.subheader("Employee Overview")
st.write(
    f"**Company:** {company_name or 'Not entered'}"
)

st.write(
    f"**Employee:** {employee_name or 'Not entered'}"
)

st.write(
    f"**Department:** {department} | "
    f"**Experience:** {experience} years"
)

# KPI metrics
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Gross Salary",
    f"₹{result['Gross Salary']:,.2f}"
)

col2.metric(
    "Deductions",
    f"₹{result['Deductions']:,.2f}"
)

col3.metric(
    "Net Salary",
    f"₹{result['Net Salary']:,.2f}"
)

col4.metric(
    "Annual Take-home",
    f"₹{result['Annual Salary']:,.2f}"
)

st.divider()

# Salary component dataframe
salary_df = pd.DataFrame({
    "Component": [
        "Basic Salary",
        "HRA",
        "Bonus"
    ],
    "Amount": [
        result["Basic Salary"],
        result["HRA"],
        result["Bonus"]
    ]
})

# Charts
chart1, chart2 = st.columns(2)

with chart1:

    st.subheader("Salary Composition")

    fig = px.pie(
        salary_df,
        names="Component",
        values="Amount",
        hole=0.55,
        color_discrete_sequence=[
            "#2563EB",
            "#14B8A6",
            "#F59E0B"
        ]
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with chart2:

    st.subheader("Salary Comparison")

    comparison_df = pd.DataFrame({
        "Category": [
            "Gross Salary",
            "Deductions",
            "Net Salary"
        ],
        "Amount": [
            result["Gross Salary"],
            result["Deductions"],
            result["Net Salary"]
        ]
    })

    fig2 = px.bar(
        comparison_df,
        x="Category",
        y="Amount",
        color="Category",
        text_auto=".2s"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

st.divider()

# Salary report
st.subheader("Detailed Salary Report")

report_df = pd.DataFrame(
    list(result.items()),
    columns=["Salary Component", "Amount (INR)"]
)

st.dataframe(
    report_df,
    use_container_width=True,
    hide_index=True
)

# Downloadable report
export_df = report_df.copy()

export_df.insert(0, "Company", company_name)

export_df.insert(
    0, "Employee", employee_name
)

export_df.insert(
    1, "Department", department
)

csv = export_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="📥 Download Salary Report",
    data=csv,
    file_name="salary_report.csv",
    mime="text/csv"
)

st.divider()

st.caption(
    "SalaryIQ | Developed using Python, "
    "Pandas, Plotly and Streamlit"
)
