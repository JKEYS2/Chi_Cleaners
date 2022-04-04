# Mainly used for sleep
import time
# For timestamping logs
from datetime import datetime
# Managing input output files
import os
# For moving output files to history folder
import shutil
# For logging current line of code
from inspect import currentframe

start_time = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
# Creates a log file on program start
# Make logs dir if it doesn't exist
if not os.path.isdir("logs"):
    os.mkdir("logs")
log_path = os.path.join("logs", f"LOG [{start_time}].csv")
# Add log titles
log_file = open(log_path, "w")
log_file.writelines("Timestamp, Line, Type, Value, Message")
log_file.close()


# Log function - this happens first so everything else can be logged
def log(line="???", log_type="", value="", comment=""):
    # Convert all parameters into strings
    log_type = str(log_type)
    value = str(value)
    comment = str(comment)
    # Commas have to be replaced with another character as they are delimiter
    log_type = log_type.replace(",", "•")
    value = value.replace(",", "•")
    comment = comment.replace(",", "•")
    # Encoded new line is removed so each log stays on one
    log_type = log_type.strip("\n")
    value = value.strip("\n")
    comment = comment.strip("\n")

    # log_file opened in append mode so a new entry can be added
    log_file = open(log_path, "a")
    # Write timestamp, code line number, log type/level, value, comment/message
    log_file.writelines(f"\n{datetime.now().strftime('%Y-%m-%d   %H-%M-%S')}, {line}, {log_type}, {value}, {comment}")
    # Close log file
    log_file.close()


# USE: get the current line of code for logging
# source: https://www.codegrepper.com/code-examples/python/print+current+line+number+python
def get_line_number():
    return str(currentframe().f_back.f_lineno)


log(get_line_number(), "start", "", "Loging started")


# USE: strikethrough discount text
# source: https://stackoverflow.com/questions/25244454/python-create-strikethrough-strikeout-overstrike-string-type
def strike(text):
    # create empty string
    result = ""
    # for each character in the string `text`
    for char in text:
        # "\u0336" is concatenated onto the character and this modified character is concatenated to result
        result = result + char + "\u0336"
    # once every character in the string `text` has been modified, and recombined into the `result` string
    # `result` is returned
    return result


# takes a number, formats it to 2 decimal places and adds "£"
# source: https://www.adamsmith.haus/python/answers/how-to-format-a-float-as-currency-in-python
def pricify(price):
    log(get_line_number(), "verbose", price, f"pricify(price)")
    # Try making the price a float
    try:
        price = float(price)
        # If this can be done then it can also be formatted
        return "£{:.2f}".format(price)
    # Sometimes the input is "" (nothing) in which would cause a crash if formatted
    except:
        log(get_line_number(), "warn", price, "price did not float - returning nothing")
        # Function just returns what the parameter it was run with (it will likely just be printed)
        return price


def make_directory_if_needed(path):
    # Checks if the directory already exists
    if not os.path.isdir(path):
        log(get_line_number(), "info", "does not exist", f'"{path}" directory will now be created...')
        # Creates directory if it doesn't exist
        os.mkdir(path)
    else:
        # There is only a log message if it does exist
        log(get_line_number(), "info", "directory already exists", f'"{path}"')


# Creates "output", "output\history" & "products" directories if they don't exist yet
make_directory_if_needed("output")
make_directory_if_needed(os.path.join("output", "history"))
make_directory_if_needed("products")

# Defining of file and folder paths for later use
receipt_path = os.path.join("output", "receipt.txt")
tags_path = os.path.join("output", "tags.txt")
history_path = os.path.join("output", "history")
products_path = os.path.join("products", "products.csv")


# This function will create a default products CSV if one does not exist already
def make_products_file():
    log(get_line_number(), "function", "make_products_file()", "Creating products.csv as it doesn't exist")
    # This is its own function so the variables are local
    products_file = open(products_path, "w")
    # Write the CSV data to the file as a multi-line string
    products_file.write("""Name,L-G,ST-SP,LPrice,SP-LPrice,G-Price,SP-GPrice
dress,l,b,8,11.2,,
eve dress,l,sp,,21,,
2 pc suit,b,b,12,16.8,12,16.8
jacket,b,b,7.5,9.1,7.5,10.5
shirt,b,b,6.5,9.1,6.5,9.1
blouse,l,b,6.5,9.1,,
2 pc eve suit,g,sp,,,,16.8
trousers,g,b,,,6.5,9.1
coat,g,b,,,9.95,13.93""")
    products_file.close()


# If products.csv doesn't exist it is created
if not os.path.isfile(products_path):
    log(get_line_number(), "warn", "fixing", "products.csv doesn't exist! Running make_products_file()")
    make_products_file()


