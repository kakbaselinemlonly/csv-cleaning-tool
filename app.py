import streamlit as st
import pandas as pd

#Backend
#Cleaning data:
#report section is for further detail design

#Drop duplicates
def clean_duplicates(data0):
  data = data0.copy()
  print(f"Before cleaning duplicates: {len(data)}")
  cleanedD = data.drop_duplicates()
  print(f"After cleaning duplicates: {len(cleanedD)}")

  return cleanedD

#Drop missing values/nulls (dropna)
def clean_nulls(data0,method="drop"):
  data = data0.copy()
  print(f"Before cleaning missing values: {len(data)}")

  if method == "drop":
    cleanedN = data.dropna()
    print(f"After cleaning missing values: {len(cleanedN)}")
    #action = "Drop all rows with any missing value"
  elif method == "fill0":
    cleanedN = data.fillna(0)
    print(f"After cleaning missing values: {len(cleanedN)}")
    #action = "Fill any missing value with '0'"
  elif method == "fillNA":
    cleanedN = data.fillna("N/A")
    print(f"After cleaning missing values: {len(cleanedN)}")
    #action = "Fill any missing value with 'N/A'"
  else:
    cleanedN = data
    #action = "No missing value cleaning applied"

  return cleanedN

#Further cleaning of column names
def clean_columns(data0):
  data = data0.copy()
  data.columns = (data.columns.str.strip().str.lower().str.replace(" ","_",regex=False).str.replace(r"[,\.\{\}\[\]\!\?\@\#\$\%\^]", "", regex=True))
  print(f"Finished cleaning column names.")

  return data

#Overall function (for frontend to use)
def run_cleaning(data, clean_dup=True, clean_null=True, clean_column=True, method="drop"):
  cleaned_df = data.copy()


  if clean_dup == True:
    cleaned_df = clean_duplicates(cleaned_df)
    print(f"Dataset shape after cleaning: {cleaned_df.shape}")
  if clean_null == True:
    cleaned_df = clean_nulls(cleaned_df, method=method)
    print(f"Dataset shape after cleaning: {cleaned_df.shape}")
  if clean_column == True:
    cleaned_df = clean_columns(cleaned_df)
    print(f"Dataset shape after cleaning: {cleaned_df.shape}")


  return cleaned_df


#Frontend
st.title("CSV format Dataset Cleaning Tool")
st.write("Upload your CSV file for Basic Data Cleaning.")

uploaded = st.file_uploader("Upload CSV file here", type=("csv")) 

if uploaded is not None:
    df = pd.read_csv(uploaded)
    subheader = ("Original Dataset")
    st.dataframe(df.head(10)) #first 10 rows

    st.write("Original dataset shape: ", df.shape)
    st.write("Number of duplicates: ", df.duplicated().sum())
    st.write("Number of missing values: ", df.isnull().sum().sum())

    subheader = ("Data Cleaning Options")

    dup = st.checkbox("Clean up the duplicates")
    miss = st.checkbox("Clean up missing values")

    method = "drop"
    if miss:
        method=st.selectbox("Choose how you gonna handle missing values: ", ["drop","fill0","fillNA"])
    
    col = st.checkbox("Trim the column names")

    if st.button("Run Cleaning"):
      cleaned_df = run_cleaning(df, clean_dup=dup, clean_null=miss, clean_column=col,method=method)

      st.subheader("Cleaned Dataset Preview")
      st.dataframe(cleaned_df.head(10)) #first 10 rows
      st.write("Cleaned dataset shape: ", cleaned_df.shape)
      st.write("Number of duplicates after cleaning: ", cleaned_df.duplicated().sum())
      st.write("Number of missing values after cleaning: ", cleaned_df.isnull().sum().sum())
      
      #download cleaned csv
      csv = cleaned_df.to_csv(index=False).encode("utf-8")

      st.download_button(label="Download the Cleaned CSV Dataset File", 
                         data=csv, 
                         file_name="cleaned_dataset.csv",
                         mime="text/csv")
    

