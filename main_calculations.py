import math
import pandas as pd


def greet_user():
    print("Welcome to the Azenco Sales Quote Generation ChatBot!")
    print("Please select a product from the list below:")
    products = ["1. R-Blade", "2. R-Shade", "3. Privacy Walls"]
    for product in products:
        print(product)
    selected_product = input("Enter the number of the product you'd like to select: ")
    return selected_product

def get_size():
    print("Please enter the size of the configuration (Width x Length in feet).")
    print("Always list Width First!")
    size = input("Enter size (e.g., 15'x13'): ")
    return size

def calculate_bays(size, product):
    width, length = [int(s.strip("'")) for s in size.split('x')]
    print(width, length)
    # Simplified logic for demonstration
    if product == "1":  # R-Blade logic
        if length<=23:
            bay_length=length
            if 8 <= int(width) <= 15:
                no_bays = 1
                bay_width = (width / no_bays)
                return 1, bay_width,bay_length  # Single bay
            elif 15 < int(width) <= 30:
                no_bays = 2
                bay_width = (width / no_bays)
                return no_bays, bay_width,bay_length
            elif 30 < int(width) <= 45:
                no_bays = 3
                bay_width = (width / no_bays)
                return no_bays, bay_width,bay_length
            else:
                return 0
        else:
            return "lenght can not be bigger then 23"

    elif product == "2":  # R-Shade logic
        if length<=23:
            bay_length=length
            if 8 <= int(width) <= 23:
                no_bays = 1
                bay_width = (width / no_bays)
                return 1, bay_width,bay_length  # Single bay
            elif 23 < int(width) <= 46:
                no_bays = 2
                bay_width = (width / no_bays)
                return no_bays, bay_width,bay_length
            elif 46 < int(width) <= 69:
                no_bays = 3
                bay_width = (width / no_bays)
                return no_bays, bay_width,bay_length
            else:
                return 0
    else:
        return 0


def cal_price(product,no_bays,width,length):
    width=math.ceil(width)
    print(width,"sssssssss",str(length)+"'",str(width)+"'")
    if product=='1':
        pType='R-Blade'
    elif product=='2':
        pType = 'R-Shade'
    else:
        return 0
    jsonfile = pd.read_json('/home/tech/PycharmProjects/azenco/static/Pricing.json')
    for onee in jsonfile['Pricing']:
        if onee['Width'] == str(width)+"'" and onee['Length'] == str(length)+"'" and onee['Type'] == pType:
            print(onee['Price'],"iiiiiiii")
            baseprice=float(onee['Price'].replace("$",'').replace(',',''))
            return baseprice*no_bays


def ask_structure_type():
    print("What type of structure is needed?")
    options = ["1. Freestanding", "2. Attached 1 Side", "3. Footings"]
    for option in options:
        print(option)
    selected_option = input("Select an option: ")
    return selected_option

def calculate_posts(size=None, structure_type=None):
    width, length = [int(s.strip("'")) for s in size.split('x')]
    if structure_type == "1":  # Freestanding
        if width <= 23:
            return 4
        elif width <= 45:
            return 6
        else:
            return 8

    elif structure_type == "2":  # Attached 1 Side
        if width <= 23:
            return 2
        elif width <= 45:
            return 3
        else:
            return 4

    elif structure_type == "3":  # Footings
        if width <= 23:
            return 4
        elif width <= 45:
            return 6
        else:
            return 8
    else:
        return 0



def main_price_cal(selected_product=None,size=None):
    # print("Please select a product from the list below:")
    # products = ["1. R-Blade", "2. R-Shade", "3. Privacy Walls"]
    # for product in products:
    #     print(product)
    selected_product = selected_product

    # print("Please enter the size of the configuration (Width x Length in feet).")
    # print("Always list Width First!")
    size =size

    bays, bay_width,bay_length = calculate_bays(size, selected_product)
    print(f"Number of Bays based on the dimensions: {bays}")
    print(f"Width of single Bay based on the dimensions: {bay_width}")

    price=cal_price(selected_product, bays, bay_width, bay_length)
    print(f"Price for Width of single Bay based on the dimensions: {bay_width}={price}")

    return bays, bay_width,bay_length, price