# Check if the "config.txt" file exists
config_path = os.path.join("products", "config.txt")
if not os.path.isfile(os.path.join("products", "config.txt")):
    # If it doesn't exist a new one will be made
    log(get_line_number(), "info", "does not exist", '"products\\config.txt" will now be created...')
    # Open config file in write mode
    config_file = open(os.path.join("products", "config.txt"), "w")
    # Write default content
    config_file.writelines("""1 - enable_additional_features (the below will not work if this is disabled (0))
1 - allow_do_quantity - prompt user for quantity?
1 - quantity_count_on_tag - if enabled, (number) will be added to each tag if a quantity more than 5 is entered (otherwise the program waits 1 second to ensure unique tags)
1 - seconds_on_tags - should tags also have on the end (not 12 digit)
0 - use_validate_products_csv (this function currently doesn't work fully - best to leave it disabled) 

# space for features that exist yet:""")
    log(get_line_number(), "info", "", "Loging started")
    config_file.close()
else:
    # config file already exists - no need to do anything (it would overwrite)
    log(get_line_number(), "info", "", 'config file created')

### Loading config options:
# Open config file in read mode
config_file = open(os.path.join("products", "config.txt"), "r")
log(get_line_number(), "info", "", "Loading config...")
# Read the first character only of the first line and store it as `enable_additional_features`
enable_additional_features = config_file.readline()
log(get_line_number(), "info", enable_additional_features, "<--- enable_additional_features[0]")
print(f"exact: {enable_additional_features}")
# If `enable_additional_features` is 0, then additional features can be active
if enable_additional_features[0] == "1":
    log(get_line_number(), "info", enable_additional_features[0],
        "Additional features can be enabled (enable_additional_features = True (1))")
    # Other non-standard options go here
    # Store each line in a named variable
    allow_do_quantity = config_file.readline()
    quantity_count_on_tag = config_file.readline()
    seconds_on_tags = config_file.readline()
    use_validate_products_csv = config_file.readline()
    # logs
    log(get_line_number(), "info", allow_do_quantity, "<--- allow_do_quantity (full line from config.txt)")
    log(get_line_number(), "info", quantity_count_on_tag, "<--- quantity_count_on_tag (full line from config.txt)")
    log(get_line_number(), "info", seconds_on_tags, "<--- seconds_on_tags (full line from config.txt)")
    log(get_line_number(), "info", use_validate_products_csv, "<--- use_validate_products_csv (full line from config.txt)")

    # If the first character is 1 (enabled)
    if allow_do_quantity[0] == "1":
        # If "1" (enabled) then `allow_do_quantity` is stored as True for later use
        allow_do_quantity = True
        log(get_line_number(), "verbose", str(allow_do_quantity), "<--- allow_do_quantity (boolean set)")
    else:
        # `allow_do_quantity` is stored as False and the "do quantity" prompt won't activate
        allow_do_quantity = False
        log(get_line_number(), "verbose", str(allow_do_quantity), "<--- don't allow_do_quantity (boolean set)")

    if quantity_count_on_tag[0] == "1":
        # If "1" (enabled) then `quantity_count_on_tag` is stored as True for later use (see config for more info)
        quantity_count_on_tag = True
        log(get_line_number(), "verbose", str(quantity_count_on_tag), "<--- quantity_count_on_tag (boolean set)")
    else:
        # `quantity_count_on_tag` is stored as False and the program will wait 1 second for a different timestamp
        quantity_count_on_tag = False
        log(get_line_number(), "verbose", str(quantity_count_on_tag), "<--- no quantity_count_on_tag (boolean set)")

    # (the spec wants tag codes to be 12 digits long - this adds two more digits for seconds)
    if seconds_on_tags[0] == "1":
        seconds_on_tags = True
        log(get_line_number(), "verbose", str(seconds_on_tags), "<--- seconds_on_tags (boolean set)")
    else:
        # `seconds_on_tags` is stored as False and seconds are excluded from tags
        seconds_on_tags = False
        log(get_line_number(), "verbose", str(seconds_on_tags), "<--- no seconds_on_tags (boolean set)")

    # This function is mostly unfinished ...but it can still be turned back on
    if use_validate_products_csv[0] == "1":
        use_validate_products_csv = True
        log(get_line_number(), "verbose", str(use_validate_products_csv), "<--- use_validate_products_csv (boolean set)")
    else:
        # `use_validate_products_csv` is stored as False and unfinished function `validate_products_csv()` is not run
        use_validate_products_csv = False
        log(get_line_number(), "verbose", str(use_validate_products_csv),
            "<--- don't use_validate_products_csv (boolean set)")
else:
    log(get_line_number(), "verbose", enable_additional_features[0],
        "All additional features disabled (enable_additional_features = False (0))")
    allow_do_quantity = False
    quantity_count_on_tag = True
    seconds_on_tags = False
    use_validate_products_csv = False
    log(get_line_number(), "verbose", str(allow_do_quantity), "<--- don't allow_do_quantity (boolean set)")
    log(get_line_number(), "verbose", str(quantity_count_on_tag), "<--- no quantity_count_on_tag (boolean set)")
    log(get_line_number(), "verbose", str(seconds_on_tags), "<--- no seconds_on_tags (boolean set)")
    log(get_line_number(), "verbose", str(use_validate_products_csv),
        "<--- don't use_validate_products_csv (boolean set)")

