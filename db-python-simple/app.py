import sqlite3
import pandas as pd
import re
from colorama import Fore, Style
from email_validator import validate_email, EmailNotValidError

#QUERYS
query_mostrar=("""

  SELECT id, Nombre, Correo, Edad, Numero FROM Users WHERE Status<>? ;

""")

query_cambios=("""

    SELECT id, Nombre, Correo, Edad, Numero FROM Users WHERE id=? ;

""")

query_crear=("""

  INSERT INTO Users (Nombre, Correo, Edad, Numero, Status)
  VALUES
  (?, ?, ?, ?, 1);

""")

query_cambiar_estado=("""
      UPDATE Users
      SET Status=?
      WHERE id=? AND Status=? LIMIT 1
  """)

query_buscar=("""

  SELECT * FROM Users WHERE id=? AND Status=?;

""")


query_email=("""

SELECT * FROM Users WHERE Correo=?;

""")

#Mostrar datos
def show_table(query, status):
  """
    Muestra el el contenido de la base segun el argumento dado.
    Si la tabla esta vacia muestra un mensaje.
    En pandas

    Args:
      query(str).
      status(int).
  """
  df=pd.read_sql(query, connection, params=(status,))

  if df.empty:
    print("\n")
    print(Fore.YELLOW + f'Tabla vacia!' + Style.RESET_ALL)
  else:
    print("\n")
    print(df.to_string(index=False))
    print("\n")


#Buscar
def search(id,status):
  """
    Comprueba si el id existe.

    Args:
        id(int).
        status(int).

    Returns:
      bool: True o False, dependiendo del resultado
  """

  cursor.execute(query_buscar, (id,status))

  if cursor.fetchone():
    return True
  else:
    return False


#Ejecutar querys
def execute_query(query, parametros):
  """
    Ejecuta diferentes querys

    Args:
      query(str).
      parametros(tuple): Contiene todos los parametros que se utlizan en el query-

    Raises:
      sqlite3.IntegrityError: Si ha ucurrido un error de integridad.

  """
  try:
    cursor.execute(query, parametros)
    connection.commit()
    print("\n")
    print(Fore.GREEN + f"Accion realizada con exito" + Style.RESET_ALL)

  except sqlite3.IntegrityError:
    print("\n")
    print(Fore.RED + f"Ha ocurrido un error, intentelo de nuevo" + Style.RESET_ALL)



#Nombre
def name_input():
  """
    Pide y comprueba un nombre valido


    Returns:
      str:El nombre.

  """
  while True:
    nombre= input("Ingrese el nombre: ").strip()

    if len(nombre)<3 or len(nombre)>45:
      print(Fore.YELLOW + "El nombre debe tener entre 3 y 45 letras." + Style.RESET_ALL)
      continue

    if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s'’-]+$", nombre):
      print(Fore.YELLOW + "El nombre solo puede contener letras, espacios, apóstrofos o guiones." + Style.RESET_ALL)
      continue

    if not nombre.isalpha():
      print(Fore.YELLOW + f"Debes ingresar un nombre válido" + Style.RESET_ALL)
      continue
    else:
      return nombre

    if len(set(nombre))==1 and nombre[0]== ' ':
      print(Fore.YELLOW + "El nombre no puede estar vacío o ser solo espacios." + Style.RESET_ALL)
      continue

    return nombre



#Email
def email_input():
  """
    Pide y comprueba un correo valido.

    Returns:
      str:El correo.
        float: El promedio de los números en la lista.

  """
  regex = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
  while True:
    correo = input("Ingrese el correo: ").strip()

    try:
      valid = validate_email(correo)
      correo = valid.email
    except EmailNotValidError:
      print(Fore.YELLOW + f"Debe ingresar un correo válido" + Style.RESET_ALL)
      continue



    cursor.execute(query_email,(correo,))



    if cursor.fetchone():
      print(Fore.YELLOW + f"Correo ya está en uso" + Style.RESET_ALL)
      continue
    else:
      return correo





#Edad
def age_input():
  """
    Pide y comprueba una edad valida.

    Returns:
      str:La edad.
  """
  while True:

    edad=input("Ingrese la edad: ")

    if not edad.isdigit():
      print(Fore.YELLOW + f"Debe ingresar una edad" + Style.RESET_ALL)
      continue
    elif not 0<int(edad)<120:
      print(Fore.YELLOW + f"La edad debe ser real" + Style.RESET_ALL)
      continue
    else:
      return edad


#Numero
def number_input():
  """
    Pide y comprueba un numero valido.

    Returns:
      str:El numero.
 """
  while True:

    numero=input("Ingrese el numero: ")


    if not numero.isdigit():
      print(Fore.YELLOW + f"Ingrese un numero válido" + Style.RESET_ALL)
      continue
    elif len(numero)!=10:
      print(Fore.YELLOW + f"Ingrese un numero de diez dígitos" + Style.RESET_ALL)
      continue
    else:
      return numero
      break

