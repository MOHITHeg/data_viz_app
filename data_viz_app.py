# data_viz_app.py

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# ------------------------------
# SECTION 1: PAGE SETUP & HEADER
# ------------------------------
st.set_page_config(page_title="DataViz Explorer", layout="wide")
st.title("📊 Data Visualization Explorer")
st.markdown("""
Welcome! Upload your dataset, pick any two columns, and explore it visually using different charts.
""")

# ------------------------------
# SECTION 2: DATA UPLOAD
# ------------------------------
@st.cache_data
def load_data(uploaded_file):
    try:
        df = pd.read_csv(uploaded_file)
        return df
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

df = None
if uploaded_file is not None:
    df = load_data(uploaded_file)

# ------------------------------
# SECTION 3: COLUMN SELECTION
# ------------------------------
if df is not None:
    st.subheader("Step 1: Select Columns to Visualize")
    columns = df.columns.tolist()

    col1, col2 = st.columns(2)
    with col1:
        x_col = st.selectbox("Select X-axis column", columns)
    with col2:
        y_col = st.selectbox("Select Y-axis column", columns, index=min(1, len(columns)-1))

    st.markdown("---")

    # ------------------------------
    # SECTION 4: VISUALIZATIONS
    # ------------------------------
    st.subheader("Step 2: Visualize the Relationship")

    chart_type = st.radio(
        "Choose a visualization type:",
        ["Scatter Plot", "Line Chart", "Bar Chart", "Box Plot", "Heatmap"],
        horizontal=True
    )

    fig = None

    try:
        if chart_type == "Scatter Plot":
            fig = px.scatter(df, x=x_col, y=y_col, title="Scatter Plot")

        elif chart_type == "Line Chart":
            fig = px.line(df, x=x_col, y=y_col, title="Line Chart")

        elif chart_type == "Bar Chart":
            fig = px.bar(df, x=x_col, y=y_col, title="Bar Chart")

        elif chart_type == "Box Plot":
            fig = px.box(df, x=x_col, y=y_col, title="Box Plot")

        elif chart_type == "Heatmap":
            corr = df[[x_col, y_col]].corr()
            plt.figure(figsize=(4, 3))
            sns.heatmap(corr, annot=True, cmap="coolwarm")
            st.pyplot(plt.gcf())

        if fig:
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Couldn't create chart: {e}")

else:
    st.info("Upload a dataset to get started.")