config_file.close()
log(get_line_number(), "info", "", "config set")


# todo validate_products_csv() - (would require significant code refactoring)
# Please excuse the mess here
def validate_products_csv():    
    # todo      some comments and stuff + logs
    # todo ensure prices are valid and exist if the indicator is there
    # if l-g is b, there needs to be a price for both those variants
    # Get products file
    products_file = open(products_path, "r")
    # Create line counter variable
    line_num = 0
    list_of_all_names = []
    list_of_invalid_names = []
    # list_of_invalid_prices = []
    # Change the line output to a list separated by the CSV commas - todo where? (this comment doesn't make sense)
    products_file.readline()
    keep_going = True
    while keep_going and line_num < 100:  # todo - fix this
        # Store one line so it can be accessed multiple times
        line = str(products_file.readline().lower())
        log(get_line_number(), "loop", line, "<--- line")  # todo
        line_num += 1
        if str(line) != "":
            line = line.split(",")
            items = line[0].split(";")
            for item in items:
                list_of_all_names.append(list((item, line_num + 1)))
                # print(f"list_of_all: {list_of_all_names}")    # debug only
            #
            # for i in line:
            #     name = line[0]
            #     ladies_or_gentlemen = line[1]
            #     standard_or_special = line[2]
            #     lprice = line[3]
            #     gprice = line[4]
            #     sp_lprice = line[5]
            #     sp_gprice = line[6]
            #     # if b:#
            #     if ladies_or_gentlemen == "b":
            #
            #         # check both prices
        else:
            # print("end loop")     # debug only
            keep_going = False

    #
    # This section deals with just product names, ensuring there are no duplicates
    i = 0
    for item1 in list_of_all_names:
        # Ensure the name is not a number
        # (the item line number can be used to select a product - a number name would cause unexpected results)
        try:
            # if it can then the data type is changed
            nothing = int(item1[0])
            list_of_invalid_names.append(item1)
        except:
            j = 0
            for item2 in list_of_all_names:
                print(f"{item1} --> {item2}")
                print(f"{i}   {j}")
                if item1[0] == item2[0] and i != j:  # or they are the same index
                    print("heck!")
                    list_of_invalid_names.append(item1)
                j += 1
        i += 1

    print("List of duplicate product names in products.csv")
    list_of_invalid_names = sorted(list_of_invalid_names)
    for item in list_of_invalid_names:
        print(item)
        # item = str(item).split(",")
        print(f"On line {item[1]}: {item[0]} was found to be a duplicate")
    print(keep_going)
    products_file.close()


# Config file can control whether this function is run or not
if use_validate_products_csv:
    validate_products_csv()


def quan_input(message):
    log(get_line_number(), "function", "quan_input(message)", f"message: {message}")
    log(get_line_number(), "input", f"Message: {message}", "quan_input")

    # Keep asking user for another input while it isn't valid
    keep_going = True
    while keep_going:
        # Store input and log
        x = input(message)
        log(get_line_number(), "input", x, message)
        # Test if the input can be converted to an int (https://stackabuse.com/python-check-if-variable-is-a-number/)
        try:
            # if it can then the data type is changed
            x = int(x)
            # Also ensure quantity can't be negative o̶r̶ ̶z̶e̶r̶o̶
            if x > -1:
                log(get_line_number(), "info", str(x), "user input is a positive whole number (or zero)")
                # If valid return the value
                return x

        except:
            # if not, the input is not a whole number
            # If the user inputs nothing the program will default to a quantity of 1
            if x == "":
                log(get_line_number(), "info", "nothing", "user input is nothing - return 1 as default quantity")
                return 1
            # else, probably a very broken input that would cause errors (should be caught above)
        print("! Please enter whole number !")
        log(get_line_number(), "info", str(x), 'User input invalid: "! Please enter whole number !"')