def postCostCal(structure_type,size=None,bays=None):
    print(structure_type,size,bays,"_________________")
    # print("What type of structure is needed?")
    # options = ["1. Freestanding", "2. Attached 1 Side", "3. Footings"]
    # for option in options:
    #     print(option)
    structure_type = structure_type

    posts = calculate_posts(size, structure_type)
    post_bases=posts
    postsCost=1500*int(posts)
    post_basesCost=275*int(post_bases)
    posts_cost=postsCost+post_basesCost
    total_cost=0
    # if footing
    if structure_type == "3":
        total_cost=600*posts
        print(f"Number of footings required: {posts}")
        print(f"Total cost: {posts} * 600 = {posts_cost}")
    else:
        print(f"Number of posts required: {posts}")
        print(f"Number of posts caps required: {post_bases}")
        print(f"Total cost: {posts} * 1500 + {post_bases} * 275 = {posts_cost}")


    # mandatory

    sensorP = bays
    b2b = p2g = 0
    if bays > 1:
        b2b = p2g = bays * (bays - 1)

    print(sensorP, "-----sensor package")
    print(b2b, "-----beam to beam ")
    print(p2g, "-----Pass Through Gutter")

    b2b_cost = b2b * 414
    p2g_cost = p2g * 662
    sensorP_cost = sensorP * 500
    Remote_control = 192
    return posts,post_bases,postsCost,post_basesCost,total_cost,sensorP,b2b,p2g,b2b_cost,p2g_cost,sensorP_cost,Remote_control

def installationCost(size=None,design_type="Corbels"):

    width, length = [int(s.strip("'")) for s in size.split('x')]
    area = width*length
    city_code="NY"
    if city_code in [ 'PA', 'NY', 'CT', 'NJ', 'DEL']:
        # intallation_cost= (length*width)  # to do
        intallation_cost=12000

    elif city_code in [ 'RI', 'MASS', 'M', 'VA']:
        # intallation_cost= (length*width)  # to do
        intallation_cost=20000
    else:
        intallation_cost = 0
    shipping_cost=5000

    material_type=design_type
    Design_cost=0
    if material_type == "Corbels":
        Design_cost = area*54
    elif material_type == "Single Cornice":
        Design_cost = area*68
    elif material_type == "Double Cornice":
        Design_cost = area*72

    Total_design_cost = Design_cost

    return intallation_cost , shipping_cost , Total_design_cost

def main_ff(selected_product=None,size=None,structure_type=None,design_type=None):
    # selected_product = "1"
    # size = "14 x 16"
    bays, bay_width, bay_length, price = main_price_cal(selected_product=selected_product, size=size)
    # structure_type = 'Freestanding'

    posts, post_bases, postsCost, post_basesCost, total_postCost, sensorP, b2b, p2g, b2b_cost, p2g_cost, sensorP_cost, Remote_control = postCostCal(
        structure_type=structure_type, size=size,bays=bays)
    # design_type = "Corbels"
    intallation_cost, shipping_cost, Total_design_cost = installationCost(size=size, design_type=design_type)

    final_cost = price + total_postCost + b2b_cost + p2g_cost + sensorP_cost + intallation_cost + shipping_cost + Remote_control + Total_design_cost
    print(final_cost)
    return final_cost

