import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================
# PAGE CONFIG
# ==========================

st.set_page_config(
    page_title="Superstore Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

# ==========================
# LOAD DATA
# ==========================

@st.cache_data
def load_data():
    df = pd.read_csv("Superstore.csv")

    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Ship Date"] = pd.to_datetime(df["Ship Date"])

    return df


df = load_data()

# ==========================
# SIDEBAR
# ==========================

st.sidebar.title("🎛 Dashboard Filter")

region = st.sidebar.multiselect(
    "Region",
    sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

category = st.sidebar.multiselect(
    "Category",
    sorted(df["Category"].unique()),
    default=sorted(df["Category"].unique())
)

segment = st.sidebar.multiselect(
    "Segment",
    sorted(df["Segment"].unique()),
    default=sorted(df["Segment"].unique())
)

years = sorted(df["Order Date"].dt.year.unique())

year = st.sidebar.multiselect(
    "Year",
    years,
    default=years
)

filtered_df = df[
    (df["Region"].isin(region))
    &
    (df["Category"].isin(category))
    &
    (df["Segment"].isin(segment))
    &
    (df["Order Date"].dt.year.isin(year))
]

# ==========================
# HEADER
# ==========================

st.title("📊 Superstore Sales Dashboard")

st.markdown(
"""
Interactive Dashboard for Superstore Sales Analysis
"""
)

st.divider()

# ==========================
# KPI
# ==========================

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order ID"].nunique()
total_customers = filtered_df["Customer ID"].nunique()

c1,c2,c3,c4 = st.columns(4)

c1.metric(
    "💰 Total Sales",
    f"${total_sales:,.0f}"
)

c2.metric(
    "📈 Total Profit",
    f"${total_profit:,.0f}"
)

c3.metric(
    "📦 Total Orders",
    total_orders
)

c4.metric(
    "👥 Customers",
    total_customers
)

st.divider()

# ==========================
# MONTHLY SALES
# ==========================

monthly_sales = (
    filtered_df
    .groupby(filtered_df["Order Date"].dt.to_period("M"))
    ["Sales"]
    .sum()
    .reset_index()
)

monthly_sales["Order Date"] = monthly_sales["Order Date"].astype(str)

fig_month = px.line(
    monthly_sales,
    x="Order Date",
    y="Sales",
    markers=True,
    title="📈 Monthly Sales Trend"
)

st.plotly_chart(
    fig_month,
    use_container_width=True
)

st.divider()

# ==========================
# SALES CATEGORY
# ==========================

left,right = st.columns(2)

sales_category = (
    filtered_df
    .groupby("Category",as_index=False)["Sales"]
    .sum()
)

fig_sales_cat = px.bar(
    sales_category,
    x="Category",
    y="Sales",
    color="Category",
    title="Sales by Category",
    text_auto=".2s"
)

left.plotly_chart(
    fig_sales_cat,
    use_container_width=True
)

profit_category = (
    filtered_df
    .groupby("Category",as_index=False)["Profit"]
    .sum()
)

fig_profit_cat = px.bar(
    profit_category,
    x="Category",
    y="Profit",
    color="Category",
    title="Profit by Category",
    text_auto=".2s"
)

right.plotly_chart(
    fig_profit_cat,
    use_container_width=True
)

st.divider()

# ==========================
# REGION
# ==========================

left,right = st.columns(2)

sales_region = (
    filtered_df
    .groupby("Region",as_index=False)["Sales"]
    .sum()
)

fig_region = px.bar(
    sales_region,
    x="Region",
    y="Sales",
    color="Region",
    title="Sales by Region",
    text_auto=".2s"
)

left.plotly_chart(
    fig_region,
    use_container_width=True
)

# ==========================
# TOP PRODUCTS
# ==========================

top_products = (
    filtered_df
    .groupby("Product Name", as_index=False)["Sales"]
    .sum()
    .sort_values("Sales", ascending=False)
    .head(10)
)

fig_top = px.bar(
    top_products,
    x="Sales",
    y="Product Name",
    orientation="h",
    color="Sales",
    title="Top 10 Products by Sales",
    text_auto=".2s"
)

right.plotly_chart(
    fig_top,
    use_container_width=True
)

st.divider()

# ==========================
# SCATTER PLOTS
# ==========================

left, right = st.columns(2)

fig_sales_profit = px.scatter(
    filtered_df,
    x="Sales",
    y="Profit",
    color="Category",
    hover_name="Product Name",
    title="Sales vs Profit",
    opacity=0.7
)

left.plotly_chart(
    fig_sales_profit,
    use_container_width=True
)

fig_discount = px.scatter(
    filtered_df,
    x="Discount",
    y="Profit",
    color="Category",
    hover_name="Product Name",
    title="Discount vs Profit",
    opacity=0.7
)

right.plotly_chart(
    fig_discount,
    use_container_width=True
)

st.divider()

# ==========================
# DATA TABLE
# ==========================

st.subheader("📋 Transaction Data")

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=450
)

# ==========================
# DOWNLOAD CSV
# ==========================

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇ Download Filtered Data",
    data=csv,
    file_name="filtered_superstore.csv",
    mime="text/csv"
)

st.divider()

# ==========================
# FOOTER
# ==========================

st.caption(
    "Developed with ❤️ using Streamlit & Plotly | Superstore Sales Dashboard"
)