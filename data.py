import pandas as pd
import streamlit as st

# Load your DataFrame (assuming it's from a CSV or other source)
data = pd.read_csv('path_to_your_file.csv')

# Check the column names
print(data.columns)

# Your further logic...
