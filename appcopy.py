import streamlit as st

# Initialize "page" in session state to "Home" if not already set
if "page" not in st.session_state:
    st.session_state["page"] = "Home"  # This ensures Home is the default page

# Create layout with two buttons (Home and Reference)
col2, col3 = st.columns([1, 1])

# Button for "Home" page
with col2:
    if st.button("Home"):
        st.session_state["page"] = "Home"  # Set to Home when clicked

# Button for "Reference" page
with col3:
    if st.button("Reference"):
        st.session_state["page"] = "Reference"  # Set to Reference when clicked

# Display the content based on the selected page
if st.session_state["page"] == "Home":
    st.write("You are on the Home page")
elif st.session_state["page"] == "Reference":
    st.write("You are on the Reference page")