def show_products():
    log(get_line_number(), "function", "show_products()", "This function is being run")
    # Open products.csv in read mode as `products_file`
    products_file = open(products_path, "r")
    # Store one line as variable `line`
    line = products_file.readline()
    log(get_line_number(), "info", line, "Title line from products CSV")
    # `line` is turned into a list so each element can be accessed individually
    line = str(line).split(",")
    # Counter for the line number is created
    line_num = 0
    log(get_line_number(), "info", str(line_num), "`line_num` initialised")
    # Print information for the user and headings for the table
    print("\nChi Cleaning - Products List:")
    print(f"#)  Names{' ' * 20}\t|\t   L/G   \t|\tSpecial?\t|\t{line[3]}\t|\t{line[4]}\t|\t{line[5]}\t|\tSP-GPrice")
    # While `line` is not empty/nothing:
    while str(line) != "['']":
        # `line_num` is incremented as a new line is started
        line_num += 1
        log(get_line_number(), "loop", str(line_num), "`line_num` incremented")
        # Redefine `line` as the next line in the products_file
        line = products_file.readline()
        log(get_line_number(), "loop", line, "`line` from products CSV")
        # `line` is turned into a list so each element can be accessed individually
        line = str(line).split(",")
        # `i` will increment from 0 to the length of the list ---> (loop through every element)
        for i in range(0, len(line)):
            log(get_line_number(), "verbose_loop", line[i], "`line` item from products CSV (line[i])")
            # Some products don't have some variants, so the price is just empty (or an encoded new line \n)
            if line[i] == "" or line[i] == "\n":
                # If this is the case, "nothing" is replaced with a longer string so the spacing doesn't break
                line[i] = "~####"
                log(get_line_number(), "verbose_loop", line[i], "`line` item was empty")

        # A line may only have 1 element causing a list out of range error (this is a lazy way of avoiding that issue)
        try:
            log(get_line_number(), "loop", str(line), "`line` before readability modification")
            """ All of this is simply string modification for better readability: """
            # Add space after ";" separator
            line[0] = line[0].replace(";", "; ")
            # Add spaces after names so the table lines up
            line[0] = line[0] + (" " * (25 - len(line[0])))

            # Replace single letters "l,g,b" with the full word they represent (also fix spacing)
            line[1] = line[1].replace("l", "Ladies   ")
            line[1] = line[1].replace("g", "Gentlemen")
            line[1] = line[1].replace("b", "Both     ")
            # Replace letters "st,sp,b" with the full word they represent (also fix spacing)
            line[2] = line[2].replace("st", "Standard")
            line[2] = line[2].replace("sp", "Special ")
            line[2] = line[2].replace("b", "Both     ")
            # Remove the new line from the end of the line
            line[6] = line[6].strip("\n")
            """ All of this is simply string modification for better readability: """
            log(get_line_number(), "loop", str(line), "`line` after readability modification")

        except:
            log(get_line_number(), "warn", "show_products",
                "List would be out of range, closing file and returning nothing")
            products_file.close()
            # return nothing instead of crashing
            # (the function doesn't return a value anyway so this is just an early exit)
            return

        # Output for this line is concatenated and stored in string variable `output`
        output = f"{line_num}) {line[0]}\t|\t{line[1]}\t|\t{line[2]}\t|\t{pricify(line[3])}\t|\t{pricify(line[4])}\t\t|\t{pricify(line[5])}\t|\t{pricify(line[6])}"
        # `output` is printed to the user
        print(output)
        log(get_line_number(), "info", "output -->", output)
    # Close products_file
    products_file.close()


def get_product(user_in):
    log(get_line_number(), "function", user_in, f"get_product() called - looking for user_in: {user_in}")
    # if the user's input is nothing the function returns "Null" so it doesn't break
    if user_in == "":
        log(get_line_number(), "warn", '"" / (nothing)',
            "get_product - invalid: user_in is nothing! (print: This product was not found)")
        # Informative error for user
        print("This product was not found")
        # Function ends returning a nothing output (the value isn't actually NULL, it is just a string)
        return "Null"

    # Open products csv in read
    products_file = open(products_path, "r")
    # create line_num counter at 0
    line_num = 0
    log(get_line_number(), "loop", line_num, "start `line_num` at zero")
    # Loop through each line in products_file
    keep_going = True  # Line limit of 2000 just in case (infinite loop protection)
    while keep_going and line_num < 2000:
        # Store one line so it can be accessed multiple times
        line = products_file.readline().lower()
        log(get_line_number(), "loop", line, f"Line number {line_num} Looping through products.csv")
        # Change the line output to a list separated by the CSV commas
        line = line.split(",")
        log(get_line_number(), "loop", line, "`line` after split on comma")
        # Also split the name column on ";" - stored as `items` list
        # this allows one product to have multiple names if needed
        items = line[0].split(";")
        log(get_line_number(), "loop", items, "<-- `items` list (line[0].split(';'))")
        # For each `item` in `items`
        for item in items:
            # If `user_in`put matches a name in the CSV OR it is equal to the `line_num`ber
            if item == user_in or str(line_num) == user_in:
                log(get_line_number(), "info", f"`{item}` == `{user_in}`", "`item` == `user_in`")
                # Remove (\n) new line symbol from last entry in `line`
                line[-1] = line[-1].strip("\n")
                # Remove the alt product names for further processing
                line[0] = items[0]
                # Do not return if line is empty
                if str(line) == "['']":
                    log(get_line_number(), "warn", user_in, "User's input was out of range")
                    print("This product was not found")
                    return "Null"
                # Inform the user of their selection
                print(f"{line[0]} has been selected")
                log(get_line_number(), "info", line[0], "...has been selected")
                # Return the name, l-g, st-sp & price information
                return line

        # Stop loop if line is empty
        if str(line) == "['']":
            keep_going = False
        log(get_line_number(), "loop", keep_going, "keep_going")
        # Increment line_num before looping into the next line
        line_num += 1
        log(get_line_number(), "loop", line_num, "line_num")
    # Close the products CSV once finished with it
    products_file.close()

    # If no product is found:
    # A message is displayed
    print("This product was not found")
    log(get_line_number(), "warn", "invalid user input", "print(This product was not found) - returning Null")
    # A null response is returned that the next function will have to handle
    return "Null"


