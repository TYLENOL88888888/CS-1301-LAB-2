# This creates the page for displaying data visualizations.
# It should read data from 'data.csv' to create graphs.

import streamlit as st
import pandas as pd
import os   # The 'os' module helps with file system operations.

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visualizations",
    page_icon="📈",
)

# PAGE TITLE AND INFORMATION
st.title("Phone Screen Time Visualizations 📈")
st.write("This page displays graphs based on the collected screen time data.")

# DATA LOADING
# A crucial step is to load the data from the files.
# It's important to add error handling to prevent the app from crashing if a file is empty or missing.

st.divider()
st.header("Load Data")

# 1. Load the data from 'data.csv' into a pandas DataFrame.
#    - Use a 'try-except' block or 'os.path.exists' to handle cases where the file doesn't exist.
try:
    df = pd.read_csv("data.csv")
    # Ensure columns are the correct type
    df["Satisfaction"] = pd.to_numeric(df["Satisfaction"], errors='coerce')
    df["Hours"] = pd.to_numeric(df["Hours"], errors='coerce')
    df["Day"] = df["Day"].astype(str).str.strip()  # Clean day column
    st.write("Data loaded from data.csv:", df.head())  # Debug output
except FileNotFoundError:
    df = pd.DataFrame(columns=["Day", "Hours", "Satisfaction"])
    st.warning("No survey data yet. Add some via the Survey page.")
    
st.info("Data loading complete.")

# GRAPH CREATION
# The lab requires you to create 3 graphs: one static and two dynamic.
# All graphs use data from 'data.csv'.

st.divider()
st.header("Graphs")

# GRAPH 1: STATIC GRAPH
st.subheader("Graph 1: Static - Average Hours per Day of the Week") 
# TO DO:
# - Create a static graph (e.g., bar chart, line chart) using st.bar_chart() or st.line_chart(). #NEW
# - Use data from the CSV file, showing all days even with no data.
if df.empty:
    st.write("No data to display for static graph.")
else:
    # Predefine all days and compute averages, filling missing days with 0
    all_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    avg_df = df.groupby("Day")["Hours"].mean().reindex(all_days, fill_value=0).reset_index()
    avg_df.columns = ["Day", "Hours"]  # Rename columns for clarity
    st.bar_chart(avg_df.set_index("Day")["Hours"]) #NEW
    # - Write a description explaining what the graph shows.
    st.write("This static graph displays the average screen time hours per day of the week from survey data, showing all days with zero hours where no data exists (non-interactive).")

# GRAPH 2: DYNAMIC GRAPH
st.subheader("Graph 2: Dynamic - Average Change in Satisfaction vs Hours") 
# TODO:
# - Create a dynamic graph showing average change in satisfaction compared to change in hours.
# - Use at least one interactive widget (e.g., st.slider, st.selectbox, st.multiselect).
# - Use Streamlit's Session State (st.session_state) to manage the interaction.
if "min_sat" not in st.session_state:
    st.session_state.min_sat = 1
if "day_filter" not in st.session_state:
    st.session_state.day_filter = "All"

# User interaction with st.slider #NEW
min_sat = st.slider("Minimum Satisfaction Level", min_value=1, max_value=10, value=st.session_state.min_sat)
st.session_state.min_sat = min_sat

# User interaction with st.selectbox #NEW
unique_days = ["All"] + sorted(df["Day"].unique().tolist())
day_filter = st.selectbox("Filter by Day", unique_days, index=unique_days.index(st.session_state.day_filter))
st.session_state.day_filter = day_filter

# Filter the DataFrame based on inputs using Streamlit's Session State.
filtered_df = df[df["Satisfaction"] >= min_sat].copy()  # Use .copy() to avoid SettingWithCopyWarning
st.write("Filter 1 (Satisfaction >=):", filtered_df)  # Debug: After satisfaction filter
if day_filter != "All":
    filtered_df = filtered_df[filtered_df["Day"] == day_filter]
st.write("Filter 2 (Day ==):", filtered_df)  # Debug: After day filter

if filtered_df.empty:
    st.warning("No data matches the filters. Adjust them or add more survey data.")
else:
    # Sort by day to compute changes
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    filtered_df = filtered_df.sort_values("Day", key=lambda x: pd.Categorical(x, categories=day_order, ordered=True))
    # Calculate changes between consecutive days
    filtered_df['Satisfaction_Change'] = filtered_df['Satisfaction'].diff()
    filtered_df['Hours_Change'] = filtered_df['Hours'].diff()
    # Average changes per day (handling NaN from first row)
    change_df = filtered_df.groupby("Day")[['Satisfaction_Change', 'Hours_Change']].mean().reindex(day_order, fill_value=0).reset_index()
    # Compute ratio or difference (using ratio for trend, avoiding division by zero)
    change_df['Change_Ratio'] = change_df['Satisfaction_Change'] / change_df['Hours_Change'].replace(0, pd.NA).fillna(0.001)  # Avoid division by zero
    st.write("Change data for plot:", change_df)  # Debug output
    st.line_chart(change_df.set_index("Day")["Change_Ratio"]) #NEW
    # - Add a '#NEW' comment next to at least 3 new Streamlit functions you use in this lab.
    # - Write a description explaining the graph and how to interact with it.
    st.write("This dynamic graph shows the average change in satisfaction per unit change in hours across days, filtered by a minimum satisfaction level (slider) and day (dropdown). All days are included, with zero changes where data is insufficient.")

# GRAPH 3: DYNAMIC GRAPH
st.subheader("Graph 3: Dynamic - Screen Time vs Satisfaction") 
# TO DO:
# - Create another dynamic graph.
# - This graph must show all data points from data.csv, updating as new data is added.
if not df.empty:  # Use full df instead of filtered_df
    st.scatter_chart(df, x="Hours", y="Satisfaction") #NEW
    st.write("Data points for plot:", df[["Hours", "Satisfaction"]])  # Debug: Show all points
    # - Remember to add a description and use '#NEW' comments.
    st.write("This dynamic graph plots all screen time hours against satisfaction levels from survey data, updating with every new entry in data.csv. It is not filtered by the widgets above.")
else:
    st.write("No data to display.")
