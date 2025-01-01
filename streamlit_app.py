import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# Function to load and process the data
@st.cache
def load_data():
    # Load the dataset
    data = pd.read_csv("Dataset/preprocessed_eclog_dataset.csv")
    # Ensure timestamp column is properly formatted
    data['TimeStamp'] = pd.to_datetime(data['TimeStamp'], format='%Y-%m-%d %H:%M:%S.%f')
    return data

# Load data
data = load_data()

# Sidebar Filters
st.sidebar.title("Filters")

# Date range filter (restrict range as per requirements)
min_date = datetime(2019, 12, 1)
max_date = datetime(2020, 5, 29)
date_range = st.sidebar.date_input(
    "Select Date Range",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# Time range filter
time_range = st.sidebar.slider("Select Time Range (24H Format)", 0, 23, (0, 23))

# Country filter
all_countries = data['CountryCode'].unique()
country_counts = data['CountryCode'].value_counts()
selected_countries = st.sidebar.multiselect(
    "Select Country for Detailed Analysis",
    options=country_counts.index.tolist(),
    default=country_counts.index[:4].tolist()  # Limit default selection to the first 4 countries
)

# Logarithmic scale toggle
log_scale = st.sidebar.checkbox("Logarithmic Scale")

# Graph selection
graph_options = st.sidebar.multiselect(
    "Select Graphs to Display",
    options=["Traffic Overview", "Time-Based Analysis", "Country Analysis", "Referrer and URI Analysis", "Device, Browser, and OS Analysis"],
    default=[]
)

# Add a Run button
if st.sidebar.button("Run"):
    # Apply filters only when Run is clicked
    selected_countries = selected_countries if selected_countries else country_counts.index[:4].tolist()  # Ensure a default selection if empty
    filtered_data = data[
        (data['TimeStamp'].dt.date >= date_range[0]) &
        (data['TimeStamp'].dt.date <= date_range[1]) &
        (data['TimeStamp'].dt.hour >= time_range[0]) &
        (data['TimeStamp'].dt.hour <= time_range[1]) &
        (data['CountryCode'].isin(selected_countries))
    ]

    # Display graphs based on selection
    if "Traffic Overview" in graph_options:
        st.header("Traffic Overview")
        http_methods = filtered_data['HttpMethod'].value_counts()
        if log_scale:
            http_methods = np.log1p(http_methods)

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x=http_methods.index, y=http_methods.values, ax=ax, palette="viridis")
        for i, v in enumerate(http_methods.values):
            ax.text(i, v + 0.05, f"{v:.2f}" if log_scale else f"{int(v)}", ha='center')
        ax.set_title("HTTP Method Distribution")
        ax.set_ylabel("Count (Log Scale)" if log_scale else "Count")
        ax.set_xlabel("HTTP Method")
        st.pyplot(fig)

    if "Time-Based Analysis" in graph_options:
        st.header("Time-Based Analysis")
        time_trends = filtered_data.groupby(filtered_data['TimeStamp'].dt.date).size()
        if log_scale:
            time_trends = np.log1p(time_trends)

        fig, ax = plt.subplots(figsize=(10, 6))
        time_trends.plot(ax=ax)
        ax.set_title("Requests Over Time")
        ax.set_ylabel("Count (Log Scale)" if log_scale else "Count")
        ax.set_xlabel("Date")
        ax.grid(True)
        st.pyplot(fig)

    if "Country Analysis" in graph_options:
        st.header("Country Analysis")
        country_counts = filtered_data['CountryCode'].value_counts()
        if log_scale:
            country_counts = np.log1p(country_counts)

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x=country_counts.index, y=country_counts.values, ax=ax, palette="plasma")
        for i, v in enumerate(country_counts.values):
            ax.text(i, v + 0.05, f"{v:.2f}" if log_scale else f"{int(v)}", ha='center')
        ax.set_title("Requests by Country")
        ax.set_ylabel("Count (Log Scale)" if log_scale else "Count")
        ax.set_xlabel("Country Code")
        st.pyplot(fig)

        # Show detailed analysis for each selected country
        for country in selected_countries:
            country_data = filtered_data[filtered_data['CountryCode'] == country]

            # URI Type Analysis
            st.subheader(f"URI Type Analysis for {country}")
            uri_counts = country_data['URI_Type'].value_counts()
            if log_scale:
                uri_counts = np.log1p(uri_counts)

            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x=uri_counts.index, y=uri_counts.values, ax=ax, palette="coolwarm")
            for i, v in enumerate(uri_counts.values):
                ax.text(i, v + 0.05, f"{v:.2f}" if log_scale else f"{int(v)}", ha='center')
            ax.set_title(f"URI Types for {country}")
            ax.set_ylabel("Count (Log Scale)" if log_scale else "Count")
            ax.set_xlabel("URI Type")
            st.pyplot(fig)

            # Referrer Type Analysis
            st.subheader(f"Referrer Type Analysis for {country}")
            referrer_counts = country_data['Referrer_Type'].value_counts()
            if log_scale:
                referrer_counts = np.log1p(referrer_counts)

            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x=referrer_counts.index, y=referrer_counts.values, ax=ax, palette="rocket")
            for i, v in enumerate(referrer_counts.values):
                ax.text(i, v + 0.05, f"{v:.2f}" if log_scale else f"{int(v)}", ha='center')
            ax.set_title(f"Referrer Types for {country}")
            ax.set_ylabel("Count (Log Scale)" if log_scale else "Count")
            ax.set_xlabel("Referrer Type")
            st.pyplot(fig)

            # Device Analysis
            st.subheader(f"Device Type Analysis for {country}")
            device_counts = country_data['Device_Type'].value_counts()
            if log_scale:
                device_counts = np.log1p(device_counts)

            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x=device_counts.index, y=device_counts.values, ax=ax, palette="viridis")
            for i, v in enumerate(device_counts.values):
                ax.text(i, v + 0.05, f"{v:.2f}" if log_scale else f"{int(v)}", ha='center')
            ax.set_title(f"Device Types for {country}")
            ax.set_ylabel("Count (Log Scale)" if log_scale else "Count")
            ax.set_xlabel("Device Type")
            st.pyplot(fig)

            # Browser Analysis
            st.subheader(f"Browser Analysis for {country}")
            browser_counts = country_data['Browser'].value_counts()
            if log_scale:
                browser_counts = np.log1p(browser_counts)

            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x=browser_counts.index, y=browser_counts.values, ax=ax, palette="plasma")
            for i, v in enumerate(browser_counts.values):
                ax.text(i, v + 0.05, f"{v:.2f}" if log_scale else f"{int(v)}", ha='center')
            ax.set_title(f"Browser Distribution for {country}")
            ax.set_ylabel("Count (Log Scale)" if log_scale else "Count")
            ax.set_xlabel("Browser")
            st.pyplot(fig)

            # OS Analysis
            st.subheader(f"OS Analysis for {country}")
            os_counts = country_data['OS'].value_counts()
            if log_scale:
                os_counts = np.log1p(os_counts)

            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x=os_counts.index, y=os_counts.values, ax=ax, palette="coolwarm")
            for i, v in enumerate(os_counts.values):
                ax.text(i, v + 0.05, f"{v:.2f}" if log_scale else f"{int(v)}", ha='center')
            ax.set_title(f"OS Distribution for {country}")
            ax.set_ylabel("Count (Log Scale)" if log_scale else "Count")
            ax.set_xlabel("Operating System")
            st.pyplot(fig)
