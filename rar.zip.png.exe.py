import sqlite3
import random
import shutil

## i do not like using the OS module (that i've noticed bas has a fondness for), as it is OS specific; there might be errors for non-unix users (windows) that i will be unable to test
## i didn't know how to use classes in a way that benifits the program, so i am using them as functions, of sorts.

dbase = "xinvet.db"
connection = sqlite3.connect(dbase)

class initilisation:
    def create_tables(self):
        cursor = connection.cursor()
        query = """
        create table if not exists customers (
        uuid integer primary key autoincrement,
        fname tinytext,
        lname tinytext,
        phone int,
        email tinytext,
        address tinytext,
        city tinytext,
        postal_code tinytext);
        """
        cursor.execute(query)

        query = """
        create table if not exists pets (
        id integer primary key autoincrement,
        name tinytext,
        type tinytext,
        breed tinytext,
        birthdate date,
        owner_uuid int);
        """
        cursor.execute(query)

        query = """
        create table if not exists visits (
        id integer primary key autoincrement,
        ownder_uuid int,
        pet_id int,
        details text,
        cost real,
        paid real);
        """
        cursor.execute(query)


class program:
    def userinstruction(self):
        cursor = connection.cursor()
        userwant = int(input(f"what would you like to do? \n   [1] add a new customer, including all relavent information \n   [2] edit customer data \n   [3] display all customer data \n (input here): "))
        instructiondone = 0
        while instructiondone == 0:
            if userwant == 1:
                fname = input("what is the customer's first name?: ")
                lname = input("what is the customer's last name?: ")
                phonegood = 0
                while phonegood == 0:
                    phone = str(input("what is the customer's phone number? \n(enter without dashes or spaces; for example, if the phone number is \"604-123-4567\", then enter \"6041234567\": "))
                    if len(phone) == 10:
                        phonegood = 1
                    else:
                        print("please enter a valid phone number")
                email = input("what is the customer's email address?: ")
                address = input("what is the customer's address?: ")
                city = input("what is the customer's city?: ")
                postal_code = input("what is the customer's postal code?: (example: \"A1B 2C3\")")

                query = f"insert into customers (fname,lname,phone,email,address,city,postal_code) values ('{fname}','{lname}',{phone},'{email}','{address}','{city}','{postal_code}');"
                instructiondone = 1
                cursor.execute(query)
                connection.commit()

            if userwant == 2:
                uuid_enter = input("Enter the UUID of the customer you want to edit: ")
                edit_value = input("Which field would you like to edit? (fname, lname, phone, email, address, city, postal_code): ")
                new_value = input(f"Enter the new value for {edit_value}: ")

                if new_value in ["fname", "lname", "email", "address", "city", "postal_code"]:
                    new_value = f"'{new_value}'"

                query = f"UPDATE customers SET {edit_value} = {new_value} WHERE uuid = {uuid_enter};"
                cursor.execute(query)
                connection.commit()
                print("Customer data has been updated")
                instructiondone = 1

            elif userwant == 3:
                terminal_size = shutil.get_terminal_size()
                terminal_width = terminal_size.columns
                if terminal_width < 130:
                    input("terminal width is too small, please resize terminal width to at least 130 characters. \n (press enter to continue)")
                query = "SELECT * FROM customers;"
                cursor.execute(query)
                rows = cursor.fetchall()
                print("\nCustomer Data:")
                print(f"{'UUID':<10}{'First Name':<15}{'Last Name':<15}{'Phone':<15}{'Email':<25}{'Address':<20}{'City':<15}{'Postal Code':<10}")
                print("一" * 65)
                for row in rows:
                    print(f"{row[0]:<10}{row[1]:<15}{row[2]:<15}{row[3]:<15}{row[4]:<25}{row[5]:<20}{row[6]:<15}{row[7]:<10}")
                print("一" * 65)
                instructiondone = 1

            if userwant != 1 and userwant != 2 and userwant != 3:
                print("error: invalid input, please try again")

init = initilisation()
init.create_tables()
execute = program()
execute.userinstruction()