from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson import ObjectId

# Configuración inicial de Flask y PyMongo
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/biblioteca"  # Cambia la URI según tu configuración de MongoDB

mongo = PyMongo(app)
libros_collection = mongo.db.libros  # Colección de libros en MongoDB


# Definición del modelo Libro usando SQLAlchemy
class Libro(db.Model):
    __tablename__ = 'libros'
    id = Column(Integer, primary_key=True)
    titulo = Column(String(100), nullable=False)
    autor = Column(String(100), nullable=False)
    anio = Column(Integer, nullable=False)

# Crear la tabla si no existe
def crear_tabla():
    db.create_all()

# Agregar nuevo libro
def agregar_libro():
    titulo = input("Título del libro: ")
    autor = input("Autor del libro: ")
    anio = int(input("Año de publicación: "))

    nuevo_libro = Libro(titulo=titulo, autor=autor, anio=anio)
    db.session.add(nuevo_libro)
    db.session.commit()
    print(f"Libro '{titulo}' agregado exitosamente.")

# Actualizar libro existente
def actualizar_libro():
    id_libro = int(input("ID del libro a actualizar: "))
    libro = Libro.query.get(id_libro)

    if libro:
        libro.titulo = input("Nuevo título del libro: ")
        libro.autor = input("Nuevo autor del libro: ")
        libro.anio = int(input("Nuevo año de publicación: "))
        db.session.commit()
        print(f"Libro ID '{id_libro}' actualizado exitosamente.")
    else:
        print(f"Libro ID '{id_libro}' no encontrado.")

# Eliminar libro existente
def eliminar_libro():
    id_libro = int(input("ID del libro a eliminar: "))
    libro = Libro.query.get(id_libro)

    if libro:
        db.session.delete(libro)
        db.session.commit()
        print(f"Libro ID '{id_libro}' eliminado exitosamente.")
    else:
        print(f"Libro ID '{id_libro}' no encontrado.")

# Ver listado de libros
def ver_libros():
    libros = Libro.query.all()

    if libros:
        print("Listado de libros:")
        for libro in libros:
            print(f"ID: {libro.id}, Título: {libro.titulo}, Autor: {libro.autor}, Año: {libro.anio}")
    else:
        print("No hay libros en la biblioteca.")

# Buscar libro por título
def buscar_libro():
    titulo = input("Título del libro a buscar: ")
    libros = Libro.query.filter(Libro.titulo.like(f"%{titulo}%")).all()

    if libros:
        print("Libros encontrados:")
        for libro in libros:
            print(f"ID: {libro.id}, Autor: {libro.autor}, Año: {libro.anio}")
    else:
        print("No se encontraron libros con ese título.")

# Función principal del menú
def menu():
    crear_tabla()  # Asegurar que la tabla de libros exista
    while True:
        print("\n--- Biblioteca de Libros ---")
        print("1. Agregar nuevo libro")
        print("2. Actualizar libro existente")
        print("3. Eliminar libro existente")
        print("4. Ver listado de libros")
        print("5. Buscar libro por título")
        print("6. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            agregar_libro()
        elif opcion == '2':
            actualizar_libro()
        elif opcion == '3':
            eliminar_libro()
        elif opcion == '4':
            ver_libros()
        elif opcion == '5':
            buscar_libro()
        elif opcion == '6':
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Intente nuevamente.")

# Ejecutar el programa
if __name__ == "__main__":
    menu()