def select_either(message="default", opt1="y", opt2="n"):
    # Function takes a `message` to prompt the user
    # ...and 2 options the user can choose between (as strings)
    # (This just manages validation)
    log(get_line_number(), "function", (message, opt1, opt2), f"{message} ({opt1}/{opt2}")
    # The while loop will `keep_going` while the user input is invalid
    keep_going = True
    while keep_going:
        # User is prompted with the message & (the two options they can choose between)
        # This is converted to lower case (so the case doesn't need to match) and stored as `user_in`
        user_in = input(f"{message} ({opt1}/{opt2}): ").lower()
        log(get_line_number(), "input", user_in, "<-- user_in - select_either()")
        # If `user_in` matches either of the options
        if user_in == opt1 or user_in == opt2:
            log(get_line_number(), "info", user_in, "match")
            # `user_in` must be valid and is returned so the choice can be handled
            return user_in
        # If `user_in` doesn't match either of the options:
        # The user is informed of this
        print(f'Your input must be either "{opt1}" or "{opt2}"')
        log(get_line_number(), "info", user_in, "user_in did not match")
        # ...and is forced to wait 0.25 seconds
        time.sleep(0.25)


def process_product_options(product):
    # `product` is returned by `get_product()`
    # if `product` is "Null" then it means a products was not found
    if product == "Null":
        log(get_line_number(), "warn", product, "`product` == Null - no match found in get_product()")
        # There are no options to process
        # Returns another Null response
        return product, "", ""

    # if `product` is valid:
    # `product` is a list - for readability the list elements are store in named variables (type string)
    log(get_line_number(), "info", product, "<--- product")
    name = product[0]
    ladies_or_gentlemen = product[1]
    standard_or_special = product[2]
    l_price = product[3]
    sp_l_price = product[4]
    g_price = product[5]
    sp_g_price = product[6]

    # Default value for `cost`
    cost = 0
    # If `ladies_or_gentlemen` = "b" (both) then it means the product has 'ladies' and 'gentlemen' versions
    if ladies_or_gentlemen == "b":
        # The user must choose between them - select_either() ensures a valid input
        log(get_line_number(), "call function", 'select_either("Select ladies or gentlemen", "l", "g")')
        ladies_or_gentlemen = select_either("Select ladies or gentlemen", "l", "g")
        log(get_line_number(), "info", ladies_or_gentlemen, "ladies_or_gentlemen has been chosen by user")
    # If `standard_or_special` = "b" (both) then it means the product has 'special' and 'standard' versions
    if standard_or_special == "b":
        # The user must choose between them - select_either() ensures a valid input
        log(get_line_number(), "call function", 'select_either("Select standard or special cleaning", "st", "sp"')
        standard_or_special = select_either("Select standard or special cleaning", "st", "sp")
        log(get_line_number(), "info", standard_or_special, "standard_or_special has been chosen by user")

    # Each product could be one of four variants which each have a unique price
    # This selects the correct price based on which variant the product is
    # ladies standard
    if ladies_or_gentlemen == "l" and standard_or_special == "st":
        cost = l_price
        log(get_line_number(), "info", l_price, "l_price - ladies standard price")
    # ladies special
    if ladies_or_gentlemen == "l" and standard_or_special == "sp":
        cost = sp_l_price
        log(get_line_number(), "info", sp_l_price, "sp_l_price - ladies special price")
    # gentlemen standard
    if ladies_or_gentlemen == "g" and standard_or_special == "st":
        cost = g_price
        log(get_line_number(), "info", g_price, "g_price - gentlemen standard price")
    # gentlemen special
    if ladies_or_gentlemen == "g" and standard_or_special == "sp":
        cost = sp_g_price
        log(get_line_number(), "info", sp_g_price, "sp_g_price - gentlemen special price")
    # The cost comes from the CSV so has to be converted from type "string" to a 'float' so maths can be performed
    cost = float(cost)

    # `standard_or_special` is stored in `output` as the start of the tag
    output = f"-{standard_or_special}"
    log(get_line_number(), "verbose", output, "`output` - basically the end of the tag")
    # print(f"output: {output}")    # debug only
    # The three values `output` (end of tag st/sp), `name` of product & `cost` (the price of this product variant)
    return output, name, cost


