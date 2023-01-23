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
# FUNCTION FOR FRUITYVICE DATA FETCHING
def data_from_fruityvice(this_fruit_choice):
  fruityvice_response = req.get("https://fruityvice.com/api/fruit/" + fruit_choice)
  fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
  return fruityvice_normalized
st.header("Fruityvice Fruit Advice!")

# TRY AND EXCEPT 
try:
  fruit_choice = st.text_input("What fruit would you like information about?")
  if not fruit_choice:
    st.error("Please select a fruit to get information")
  else:
    from_function = data_from_fruityvice(fruit_choice)
    st.dataframe(from_function)

except URLError as e:
  st.error()

# import snowflake.connector - SNOWFLAKE DATA (FDC DATA) -------------------------------------------
st.header("View Our Fruit List - Add Your Favorites!")
#sNOWFLAKE-RELATED FUNCTIONS
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
    return my_cur.fetchall()

#BUTTON THAT LOADS THE DATA BY CALLING THE ABOVE FUNCTION
if st.button('Get Fruit List'):
  my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
  my_data_row = get_fruit_load_list()
  my_cnx.close()
  st.dataframe(my_data_row)
 

def insert_row_snowflake(new_fruit):
  my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into fruit_load_list values('"+new_fruit+"')")
    my_cnx.close()
    return "Thank you for adding " + new_fruit

add_my_fruit = st.text_input("What fruit would you like to add?")
try:
  if not add_my_fruit:
    st.error("No fruit to Add")
  else:
    st.write(insert_row_snowflake(add_my_fruit))

except URLError as e:
  st.error()
st.stop()
