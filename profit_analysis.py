import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Profit Analysis",
    layout="wide"
)

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("data/sales.xls")

    df.columns = df.columns.str.strip()

    if "Order Date" in df.columns:
        df["Order Date"] = pd.to_datetime(
            df["Order Date"],
            errors="coerce"
        )

        df["Year"] = df["Order Date"].dt.year
        df["Month"] = df["Order Date"].dt.month_name()

    return df

df = load_data()

# -----------------------------
# Title
# -----------------------------
st.title("Profit Analysis Dashboard")

# -----------------------------
# KPI Cards
# -----------------------------
st.subheader("Profit KPIs")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    total_profit = df["Profit"].sum()
    st.metric("Total Profit", f"{total_profit:,.2f}")

with kpi2:
    avg_profit = df["Profit"].mean()
    st.metric("Average Profit", f"{avg_profit:,.2f}")

with kpi3:
    max_profit = df["Profit"].max()
    st.metric("Maximum Profit", f"{max_profit:,.2f}")

with kpi4:
    min_profit = df["Profit"].min()
    st.metric("Minimum Profit", f"{min_profit:,.2f}")

# -----------------------------
# Profit by Category
# -----------------------------
st.subheader("Profit by Category")

category_profit = df.groupby(
    "Category",
    as_index=False
)["Profit"].sum()

fig1 = px.bar(
    category_profit,
    x="Category",
    y="Profit",
    text_auto=True,
    title="Profit by Category",
    color="Category",
    color_discrete_sequence=["red", "blue", "green"]
)

st.plotly_chart(fig1, use_container_width=True)

# -----------------------------
# Monthly Profit Trend
# -----------------------------
st.subheader("Monthly Profit Trend")

monthly_profit = df.groupby(
    df["Order Date"].dt.to_period("M")
)["Profit"].sum().reset_index()

monthly_profit["Order Date"] = monthly_profit[
    "Order Date"
].astype(str)

fig2 = px.line(
    monthly_profit,
    x="Order Date",
    y="Profit",
    markers=True,
    title="Monthly Profit Trend",
    color_discrete_sequence=["red"]
)

st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# Yearly Profit Analysis
# -----------------------------
st.subheader("Yearly Profit Analysis")

yearly_profit = df.groupby(
    "Year",
    as_index=False
)["Profit"].sum()

fig3 = px.bar(
    yearly_profit,
    x="Year",
    y="Profit",
    text_auto=True,
    title="Yearly Profit",
    color_discrete_sequence=["red", "blue", "green"]
)

st.plotly_chart(fig3, use_container_width=True)

# -----------------------------
# Monthly Profit by Month Name
# -----------------------------
st.subheader("Monthly Profit")

month_order = [
    "January", "February", "March",
    "April", "May", "June",
    "July", "August", "September",
    "October", "November", "December"
]

monthly_name_profit = df.groupby(
    "Month",
    as_index=False
)["Profit"].sum()

monthly_name_profit["Month"] = pd.Categorical(
    monthly_name_profit["Month"],
    categories=month_order,
    ordered=True
)

monthly_name_profit = monthly_name_profit.sort_values(
    "Month"
)

fig4 = px.bar(
    monthly_name_profit,
    x="Month",
    y="Profit",
    text_auto=True,
    title="Monthly Profit"
)

st.plotly_chart(fig4, use_container_width=True)