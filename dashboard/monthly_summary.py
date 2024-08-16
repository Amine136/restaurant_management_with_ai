import streamlit as st
import plotly.express as px
import pandas as pd


def soustraction(lst1, lst2):
    return [item for item in lst1 if item not in lst2]


def show(df):
    df = pd.DataFrame(df)
    df['detection_time'] = pd.to_datetime(df['detection_time'])

    # Step 1: Round detection_time to the nearest minute
    df['detection_time'] = df['detection_time'].dt.floor('T')

    # Step 2: Group by the new rounded detection_time and compute the max for each group
    grouped = df.groupby('detection_time').max().reset_index()

    # Step 3: Assign a new 'id' column
    grouped['id'] = range(1, len(grouped) + 1)

    # Rearrange columns to have 'id' first
    cols = ['id'] + [col for col in grouped.columns if col != 'id']
    result = grouped[cols]

    df = None
    df = result
    result = None
    df['date'] = df['detection_time'].dt.date  # Extract date without time

    # Define pizza types and their ingredients
    pizza_types = {
        'Pepperoni Pizza': {
            'obligatory': ['pepperoni'],
            'optional': ['basil', 'black_olives', 'tomatoes']
        },
        'Supreme Pizza': {
            'obligatory': ['pepperoni', 'mushrooms'],
            'optional': ['onions', 'peppers', 'black_olives']
        },
        'Vegetarian Pizza': {
            'obligatory': ['mushrooms', 'black_olives'],
            'optional': ['onions', 'peppers', 'tomatoes', 'basil']
        },
        'Margherita Pizza': {
            'obligatory': ['basil'],
            'optional': ['tomatoes']
        },
        'Neptune Pizza': {
            'obligatory': ['Neptune'],
            'optional': ['black_olives', 'onions', 'peppers', 'tomatoes']
        }
    }
    columns = ["pepperoni", "mushrooms", "onions", "peppers", "black_olives", "tomatoes", "basil", "Neptune"]

    # Initialize dictionary to store pizza counts per date
    pizza_counts_per_date = {}

    for i in range(df.shape[0]):
        t = None
        for Type, ingredients in pizza_types.items():
            ob = True
            dy = True
            obligatory = ingredients['obligatory']
            optional = ingredients['optional']
            deny = soustraction(columns, obligatory)
            deny = soustraction(deny, optional)

            # Check all obligatory ingredients
            for element in obligatory:
                if df.iloc[i][element] == 0:
                    ob = False
                    break

            # Check no unwanted ingredients
            for element in deny:
                if df.iloc[i][element] != 0:
                    dy = False
                    break

            if ob and dy:
                t = Type
                break  # Found a matching pizza type, exit the loop

        if t:
            date = df.iloc[i]['date']
            if date not in pizza_counts_per_date:
                pizza_counts_per_date[date] = {
                    'Pepperoni Pizza': 0,
                    'Supreme Pizza': 0,
                    'Vegetarian Pizza': 0,
                    'Margherita Pizza': 0,
                    'Neptune Pizza': 0
                }
            pizza_counts_per_date[date][t] += 1

    # Create the DataFrame from the accumulated counts
    pizza_summary = []
    for date, counts in pizza_counts_per_date.items():
        row = {'date': date}
        row.update(counts)
        pizza_summary.append(row)

    pizza_summary_df = pd.DataFrame(pizza_summary)

    # Add the 'id' column with consecutive numbers starting from 1
    pizza_summary_df.insert(0, 'id', range(1, len(pizza_summary_df) + 1))

    # Melt the DataFrame to long format for plotting
    plot_df = pizza_summary_df.melt(id_vars=['id', 'date'], var_name='Pizza', value_name='Count')

    # Plot the data
    fig = px.line(plot_df, x='date', y='Count', color='Pizza', markers=True, title='Pizza Counts Per Day in Current Month')
    st.plotly_chart(fig)
