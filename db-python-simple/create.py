import sqlite3
import pandas as pd
import re
from colorama import Fore, Style
from email_validator import validate_email, EmailNotValidError

connection = sqlite3.connect("Database.db")

cursor=connection.cursor()


try:
  query_create_table=("""

    CREATE TABLE Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Nombre TEXT NOT NULL,
    Correo TEXT NOT NULL UNIQUE,
    Edad INTEGER NOT NULL,
    Numero INTEGER NOT NULL,
    Status Integer NOT NULL
    );

  """)

  cursor.execute(query_create_table)

  query_insert=("""

  INSERT INTO Users (Nombre, Correo, Edad, Numero, Status)
  VALUES
  ('Pablo', 'pablo@example.com', 25, 5512345678, 1),
  ('Pedro', 'pedro@example.com', 30, 5598765432, 1),
  ('Lucía', 'lucia@example.com', 28, 5543210987, 1),
  ('María', 'maria@example.com', 22, 5587654321, 1),
  ('Carlos', 'carlos@example.com', 35, 5523456789, 1),
  ('Sofía', 'sofia@example.com', 27, 5578901234, 1),
  ('Jorge', 'jorge@example.com', 40, 5590123456, 1),
  ('Ana', 'ana@example.com', 33, 5545678901, 1),
  ('Luis', 'luis@example.com', 24, 5589012345, 1),
  ('Fernanda', 'fernanda@example.com', 29, 5567890123, 1);
  """)



  cursor.execute(query_insert)
  connection.commit()
except sqlite3.OperationalError:
  print("La base de datos ya existe")

connection.close()
