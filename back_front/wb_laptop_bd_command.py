import psycopg2
from psycopg2 import OperationalError


def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    except Exception as e:
        print(f"Произошло исключение: '{e}'")
    return connection

connection = create_connection("postgres","postgres","postgres","postgres","5432")


def create_database(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    except Exception as e:
        print("База данных уже существует")
        pass
create_database_query = "CREATE DATABASE experiment"
create_database(connection, create_database_query)


def create_connection_db(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection


connection = create_connection_db("experiment","postgres","postgres","postgres","5432")


def execute_query(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Query(table) executed successfully")
    except OperationalError as e:
        print(f"The error '{e}' occurred")

create_features_table = """
CREATE TABLE IF NOT EXISTS features (
    id SERIAL PRIMARY KEY,
    number_of_photos int,
    full_name varchar(100),
    brand varchar(100),
    product_code int,
    price_with_a_discount int,
    price_without_a_discount int,
    grade varchar(100),
    total_assessments int,
    review_list text,
    color varchar(100),
    model varchar(100),
    a_series_of_laptops varchar(100),
    operating_system varchar(100),
    the_version_of_the_operating_system varchar(100),
    warranty_period varchar(100),
    the_diagonal_of_the_screen varchar,
    type_of_matrix varchar(100),
    screen_resolution varchar(100),
    update_frequency varchar(100),
    the_surface_of_the_screen varchar(100),
    the_ram_volume_gb varchar(100),
    type_of_ram varchar(100),
    the_number_of_ram_slots varchar(100),
    expansion_of_ram varchar(100),
    support_for_memory_cards varchar(100),
    battery_capacity varchar(100),
    working_time_from_the_battery varchar(100),
    cpu varchar(100),
    processor_line varchar(100),
    the_processor_clock_frequency varchar(100),
    the_number_of_processor_nuclei varchar(100),
    cache_memory varchar(100),
    wireless_interfaces varchar(100),
    usb_2_0_port varchar(100),
    port_usb_3_x varchar(100),
    usb_c_port varchar(100),
    memory_card_connector varchar(100),
    headphone_microphone_jack_3_5mm varchar(100),
    hdmi_connector varchar(100),
    the_connector_m_2 varchar(100),
    lan_connector_rj45 varchar(100),
    interface varchar(100),
    webcam varchar(100),
    ssd_volume varchar(100),
    type_of_drive varchar(100),
    type_of_video_card varchar(100),
    video_card varchar(100),
    the_video_card_volume varchar(100),
    corps_material varchar(100),
    game_laptop varchar(100),
    keyboard_layout varchar(100),
    keyboard_backlight varchar(100),
    additional_laptop_options varchar(500),
    complete varchar(500),
    the_country_of_production varchar(100),
    weight_without_packaging_kg varchar(100),
    packaging_weight_kg varchar(100),
    the_width_of_the_subject varchar(100),
    the_depth_of_the_subject varchar(100),
    the_thickness_of_the_subject varchar(100),
    the_length_of_the_package varchar(100),
    the_height_of_the_packaging varchar(100),
    the_width_of_the_packaging varchar(100)
)
"""

execute_query(connection, create_features_table)


def check_column(column):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        query = """SELECT TABLE_NAME 
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE COLUMN_NAME = '%s' """ % column
        cursor.execute(query)
        result = cursor.fetchall()
        if len(result) == 0:
            print("[INFO] Такой колонки нет")
            return 0
        else:
            print("[X] Такая колонка существует")
            return 1
    except OperationalError as e:
        print(f"The error '{e}' occurred")

def column_query(column):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(f"""
                        Alter table features add {column} varchar(100) 
                        """)
        print("New Column executed successfully")
    except OperationalError as e:
        print(f"The error '{e}' occurred")


def insert_news(b,g):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(f"""
                        INSERT INTO features ({b}) 
                        VALUES ({g})
                            """)
        print("InsertQuery executed successfully")
    except OperationalError as e:
        print(f"The error '{e}' occurred")


def check_news(title):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        query = "Select product_code from features where product_code = %s" % title
        cursor.execute(query)
        result = cursor.fetchall()
        if len(result) == 0:
            print("[INFO] Такой записи нет")
            return 0
        else:
            print("[X] Такая запись существует")
            return 1
    except OperationalError as e:
        print(f"The error '{e}' occurred")


def get_data_from_db():
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM features")
        data_set = cursor.fetchall()
        return data_set
    except OperationalError as e:
        print(f"The error '{e}' occurred")


def get_distinct_data_from_db(parameter):
    cursor = connection.cursor()
    try:
        cursor.execute(f"SELECT distinct {parameter} from features")
        data_set = cursor.fetchall()
        return data_set
    except OperationalError as e:
        print(f"The error '{e}' occurred")

def get_filtr_from_db(query):
    cursor = connection.cursor()
    try:
        cursor.execute(f"{query}")
        data_set = cursor.fetchall()
        return data_set
    except OperationalError as e:
        print(f"The error '{e}' occurred")

def get_columns_from_db():
    cursor = connection.cursor()
    try:
        cursor.execute("""SELECT column_name FROM information_schema.columns 
                       WHERE table_name = 'features' ORDER BY ordinal_position""")
        data_set = cursor.fetchall()
        return data_set
    except OperationalError as e:
        print(f"The error '{e}' occurred")
