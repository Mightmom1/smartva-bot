
import streamlit as st
from openai import OpenAI
import os
import gspread
from google.oauth2.service_account import Credentials

# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
client = OpenAI()

# Google Sheets integration
scope = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
client_gsheets = gspread.authorize(creds)
sheet = client_gsheets.open_by_url("https://docs.google.com/spreadsheets/d/1NGbGEQbj1XJVDpoXYxGMUgbnpCG40pe_2vmwm0dHueE/edit").sheet1

# Session state for storing leads
if "leads" not in st.session_state:
    st.session_state.leads = []

st.title("\U0001F3E1 SmartVA - Home Seller Assistant")
st.write("Hi there! I'm SmartVA. I'm here to help homeowners explore their options. Let's chat!")

name = st.text_input("What's your name?")
location = st.text_input("Where is your property located?")
selling_interest = st.radio("Are you considering selling your home soon?", ("Yes", "No", "Not Sure"))
email = st.text_input("What's your email (so we can follow up with helpful info)?")

if st.button("Submit"):
    if name and location and email:
        lead = {
            "name": name,
            "location": location,
            "interest": selling_interest,
            "email": email
        }
        st.session_state.leads.append(lead)
        sheet.append_row([lead["name"], lead["location"], lead["interest"], lead["email"]])
        st.success("Thanks, we'll be in touch soon!")
    else:
        st.warning("Please fill out all fields.")

st.write("\n---\n")

st.subheader("\U0001F4AC Ask SmartVA a Question")
user_input = st.text_input("Type your question here:")

if user_input:
    with st.spinner("Thinking..."):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You're a friendly virtual assistant helping homeowners explore selling their property."},
                {"role": "user", "content": user_input}
            ]
        )
        reply = response.choices[0].message.content
        st.write(f"**SmartVA:** {reply}")
