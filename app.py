from database import *

# creating database name variable to use it later
database = "taxi.db"

# create a database connection
conn = create_connection(database)

if not conn:
    print("Error! cannot create the database connection.")
    exit()

create_tables(conn)

# create dummy company and drivers
if (not get_drivers(conn)):
    company_data = ("BedsTaxi Ltd",)
    company_id = create_company(conn, company_data)
    driver_data = ("Sam", "Callsen", "+446943869549", "BMW", "Red", company_id)
    create_driver(conn, driver_data)
    driver_data = ("Sasha", "Kowalski", "+44677454332", "Lada", "Black", company_id)
    create_driver(conn, driver_data)

current_user = None

def register():
    global current_user

    email = input("Email: ")
    password = input("Password: ")
    first_name = input("First name: ")
    last_name = input("Last name: ")
    phone_number = input("Phone number: ")

    data = (email, password, first_name, last_name, phone_number)
    current_user = create_customer(conn,data)
    
    print(f"Hello {first_name}, Your account has been created.")
    input("Press any key to continue...")
    show_menu()

def login():
    global current_user

    email = input("Email: ")
    password = input("Password: ")

    data = (email,password)
    try: 
        user = login_customer(conn, data)
        user_id = user[0]
        user_first_name = user[3]
        current_user = user_id
    except:
        print("Bad email or password.")
        show_menu()

    print(f"Hello {user_first_name}, You are logged in.")    
    input("Press any key to continue...")
    show_menu()

def create_booking():
    drivers = get_drivers(conn)
    print("Available drivers:")
    for i, driver in enumerate(drivers):
        print(str(i)+"."+str(driver[1])+" "+str(driver[2]))
    
    _input = input("Select option: ")
    index = int(_input)
    driver = drivers[index]
    driver_id = driver[0]
    customer_id = current_user
    start_time = input("Start time: ")
    start_place = input("Start place: ")
    end_time = input("End time: ")
    end_place = input("End place: ")
    payment_method = input("Payment method: ")

    data = (driver_id, customer_id, start_time, start_place, end_time, end_place, payment_method)
    trip = create_trip(conn, data)
    print("Booking created!")
    input("Press any key to continue...")
    show_menu()

def show_bookings():
    bookings = get_trips(conn)
    if not bookings:
        print("No bookings.")
    else:
        print("Available bookings:")
        for i, booking in enumerate(bookings):
            print(str(i)+". "+str(booking[5])+" -> "+str(booking[7]))
        
    input("Press any key to continue...")
    show_menu()

def remove_booking():
    bookings = get_trips(conn)

    if not bookings:
        print("No bookings.")
    else:
        print("Select booking to delete:")
        for i, booking in enumerate(bookings):
            print(str(i)+". "+str(booking[5])+" -> "+str(booking[7]))
        
        _input = input("Select option: ")
        index = int(_input)
        booking = bookings[index]
        booking_id = booking[0]

        delete_trip(conn, booking_id)
        print("Booking deleted.")
    input("Press any key to continue...")
    show_menu()

def show_menu():
    if(not current_user):
        print("1.Register")
        print("2.Login")
        _input = input("Select option: ")

        if _input == "1":
            register()
        elif _input == "2":
            login()

    else:
        print("1.Make Booking")
        print("2.View Bookings")
        print("3.Cancel Booking")
        _input = input("Select option: ")

        if _input == "1":
            create_booking()

        elif _input == "2":
            show_bookings()

        elif _input == "3":
            remove_booking()

    


show_menu()
