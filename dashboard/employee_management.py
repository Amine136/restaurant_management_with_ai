import streamlit as st
import pandas as pd
import json
from datetime import datetime, timedelta

# Load the timetable data from JSON
def load_timetable(json_path):
    with open(json_path, 'r') as f:
        timetable = json.load(f)
    return timetable

# Function to calculate the time at work and retard for each employee
def calculate_work_metrics(df, timetable):
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['date'] = df['timestamp'].dt.date
    
    work_metrics = {}
    for employee in timetable.keys():
        employee_df = df[df['name'] == employee].sort_values(by='timestamp')
        employee_metrics = []

        grouped = employee_df.groupby('date')
        for date, group in grouped:
            day_name = date.strftime('%A').lower()
            expected_start_time = timetable[employee].get(day_name, None)
            if not expected_start_time:
                continue

            if len(expected_start_time) > 0:
                expected_start_time = datetime.strptime(expected_start_time[0], '%H:%M').time()
                actual_start_time = group[group['event_type'] == 'enters'].iloc[0]['timestamp'].time()
                actual_exit_time = group[group['event_type'] == 'exit'].iloc[-1]['timestamp'].time()

                retard = datetime.combine(datetime.today(), actual_start_time) - datetime.combine(datetime.today(), expected_start_time)
                time_at_work = datetime.combine(datetime.today(), actual_exit_time) - datetime.combine(datetime.today(), actual_start_time)
                
                if retard < timedelta(0):
                    retard = timedelta(0)

                employee_metrics.append({
                    'day': date,
                    'retard': str(retard),
                    'time_at_work': str(time_at_work)
                })

        work_metrics[employee] = employee_metrics
    
    return work_metrics

# Dictionary of employee images
employee_images = {
    "Elon Musk": r"https://cdn.britannica.com/05/236505-050-17B6E34A/Elon-Musk-2022.jpg",
    "Mark zuckerberg": r"https://upload.wikimedia.org/wikipedia/commons/thumb/7/71/Mark_Zuckerberg_2019_%28cropped%29.jpg/800px-Mark_Zuckerberg_2019_%28cropped%29.jpg",
    "Jeff Bezoz": r"https://cdn.futura-sciences.com/sources/images/Jeff%20bezos.jpg"
}

# Show the employee management page
def show(df):
    timetable_path = '../pc_face_reco/timetable/timetable.json'
    timetable = load_timetable(timetable_path)
    
    st.title("Employee Management")

    # Create tabs for each employee
    tabs = st.tabs([employee for employee in timetable.keys()])
    
    # Calculate work metrics
    work_metrics = calculate_work_metrics(df, timetable)
    
    # Iterate over each tab and display the work schedule
    for i, (employee, schedule) in enumerate(timetable.items()):
        with tabs[i]:
            st.header(f"Work Schedule for {employee}")
            col1, col2 = st.columns([3, 1])
            with col1:
                for day, hours in schedule.items():
                    if hours:
                        st.write(f"**{day.capitalize()}:** {hours[0]} - {hours[1]}")
                    else:
                        st.write(f"**{day.capitalize()}:** Off")

                # Display the work metrics
                st.subheader("Daily Work Metrics")
                if employee in work_metrics:
                    metrics_df = pd.DataFrame(work_metrics[employee])
                    st.dataframe(metrics_df)
                else:
                    st.write("No work metrics available.")

            with col2:
                if employee in employee_images:
                    st.image(employee_images[employee], use_column_width=True)
                else:
                    st.write("No image available.")
