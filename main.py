import streamlit as st
import pandas as pd
import plotly.express as px
import pytz

def find_columns_with_most_255(df):
    # Count occurrences of 255 for each Byte column
    counts = {col: (df[col] == 255).sum() for col in df.columns if col.startswith('Byte')}
    
    # Sort columns by counts and return the two columns with the most occurrences
    sorted_columns = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    return [col[0] for col in sorted_columns[:2]]

# Set up the Streamlit app
st.title("Blood Volume Pulse Signal")

# File uploader
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the CSV file
    df = pd.read_csv(uploaded_file)

    # Optionally display the data preview
    # st.write("Data Preview:")
    # st.dataframe(df.head())

    # Find columns with the most occurrences of 255
    max_columns = find_columns_with_most_255(df)

    if len(max_columns) < 2:
        st.warning("Check file. Not enough valid Byte columns found.")
    else:
        # Extract the numerical part of the column names
        index1 = int(max_columns[0][4:])  # Extracts the number from "ByteX"
        index2 = int(max_columns[1][4:])  # Extracts the number from "ByteY"

        # Calculate the new Byte column indices
        new_index1 = (index1 + 4) % 9
        new_index2 = (index2 + 4) % 9

        # Determine which Byte column has the larger number
        larger_byte_index = max(new_index1, new_index2)
        byte_column_to_plot = f"Byte{larger_byte_index}"

        # Check if the selected column exists
        if byte_column_to_plot in df.columns:
            if 'Timestamp' in df.columns:
                # Convert the epoch timestamp to datetime in IST
                df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='s').dt.tz_localize('UTC').dt.tz_convert('Asia/Kolkata')

                # Plot the data
                fig = px.line(df, x='Timestamp', y=byte_column_to_plot, title='Blood Volume Pulse over Timestamp (IST)')
                st.plotly_chart(fig)
                st.write(f"Using {byte_column_to_plot} from the CSV for plotting.")
            else:
                st.warning("Timestamp column is missing from the dataset.")
        else:
            st.warning(f"{byte_column_to_plot} column is missing in the dataset.")

# Add some instructions
st.write("""
## Instructions:
1. Upload a CSV file containing epoch timestamps and Byte columns.
2. The application will automatically identify the appropriate Byte column and plot the Blood Volume Pulse signal over time.
""")