def historic_copy(path):
    # This function copies a file into the "output\history" directory with a timestamp appended to the name
    log(get_line_number(), "function", f"historic_copy({path})",
        "historic_copy(path) - copying outputs to history folder")
    # If the file does exist
    if os.path.isfile(path):
        # Get only the file name from the file path by splitting on the directory separator symbol "\"
        # ...then selecting the last element of the resulting list (the end of the path is the file name)
        file_name = path.split("\\")[-1]
        # Directory separator on Linux is different to Windows ( "/" not "\" )
        # (If running on Linux, \ won't be in the file path so the first operation won't do anything)
        # (same thing the other way round)
        file_name = file_name.split("/")[-1]
        log(get_line_number(), "info", file_name, "original file_name")
        # Get the timestamp of the current time (when the file is being created)
        new_now = datetime.now()
        file_time = new_now.strftime("%Y-%m-%d %H-%M-%S")
        # The file_time is concatenated to the front of the file_name
        # This creates a unique file name that doesn't try to overwrite the existing file
        new_file_name = f"[{file_time}] {file_name}"
        log(get_line_number(), "info", new_file_name, "new_file_name")
        # Shutil is used to copy the file to the output\history directory with the new_file_name
        shutil.copy(path, os.path.join("output", "history", new_file_name))
        log(get_line_number(), "info", "shutil.copy()", "New file created in history directory")


# Calculations and writing values to "receipt.txt"
def make_receipt(order_list):
    log(get_line_number(), "function", f"make_receipt({order_list})", "make_receipt(order_list) is running")
    # Open "receipt.txt" in write mode as a variable called `receipt`
    receipt = open(receipt_path, "w")
    # Writing some titles and stuff to `receipt`
    receipt.write("Chi Cleaners - Order Summary\n\n")
    receipt.write(f"\tItem{' ' * 24} \t|\t Base Price \t|\t Excluding VAT\n")
    # Printing the same stuff to the user
    print("Chi Cleaners - Order Summary\n")
    print(f"\tItem{' ' * 24} \t|\t Base Price \t|\t Excluding VAT")

    # Create total counter for base cost (the price including VAT, before discounts)
    total_base_cost = 0
    log(get_line_number(), "loop", total_base_cost, "start total_base_cost at zero")
    log(get_line_number(), "info", order_list, "order_list")
    # for every order item in `order_list`:
    for item in order_list:
        log(get_line_number(), "loop", item, "`item` in order_list")
        # Each order item is a list
        # the below gives each element of this list clear variable names
        name = item[1]
        base_price = item[2]
        # todo
        # Calculate the price excluding VAT per item to display to user
        price_excluding_vat = base_price / 1.2
        log(get_line_number(), "loop", name, "`name`")
        log(get_line_number(), "loop", str(base_price), "`base_price`")
        log(get_line_number(), "loop", str(price_excluding_vat), "`price_excluding_vat`")

        # Write the name and price of each item on the receipt to "receipt.txt"
        receipt.write(f"\t{name}{' ' * (28 - len(name))} \t|\t {pricify(base_price)} \t\t|\t {pricify(price_excluding_vat)}\n")
        print(f"\t{name}{' ' * (28 - len(name))} \t|\t {pricify(base_price)} \t\t|\t {pricify(price_excluding_vat)}\n")
        # Increase cumulative total
        total_base_cost += base_price
        # log the new total after each increment
        log(get_line_number(), "verbose", str(total_base_cost), "Running total | `total_base_cost`")

    # Also calculate total price excluding VAT, so it can be outputted
    total_excluding_vat = total_base_cost / 1.2
    log(get_line_number(), "info", str(total_base_cost), "Finished total | `total_base_cost`")
    log(get_line_number(), "info", str(total_excluding_vat), "`total_excluding_vat`")
    # Write and print the total number of items (in `order_list`) and the total price
    receipt.write(f"Total number of items: {len(order_list)}\n")
    receipt.write(f"Total including VAT: {pricify(total_base_cost)}\n")
    receipt.write(f"Total excluding VAT: {pricify(total_excluding_vat)}\n\n")
    print(f"Total number of items: {len(order_list)}")
    print(f"Total including VAT: {pricify(total_base_cost)}")
    print(f"Total excluding VAT: {pricify(total_excluding_vat)}\n")

    # Calculate discount eligibility from VAT inclusive price
    # If `total_base_cost` larger than or equal to 30
    if total_base_cost >= 30: # todo - I did big dumb here: first one was "is larger than 15?" so never gets to larger discount
        # `discount` percentage (as a decimal) is set to 0.15 (15%)
        discount = 0.15
        log(get_line_number(), "info", str(discount), "discount 15%")
    # If `total_base_cost` larger than or equal to 15
    elif total_base_cost >= 15:
        # `discount` percentage (as a decimal) is set to 0.1 (10%)
        discount = 0.1
        log(get_line_number(), "info", str(discount), "discount 10%")
    # Else: total_base_cost must be less than 15
    else:
        # `discount` percentage (as a decimal) is set to 0 (no discount)
        discount = 0
        log(get_line_number(), "info", str(discount), "order does not fulfil discount requirements")
    # Write and print the discount percentage
    receipt.write(f"Discount: ({round(discount * 100)}%)\n")
    print(f"Discount: ({round(discount * 100)}%)")
    # Calculate price after discount
    discounted_price = total_base_cost * (1 - discount)
    discount_amount = total_base_cost - discounted_price
    log(get_line_number(), "info", str(discounted_price), "discounted_price")
    log(get_line_number(), "info", str(discount_amount), "discount_amount")
    # Write and print the discount amount (and impact on the original price)
    receipt.write(f"{pricify(total_base_cost)} - {pricify(discount_amount)} = {pricify(discounted_price)}\n")
    print(f"{pricify(total_base_cost)} - {pricify(discount_amount)} = {pricify(discounted_price)}")

    # Calculate VAT on `discounted_price`
    vat_amount = discounted_price - (discounted_price / 1.2)
    log(get_line_number(), "info", str(vat_amount), "vat_amount")
    # Write VAT info to `receipt`
    receipt.write(f"Discounted price including VAT: {pricify(discounted_price)}\n")
    receipt.write(f"Discounted price excluding VAT: {pricify(discounted_price - vat_amount)}\n")
    receipt.write(f"VAT amount: {pricify(vat_amount)}\n\n\n")
    # Also print this information to the user
    print(f"Discounted price including VAT: {pricify(discounted_price)}")
    print(f"Discounted price excluding VAT: {pricify(discounted_price - vat_amount)}")
    print(f"VAT amount: {pricify(vat_amount)}\n\n")

    # Write the final total to `receipt`
    receipt.write(f"Total due: {pricify(discounted_price)}\n\n\n")
    # Add a nice message too
    receipt.write(f"Thank you for choosing Chi Cleaners")
    # Also write this information to the screen for the user to see
    print(f"Total due: {pricify(discounted_price)}\n\n")
    print(f"Thank you for choosing Chi Cleaners")
    # Close `receipt` as nothing else needs to be added
    receipt.close()
    # Artificial wait (2 seconds) while user reads some stuff and before starting a new order
    time.sleep(2)
    # Print some line breaks to separate the new order from the previous order
    print("\n\n")
    # Create a copy of the receipt in the history directory
    log(get_line_number(), "call function", f"historic_copy({receipt_path})", "historic_copy(receipt_path)")
    historic_copy(receipt_path)


