import streamlit as st
import numpy as np
import os
import random
from itertools import chain, combinations
from menu import menu_dict

from grocery import tj_list
from grocery import costco_list
from grocery import vons_list
from grocery import hmart_list

from ingredients import proteins_list
from ingredients import meat_list
from ingredients import veggies_list
from ingredients import staple_list
from ingredients import sides_list

def main():
    st.title("Make a Dish! 🪄:sparkles:")
    st.markdown(''':rainbow[recipe generator for healthy food options]''')    

    ### INGREDIENT SELECTION
    st.header("What ingredients do you have?")
    # protein
    protein = st.multiselect(
        'protein 🍖',
        proteins_list
    )

    # veggies
    veggies = st.multiselect(
        'veggies :cucumber:',
        veggies_list
    )

    # staple
    staple = st.multiselect(
        'staple 🍚',
        staple_list
    )

    # tool
    tool = st.multiselect(
        'tool :cooking:',
        ['microwave', 'oven', 'air fryer', 'wok']
    )



    ### SIDEBAR 1 : FOOD STYLE SELECTION
    food_style = ["healthy", "still healthy"] 
    choice = st.sidebar.selectbox("What kind of food?", food_style)

    ## healthy
    if choice == 'healthy':
                
#### v1.0.1.231222_beta FIXED add multiple ingredients within same category!!! ####
        
#### v1.0.2.231224_beta FIXED suggest multiple recipe when there are matches!!! ####
        selected_ingredients = set(protein + veggies + staple + tool)

        # Check if the selected ingredients match any entry in menu_dict
        matched_dishes = [recipe for ingredients, recipe in menu_dict.items() if set(selected_ingredients).issuperset(set(ingredients))]

        if matched_dishes:
            st.subheader("Suggested Recipes:")
            for dish in matched_dishes:
                st.subheader(f"- {''.join(dish)}")
        else:
            st.text("No matching recipe found.")

        # missing ingredients
        selected_ingredients = list(set(sorted(protein + veggies + staple + tool))) # same but list
        missing_ingredients_counts = []

        for dish_ingredients, missing_count in missing_ingredients_counts:
            if missing_count > 0:
                st.text(f"{', '.join(dish_ingredients)}: {missing_count} missing ingredient(s)")


        # Ask the user if they want to add missing ingredients to make a dish
        if missing_ingredients_counts:
            add_ingredients = st.checkbox("Do you want to add missing ingredients to make a dish?")
            
            if add_ingredients:
                # Provide suggestions based on the menu
                suggested_dishes = [menu_dict[dish_ingredients] for dish_ingredients, count in missing_ingredients_counts if count <= 2]
            
                st.text(f"Suggested dishes with added ingredients: {', '.join(suggested_dishes)}")
            else:
                st.text("No specific recipe suggestion for the selected ingredients. Be creative!")

        else:
            st.text("No missing ingredients. You have all the ingredients for the dishes in the menu.")

    st.divider()



    ### SIDEBAR 2 : GROCERY SUGGESTION SELECTION

    ## select dish to get grocery list
    st.header("Check all you want to eat")
    
    selected_dishes = st.multiselect("Select dishes", list(menu_dict.values()))
    def grocery_suggestions(selected_dishes):
        grocery_list = set()
        for dish in selected_dishes:
            for ingredients, dish_name in menu_dict.items():
                if dish_name in selected_dishes:
                    grocery_list.update(ingredients)
        return grocery_list

    suggested_groceries = set()
    if selected_dishes:
        suggested_groceries = grocery_suggestions(selected_dishes)
        bold_groceries = [f'**{ingredient}**' for ingredient in suggested_groceries]
        st.markdown(f"Suggested Grocery List: {', '.join(bold_groceries)}")
    else:
        st.text("No dishes selected. Select dishes to get grocery suggestions.")


    ## select store to buy ingredients
    st.header("Which grocery store are you going to?")
    grocery_suggestion = ["Trader Joe", "Costco", "VONS", "H-Mart"] # 2 buttons
    choice2 = st.sidebar.selectbox("Grocery Suggestions", grocery_suggestion)

    if choice2 == 'Trader Joe':
        st.subheader(":red[Trader Joe]")
        st.markdown(''':rainbow[Yay my favorite!]''')

        # match suggested_groceries with tj_list 
        found_items = []
        for ingredient in suggested_groceries:
            for items in tj_list:
                if ingredient in items:
                    #found_items.append(''.join(items))
                    found_items.append('[' + ''.join(items) + ']')

        if found_items:
            st.text(f"You could find {', '.join(found_items)} in Trader Joe's!")
        else:
            st.text("Sorry, we couldn't find matching items in Trader Joe's.")


    elif choice2 == 'Costco':
        st.subheader(":red[Costco]")
        st.markdown(''':rainbow[A LOT]''')

        # match suggested_groceries with costco_list
        found_items = []
        for ingredient in suggested_groceries:
            for items in costco_list:
                if ingredient in items:
                    found_items.append(''.join(items))

        if found_items:
            st.text(f"You could find {', '.join(found_items)} in Costco!")
        else:
            st.text("Sorry, we couldn't find matching items in Costco.")

    elif choice2 == 'VONS':
        st.subheader(":red[VONS]")
        st.markdown(''':rainbow[Great deals!]''')

        found_items = []
        for ingredient in suggested_groceries:
            for items in vons_list:
                if ingredient in items:
                    found_items.append(''.join(items))

        if found_items:
            st.text(f"You could find {', '.join(found_items)} in VONS!")
        else:
            st.text("Sorry, we couldn't find matching items in VONS.")

    elif choice2 == 'H-Mart':
        st.subheader(":red[H-Mart]")
        st.markdown(''':rainbow[Asian fooood!]''')

        found_items = []
        for ingredient in suggested_groceries:
            for items in hmart_list:
                if ingredient in items:
                    found_items.append(''.join(items))

        if found_items:
            st.text(f"You could find {', '.join(found_items)} in H-Mart!")
        else:
            st.text("Sorry, we couldn't find matching items in H-Mart.")

    st.divider()

    ### SIDEBAR 3 : RANDOM PLATE GENERATOR
    st.header("Help me decide!")
    st.text("We got you, a randomly generated healthy plate after boop!")
    
    if st.button("boop!🪄", key="unique_key_for_boop"):
        pick1 = random.choice(meat_list)
        pick2 = random.sample(veggies_list, 2)
        pick3 = random.sample(sides_list, 2)
        plate = [pick1] + pick2 + pick3
        st.text(plate)



if __name__ == '__main__':
    main()