import streamlit as st
import plotly.express as px
import pandas as pd
def show(df):
    st.subheader("Stock Summary")

    # Initial stock quantities at the beginning of the day
    initial_stock = {
        'pepperoni': 1000,
        'mushrooms': 500,
        'onions': 300,
        'peppers': 200,
        'black_olives': 400,
        'tomatoes': 600,
        'basil': 150
    }

   
    # Group by minute and take the maximum count for each ingredient
    df['minute'] = df['detection_time'].dt.floor('T')
    grouped_df = df.groupby('minute').max().reset_index()

    # Calculate total detections for each ingredient
    #total_detections = grouped_df[['pepperoni', 'mushrooms', 'onions', 'peppers', 'black_olives', 'tomatoes', 'basil']].sum()

 #Group by day 
    today = pd.to_datetime('today').normalize()
    today_df = grouped_df[grouped_df['detection_time'].dt.normalize() == today]

    # Sum the detections for each ingredient for today
    total_detections = today_df[['pepperoni', 'mushrooms', 'onions', 'peppers', 'black_olives', 'tomatoes', 'basil']].sum()



    # Calculate remaining stock and percentage
    remaining_stock = initial_stock.copy()
    for ingredient, initial in initial_stock.items():
        remaining_stock[ingredient] = initial - total_detections[ingredient]

    # Calculate percentage remaining
    percentage_remaining = {}
    for ingredient, initial in initial_stock.items():
        if initial == 0:
            percentage_remaining[ingredient] = 0
        else:
            percentage_remaining[ingredient] = (remaining_stock[ingredient] / initial) * 100

    tabs = st.tabs([ingredient.capitalize() for ingredient in initial_stock.keys()])
    for i, ingredient in enumerate(initial_stock.keys()):
        with tabs[i]:
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Total Detected", value=int(total_detections[ingredient]), delta=f"{total_detections[ingredient]} units")
            with col2:
                st.metric(label="Remaining Stock", value=f"{percentage_remaining[ingredient]:.2f} %")

    st.subheader("Ingredient Usage Over Time")
    fig = px.line(
        grouped_df,
        x='minute',
        y=['pepperoni', 'mushrooms', 'onions', 'peppers', 'black_olives', 'tomatoes', 'basil'],
        markers=True,
        #title='Ingredient Usage Over Time'
    )
    st.plotly_chart(fig)