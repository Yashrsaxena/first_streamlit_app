#All the imports are here
import streamlit as st
import pandas as pd
import requests as req
import snowflake.connector
from urllib.error import URLError 

#Designing Starts from here
st.title('My Mom\'s New Healthy Diner')

st.header('Breakfast Favorites')
st.text('🥣 Omega 3 & Blueberry Oatmeal')
st.text('🥗 Kale, Spinach & Rocket Smoothie')
st.text('🐔 Hard-Boiled Free-Range Egg')
st.text('🥑🍞 Avocado Toast')

st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# import pandas as pd
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
st.dataframe(fruits_to_show)
# FRUITYVICE DATA ---------------------------------------------------------------------------------
st.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = st.text_input("What fruit would you like information about?")
  if not fruit_choice:
    st.error("Please enter any fruit")
  else:
    fruityvice_response = req.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    st.dataframe(fruityvice_normalized)

except URLErrora as e:
  st.error()

st.stop()

# import snowflake.connector - SNOWFLAKE DATA (FDC DATA) -------------------------------------------
my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
my_data_row = my_cur.fetchall()
st.header("THE FRUIT LOAD LIST CONTAINS:")
st.dataframe(my_data_row)

add_my_fruit = st.text_input("What fruit would you like to add?", "Jackfruit")
st.write("Thank you for adding " + add_my_fruit)
my_cur.execute("INSERT INTO FRUIT_LOAD_LIST VALUES (FROM_STREAMLIT)")
