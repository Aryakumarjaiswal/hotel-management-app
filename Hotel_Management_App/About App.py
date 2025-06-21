import streamlit as st

# Set the title of the app
st.set_page_config(page_title="Welcome to Hotel Management App", page_icon="🏨", layout="centered")

# App title
st.title("🏨 Welcome to Hotel Management App")
st.subheader("Get the Information You Need – Fast and Easy")

# Description
st.write("Choose the right portal based on who you are:")

# Internal Users Section
st.header("🔒 Internal Users")
st.write("Are you part of our team? Access detailed insights, ask questions, and explore data within our system.")
st.write("**Features:**")
st.write("- Query hotel data effortlessly")
st.write("- Analyze commissions, guest details, and more")
#if st.button("Go to Internal Portal"):
#    st.success("Redirecting to Internal Users Portal...")
    # Add redirection or functionality here

# Separator
st.markdown("---")

# Registered Users Section
st.header("👤 Registered Users")
st.write("Are you a guest or customer? Check your booking details, explore room options, or manage your reservations.")
st.write("**Features:**")
st.write("- Access your booking information")
st.write("- Get details about your stay")
st.write("- Update or manage your reservation")

st.markdown("---")
st.write("🌟 Easy to use | 🌟 Accurate answers | 🌟 Tailored for your needs")
st.write("Start by selecting the right option above!")

