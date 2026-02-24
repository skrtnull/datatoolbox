from kit import DataToolBox
import pandas as pd
import os

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

# 1. Inicializar y cargar configuración
info = DataToolBox()
info.Configure() 

limpiar_pantalla()

# --- NUEVA SECCIÓN: VER TABLA AL PRINCIPIO ---
print("=======================================================")
print("             REGLAS DE LIMPIEZA ACTUALES               ")
print("=======================================================")
if info.config is not None and not info.config.empty:
    # Usamos el modo portable para ver la tabla directamente en consola
    info.View(filas=20, portable=True, list=info.config)
else:
    print("\n[!] La tabla de configuración está vacía o no existe.")
print("=======================================================\n")

# --- MENÚ PRINCIPAL ---
print("¿Qué desea hacer?")
print("(1) AGREGAR: Añadir nuevas reglas a las existentes.")
print("(2) REEMPLAZAR: Borrar TODO y crear configuración nueva.")
print("(3) SALIR")
print("-------------------------------------------------------")

modo = input("\nSeleccione cómo desea proceder: ")

if modo in ["1", "2"]:
    # Determinamos el modo de ExportSQL basado en la elección inicial
    metodo_guardado = "append" if modo == "1" else "replace"
    
    limpiar_pantalla()
    if modo == "1":
        print(">>> MODO ACTUAL: AGREGAR REGLAS\n")
    else:
        print(">>> MODO ACTUAL: REEMPLAZAR (Se borrarán los datos anteriores al guardar)\n")

    # --- CAPTURA DE DATOS ---
    columna = input("-> Nombre de la columna a configurar: ")
    
    print("\nTipos disponibles:")
    print("(1) int (Entero)")
    print("(2) str (Texto)")
    print("(3) date (Fecha)")
    print("(4) decimal (Flotante)")
    
    opc_tipo = input("\nSeleccione tipo (1-4): ")
    mapa = {"1": "int", "2": "str", "3": "date", "4": "decimal"}
    tipo = mapa.get(opc_tipo, "str")
    
    digitos = input("\n-> Cantidad de dígitos/decimales (0 si no aplica): ")
    digitos = int(digitos) if digitos.isdigit() else 0

    # --- PROCESAMIENTO ---
    opciones = pd.DataFrame([{
        "Columna": columna,
        "Tipo": tipo,
        "Digitos": digitos
    }])

    # Cargamos el DataFrame en el objeto
    info.Refresh(opciones)
    
    # Exportamos usando el método elegido (append o replace)
    # Importante: Asegúrate que en kit.py ExportSQL acepte el argumento 'modo'
    info.ExportSQL("configuracion", modo=metodo_guardado)
    
    print(f"\n✅ Proceso completado exitosamente en modo: {metodo_guardado.upper()}")
    input("\nPresione Enter para finalizar...")

else:
    print("\nSaliendo del programa.")