def make_tags(order_list):
    log(get_line_number(), "function", f"make_tags({order_list})", "make_tags(order_list)")
    # open tags file in write mode and store as `tags_file`
    tags_file = open(tags_path, "w")
    # For each `item` in the `order_list`:
    for item in order_list:
        # todo testing item[0] = "so this is quite a long string"

        # Set `tag_len` equal to the length of the longest part of the item
        tag_len = len(item[0])
        # If the second part of `item` is longer than the first:
        if len(item[1]) > tag_len:
            # Set `tag_len` to the (longer) second item's length
            tag_len = len(item[1])
        # This length is needed to ensure the margin is the correct size for the content
        # The margin and spacings have to be longer for longer content
        # The spacers are set based on `tag_len`
        space_spacers = ' ' * tag_len
        equals_spacers = '=' * tag_len
        # Write top margin to tags.txt
        tags_file.write(f"  .{equals_spacers}.\n")
        tags_file.write(f" / {space_spacers} \\  \n")
        # Write the item name and spacing (remove the length of the item itself) (+ margin)
        tags_file.write(f"|| {item[1] + (' ' * (tag_len - len(item[1])))} ||\n")
        # Write the item tag code and spacing (remove the length of the item itself) (+ margin)
        tags_file.write(f"|| {item[0] + (' ' * (tag_len - len(item[0])))} ||\n")
        # Write bottom margins
        tags_file.write(f" \\ {space_spacers} / \n")
        tags_file.write(f"  '{equals_spacers}'\n")
    tags_file.close()
    # Create a copy of the tags file in the history directory
    log(get_line_number(), "call function", f"historic_copy({tags_path})", "historic_copy(tags_path)")
    historic_copy(tags_path)


