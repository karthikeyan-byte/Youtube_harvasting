 
import pandas as pd 
import streamlit as st 
import sqlite3


conn= sqlite3.connect("Youtube.db")
query = """ 
        SELECT channel_title,AVG(duration) FROM Youtube  GROUP BY channel_title
        """
df=pd.read_sql_query(query, conn)
print(df)