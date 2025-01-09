import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from sklearn.linear_model import LinearRegression
import numpy as np
import plotly.express as px
import requests

# Page Configuration
st.set_page_config(page_title="Health Awareness Dashboard", layout="wide")

# Title
st.title("Enhanced Health Awareness Dashboard")

# Sidebar Filters
st.sidebar.header("Upload or Fetch Data")

# Option to Upload CSV File
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")

# Option to Fetch Real-Time Data
fetch_data = st.sidebar.button("Fetch WHO Real-Time Data")

if fetch_data:
    def fetch_who_data():
        url = "https://ghoapi.azureedge.net/api/Indicator"  # Example WHO API endpoint
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return pd.json_normalize(data["value"])  # Adjust based on API structure
        else:
            st.error("Failed to fetch data from WHO API.")
            return None

    data = fetch_who_data()
else:
    if uploaded_file:
        data = pd.read_csv(uploaded_file)
    else:
        data = None

if data is not None:
    st.write("### Dataset Preview")
    st.dataframe(data.head())

    # Sidebar Options
    st.sidebar.header("Options")
    analysis_type = st.sidebar.selectbox(
        "Select Analysis Type",
        ["Overview", "Visualization", "Comparative Analysis", "Predictions", "Geospatial Mapping"]
    )

    if analysis_type == "Overview":
        st.subheader("Dataset Overview")
        st.write("Shape of the dataset:", data.shape)
        st.write("Columns in the dataset:", data.columns.tolist())
        st.write(data.describe())

    elif analysis_type == "Visualization":
        st.subheader("Data Visualization")

        # Metric Selection
        metric = st.selectbox("Select a metric to visualize", data.columns[2:])

        # Plot Bar Chart
        st.write(f"### {metric} Across All Countries")
        fig = px.bar(data, x="Year", y=metric, title=f"{metric} Over Time Across All Countries")
        st.plotly_chart(fig)

    elif analysis_type == "Comparative Analysis":
        st.subheader("Comparative Analysis")

        # Select Countries and Metric
        countries = st.multiselect("Select countries to compare", data["Country"].unique())
        metric = st.selectbox("Select a metric", data.columns[2:])

        # Plot Comparison
        if countries:
            comparison_data = data[data["Country"].isin(countries)]
            fig = px.line(
                comparison_data,
                x="Year",
                y=metric,
                color="Country",
                title=f"Comparison of {metric} Across Selected Countries"
            )
            st.plotly_chart(fig)

    elif analysis_type == "Predictions":
        st.subheader("Predict Future Trends")

        # Metric Selection
        metric = st.selectbox("Select a metric for prediction", data.columns[2:])

        # Prepare Data for Prediction
        X = data["Year"].values.reshape(-1, 1)
        y = data[metric].values

        # Train Linear Regression Model
        model = LinearRegression()
        model.fit(X, y)

        # Predict for Future Years
        future_years = np.arange(X[-1, 0] + 1, X[-1, 0] + 6).reshape(-1, 1)
        predictions = model.predict(future_years)

        # Display Predictions
        prediction_df = pd.DataFrame({
            "Year": future_years.flatten(),
            "Predicted": predictions
        })
        st.write("### Predicted Values for Entire Dataset")
        st.dataframe(prediction_df)

        # Plot Predictions
        fig = px.line(
            prediction_df,
            x="Year",
            y="Predicted",
            title=f"Predicted {metric} for All Countries"
        )
        st.plotly_chart(fig)

    elif analysis_type == "Geospatial Mapping":
        st.subheader("Geospatial Mapping")

        # Example dataset for mapping
        st.write("Mapping Health Metrics Globally")
        if "Latitude" in data.columns and "Longitude" in data.columns:
            fig = px.scatter_geo(
                data,
                lat="Latitude",
                lon="Longitude",
                size="HealthMetric",  # Ensure the relevant column is used here for global health metrics
                color="HealthMetric",  # Adjust according to the metric you want to map
                hover_name="Country",
                title="Global Health Metrics",
                projection="natural earth"
            )
            st.plotly_chart(fig)
        else:
            st.error("The dataset does not contain 'Latitude' and 'Longitude' columns for mapping.")

else:
    st.write("Please upload a dataset or fetch real-time data to proceed.")

# Footer
st.sidebar.markdown("### Powered by Streamlit")
