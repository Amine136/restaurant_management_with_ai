import streamlit as st
from utils import get_engine, load_data, load_data_2
import daily_summary
import monthly_summary
import welcome_page
import employee_management


st.set_page_config(page_title="Stock Management Dashboard", layout="wide")

# Custom CSS for better styling
st.markdown("""
    <style>
    .stMetric {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px;
    }
    dl {
        margin: 0;
        padding: 0;
    }
    dt {
        font-size: 1.2em;
        font-weight: bold;
        margin-top: 10px;
    }
    dd {
        margin-left: 20px;
        font-size: 1.0em;
        color: black;
    }
    a {
        text-decoration: none;
        color: black;
    }
    a:hover {
        color: #007BFF;
    }
    .welcome-container {
        background-color: #F0F8FF;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    .welcome-title {
        font-size: 2em;
        font-weight: bold;
        color: #FF69B4;
    }
    .welcome-message {
        font-size: 1.2em;
        color: #8A2BE2;
        margin-top: 10px;
    }
    .welcome-image {
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Welcome")

# Sidebar for navigation
st.sidebar.markdown("""
<dl>
  <dt><a href="?page=welcome">Home</a></dt>
  <dt><a href="?page=employee_management">Employee Management</a></dt>
  <dt>Pizza Detection</dt>
  <dd><a href="?page=daily_summary">Daily Summary</a></dd>
  <dd><a href="?page=monthly_summary">Type Pizza Summary</a></dd> 
</dl>
""", unsafe_allow_html=True)

# Extract the page parameter from the URL
query_params = st.experimental_get_query_params()
page = query_params.get('page', ['welcome'])[0]

# Load data
engine = get_engine()
df = load_data(engine)

df_2 = load_data_2(engine)

# Route to the appropriate page
if page == "daily_summary":
    daily_summary.show(df)
elif page == "monthly_summary":
    monthly_summary.show(df)
elif page == "employee_management":
    employee_management.show(df_2)  # Placeholder for employee management content
else:
    #st.write("Welcome Page")  # Placeholder for welcome content
    welcome_page.show_welcome_page()
#st.write("Note: Data is grouped by minute and the maximum count for each ingredient is taken for that minute.")
