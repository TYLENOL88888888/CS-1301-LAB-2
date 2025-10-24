# This creates the page for users to input data.
# The collected data should be appended to the 'data.csv' file.

import streamlit as st
import pandas as pd
import os # The 'os' module is used for file system operations (e.g. checking if a file exists).

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Survey",
    page_icon="📝",
)

# PAGE TITLE AND USER DIRECTIONS
st.title("Phone Screen Time Survey")
st.write("Enter your screen time data for a specific day. You can and you SHOULD submit multiple times for different days for cool features and the best outcome of the data.")

# DATA INPUT FORM
# 'st.form' creates a container that groups input widgets.
# The form is submitted only when the user clicks the 'st.form_submit_button'.
# This is useful for preventing the app from re-running every time a widget is changed.
with st.form("survey_form"):
    # Create text input widgets for the user to enter data.
    # The first argument is the label that appears above the input box.
    day = st.selectbox("Day of the week", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
    hours = st.number_input("Screen time hours that day", min_value=0.0, max_value=24.0, step=0.5)
    sat = st.number_input("Satisfaction level with usage (1-10)", min_value=1, max_value=10, step=1)

    # The submit button for the form.
    submitted = st.form_submit_button("Submit Data")

    # This block of code runs ONLY when the submit button is clicked.
    if submitted:
        # --- YOUR LOGIC GOES HERE ---
        # TO DO:
        # 1. Create a new row of data from 'day', 'hours', and 'sat' (corrected from category_input/value_input).
        new_data = {"Day": [day], "Hours": [hours], "Satisfaction": [sat]}
        new_df = pd.DataFrame(new_data)
        st.write("New data to save:", new_df)  # Debug: Show data before saving
        # 2. Append this new row to the 'data.csv' file.
        #    - You can use pandas or Python's built-in 'csv' module.
        #    - Make sure to open the file in 'append' mode ('a').
        #    - Don't forget to add a newline character '\n' at the end.
        try:
            existing_df = pd.read_csv("data.csv")
            updated_df = pd.concat([existing_df, new_df], ignore_index=True)
        except (FileNotFoundError, pd.errors.EmptyDataError):
            updated_df = new_df
        
        updated_df.to_csv("data.csv", index=False)
        st.success("Your data has been submitted!")
        st.write(f"You entered: **Day:** {day}, **Hours:** {hours}, **Satisfaction:** {sat}")

# DATA DISPLAY
# This section shows the current contents of the CSV file, which helps in debugging.
st.divider() # Adds a horizontal line for visual separation.
st.header("Current Data in CSV")

# Check if the CSV file exists and is not empty before trying to read it.
if os.path.exists('data.csv') and os.path.getsize('data.csv') > 0:
    # Read the CSV file into a pandas DataFrame, handling empty data errors.
    try:
        current_data_df = pd.read_csv('data.csv')
        # Display the DataFrame as a table.
        st.dataframe(current_data_df)
    except pd.errors.EmptyDataError:
        st.warning("The 'data.csv' file exists but is empty or contains no valid data.")
else:
    st.warning("The 'data.csv' file is empty or does not exist yet.")