def make_order():
    log(get_line_number(), "function", "make_order()", 'Run when the user has finished ("done") their order')
    # Give user information about the inputs they can enter to control the program
    print('''Order started:
        - enter "show" to display product information
        - enter "help" to see this message again
        - enter "done" to finish this order''')
    print("Clothes items can be selected with their name or the line they appear on")
    # Each item that is added to the order will be added to the `order_list`
    order_list = []
    log(get_line_number(), "info", order_list, "order_list created (empty)")
    # Loop until the user ends the loop (keep adding more products to the order)
    keep_going = True
    while keep_going:
        # Store user input as `user_in`
        user_in = input('Input clothes item ("done" to finish): ')
        log(get_line_number(), "input", user_in, "<-- order item input")

        # If the user enters "show":
        if user_in.lower() == "show":
            # Run the function that shows the user all products
            log(get_line_number(), "call function", "show_products()")
            show_products()
        # Tf the user enters "help" they can see this help message
        elif user_in.lower() == "help":
            print('''
- enter the name of a product to select it
- enter "show" to display product information
- enter "done" to finish this order
There is also a user guide {where to find user guide}''')
            log(get_line_number(), "info", user_in, 'User inputted "help" - help message displayed')
        # As long as the user is not done:
        elif user_in.lower() != "done":
            log(get_line_number(), "info", user_in, "Order continuing...")
            # `user_in` goes into `get_product()` which should return product information
            # `process_product_options()` then takes the product information from `get_product()`
            #  this is stored in these three variables (see the referenced function for more detail)
            standard_or_special, name, cost = process_product_options(get_product(user_in))
            log(get_line_number(), "info", standard_or_special,
                "`standard_or_special` - From process_product_options(get_product(user_in))")
            log(get_line_number(), "info", name,
                "`name` - From process_product_options(get_product(user_in))")
            log(get_line_number(), "info", cost,
                "`cost` - From process_product_options(get_product(user_in))")

            # if process_product_options(get_product(user_in)) does return product information: process it
            # (else: loop back up to the user input ---> user_in = input("Input clothes item: "))
            if standard_or_special != "Null" and standard_or_special != "":
                if do_quantity:
                    # Prompt for quantity input (only if the user choose it at the start of the full order)
                    # `quan_input()` verifies that the input is a whole number & larger than zero
                    quantity = quan_input("Quantity: ")
                    log(get_line_number(), "info", quantity, "<-- user has inputted quantity")
                else:
                    # The prompt is skipped if quantity is not being used (it is set to 1)
                    quantity = 1
                    log(get_line_number(), "info", quantity, "No quantity prompt - default = 1")

                # Loop for the number of times of `quantity` - each loop adds the item to the order list
                for i in range(0, quantity):
                    log(get_line_number(), "verbose loop", i, "loop number")
                    # # First set `timestamp` format
                    # `seconds_on_tags` is defined by config file - adds seconds to tag timestamp (exceeds 12 digits)
                    if seconds_on_tags:
                        # Adds seconds to tag timestamp (exceeds 12 digits)
                        timestamp = datetime.now().strftime("%d%m%Y%H%M%S")
                        log(get_line_number(), "verbose loop", timestamp, "<-- seconds included on tags timestamp")
                    # Alternately, seconds are not added keeping to specification (elif used for readability)
                    elif not seconds_on_tags:
                        timestamp = datetime.now().strftime("%d%m%Y%H%M")
                        log(get_line_number(), "verbose loop", timestamp, "<-- no seconds on tags timestamp")

                    # If quantity is larger than 5:
                    if quantity_count_on_tag and quantity > 5:
                        # (number) is added to the end of the timestamp - User doesn't have to wait for a new timestamp
                        # tag is made up of a timestamp(number)-standard_or_special ~ name and cost are also included
                        temp_list = [f"{timestamp}({i + 1}){standard_or_special}", name, cost]
                        log(get_line_number(), "verbose loop", temp_list, "`temp_list`")
                    else:
                        # tag is just timestamp-standard_or_special
                        temp_list = [timestamp + standard_or_special, name, cost]
                        log(get_line_number(), "verbose loop", temp_list, "`temp_list`")
                        # If quantity is larger than 1
                        if quantity > 1:
                            # The program will wait 1 second so the tag timestamp will be unique
                            # This only happens if quantity is not displayed instead (`quantity_amount_on_tag` = False)
                            time.sleep(1)

                    # Append `temp_list` to the final order
                    order_list.append(temp_list)
                    log(get_line_number(), "loop", order_list, "<-- `order_list`")

        # Else, `user_in` must equal "done"
        else:
            log(get_line_number(), "info", user_in, "user is done with order")
            # finish loop
            keep_going = False
            # make_receipt and make-tags using the `order_list`
            log(get_line_number(), "call function", f"make_receipt({order_list})", "make_receipt(order_list)")
            make_receipt(order_list)
            log(get_line_number(), "call function", f"make_tags({order_list})", "make_tags(order_list)")
            make_tags(order_list)


# While the program is running ---> start a new order
while True:
    # The config file can block the prompt for quantity altogether
    if allow_do_quantity:
        # The user can choose to use the quantity feature or not
        if select_either("Would you like to be prompted for quantity?") == "y":
            # stored in a variable
            do_quantity = True
            log(get_line_number(), "info", do_quantity, "do_quantity true - user can input quantity of order items")
        else:
            # stored in a variable
            do_quantity = False
            log(get_line_number(), "info", do_quantity,
                "do_quantity false - quantity will default to 1 - user will not be prompted")
    else:
        # stored in a variable
        do_quantity = False
        log(get_line_number(), "info", do_quantity,
            "do_quantity false - quantity will default to 1 - user will not be prompted")
    # Start the main make_order function
    log(get_line_number(), "call function", "make_order()")
    make_order()

    # If the user wants to quit they can choose to do so
    if select_either("Quit?") == "y":
        # Message and artificial wait
        print("Closing...")
        time.sleep(0.65)
        log(get_line_number(), "QUIT", "now i guess", "The user has chosen to quit - bye!")
        # Program quits
        quit(code=None)
