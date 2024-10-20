import streamlit as st

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="centered",
    page_title="Specifications Drafter"
)
# endregion <--------- Streamlit App Configuration --------->

st.title("About this App")

st.write("This is a Specifications Drafter which is designed to help PMTs to come out with the first draft of the specifications for the purchase. We hope it will speed up the procurement process for you.")

with st.expander("Project Scope"):
    st.write("1. Enter your prompt in the text area.")

with st.expander("Project Objectives"):
    st.write("1. Enter your prompt in the text area.")   

with st.expander("Data Sources"):
    st.write("1. Enter your prompt in the text area.")

with st.expander("Features"):
    st.write("1. Enter your prompt in the text area.")
    st.write("2. Click the 'Submit' button.")
    st.write("3. The app will generate a the draft specfications based on your prompt.")
    st.write("4. It is that simple. Give it a try!")