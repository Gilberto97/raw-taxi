import sqlite3
from sqlite3 import Error

# functions to manage our database:

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None

    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    
    return conn

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def create_customer(conn, customer):
    sql = ''' INSERT INTO customers(email, password, first_name, last_name, phone_number)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, customer)
    conn.commit()
    return cur.lastrowid


def create_driver(conn, driver):
    sql = ''' INSERT INTO drivers(first_name, last_name, phone_number, car_model, car_color, company_id)
              VALUES(?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, driver)
    conn.commit()
    return cur.lastrowid

def create_company(conn, company):
    sql = ''' INSERT INTO companies(name)
              VALUES(?) '''
    cur = conn.cursor()
    cur.execute(sql, company)
    conn.commit()
    return cur.lastrowid

def create_trip(conn, trip):
    sql = ''' INSERT INTO trips(driver_id, customer_id, start_time, start_place, end_time, end_place, payment_method)
              VALUES(?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, trip)
    conn.commit()
    return cur.lastrowid

def create_tables(conn):
    sql_create_companies_table = """ CREATE TABLE IF NOT EXISTS companies (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL
                                ); """
    
    sql_create_drivers_table = """ CREATE TABLE IF NOT EXISTS drivers (
                                        id integer PRIMARY KEY,
                                        first_name text NOT NULL,
                                        last_name text NOT NULL,
                                        phone_number text UNIQUE,
                                        car_model text NOT NULL,
                                        car_color text,
                                        company_id integer NOT NULL,
                                        FOREIGN KEY (company_id) REFERENCES companies (id)
                                    ); """
    
    sql_create_customers_table = """ CREATE TABLE IF NOT EXISTS customers (
                                        id integer PRIMARY KEY,
                                        email text UNIQUE NOT NULL,
                                        password text NOT NULL,
                                        first_name text NOT NULL,
                                        last_name text NOT NULL,
                                        phone_number text
                                    ); """

    sql_create_trips_table = """ CREATE TABLE IF NOT EXISTS trips (
                                    id integer PRIMARY KEY,
                                    driver_id integer NOT NULL,
                                    customer_id integer NOT NULL,
                                    start_time text NOT NULL,
                                    start_place text NOT NULL,
                                    end_time text NOT NULL,
                                    end_place text NOT NULL,
                                    payment_method text NOT NULL,
                                    FOREIGN KEY (driver_id) REFERENCES drivers (id),
                                    FOREIGN KEY (customer_id) REFERENCES customers (id)
                                ); """
    
    # create customers table
    create_table(conn, sql_create_customers_table)
    # create drivers table
    create_table(conn, sql_create_drivers_table)
    # create companies table
    create_table(conn, sql_create_companies_table)
    # # create trips table
    create_table(conn, sql_create_trips_table)
    
def login_customer(conn, user):
    sql = ''' SELECT * FROM customers WHERE email=? AND password=?'''
    cur = conn.cursor()
    cur.execute(sql, user)
    first = cur.fetchall()[0] 
    return first

def get_drivers(conn):
    sql = ''' SELECT * FROM drivers'''
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()

def get_trips(conn):
    sql = ''' SELECT * FROM trips'''
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()

def delete_trip(conn, id):
    sql = 'DELETE FROM trips WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()


