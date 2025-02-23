import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Set up our App
st.set_page_config(page_title="🧹 Data sweeper", page_icon="🧊", layout="wide")
st.title("🧹 Data sweeper")
st.write("This app allows you to clean your data by removing rows with missing values. You can also download the cleaned data as a CSV file.")

uploaded_file = st.file_uploader("Upload a CSV file (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_file:
    for file in uploaded_file:
        file_ext = os.path.splitext(file.name)[-1].lower()
        
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file format: {file_ext}")
            continue

        # Display info about the file
        st.write(f"**File name:** {file.name}")
        st.write(f"**File Size:** {file.size/1024:.2f} KB")
        
        # Show 5 rows of our df
        st.write("🔎 Preview the Head of the Dataframe")
        st.dataframe(df.head())
        
        # Options for data cleaning
        st.subheader("🛠️ Data Cleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("☑️ Duplicates Removed!")
                    
            with col2:
                if st.button(f"Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing Values Filled!")
           
        # Choose Specific Columns to keep or Convert 
        st.subheader("Select columns to Convert")   
        columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)   
        df = df[columns]
        
        # Create Some Visualizations
        st.subheader("📈 Data Visualizations")  
        if st.checkbox(f"Show Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])
            
        # Convert the File -> CSV to Excel
        st.subheader("🔁 Conversion Options")  
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv" 
                
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)
            
            # Download Button
            st.download_button(
                label=f"🔻 Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )
                    
st.success("🎉 All Files processed!")