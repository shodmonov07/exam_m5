import psycopg2
import threading
import time
import requests


# 1-masala
def create_table():
    conn = psycopg2.connect(host='localhost',
                            database='mydatabase',
                            port='5433',
                            user='postgres',
                            password='0707')
    curr = conn.cursor()
    curr.execute('''CREATE TABLE Product (
                    id         SERIAL PRIMARY KEY,
                    name       VARCHAR(255) NOT NULL,
                    price      NUMERIC NOT NULL,
                    color      VARCHAR(50),
                    image      VARCHAR(255)
                );''')
    conn.commit()
    curr.close()
    conn.close()


# 2-masala
def insert_product(name, price, color, image):
    conn = psycopg2.connect(host='localhost',
                            database='mydatabase',
                            port='5433',
                            user='postgres',
                            password='0707')
    curr = conn.cursor()
    curr.execute("INSERT INTO product (name, price, color, image) VALUES (%s, %s, %s, %s)",
                 (name, price, color, image))
    conn.commit()
    curr.close()
    conn.close()


def select_all_products():
    conn = psycopg2.connect(host='localhost',
                            database='mydatabase',
                            port='5433',
                            user='postgres',
                            password='0707')
    curr = conn.cursor()
    curr.execute("SELECT * FROM product")
    rows = curr.fetchall()
    for row in rows:
        print(row)
    curr.close()
    conn.close()


def update_product(product_id, name, price, color, image):
    conn = psycopg2.connect(host='localhost',
                            database='mydatabase',
                            port='5433',
                            user='postgres',
                            password='0707')
    curr = conn.cursor()
    curr.execute("UPDATE product SET name=%s, price=%s, color=%s, image=%s WHERE id=%s",
                 (name, price, color, image, product_id))
    conn.commit()
    curr.close()
    conn.close()


def delete_product(product_id):
    conn = psycopg2.connect(host='localhost',
                            database='mydatabase',
                            port='5433',
                            user='postgres',
                            password='0707')
    curr = conn.cursor()
    curr.execute("DELETE FROM product WHERE id=%s", (product_id,))
    conn.commit()
    curr.close()
    conn.close()


# 3-masala
class Alphabet:
    def __init__(self):
        self.letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.letters):
            letter = self.letters[self.index]
            self.index += 1
            return letter
        else:
            raise StopIteration


# 4-masala
def print_numbers():
    for i in range(1, 16):
        print(i)
        time.sleep(1)


def print_letters():
    for letter in 'ABCDE':
        print(letter)
        time.sleep(1)


t1 = threading.Thread(target=print_numbers)
t2 = threading.Thread(target=print_letters)
t1.start()
t2.start()
t1.join()
t2.join()


# 5-masala
class Product:
    def __init__(self, name, price, color, image):
        self.name = name
        self.price = price
        self.color = color
        self.image = image

    def save(self):
        conn = psycopg2.connect(host='localhost',
                                database='mydatabase',
                                port='5433',
                                user='postgres',
                                password='0707')
        curr = conn.cursor()
        curr.execute("INSERT INTO product (name, price, color, image) VALUES (%s, %s, %s, %s)",
                     (self.name, self.price, self.color, self.image))
        conn.commit()
        curr.close()
        conn.close()


# 6-masala
class DbConnect:
    def __init__(self, host, database, port, user, password):
        self.host = host
        self.database = database
        self.port = port
        self.user = user
        self.password = password

    def __enter__(self):
        self.conn = psycopg2.connect(
            host=self.host,
            database=self.database,
            port=self.port,
            user=self.user,
            password=self.password
        )
        self.cur = self.conn.cursor()
        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.cur.close()
        self.conn.close()


# 7-masala
def save_to_product():
    response = requests.get("https://dummyjson.com/products")
    products = response.json()['products']

    conn = psycopg2.connect(host='localhost',
                            database='mydatabase',
                            port='5433',
                            user='postgres',
                            password='0707')
    curr = conn.cursor()

    for product in products:
        curr.execute("INSERT INTO product (id, name, price, color, image) "
                     "VALUES (%s, %s, %s, %s, %s)",
                     (product['id'],
                      product['title'],
                      product['price'],
                      product['description'],
                      product['thumbnail']))

    conn.commit()
    curr.close()
    conn.close()


create_table()
insert_product("cooker", 500.0, "black", "cooker.jpg")
insert_product("macbook", 1500.0, "grey", "laptop.jpg")
select_all_products()
update_product(1, "cooker", 500.0, "white", "cooker2.jpg")
select_all_products()
delete_product(2)
select_all_products()

alphabet = Alphabet()
for letter in alphabet:
    print(letter)

p = Product("iphone 15 pro", 1250.0, "titanium", "phone.jpg")
p.save()

with DbConnect("localhost",
               "mydatabase",
               "5433",
               "postgres",
               "0707") as cur:
    cur.execute("SELECT * FROM Product")
    print(cur.fetchall())

save_to_product()