#ID
def id_input(status):
  """
    Pide y busca un id valido.

    Args:
      status(int).

    Returns:
      int: El id.

    Raises:
        ValueError: Si se ha ingresado otro tipo de informacion.
  """
  while True:
    try:
      id=int(input("Ingrese el id: "))
    except ValueError:
      print(Fore.RED + f"Valor inválido" + Style.RESET_ALL)
      continue

    if search(id,status)==True:
      return id
    else:
      print(Fore.YELLOW + f"Usuario no existe" + Style.RESET_ALL)
      continue




def edit(col, val, id):
  """
    Arma una query para poder editar una columna.

    Args:
      col(str): La columna a editar.
      val(str): El nuevo valor.
      id(int): El id.

    Returns:
        float: El promedio de los números en la lista.

  """

  query_edit=(f"""

  UPDATE Users
  SET {col}=?
  WHERE id=? AND Status=1

  """)
  parametros=(val,id)
  execute_query(query_edit,parametros)




def change_status(status, new_status):
  while True:
    print(Fore.BLUE + f"""
    -------------------------------------------------
    Ingrese lo siguiente:
    *-El ID a eliminar
    *-'Salir' para regresar
    -------------------------------------------------
        """ + Style.RESET_ALL)
    id=input("Escriba una opción: ")
    id=id.strip()
    id=id.title()



    if id=="Salir":
      print(Fore.GREEN + f"Proceso terminado con exito" + Style.RESET_ALL)
      break
    elif search(id,status):
      parameters=(new_status,id,status)
      execute_query(query_cambiar_estado,parameters)
      show_table(query_mostrar, new_status)
      continue
    else:
      print(Fore.YELLOW + f"ID no se encuentra" + Style.RESET_ALL)
      continue
if __name__=="__main__":

  connection = sqlite3.connect("Database.db")

  cursor=connection.cursor()
  aux_menu=0
  while aux_menu!=7:
      try:
          print(Fore.BLUE + f"""
  -------------------------------------------------
  1.-Ver datos
  2.-Ver usuarios eliminados
  3.-Crear
  4.-Editar
  5.-Borrar
  6.-Deshacer (Activar)
  7.-Salir
  -------------------------------------------------
          """ + Style.RESET_ALL)
          aux_menu=int(input("Seleccione una opción: "))
          #Mostrar tablas
          if aux_menu==1:
            show_table(query_mostrar, 0)
          #Mostrar tablas de eliminados
          elif aux_menu==2:
            show_table(query_mostrar, 1)
          #Crear
          elif aux_menu==3:
            show_table(query_mostrar, 0)

            parameters = (name_input(), email_input(), age_input(), number_input())

            execute_query(query_crear, parameters)
          #Editar
          elif aux_menu==4:
            show_table(query_mostrar, 0)
            id=id_input(1)
            while True:
              print(Fore.BLUE + f"""
          -------------------------------------------------
          Ingrese lo siguiente:
          *-La columna a editar
          *-'Todas' para editar todas las columnas
          *-'Salir' para regresar
          -------------------------------------------------
                  """ + Style.RESET_ALL)

              col=input("Escriba una opción : ")
              col=col.strip()
              col=col.title()

              if col=="Nombre":
                nombre=name_input()
                edit(col,nombre,id)
                show_table(query_cambios, id)
                continue
              elif col=="Correo":
                correo=email_input()
                edit(col,correo,id)
                show_table(query_cambios, id)
                continue
              elif col=="Edad":
                edad=age_input()
                edit(col,edad,id)
                show_table(query_cambios, id)
                print(edad)
                continue
              elif col=="Numero":
                numero=number_input()
                edit(col,numero,id)
                show_table(query_cambios, id)
                continue

              elif col=="Todas":
                nombre=name_input()
                edit("Nombre",nombre,id)

                correo=email_input()
                edit("Correo",correo,id)

                edad=age_input()
                edit("Edad",edad,id)

                numero=number_input()
                edit("Numero",numero,id)

                show_table(query_cambios, id)
              elif col=="Salir" or col=="SALIR":
                break
              else:
                print("\n")
                print(Fore.YELLOW + f"La columna no existe" + Style.RESET_ALL)
                continue
          #Eliminar
          elif aux_menu==5:
            show_table(query_mostrar, 0)
            change_status(1,0)

          #Activar
          elif aux_menu==6:
            show_table(query_mostrar, 1)
            change_status(0,1)
          #Despedida
          elif aux_menu==7:
            print(Fore.GREEN + f"Bye!!" + Style.RESET_ALL)
          else:
            print("\n")
            print(Fore.YELLOW + f"{aux_menu} no es una opción" + Style.RESET_ALL)

      except ValueError:
        print("\n")
        print(Fore.RED +f"Ha ingresado un valor inválido" + Style.RESET_ALL)

  connection.close()
