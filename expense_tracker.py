import streamlit as st
import pandas as pd
import datetime
import io #in memory buffer created to create a fake file

st.title("Personal Expense Tracker")

if "df" not in st.session_state: #prevents the table from resetting every time the app reruns.
    st.session_state.df = pd.DataFrame(columns=["Date", "Category", "Description", "Amount"])

st.subheader("Add a new expense")
with st.form("entry_form"):
    date = st.date_input("Date", datetime.date.today())
    ##st.write("Formatted Date:", date.strftime("%d-%m-%Y"))
    category = st.selectbox("Category", ["Select","Food", "Travel", "Shopping", "Health", "Other"])
    description = st.text_input("Description")
    amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    submitted = st.form_submit_button("Add Expense")
    
    if submitted:
        if category == "Select":
            st.warning("Please select a valid category before submitting.")
        if amount == 0.0:
            st.warning("Please select a valid amount before submitting.")
        if description == "":
            st.warning("Please select a valid description before submitting.")
        else:
            new_data = {"Date": date, "Category": category, "Description": description, "Amount": amount}
            st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([new_data])], ignore_index=True)
            st.success("Expense added!")
        
st.subheader("📋 All Expenses")
st.write(st.session_state.df)

st.subheader("📊 Summary")
if not st.session_state.df.empty: #Avoid showing summary/chart if no data, Avoid offering a download button if the table is empty
    total = st.session_state.df["Amount"].sum()
    by_category = st.session_state.df.groupby("Category")["Amount"].sum()
    st.write(f"**Total Spent:** ₹ {total:.2f}")
    st.bar_chart(by_category)
    
st.subheader("⬇️ Download as Excel")
@st.cache_data #speeds things up by caching the result
def convert_df_to_excel(df): #
    output = io.BytesIO() #io.BytesIO()=Creates a fake file in memory
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False) #to_excel()=writes the DataFrame to the in-memory file
    return output.getvalue() #returns the byte content of that Excel file, ready to be downloaded

if not st.session_state.df.empty:
    excel_data = convert_df_to_excel(st.session_state.df)
    st.download_button(
         "Download Excel File",
         data=excel_data,
         file_name="expenses.xlsx",
         mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    
    