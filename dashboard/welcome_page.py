import streamlit as st

def show_welcome_page():
    st.markdown("""
    <div class="welcome-container">
        <div class="welcome-title">Welcome to the Restaurant Management Dashboard!</div>
        <div class="welcome-message">
            We're excited to have you here. Explore our various sections to manage your stock efficiently.
            Use the navigation menu on the left to get started.
        </div>
        <div class="welcome-image">
            <img src="https://robbreport.com/wp-content/uploads/2022/06/Pizzeria_Bianco_dining_room.jpg?w=1000" alt="Cute Welcome Image" width="300">
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Add additional CSS for the welcome page if needed
    st.markdown("""
    <style>
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
