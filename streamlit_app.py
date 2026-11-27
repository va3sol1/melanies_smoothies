# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f"Customize your smoothie :cup_with_straw:")
st.write(
  """Choose the fruits you want"""
)

cnx = st.connection("snowflake")
session = cnx.session()

name_on_order = st.text_input("your name:")
st.write("The name on your smoothie will be: ", name_on_order)

my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients",
    my_dataframe,
    max_selections=5
)
if ingredients_list:

    ingredients_string = ""
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + " "


    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                    values ('""" + ingredients_string + """', '""" + name_on_order + """')"""
    time_to_insert = st.button("Submit order")
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
