import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Conexión a la base de datos
def conectar_bd():
    return sqlite3.connect("sistema_experto.db")

# Crear base de datos y tabla
def inicializar_base_datos():
    conexion = conectar_bd()
    cursor = conexion.cursor()

    # Crear la tabla automoviles
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS automoviles (
            id_automovil INTEGER PRIMARY KEY AUTOINCREMENT,
            marca TEXT,
            modelo TEXT,
            precio REAL,
            tipo TEXT,
            economia_combustible TEXT,
            calificacion_seguridad INTEGER,
            anio INTEGER,
            bolsas_aire INTEGER,
            kilometraje REAL
        )
    """)

    # Insertar datos iniciales si la tabla está vacía
    cursor.execute("SELECT COUNT(*) FROM automoviles")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO automoviles (marca, modelo, precio, tipo, economia_combustible, calificacion_seguridad, anio, bolsas_aire, kilometraje) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [
                ("Toyota", "Corolla", 180000, "compacto", "alta", 5, 2020, 6, 15000),
                ("Ford", "Mustang", 350000, "deportivo", "baja", 4, 2019, 4, 25000),
                ("Honda", "Civic", 200000, "compacto", "alta", 5, 2021, 6, 12000),
                ("Chevrolet", "Tahoe", 500000, "SUV", "media", 5, 2018, 8, 30000),
                ("Hyundai", "Elantra", 190000, "compacto", "alta", 4, 2022, 6, 10000),
                ("Kia", "Rio", 160000, "subcompacto", "alta", 4, 2020, 4, 20000),
                ("Nissan", "Versa", 170000, "subcompacto", "alta", 5, 2021, 6, 15000),
                ("Toyota", "Prius", 240000, "híbrido", "alta", 5, 2022, 8, 8000),
                ("Honda", "Insight", 250000, "híbrido", "alta", 5, 2021, 6, 9000),
                ("Ford", "Escape Hybrid", 300000, "SUV", "alta", 5, 2020, 8, 18000)
            ]
        )

    conexion.commit()
    conexion.close()

# Motor de inferencia sencillo
def inferir_automovil_por_precio(precio):
    conexion = conectar_bd()
    cursor = conexion.cursor()

    # Seleccionamos los autos por precio
    cursor.execute("SELECT * FROM automoviles WHERE precio <= ?", (precio,))
    resultados = cursor.fetchall()

    conexion.close()
    return resultados

# Función para mostrar recomendaciones en tabla
def mostrar_recomendaciones(recomendaciones):
    ventana_resultados = tk.Toplevel()
    ventana_resultados.title("Resultados de Recomendación")
    ventana_resultados.geometry("800x400")

    # Crear tabla
    columnas = ["Marca", "Modelo", "Precio", "Tipo", "Economía", "Seguridad", "Año", "Bolsas de Aire", "Kilometraje"]
    tabla = ttk.Treeview(ventana_resultados, columns=columnas, show="headings")

    for col in columnas:
        tabla.heading(col, text=col)

    # Insertar datos
    for auto in recomendaciones:
        tabla.insert("", tk.END, values=auto[1:])

    tabla.pack(fill=tk.BOTH, expand=True)

# Funciones para la interfaz de usuario
def recomendar_autos():
    try:
        presupuesto = float(entry_presupuesto.get())
        recomendaciones = inferir_automovil_por_precio(presupuesto)

        if recomendaciones:
            mostrar_recomendaciones(recomendaciones)
        else:
            messagebox.showinfo("Recomendaciones", "No se encontraron automóviles dentro del presupuesto.")
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese un presupuesto válido.")

# Interfaz de usuario
def interfaz_usuario():
    ventana = tk.Tk()
    ventana.title("Sistema Experto - Selección de Automóviles")
    ventana.geometry("400x300")

    tk.Label(ventana, text="Presupuesto (MXN):").pack(pady=5)

    global entry_presupuesto
    entry_presupuesto = tk.Entry(ventana)
    entry_presupuesto.pack(pady=5)

    tk.Button(ventana, text="Recomendar Automóviles", command=recomendar_autos).pack(pady=10)

    ventana.mainloop()

# Ejecutar la interfaz de usuario
if __name__ == "__main__":
    inicializar_base_datos()
    interfaz_usuario()