# def main_cal(user_input=None):
#
#     selected_product = greet_user()
#     size = get_size()
#     bays, bay_width, bay_length = calculate_bays(size, selected_product)
#     print(f"Number of Bays based on the dimensions: {bays}")
#     print(f"Width of single Bay based on the dimensions: {bay_width}")
#
#     price = cal_price(selected_product, bays, bay_width, bay_length)
#     print(f"Price for Width of single Bay based on the dimensions: {bay_width}={price}")
#     structure_type = ask_structure_type()
#     posts = calculate_posts(size, structure_type)
#     post_bases = posts
#     postsCost = 1500 * int(posts)
#     post_basesCost = 275 * int(post_bases)
#     posts_cost = postsCost + post_basesCost
#     # if footing
#     if structure_type == "3":
#         total_cost = 600 * posts
#         print(f"Number of footings required: {posts}")
#         print(f"Total cost: {posts} * 600 = {posts_cost}")
#     else:
#         print(f"Number of posts required: {posts}")
#         print(f"Number of posts caps required: {post_bases}")
#         print(f"Total cost: {posts} * 1500 + {post_bases} * 275 = {posts_cost}")
#     #############
#
#     sensorP = bays
#     b2b = p2g = 0
#     if bays > 1:
#         b2b = p2g = bays * (bays - 1)
#
#     print(sensorP, "-----sensor package")
#     print(b2b, "-----beam to beam ")
#     print(p2g, "-----Pass Through Gutter")
#
#     b2b_cost = b2b * 414
#     p2g_cost = p2g * 662
#     sensorP_cost = sensorP * 500
#     Remote_control = 192
#
#     # installation cost
#
#     # input("Enter your city:")    #   PA - Pennsylvania
#     #   NY - New York
#     #   CT - Connecticut
#     #   NJ - New Jersey
#     #   DEL - Delaware
#     #   RI - Rhode Island
#     #   MASS - Massachusetts
#     #   MD - Maryland
#     #   VA - Virginia
#
#     # Installation Charges:
#     #   For Installation in  PA, NY, CT, NJ, DEL: "$36 per Sq Ft, min $12k
#     #   For Installation in  RI, MASS, MD: "$46 per Sq Ft, min $18k."
#     #   For Installation in VA: "$50 per Sq Ft, min $20k."
#     width, length = [int(s.strip("'")) for s in size.split('x')]
#     area = width * length
#     city_code = "NY"
#     if city_code in ['PA', 'NY', 'CT', 'NJ', 'DEL']:
#         # intallation_cost= (length*width)  # to do
#         intallation_cost = 12000
#
#     elif city_code in ['RI', 'MASS', 'M', 'VA']:
#         # intallation_cost= (length*width)  # to do
#         intallation_cost = 20000
#     else:
#         intallation_cost = 0
#     shipping_cost = 5000
#
#     design_elements = "Corbels"
#     ############################################################################################################
#     #   A. Corbels
#     #   B. Single Cornice
#     #   C. Double Cornice
#     #   D. Custom Trim Package version 3
#     #   E. Custom Trim Package version 4
#     # Cost of one Corbels = $ 54.00 Per Square Foot
#     # Cost of one Single Cornice = $68.00 Per Square Foot
#     # Cost of one Double Cornice = $72.00 Per Square Foot
#     # Cost of one Custom Trim Package version 3 = minimum cost of $10,000.
#     #           (if threshold not met x $32.00 Sq Ft)
#     # Cost of one Custom Trim Package version 4 = minimum cost of $15,000.
#     #           (if threshold not met x $42.00 Sq Ft)
#
#     material_type = "Corbels"
#     if material_type == "Corbels":
#         Design_cost = area * 54
#     elif material_type == "Single Cornice":
#         Design_cost = area * 68
#     elif material_type == "Double Cornice":
#         Design_cost = area * 72
#
#     Total_design_cost = Design_cost
#
#     # if material_type = "Custom Trim Package version 3":
#     #     Design_cost = area*54
#     # if material_type = "Custom Trim Package version 4":
#     #     Design_cost = area*54
#     ##################################################################################
#
#     # Quetion 3: Ask the user if any of the following accessories required, if yes specify quantity:
#     #   Lighting and App Controls
#     #     (RL) Recessed Lights : $250 Each
#     #     (RP) Ramp Lights : $250 Each
#     #     (SL) Strip Light Control Box: $1,042 (1 per Bay)
#     #     (LED) LED Strip Lights: $92 per foot
#
#     #     Recommended Options:
#     #       • R. Ramp Lights: 4 to 6 Recommended (6 max per bay)
#     #       • S. Recessed Lights: 2 per fan/light beam
#     #       • T. LED Strip Lights: Provide pricing based on length
#
#     # For LED Strip Lights:
#     #   Calculate 2*Width + Length = Total Linear ft x $92 + $1000 for control panel
#     # For Fan:
#     #   Total Cost = $1,000(One Fan) + $800(Fan Beam)
#
#     #   Smart Controls
#     #     (BA) Bond Home App Controls: $600
#
#     #   Fans & Heaters
#     #     (F) Fans: $1,000 each
#     #     (FB) Fan Beam: $1,500 each
#     #     (H) Heaters: $2,500 each
#
#     #   Motorized Side Shades
#     #     (A) Motorized Shades 5' to 15': $5,800
#     #     (B) Motorized Shades 15' to 23': $7,800
#     #     (C) Motorized Shades 24' to 30': $9,000
#     #     (D) Privacy Walls: (Specify Width x Height, Color, Spacing, and additional post if needed)
#
#     FINAL_COST = price + posts_cost + b2b_cost + p2g_cost + sensorP_cost + intallation_cost + shipping_cost + Remote_control + Total_design_cost
#
#     print(FINAL_COST)


if __name__ == "__main__":
    selected_product="1"
    size="14 x 16"
    # bays, bay_width,bay_length, price=main_price_cal(selected_product=selected_product,size=size)
    structure_type='Freestanding'
    #
    # posts,post_bases,postsCost,post_basesCost,total_postCost,sensorP,b2b,p2g,b2b_cost,p2g_cost,sensorP_cost,Remote_control=postCostCal(structure_type=structure_type,size=size,bays=bays)
    design_type="Corbels"
    # intallation_cost, shipping_cost, Total_design_cost=installationCost(size=size,design_type=design_type)

    # final_cost = price+total_postCost+ b2b_cost+p2g_cost+sensorP_cost+intallation_cost+shipping_cost+Remote_control+Total_design_cost
    # print(final_cost)
    final_cost=main_ff(selected_product, size, structure_type, design_type)