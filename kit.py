from __future__ import annotations
from typing import Optional, Any, Union
import pandas as pd
import numpy as np
import time
from datetime import datetime
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, text
from sqlalchemy.orm import declarative_base, sessionmaker
import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, PatternMatchingEventHandler

#Clase para monitorear archivos automaticamente
class MyEventHandler(PatternMatchingEventHandler):

    def __init__(self, kit_instance: DataToolBox):
        # USAMOS EL FILTRO ORIGINAL DE WATCHDOG AQUÍ:
        super().__init__(
            patterns=["*.csv", "*.xlsx", "*.xls", "*.json", "*.parquet"], 
            ignore_patterns=None,
            ignore_directories=True, 
            case_sensitive=False
        )
        self.kit = kit_instance

    def on_created(self, event):
        if not event.is_directory:
            print(event.src_path, f"Archivo detectado [{event.src_path}].")
            self.kit.Autorun("bandeja")
        

#-----------------------------------------------------------------------------------

#Clase de heramienta ETL DATATOOLBOX
class DataToolBox():

    def __init__(self, file:Optional[str] =None):

        # 1. Definimos las variables con valores por defecto SIEMPRE al principio
        self.df = pd.DataFrame()
        self.ruta = "" 
        self.engine = None

        #configuraciones de automatisacion
        self.config_st = None
        self.config_op = None

        if file is not None:
        
            # Si nos pasaron un DataFrame directamente
            if isinstance(file, pd.DataFrame):
                self.df = file
                print("✅ Objeto cargado desde DataFrame.")
                
            # Si nos pasaron un string (ruta de archivo)
            elif isinstance(file, str) and file != "":
    
                try:

                    # Extraemos la extensión (ej: '.parquet', '.csv')
                    _, extension = os.path.splitext(file)
                    extension = extension.lower()

                    match extension:

                        case  '.csv':
                            self.df = pd.read_csv(file)
                            self.ruta = file  # Solo se actualiza si la carga es real
                            print(f"✅ Archivo '{file}' cargado con éxito.")

                        case   '.parquet':
                            self.df = pd.read_parquet(file)
                            self.ruta = file  # Solo se actualiza si la carga es real
                            print(f"✅ Archivo '{file}' cargado con éxito.")

                        case   '.json':
                            self.df = pd.read_json(file)
                            self.ruta = file  # Solo se actualiza si la carga es real
                            print(f"✅ Archivo '{file}' cargado con éxito.")

                        case   '.xlsx':
                            self.df = pd.read_excel(file)
                            self.ruta = file  # Solo se actualiza si la carga es real
                            print(f"✅ Archivo '{file}' cargado con éxito.")

                        case   '.xls':
                            self.df = pd.read_excel(file)
                            self.ruta = file  # Solo se actualiza si la carga es real
                            print(f"✅ Archivo '{file}' cargado con éxito.")

                        case _:
                            raise ValueError(f"Formato {extension} no soportado")
                    
                except Exception as e:
                    print(f"⚠️ No se pudo cargar '{file}': {e}")
    
    #enlista los archivos que hayan en la ruta escogida
    def List_files(self, ruta_carpeta:str ="./", extension:str =".csv"):
        
        try:
            # Listamos todo y filtramos por extensión y que sea archivo
            archivos = [f for f in os.listdir(ruta_carpeta) 
                       if f.endswith(extension) and os.path.isfile(os.path.join(ruta_carpeta, f))]
            
            if not archivos:
                print(f"⚠️ No se encontraron archivos {extension} en: {ruta_carpeta}")
            else:
                print(f"📂 Archivos detectados en '{ruta_carpeta}': \n")
                
                for i,files in enumerate(archivos, start=1):
                    print (f"({i}) {files}") 
            
            return archivos
        except Exception as e:
            print(f"Aun no se ah establecido una ruta: {e}")
            return []

    #limpiar terminal
    def limpiar_pantalla(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    #----------------------------Configuracion---------------------------------------

    #menu para configurar la automatizacion\
    def Menu(self):

        info = DataToolBox()
        info.Configure() 

        while True:
            info.limpiar_pantalla()
            print("=======================================================")
            print("             DATATOOLBOX: PANEL DE CONTROL             ")
            print("=======================================================\n")

            # --- VISTA DE ESTADO ---
            print(f"[1] REGLAS DE LIMPIEZA: {'✅ ' + str(len(info.config_st)) if not info.config_st.empty else '❌ Vacía'}")
            info.View(20, True, info.config_st)
            print(f"\n[2] OPERACIONES:        {'✅ ' + str(len(info.config_op)) if not info.config_op.empty else '❌ Vacía'}")
            info.View(20, True, info.config_op)
            print("\n=======================================================")
            print("1. GESTIONAR LIMPIEZA (Configuracion)")
            print("2. GESTIONAR OPERACIONES (Operaciones)")
            print("3. INICIAR TUBERIA AUTOMATICA")
            print("4. SALIR")
            print("=======================================================")

            menu_principal = input("\nSeleccione una sección: ")

            if menu_principal == "1":
                # --- SUBMENÚ LIMPIEZA ---
                while True:

                    info.limpiar_pantalla()
                    print(">>> GESTIÓN DE LIMPIEZA")
                    if not info.config_st.empty:
                        info.View(20, True, info.config_st)

                    #pone si el usuario ingresa un valor que no es valido
                    try:
                    
                        print("\n[1] Agregar Regla  [2] Herramientas  [3] Resetear esta tabla  [4] Volver")
                        sub = int(input("\nSelección: "))

                        if sub == 1:

                            col = input("Columna: ")

                            print("\n[1] int")
                            print("[2] str")
                            print("[3] date")
                            tipo = int(input("\nSeleccione el tipo de datos: "))

                            if tipo == 1:
                                tipo = "int"
                                dig = int(input("Dígitos: ") or 0)
                                print("\n[1] Conservar filas sin digitos")
                                print("[2] Eliminar filas sin digitos")
                                lvl = int(input("\nNivel de limpieza: ") or 0)
                            elif tipo == 2:
                                tipo = "str"
                                dig = 0
                                print("\n[1] Conservar numeros")
                                print("[2] Sin numeros")
                                lvl = int(input("\nNivel de limpieza: ") or 0)
                            elif tipo == 3:
                                tipo = "date"
                                dig = 0
                                print("\n[1] Conservar filas sin fechas")
                                print("[2] Eliminar filas sin fechas")
                                lvl = int(input("\nNivel de limpieza: ") or 0)
                            elif tipo == 4:
                                tipo = "decimal"
                                dig = int(input("Dígitos: ") or 0)
                                lvl=0
                                
                            info.Consulta(f"INSERT INTO Configuracion (Columna, Tipo, Digitos, Lvl) VALUES ('{col}', '{tipo}', '{dig}', '{lvl}');")
                            info.Configure() # Recarga para mostrar cambios
                        
                        elif sub == 2:

                            col = input("Columna: ")

                            print("\n[1] Estandarizar ID")
                            print("[2] Decimal")
                            print("[3] Outliers")
                            print("[4] Limpieza de estructura")
                            print("[5] Extractor de Email/Telefono\n")
                            tipo = int(input("Seleccione el tipo de datos: "))

                            if tipo == 1:
                                tipo = "id"
                            elif tipo == 2:
                                tipo = "decimal"
                            elif tipo == 3:
                                tipo = "outliers"
                            elif tipo == 4:
                                tipo = "structure"
                            elif tipo == 5:
                                tipo = "extract"
                            
                            dig = 0
                            lvl=0

                            info.Consulta(f"INSERT INTO Configuracion (Columna, Tipo, Digitos, Lvl) VALUES ('{col}', '{tipo}', '{dig}', '{lvl}');")
                            info.Configure() # Recarga para mostrar cambios

                        elif sub == 3:

                            print ("[1] borrar solo una configuracion")
                            print ("[2] restablecer todsas las configuraciones")
                            ops = int(input ("seleccion: "))


                            if ops == 1:
                                
                                # 1. Solicitar el índice a eliminar
                                try:
                                    fill = int(input("Número de configuración a eliminar: ")) 
                                    
                                    # 2. SINCRONIZACIÓN: ExportSQL usa 'self.df', así que cargamos la configuración allí
                                    info.df = info.config_st.copy()

                                    # 3. Borrado selectivo y reseteo de índices
                                    if fill in info.df.index:
                                        info.df = info.df.drop(labels=fill, axis=0).reset_index(drop=True)
                                        
                                        # Actualizamos la variable de estado para que la vista se refresque
                                        info.config_st = info.df.copy()

                                        # 4. PERSISTENCIA: Ahora 'self.df' tiene la lista corregida, la subimos al SQL
                                        info.ExportSQL("Configuracion", modo="replace")
                                        
                                        # 5. RECARGA: Volvemos a leer de SQL para asegurar integridad
                                        info.Configure()
                                        print(f"✅ Configuración {fill} eliminada correctamente.")
                                    else:
                                        print(f"⚠️ El índice {fill} no existe en la lista actual.")
                                        
                                except ValueError:
                                    print("❌ Error: Por favor ingresa un número válido.")
                                
                                input('\nPresiona Enter para continuar...')

                            elif ops == 2:
                                
                                info.Consulta("DROP TABLE IF EXISTS Configuracion;")
                                print("✅ Tabla eliminada por completo.")
                                
                                info.Configure()
                                # Lógica igual al menú de limpieza (Reset)
                                print("\n--- 🔄 DESHACER CAMBIOS ---")
                                
                        elif sub == 4:
                            break
                        
                    except Exception as e:
                        # --- CASO GENERAL: OTROS ERRORES (ej. letras en vez de números) ---
                        print(f"Asegurece de ingresar respuestas validas")
                        print(f"❌ ERROR INESPERADO: {e}")
                                        
            elif menu_principal == "2":


                # --- SUBMENÚ OPERACIONES ---
                # CONFIGURAR OPERACIONES
                while True:

                    info.limpiar_pantalla()
                    print(">>> GESTIÓN DE LIMPIEZA")
                    if not info.config_op.empty:
                        info.View(20, True, info.config_op)
                        
                    print("\n--- ⚙️ CONFIGURAR OPERACIONES ---")
                    print("[1] Operadores Lógicos (Básicos)")
                    print("[2] Fórmulas (Calculadora Plus)")
                    print("[3] Deshacer cambios")
                    print("[4] Volver al Menú Principal")
                    

                    #filtramos los errores errores
                    try:

                        sub_opc = input("\nSeleccione una subsección: ").strip()

                        if sub_opc == "1":
                            print("\n--- ➕ OPERADORES LÓGICOS ---")
                            print("[1] Suma\n[2] Resta\n[3] Multiplicación\n[4] División\n[5] Volver")
                            op_log = input("Seleccione operación: ").strip()
                            
                            # Mapeo según los casos de tu función Calculadora()
                            mapeo_log = {"1": "+", "2": "-", "3": "*", "4": "/"}
                            
                            if op_log in mapeo_log:
                                op = mapeo_log[op_log]
                                col1 = input("Nombre de la Columna A: ")
                                col2 = input("Nombre de la Columna B: ")
                                col3 = input("Nombre de la nueva columna (Opcional): ")
                                
                                info.Consulta(f"INSERT INTO Operaciones (Preconfig, Op, Col1, Col2, Col3) VALUES ('', '{op}', '{col1}', '{col2}', '{col3}');")
                                info.Configure() # Recarga para mostrar cambios
                                
                            elif op_log == "5": continue

                        elif sub_opc == "2":
                            # --- SECCIÓN DE FÓRMULAS (CALCULADORA PLUS COMPLETA) ---
                            print("\n--- 🧪 FÓRMULAS DISPONIBLES (TODOS LOS CASOS) ---")
                            print("[1] Costo Unitario")
                            print("[2] Subtotal (Cantidad * Precio)")
                            print("[3] IVA")
                            print("[4] Descuento")
                            print("[5] Precio Final (Subtotal + Imp - Desc)")
                            print("[6] Margen Bruto")
                            print("[7] Margen PCT (%)")
                            print("[8] Margen Porcentual")
                            print("[9] Envío por KG")
                            print("[10] Conversión Divisa")
                            print("[11] Rango (Categorización Mayor/Menor)")
                            print("[12] Volver")

                            op_plus = input("\nSeleccione la fórmula: ").strip()

                            # Mapeo exacto a los 'case' en kit.py
                            mapeo_plus = {
                                "1": "costo_unitario",
                                "2": "subtotal",
                                "3": "iva",
                                "4": "descuento",
                                "5": "precio_final",
                                "6": "margen_bruto",
                                "7": "margen_pct",
                                "8": "margen_porcent",
                                "9": "envio_KG",
                                "10": "conversion_divisa",
                                "11": "rango"
                            }
                        
                            if op_plus in mapeo_plus:
                                op = mapeo_plus[op_plus]
                                col1 = input("Nombre de la Columna A: ")

                                if op_plus == "iva" or "descuento":
                                    col2 = input("Ingrese el porcentaje: ")
                                else:
                                    col2 = input("Ingrese el porcentaje: ")

                                if op_plus == "precio_final":
                                    col3 = input("Porcentaje de descuento: ")
                                else:
                                    col3 = ""
                                
                                info.Consulta(f"INSERT INTO Operaciones (Preconfig, Op, Col1, Col2, Col3) VALUES ('{op}', '', '{col1}', '{col2}', '{col3}');")
                                info.Configure() # Recarga para mostrar cambios

                        elif sub_opc == "3":

                            print ("[1] borrar solo una configuracion")
                            print ("[2] restablecer todsas las configuraciones")
                            ops = int(input ("seleccion: "))


                            if ops == 1:
                                
                                # 1. Solicitar el índice a eliminar
                                try:
                                    fill = int(input("Número de Operaciones a eliminar: ")) 
                                    
                                    # 2. SINCRONIZACIÓN: ExportSQL usa 'self.df', así que cargamos la Operacion allí
                                    info.df = info.config_op.copy()

                                    # 3. Borrado selectivo y reseteo de índices
                                    if fill in info.df.index:
                                        info.df = info.df.drop(labels=fill, axis=0).reset_index(drop=True)
                                        
                                        # Actualizamos la variable de estado para que la vista se refresque
                                        info.config_op = info.df.copy()

                                        # 4. PERSISTENCIA: Ahora 'self.df' tiene la lista corregida, la subimos al SQL
                                        info.ExportSQL("Operaciones", modo="replace")
                                        
                                        # 5. RECARGA: Volvemos a leer de SQL para asegurar integridad
                                        info.Configure()
                                        print(f"✅ Operaciones {fill} eliminada correctamente.")
                                    else:
                                        print(f"⚠️ El índice {fill} no existe en la lista actual.")
                                        
                                except ValueError:
                                    print("❌ Error: Por favor ingresa un número válido.")
                                
                                input('\nPresiona Enter para continuar...')

                            elif ops == 2:

                                info.Consulta("DROP TABLE IF EXISTS Operaciones;")
                                print("✅ Tabla eliminada por completo.")
                                
                                info.Configure()
                                # Lógica igual al menú de limpieza (Reset)
                                print("\n--- 🔄 DESHACER CAMBIOS ---")

                        elif sub_opc == "4":
                            break  # Rompe el bucle interno para volver al menú principal
                        
                        else:
                            print("❌ Opción inválida, intente de nuevo.")


                    except Exception as e:
                        # --- CASO GENERAL: OTROS ERRORES (ej. letras en vez de números) ---
                        print(f"Asegurece de ingresar respuestas validas")
                        print(f"❌ ERROR INESPERADO: {e}")
                    
            elif menu_principal == "3":
                print("-------- [INICIANDO TUBERIA] -------------")
                ruta = input("Nombre de carpeta para bigilar: ")
                info.Autorun(ruta)
                break

            elif menu_principal == "4":
                print("Saliendo...")
                break

    #script para escanear periodicamente la bandeja de procesameinto
    def Autorun(self, bandeja):

        #--------------------Configuraciones----------------------------

        df_st = self.config_st
        df_op = self.config_op

        #---------------------------------------------------------------
    
        # Obtener lista de todos los archivos en la carpeta
        archivos = os.listdir(bandeja)
        
        #consulta si existe la carpeta bandeja
        if not os.path.exists(bandeja):
            os.makedirs(bandeja, exist_ok=True)

        #Consulta la bandeja de procesados
        if not os.path.exists(f"{bandeja}/procesados/."):
            os.makedirs(f"{bandeja}/procesados/.", exist_ok=True)

        #Consulta la bandeja de archivos originales
        if not os.path.exists(f"{bandeja}/original/."):
            os.makedirs(f"{bandeja}/original/.", exist_ok=True)

        print(f"🔍 Escaneando carpeta: {bandeja}")
        
        for archivo in archivos:
            # Filtramos para no leer carpetas o archivos ocultos
            if archivo.endswith(('.csv', '.xlsx', 'xls', '.parquet', 'json')):
                ruta_completa = os.path.join(bandeja, archivo)
                print(f"📌 Archivo encontrado para procesar: {archivo}\n")
                # Aquí llamarías a tu: tool.Load(ruta_completa)

                self.Refresh(ruta_completa)
                # Mover el archivo original a una carpeta de histórico
                shutil.move(ruta_completa, os.path.join(f"{bandeja}/original/.", archivo))

                #------------------Auto-Limpieza------------------ 

                try:

                    for regla in df_st.itertuples():
                        
                        columna = regla.Columna
                        tipo = regla.Tipo
                        lvl = regla.Lvl
                        digitos = regla.Digitos
                        
                        if self.config_st.empty:

                            print ("\n🔥No hay datos para limpiar") 
                        
                        else:

                            #----------------HERRAMIENTAS----------------

                            if tipo == "structure":
                                self.Clean("structure")

                    for regla in df_st.itertuples():
                    
                        columna = regla.Columna
                        tipo = regla.Tipo
                        lvl = regla.Lvl
                        digitos = regla.Digitos
                        
                        if self.config_st.empty:

                            print ("\n🔥No hay datos para limpiar") 
                        
                        else:

                            #-----------------LIMPIEZA------------------

                            if tipo == "int":
                                self.Clean("numb", columna, lvl)
                                self.Clean("decimal", columna, digitos)
                            elif tipo == "str":
                                self.Clean("text", columna, lvl)
                            elif tipo == "date":
                                self.Clean("date", columna, lvl)

                    for regla in df_st.itertuples():
                    
                        columna = regla.Columna
                        tipo = regla.Tipo
                        lvl = regla.Lvl
                        digitos = regla.Digitos
                        
                        if self.config_st.empty:

                            print ("\n🔥No hay datos para limpiar") 
                        
                        else:

                            #----------------HERRAMIENTAS----------------

                            if tipo == "decimal":
                                self.Clean("numb", columna, lvl)
                                self.Clean("decimal", columna, digitos)
                            
                    print ("🔥Limpieza Automatica realizada\n")   
                    
                except Exception as e:
                    # --- CASO GENERAL: OTROS ERRORES (ej. letras en vez de números) ---
                    print(f"❌ ERROR INESPERADO [Auto-limpieza]: {e}")    
                    
                #----------------Auto-Operaciones----------------       
                
                try:
                    
                    for regla in self.config_op.itertuples():

                        preconfig = regla.Preconfig
                        opera = regla.Op
                        #variables de calculo
                        col1 = regla.Col1
                        col2 = regla.Col2
                        col3 = regla.Col3
                        
                        if self.config_op.empty:

                            print ("\n🔥No hay operaciones para realizar") 
                        
                        else:

                            #en caso de no existir una preconfoguracion saltamops a una operacion manual
                            if preconfig is not None:

                                match preconfig:

                                    case "costo_unitario":
                                        #Subtotal: cantidad vendida + cantidad total 

                                        self.CalculadoraPlus(**{
                                        "tipo" : "costo_unitario",
                                        "col1" : col1,
                                        "col2" : col2                
                                        })

                                    case "subtotal":
                                        #Subtotal: cantidad * precio 

                                        self.CalculadoraPlus(**{
                                        "tipo" : "subtotal",
                                        "col1" : col1,
                                        "col2" : col2                
                                        })

                                    case "iva":
                                        # Fórmula: Subtotal * tasa

                                        #para calcular porcentaje
                                        col2 = int(col2) / 100
                                        
                                        self.CalculadoraPlus(**{
                                        "tipo" : "iva",
                                        "col1" : col1,
                                        "col2" : col2,              
                                        })
                                        
                                    case "descuento":
                                        # Fórmula: Precio * (1 - pct) (donde 0.10 son como 10%)

                                        #para calcular porcentaje
                                        col2 = int(col2) / 100

                                        self.CalculadoraPlus(**{
                                        "tipo" : "descuento",
                                        "col1" : col1,              
                                        "col2" : col2,              
                                        })

                                    case "margen_bruto":
                                        # Fórmula: Precio de venta - Costo
                                        
                                        self.CalculadoraPlus(**{
                                        "tipo" : "margen_bruto",
                                        "col1" : col1,
                                        "col2" : col2               
                                        })
                                        
                                    case "margen_pct":
                                        # Fórmula: (Margen / Ventas) * 100

                                        self.CalculadoraPlus(**{
                                        "tipo" : "margen_pct",
                                        "col1" : col1,
                                        "col2" : col2                
                                        })

                                    case "margen_porcent":
                                        # Fórmula: (Margen / Precio de Venta) * 100.
                                        
                                        self.CalculadoraPlus(**{
                                        "tipo" : "margen_porcent",
                                        "col1" : col1,
                                        "col2" : col2                
                                        })

                                    case "envio_KG":
                                        # Fórmula: Peso * Tarifa_por_Kg
                                        
                                        self.CalculadoraPlus(**{
                                        "tipo" : "envio_KG",
                                        "col1" : col1,
                                        "col2" : col2               
                                        })

                                    case "conversion_divisa":
                                        # Fórmula: Subtotal * tasa
                                        
                                        self.CalculadoraPlus(**{
                                        "tipo" : "conversion_divisa",
                                        "col1" : col1,
                                        "col2" : col2               
                                        })

                                    case "rango":

                                        self.CalculadoraPlus(**{
                                        "tipo" : "rango",
                                        "col1" : col1,
                                        "col2" : col2                
                                        })

                                    case "precio_final":
                                        # Fórmula: Precio Final: Subtotal + Impuestos - Descuentos
                                        
                                        self.CalculadoraPlus({
                                        "res" : "precio_final",
                                        "col1" : col1,
                                        "col2" : col2,
                                        "col3" : col3               
                                        })

                                    case _:

                                        print(f"Caso indefinido: [{preconfig}]")
                            
                            #la operacion manual
                            else:

                                match opera:

                                    case "+":

                                        #Calculamos subtotal
                                        self.CalculadoraPlus(**{
                                                                'tipo': 'subtotal',       # Define qué bloque del match-case entrará
                                                                'col1': col1,          # Primera columna
                                                                'col2': col2        # Segunda columna
                                                            })
                                    
                                    case "++":

                                        #Calculamos subtotal
                                        self.CalculadoraPlus(**{
                                                                'tipo': 'subtotal',       # Define qué bloque del match-case entrará
                                                                'col1': col1,          # Primera columna
                                                                'col2': col2        # Segunda columna
                                                            })
                                        
                                    case "-":

                                        #Calculamos subtotal
                                        self.CalculadoraPlus(**{
                                                                'tipo': 'subtotal',       # Define qué bloque del match-case entrará
                                                                'col1': col1,          # Primera columna
                                                                'col2': col2        # Segunda columna
                                                            })
                                        
                                    case "/":

                                        #Calculamos subtotal
                                        self.CalculadoraPlus(**{
                                                                'tipo': 'subtotal',       # Define qué bloque del match-case entrará
                                                                'col1': col1,          # Primera columna
                                                                'col2': col2        # Segunda columna
                                                            })
                                        
                                    case "*":

                                        #Calculamos subtotal
                                        self.CalculadoraPlus(**{
                                                                'tipo': 'subtotal',       # Define qué bloque del match-case entrará
                                                                'col1': col1,          # Primera columna
                                                                'col2': col2        # Segunda columna
                                                            })

                                    case _:

                                        print(f"Caso indefinido: [{opera}]")

                    print ("🔥Operaciones Automaticas realizada\n")   
                    
                except Exception as e:
                    # --- CASO GENERAL: OTROS ERRORES (ej. letras en vez de números) ---
                    print(f"❌ ERROR INESPERADO [Auto-Operaciones]: {e}")              

                #-----------------------EXPORTACION----------------------
                
                self.Export("procesado","bandeja/procesados")

        #-------------------------RESETEO--------------------------------
        
        print("Vigilando carpeta") 
        print("presione Crtl+C para finalizar script")

        try:

            class_ob = MyEventHandler(self)

            #aqui invocamos el observador de la carpeta para que cada que ingrese un archivo se dispare esta funcion
            observer = Observer()
            observer.schedule(class_ob, f"{bandeja}", recursive=False)
            observer.start()
            try:
                while observer.is_alive():
                    observer.join(1)
            except KeyboardInterrupt:
                observer.stop()
            observer.join()

        except Exception as e:
            # --- CASO GENERAL: OTROS ERRORES (ej. letras en vez de números) ---
            print(f"Posiblemente sea por no haber archivos para limpiar")              
            print(f"❌ ERROR INESPERADO [Vigilante]: {e}")              

    #configuraciones para autoarranque
    def Configure(self):

        if self.config_st is None:
            # Ejemplo de uso
            sql = {"red":"false",
                    "motor":"sqlite",
                    "bd":"config.bd"}
            
            self.Conexion(**sql)

        self.Consulta("""CREATE TABLE IF NOT EXISTS Configuracion (
                            ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            Columna TEXT NOT NULL,
                            Tipo TEXT NOT NULL,
                            Digitos INTEGER NOT NULL,
                            Lvl INTEGER NOT NULL
                        );""")
        
        self.Consulta("""CREATE TABLE IF NOT EXISTS Operaciones (
                            ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            Preconfig TEXT NOT NULL,
                            Op TEXT NOT NULL,
                            Col1 TEXT NOT NULL,
                            Col2 TEXT NOT NULL,
                            Col3 TEXT NOT NULL
                        );""")

        # 2. ASEGURAR TABLA (Si no, read_sql falla siempre)
        # pd.read_sql NO crea tablas. Necesitas esto:
        metadata = MetaData()

        config_rst = Table('Configuracion', metadata,
            Column('ID', Integer, primary_key=True, autoincrement=True),
            Column('Columna', String),
            Column('Tipo', String),
            Column('Lvl', Integer),
            Column('Digitos', Integer))
        
        # TABLA 2: Historial de la "Carpeta Bandeja" (Nueva)
        config_ops = Table('Operaciones', metadata,
            Column('ID', Integer, primary_key=True, autoincrement=True),
            Column('Preconfig', String),
            Column('Op', String),
            Column('Col1', String),
            Column('Col2', String),
            Column('Col3', String)
        )

        # EL TRUCO MÁGICO: Esto crea TODAS las tablas que estén en el metadata        
        metadata.create_all(self.engine) 

        # 3. Leer los datos
        try:
            self.config_st = pd.read_sql("SELECT * FROM Configuracion", self.engine)
            self.config_op = pd.read_sql("SELECT * FROM Operaciones", self.engine)
        except:
            self.config_st = pd.DataFrame()
            self.config_op= pd.DataFrame()
    
    #----------------------------SQL---------------------------------------

    # --- ESTRUCTURA INFALIBLE ---
    def Consulta(self, query_string):
        
        #motor para hacer consultas
        with self.engine.begin() as con:
            # Usamos text() para que SQLAlchemy no rechace el string
            con.execute(text(query_string))
        # Al salir del 'with', el COMMIT se hace solo.
        
    #conectamos con la base de datos
    def Conexion(self, **kwargs:Optional[str]):

        # if self.engine is not None:
        #     print("⚡ Conexión ya establecida. Saltando configuración...")
        #     return

            # Ejemplo de uso
            # sql = {"red":"true o false",
            #        "motor":"motor", 
            #        "usser":"usuario", 
            #        "password":"password", 
            #        "server":"servidor", 
            #        "puerto":"puerto", 
            #        "bd":"datos.bd"}
        
        if(kwargs.get('red') == True):

            #internet
            motor = kwargs.get('motor')
            usser = kwargs.get('usser')
            password = kwargs.get('password')
            server = kwargs.get('server')
            puerto = kwargs.get('puerto')
            bd = kwargs.get('bd')
            #asignamos ruta
            ruta = f"{motor}://{usser}:{password}@{server}:{puerto}/{bd}"

        else:

            #local
            bd = kwargs.get('bd')
            #asignamos ruta
            ruta = f"sqlite:///{bd}"

        #luego establecer la ruta se consultan los datos y los insertamos en el objeto
        try:

            #aqui va la ruta sql
            self.engine = create_engine(ruta)
            print("⚡ Conexión establecida.")

        except Exception as e:

            print(f"❌ Error al al cargar ruta: {e}")
            self.engine = None # Aseguramos que quede limpio si falla
            return []
    
    #convertir una tabla en un DataFrame
    def CargarTabla(self, tabla:str):

        if self.engine is None:

            print("⚠️ Error: Primero debes llamar a 'Conexion' antes de cargar una tabla.")
            return

        try:
            # Usamos pd.read_sql_query para extraer la información
            # Si pasas solo el nombre de una tabla, f-string la convierte en query
            query = f"SELECT * FROM {tabla}" if " " not in tabla else tabla
            
            self.df = pd.read_sql_query(query, self.engine)
            print(f"✅ Lista '{tabla}' cargada al DataFrame ({len(self.df)} filas).")

        except Exception as e:
            print(f"❌ Error al extraer datos de SQL: {e}")

    # Guardar el DataFrame actual en una tabla SQL
    def ExportSQL(self, tabla:str, modo:str ='append'):
        """
        Exporta el contenido de self.df a la base de datos conectada.
        modo 'append': Agrega los datos al final.
        modo 'replace': Borra la tabla y crea una nueva con los datos actuales.
        """
        # 1. Verificación de seguridad: ¿Hay conexión y hay datos?
        if self.engine is None:
            print("⚠️ ERROR: No hay conexión activa. Usa 'Conexion' primero.")
            return
            
        if self.df.empty:
            print("⚠️ Vaciando tabla.")

        try:

            # 1. Verificamos si queremos limpiar la tabla antes de meter datos nuevos
            # Pero lo hacemos con DELETE (SQL) no con DROP (Pandas)
            if modo == "replace":
                self.Consulta(f"DELETE FROM {tabla}")
                modo = "append" # Cambiamos a append para que no intente borrar la tabla otra vez
            
            # 2. Quitamos el ID de la memoria de Pandas si existe
            # Esto permite que la base de datos gestione su propio AUTOINCREMENT
            df_seguro = self.df.drop(columns=['ID', 'id'], errors='ignore')
            
            # 3. Insertamos
            df_seguro.to_sql(tabla, con=self.engine, if_exists=modo, index=False)
            
            print(f"✅ Datos exportados a {tabla} sin romper la estructura.")
            
        except Exception as e:
            print(f"❌ ERROR al exportar a SQL: {e}")
            self.Reporte(f"FALLO EXPORTACIÓN SQL: {e}")

    #---------------------------Utilieria------------------------------- 

    #Ver lista
    def View(self, filas:int =10, portable:bool =False, list:Optional[list] =None):

        if filas > 500:
            confirmar = input(f"⚠️ Vas a imprimir {filas} filas. ¿Seguro? (s/n): ")
            if confirmar.lower() != 's':
                return

        if (portable == True):
            """Imprime el DataFrame de forma segura y rápida"""
            print(f"\n>>> Mostrando {filas} filas de {list.shape[0]} totales:")
            # Usamos pd.option_context para forzar que no haya límites en filas ni columnas
            with pd.option_context('display.max_rows', None, 'display.max_columns', None):
                print(list.head(filas))
            print("-" * 30)
        else:
            """Imprime el DataFrame de forma segura y rápida"""
            print(f"\n>>> Mostrando {filas} filas de {self.df.shape[0]} totales:")
            # Usamos pd.option_context para forzar que no haya límites en filas ni columnas
            with pd.option_context('display.max_rows', None, 'display.max_columns', None):
                print(self.df.head(filas))
            print("-" * 30)

    #genera documento de texto con las operaciones realizadas
    def Reporte(self, mensaje:str):
        from datetime import datetime
        hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("factura_proceso.txt", "a", encoding="utf-8") as f:
            f.write(f"[{hora}] {mensaje}\n")

    #Renombras filas de una lista
    def Rename(self, esquema:Optional[str]):

        #Ejemplo de uso
        # cambios = {
        #     "Product_ID": "ID",
        #     "Item": "Producto",
        #     "Cost": "Precio"
        # }

        """
        Cambia el nombre de las columnas.
        Argumento 'esquema': un diccionario {'viejo': 'nuevo'}
        """
        try:
            self.df.rename(columns=esquema, inplace=True)
            print("✅ Columnas renombradas con éxito.")
        except Exception as e:
            print(f"❌ Error al renombrar: {e}")

    #refrescamos o asignamos una lista al dataframe
    def Refresh(self, file:str):

        if file is not None:
        
            # Si nos pasaron un DataFrame directamente
            if isinstance(file, pd.DataFrame):
                self.df = file
                print("✅ Objeto cargado desde DataFrame.")
                
            # Si nos pasaron un string (ruta de archivo)
            elif isinstance(file, str) and file != "":
    
                try:

                    # Extraemos la extensión (ej: '.parquet', '.csv')
                    _, extension = os.path.splitext(file)
                    extension = extension.lower()

                    match extension:

                        case  '.csv':
                            self.df = pd.read_csv(file)
                            self.ruta = file  # Solo se actualiza si la carga es real
                            print(f"✅ Archivo '{file}' cargado con éxito.")

                        case   '.parquet':
                            self.df = pd.read_parquet(file)
                            self.ruta = file  # Solo se actualiza si la carga es real
                            print(f"✅ Archivo '{file}' cargado con éxito.")

                        case   '.json':
                            self.df = pd.read_json(file)
                            self.ruta = file  # Solo se actualiza si la carga es real
                            print(f"✅ Archivo '{file}' cargado con éxito.")

                        case   '.xlsx':
                            self.df = pd.read_excel(file)
                            self.ruta = file  # Solo se actualiza si la carga es real
                            print(f"✅ Archivo '{file}' cargado con éxito.")

                        case   '.xls':
                            self.df = pd.read_excel(file)
                            self.ruta = file  # Solo se actualiza si la carga es real
                            print(f"✅ Archivo '{file}' cargado con éxito.")

                        case _:
                            raise ValueError(f"Formato {extension} no soportado")
                    
                except Exception as e:
                    print(f"⚠️ No se pudo cargar '{file}': {e}")
    
    #exportar a los formatos disponibles
    def Export(self, name:str= "archivo", carpeta:str= "./", formato:str = "csv"):

        try:

            if not os.path.exists(carpeta):
                os.makedirs(carpeta)
                
            match (formato):
            
                case 'csv':
                    ruta_completa = os.path.join(carpeta, f"{name}.csv")
                    self.df.to_csv(ruta_completa, index=False)
                case 'parquet':
                    ruta_completa = os.path.join(carpeta, f"{name}.parquet")
                    self.df.to_parquet(ruta_completa, engine='pyarrow', compression='snappy')
                case 'json':
                    ruta_completa = os.path.join(carpeta, f"{name}.json")
                    self.df.to_json(ruta_completa, orient='records', indent=4)
                case 'excel':
                    ruta_completa = os.path.join(carpeta, f"{name}.excel")
                    self.df.to_excel(ruta_completa, sheet_name=f"{name}")
            
            print(f"✅ ¡Éxito! Archivo guardado en: {ruta_completa}")
            self.Reporte(f"Exportación exitosa: {name}.{formato}") # Usando tu sistema de log
            
        except PermissionError:
            print(f"❌ ERROR: No se pudo guardar. Cierra el archivo '{name}.{formato}' si lo tienes abierto en Excel.")
        except Exception as e:
            print(f"❌ ERROR INESPERADO al exportar: {e}")
            self.Reporte(f"Fallo en exportación: {e}")

    #-------------------------Motor de Normalizacion---------------------------

    #Testear estado de lista
    def TestData(self):
        print("--- 📊 REPORTE DE INSPECCIÓN ---")

        # 1. ¿Cuántas filas y columnas tenemos en total?
        print(f"Dimensiones totales: {self.df.shape}") 

        # 2. ¿Qué columnas hay y de qué tipo son? (Para ver si Precio es número)
        print("\nTipos de datos por columna:")
        print(self.df.dtypes)

        # 3. ¿Hay valores nulos (vacíos) que se nos escaparon?
        print("\nConteo de valores nulos:")
        print(self.df.isnull().sum())

        #test de nulos
        resumen_nulos = self.df.isnull().sum()
        print(f"🔍 Mapa de huecos en el archivo:\n{resumen_nulos}")
        # Esto te dice el % de basura por columna
        print(f"\n📊 Porcentaje de suciedad:\n{(self.df.isnull().sum() / len(self.df)) * 100}%")

        # 4. Un resumen estadístico (Solo para las columnas numéricas como Precio)
        #print("\nResumen matemático del Precio:")
        #print(self.df.describe())

    #Unir verticalmente o horizontalemnte (con lado='h') 2 filas
    def Merge(self, add: DataToolBox, lado="v"):
        
        #horizontal
        if(lado == 'h' or lado == 'H'):
            lado=1
        #vertical
        elif(lado == 'v' or lado == 'V'):
            lado=0
        else:
            lado=0

            print ("Imprimiendo horizontal por defecto:")
            print ("Los valores permitidos son H (horizontal) o V (Vertical)")
        
        # 1. Verificamos que sea un objeto de nuestra clase
        if not hasattr(add, 'df'):
            print("❌ ERROR: Solo puedo unir con otro objeto DataToolBox")
            return

        # 2. Verificamos que las columnas coincidan
        if list(self.df.columns) != list(add.df.columns):
            print("⚠️ ALERTA: Las columnas no coinciden. El resultado tendrá valores vacíos (NaN).")

        # 3. Hacemos la unión
        self.df = pd.concat([self.df, add.df], ignore_index=True, axis=lado)
        print("🚀 Unión completada con éxito.")

    #unifacion de lista con extendido
    def MergePlus(self, rutas:str, lado:str='v'):
        #aqui se almacenaran las listas que no se puedan integrar
        rezagados=[]

        if isinstance(rutas, str):
            rutas = [rutas]
        
            for nombre in rutas:
                # 1. Filtro rápido: ¿Soy yo mismo? -> Salto
                if self.ruta == nombre:
                    continue
                    
                # 2. El paracaídas: Si algo falla adentro, no explota el código
                try:
                    nuevo_envio = DataToolBox(nombre)
                    
                    # 3. Validación de columnas
                    if list(self.df.columns) == list(nuevo_envio.df.columns):
                        self.Merge(nuevo_envio, lado)
                    # Dentro de MergePlus en kit.py
                    elif list(self.df.columns) != list(nuevo_envio.df.columns):
                        print("⚠️ ¡Cuidado! Las columnas no coinciden exactamente.")
                    else:
                        print ("Error inesperado")
                
                except Exception as e:
                    # Si el archivo no existe o está corrupto
                    print(f"❌ Error con {nombre}: {e}")
                    rezagados.append(nombre)

            else:
                # 2. El paracaídas: Si algo falla adentro, no explota el código
                try:
                    nuevo_envio = DataToolBox(nombre)
                    
                    # 3. Validación de columnas
                    if list(self.df.columns) == list(nuevo_envio.df.columns):
                        self.Merge(nuevo_envio, lado)
                    # Dentro de MergePlus en kit.py
                    elif list(self.df.columns) != list(nuevo_envio.df.columns):
                        print("⚠️ ¡Cuidado! Las columnas no coinciden exactamente.")
                    else:
                        print ("Error inesperado")
                
                except Exception as e:
                    # Si el archivo no existe o está corrupto
                    print(f"❌ Error con {nombre}: {e}")
                    rezagados.append(nombre)

        # 4. Aqui se imprimen los rezagados por unificar
        if rezagados: # 👈 Esto significa: "Si la lista NO está vacía"
            print("\n⚠️ Los siguientes archivos requieren revisión:")
            for archivo in rezagados:
                print(f" - {archivo}")
        else: # 👈 Esto significa: "Si la lista está vacía"
            print("✨ ¡Éxito total! No hubo rezagados.\n")

    #kit de limpieza
    def Clean(self, tipo:str, columna:str = None, lvl:int= 1, ops:str= None):

        try:

            match tipo:

                #Standart id
                case "id":

                    #Nos aseguramos de que no este vacio del dataframe
                    if not self.df.empty:
                                                
                        if ops is not None:
                            digits = ops 

                        #hacemos una copia para no afectar los datos originales
                        dupli = pd.DataFrame(self.df)
                        comp = pd.DataFrame(self.df)

                        if digits is not None:

                            comp[columna] = self.df[columna].astype(str).str.len()

                            #ids que no cumplen con el largo
                            malo = self.df[comp[columna] != digits]
                
                            #creamos el numero de ids segun el numero de filas de mala
                            ids = np.random.randint(1000, 10000, size=len(malo))
                            #reseteamos la indexacion de indices para poder reasginar las ids
                            malo.loc[:, columna] = ids

                            #digitos que cumplen con el largo
                            bueno = self.df[comp[columna] == digits]

                            #unificamos
                            self.df = pd.concat([bueno, malo], ignore_index=True, axis=0)
                        
                        ##------------------------------------------------------------

                        #detectamos los duplicados
                        dupli = dupli.duplicated(subset=[columna], keep=False)

                        #hacemos una copia para no afectar los datos originales
                        dupli = pd.DataFrame(self.df)
                        #detectamos los duplicados
                        dupli = dupli.duplicated(subset=[columna], keep=False)
                    
                        #mitad mala
                        mala = self.df[dupli]
                        #creamos el numero de ids segun el numero de filas de mala
                        ids = np.random.randint(1000, 10000, size=len(mala))
                        #reseteamos la indexacion de indices para poder reasginar las ids
                        mala.loc[:, columna] = ids
                        #mitad buena
                        buena = self.df[~dupli]
                        
                        #reasignamos ids
                        self.df = pd.concat([buena, mala], ignore_index=True, axis=0)

                    else:
                        print("⚠️ El archivo está vacío.")

                #Normalizar textos
                case "text":

                    #lvl 1 = eliman los simbolos y caracteres extra;os pero mantiene numeros
                    #lvl 2 = eliman los simbolos y numeros,  solo deja texto
                    
                    # Nos aseguramos de que no este vacio
                    if not self.df.empty:
                        
                        if lvl == 2:

                            # 2. 🔥 NUEVO: Eliminar símbolos (solo deja letras y espacios)
                            self.df[columna] = self.df[columna].str.replace(r'[^a-zA-Z\s]', '', regex=True)
                        
                        elif lvl == 1:

                            # 2. 🔥 NUEVO: Eliminar símbolos (solo deja letras, números y espacios)
                            self.df[columna] = self.df[columna].str.replace(r'[^a-zA-Z0-9\s]', '', regex=True)

                        # A. Limpiar espacios vacíos en los nombres y poner la primera en Mayúscula
                        # Quita espacios, pone todo en minúsculas y elimina acentos
                        self.df[columna] = self.df[columna].astype(str).str.strip().str.lower().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
                        
                        # .str.strip() quita espacios, .str.capitalize() pone la primera en mayúscula
                        self.df[columna] = self.df[columna].str.strip().str.capitalize()

                    else:
                        print("⚠️ El archivo está vacío.")

                #Normalizar numeros
                case "numb":

                    #lvl 1 = mantiene las filas que hayan quedado nulas por la depuracion
                    #lvl 2 = elimina la filas que queden nulas
                    
                    # Nos aseguramos de que no este vacio
                    if not self.df.empty:
                        
                        sib = ops 

                        #limpiamos los numeros de simbolos
                        if sib is not None:
                            if self.df[columna].dtype == 'object':
                                self.df[columna] = self.df[columna].str.replace(sib, '', regex=False)
                        #eliminamos cualquier presencia de letra
                        
                        # Extrae solo los números (0-9) y los une.
                        self.df[columna] = self.df[columna].astype(str).str.extract(r'(\d+)').astype(float)
                        #transformamor caracteres en numeros
                        self.df[columna] = pd.to_numeric(self.df[columna], errors='coerce')

                        if lvl == 2:
                            #eliminamos nulos
                            self.df[columna] = self.df[columna].fillna(0)
                        
                        #convertir en entero
                        self.df[columna] = self.df[columna].round(0).astype('Int64')

                    else:
                        print("⚠️ El archivo está vacío.")

                #Estandarizar fechas
                case "date":

                    #lvl 1 = deja las filas que queden nulas luego de la depuracion
                    #lvl 2 = elimina las filas que queden nulas
                    
                    #Nos aseguramos de que no este vacio
                    if not self.df.empty:
                        
                        ##Eliminamos espacios
                        self.df[columna] = self.df[columna].astype(str).str.strip() # Quita espacios
                        # Convierte a Fecha
                        self.df[columna] = pd.to_datetime(
                            self.df[columna], 
                            format='%d/%m/%Y', # <--- Aquí le dices exactamente cómo leerla
                            errors='coerce'
                        )

                        if lvl == 2:

                            # ahora donde haya NaT El subset asegura que SOLO eliminara solo esas fechas inexistentes
                            self.df = self.df .dropna(subset=[columna])
                        
                    else:
                        print("⚠️ El archivo está vacío.")

                #Limpiar decimales
                case "decimal":
                    
                    # Nos aseguramos de que no este vacio
                    if not self.df.empty:
                        
                        if ops is None:
                            decimales = 0
                        else:
                            decimales = ops
                            print (decimales)

                        # En kit.py, dentro de un nuevo método o en CalculadoraPlus
                        self.df[columna] = pd.to_numeric(self.df[columna], errors='coerce').round(decimales)
                                                    
                    else:
                        print("⚠️ El archivo está vacío.")
                    
                #limpiar datos mentirosos o con valores fuera de las metricas
                case "outliers":
                    
                    # Nos aseguramos de que no este vacio
                    if not self.df.empty:
                        
                        #normalizamos en caso que no se haya echo ya
                        self.df[columna] = pd.to_numeric(self.df[columna], errors='coerce')

                        #limpieza de lvl2
                        Q1 = self.df[columna].quantile(0.25)
                        Q3 = self.df[columna].quantile(0.75)
                        IQR = Q3 - Q1
                        # Solo deja los datos que están en el rango normal
                        self.df = self.df[~((self.df[columna] < (Q1 - 1.5 * IQR)) | (self.df[columna] > (Q3 + 1.5 * IQR)))]
                        
                    else:
                        print("⚠️ El archivo está vacío.")

                #Limpieza estructural: Eliminar filas inservibles o con todo nulos
                case "structure":
                    
                    # Nos aseguramos de que no este vacio
                    if not self.df.empty:
                        
                        # 1. Eliminamos filas donde TODOS los valores sean nulos
                        antes = len(self.df)
                        self.df = self.df.dropna(how='all')
                        
                        # 2. Eliminamos filas que tengan nulos en columnas críticas (ej. Producto)
                        despues = len(self.df)
                        print(f"🧹 Estructura limpiada: Se eliminaron {antes - despues} filas vacías.")
                        
                    else:
                        print("⚠️ El archivo está vacío.")

                #recuperar correo y numeros cuando la informacion en la columna sea ilegible
                case "extract":
                    
                    # Nos aseguramos de que no este vacio
                    if not self.df.empty:
                        
                        default:str=r"[\w\.-]+@[\w\.-]+"

                        if ops is not None:
                            patron = ops
                        else:
                            patron = default

                        # Por defecto busca emails, pero puedes pasarle cualquier patron
                        self.df[columna] = self.df[columna].str.findall(patron).str[0]
                        print("📧 Información extraída mediante patrones complejos.")
                        
                    else:
                        print("⚠️ El archivo está vacío.")

                #en caso de no estar asignado un caso
                case _:
                    
                    print("❌ Operación no válida: no se especifico operacion")

            print(f"✅ Cálculo de {tipo} completado.")
            self.Reporte(f"LIMPIEZA REALIZADA: {tipo} || PROCESO EXITOSO")
        
            return self.df
        
        except Exception as e:
            # --- CASO GENERAL: OTROS ERRORES (ej. letras en vez de números) ---
            print(f"❌ ERROR INESPERADO: {e}")
            self.Reporte(f"LIMPIEZA REALIZADA: {tipo} || ERROR: {e}")
    
    #cambia el nombre de columnas de acuerdo al orden que tengan
    def StandarCol(self, nuevos_nombres:str):
        """
        Fuerza el nombre de las columnas 
        sin importar cómo se llamen originalmente,
        funciona en base al orden que se configure.
        """
        if (nuevos_nombres != None):
            nuevos_nombres = {
                self.df.columns[0]: 'ID',
                self.df.columns[1]: 'Producto',
                self.df.columns[2]: 'Precio'
            }
            self.Rename(nuevos_nombres)

    #---------------------------Motor de calculo-------------------------------

    #Operaciones y formulas de calculo
    def Calculadora(self, config:Optional[str]):

        op = config.get('op')
        res = config.get('res')
        c1 = config.get('col1')
        c2 = None
        c2 = config.get('col2')
        pase = config.get('pass', False)

        if pase is not True:
            
            # 1. Verificamos que las columnas de origen existan en el DataFrame
            if c1 not in self.df.columns or c2 not in self.df.columns:
                print(f"⚠️ ERROR: No se puede calcular '{res}'.")
                print(f"Faltan columnas: {[c for c in [c1, c2] if c not in self.df.columns]}")
                return # Salimos de la función sin romper el programa

        else:

            if c1 not in self.df.columns:
                print(f"⚠️ ERROR: No se puede calcular '{res}'.")
                print(f"Faltan columnas: {[c for c in [c1, c2] if c not in self.df.columns]}")
                return # Salimos de la función sin romper el programa

        # 1. Preparamos los operandos: ¿Son columnas o números?
        # Si c1 está en las columnas, usamos la serie; si no, usamos el valor tal cual

        if c1 in self.df.columns:
            val1 = self.df[c1] 
        else: 
            val1 = c1
            if c1 is None:
                c1 = 0
            
        if c2 in self.df.columns:
            val2 = self.df[c2] 
        else: 
            val2 = c2
            if c2 is None:
                c2 = 0

        #self.View(20, True, val1)
        #print (val2)

        # 2. Si existen, procedemos con el match-case que ya hiciste
        
        match op:

            case "+":

                try:
                    ## Lógica para sumar
                    resultado_calculado = val1 + val2
                except Exception as e:
                    print(f"❌ Error inesperado al sumar: {e}")
                    resultado_calculado = None
                
            case "++":
                
                try:
                    ## Lógica para sumar columna
                    resultado_calculado = val1.sum()
                except Exception as e:
                    print(f"❌ Error inesperado al sumar columna: {e}")
                    resultado_calculado = None

            case "-":

                try:
                    ## Lógica para restar
                    resultado_calculado = val1 - val2
                except Exception as e:
                    print(f"❌ Error inesperado al restar: {e}")
                    resultado_calculado = None
                
            case "*":

                try:
                    ## Lógica para multiplicar
                    resultado_calculado = val1 * val2
                except Exception as e:
                    print(f"❌ Error inesperado al multiplicar: {e}")
                    resultado_calculado = None

            case "/":

                try:
                    ## División con seguridad para no romper por ceros
                    resultado_calculado = val1 / val2.replace(0, 1) 
                except ZeroDivisionError:
                    print("⚠️ Advertencia: Intento de división por cero. Se asignó 0.")
                    resultado_calculado = 0
                except Exception as e:
                    print(f"❌ Error inesperado al dividir: {e}")
                    resultado_calculado = None
                                
            case _:
                print("❌ Operación no válida: no se especifico operacion")

        if(res):

            self.df[res] = resultado_calculado
            print(f"✅ Columna '{res}' creada en el DataFrame.")
            self.Reporte(f"OPERACION REALIZADA: {op} || COLUMNA CREADA: {res}")
            return resultado_calculado # <--- Retorna el resultado para operaciones encadenadas

        else:
            print(f"✅ Operacion realizada.")
            self.Reporte(f"OPERACION  REALIZADA: {op}")
            return resultado_calculado # <--- Retorna el resultado para operaciones encadenadas

    #calculo por formulas
    def CalculadoraPlus(self, **kwargs:Optional[str]):

        try:
            # --- Recorremos los casos ---
            tipo = kwargs.get('tipo')
                        
            match tipo:

                case "costo_unitario":
                    #Subtotal: cantidad vendida / cantidad total 

                    self.Calculadora({
                    "op" : "/",
                    "res" : "Costo_unitario",
                    "col1" : kwargs.get('col1'),
                    "col2" : kwargs.get('col2')                
                    })

                case "subtotal":
                    #Subtotal: cantidad * precio 

                    self.Calculadora({
                    "op" : "*",
                    "res" : "Subtotal",
                    "col1" : kwargs.get('col1'),
                    "col2" : kwargs.get('col2')                
                    })

                case "iva":
                    # Fórmula: Subtotal * tasa
                    
                    self.Calculadora({
                    "op" : "*",
                    "res" : "IVA",
                    "col1" : kwargs.get('col1'),
                    "col2" : kwargs.get('col2', 0.03),             
                    "pass" : True                
                    })
                    
                case "descuento":
                    # Fórmula: Precio * (1 - pct) (donde 0.10 son como 10%)

                    self.Calculadora({
                    "op" : "*",
                    "res" : "Descuento",
                    "col1" : kwargs.get('col1'),              
                    "col2" : kwargs.get('col2', 0.10),             
                    "pass" : True             
                    })

                case "margen_bruto":
                    # Fórmula: Precio de venta - Costo
                    
                    self.Calculadora({
                    "op" : "-",
                    "res" : "Margen_bruto",
                    "col1" : kwargs.get('col1'),
                    "col2" : kwargs.get('col2')                
                    })
                    
                case "margen_pct":
                    # Fórmula: (Margen / Ventas) * 100

                    margen = self.Calculadora({
                    "op" : "/",
                    "res" : "",
                    "col1" : kwargs.get('col1'),
                    "col2" : kwargs.get('col2')                
                    })

                    self.Calculadora({
                    "op" : "*",
                    "res" : "Margen",
                    "col1" : margen,
                    "col2" : 100               
                    })

                case "margen_porcent":
                    # Fórmula: (Margen / Precio de Venta) * 100.
                    
                    op1=self.Calculadora({
                    "op" : "/",
                    "res" : "",
                    "col1" : kwargs.get('col1'),
                    "col2" : kwargs.get('col2')                
                    })

                    self.Calculadora({
                    "op" : "*",
                    "res" : "margen_porcent",
                    "col1" : op1,
                    "col2" : 100               
                    })

                case "envio_KG":
                    # Fórmula: Peso * Tarifa_por_Kg
                    
                    self.Calculadora({
                    "op" : "*",
                    "res" : "Logistica",
                    "col1" : kwargs.get('col1'),
                    "col2" : kwargs.get('col2', 15)                
                    })

                case "conversion_divisa":
                    # Fórmula: Subtotal * tasa
                    
                    self.Calculadora({
                    "op" : "*",
                    "res" : "Conversion",
                    "col1" : kwargs.get('col1'),
                    "col2" : kwargs.get('col2', 1)                
                    })

                case "rango":

                    #formula : mayor o menor a

                    limite = kwargs.get('limite')
                    res = kwargs.get('res')
                    col1 = kwargs.get('col1')

                    # Bloque: Creación de categoría rápida
                    resultado_calculado = np.where(self.df[col1] > limite, "Mayor", 'Menor')

                    if(res):

                        self.df[res] = resultado_calculado
                        print(f"✅ Columna '{res}' creada en el DataFrame.")
                        self.Reporte(f"OPERACION REALIZADA: EN LA COLUMNA {col1}={resultado_calculado} || COLUMNA CREADA: {res}")
                        return resultado_calculado # <--- Retorna el resultado para operaciones encadenadas

                    else:
                        print(f"✅ Operacion realizada.")
                        self.Reporte(f"OPERACION  REALIZADA: EN LA COLUMNA {col1}={resultado_calculado}")
                        return resultado_calculado # <--- Retorna el resultado para operaciones encadenadas

                case "precio_final":
                    # Fórmula: Precio Final: Subtotal + Impuestos - Descuentos
                    
                    op1=self.Calculadora({
                    "op" : "+",
                    "res" : "",
                    "col1" : kwargs.get('col1'),
                    "col2" : kwargs.get('col2')                
                    })

                    descuento = kwargs.get('col3')
                    if descuento is None:
                        descuento = descuento / 100
                    

                    self.Calculadora({
                    "op" : "*",
                    "res" : "Precio_final",
                    "col1" : op1,
                    "col2" : descuento                
                    })

                case _:
                    print("❌ Operación no válida: no se especifico operacion")

            print(f"✅ Cálculo de {tipo} completado.")
            self.Reporte(f"OPERACION REALIZADA: {tipo} || PROCESO EXITOSO")
            
        except Exception as e:
            # --- CASO GENERAL: OTROS ERRORES (ej. letras en vez de números) ---
            print(f"❌ ERROR INESPERADO: {e}")
            self.Reporte(f"OPERACION REALIZADA: {tipo} || ERROR: {e}")

    #operaciones con fechas
    def Time(self, config:Optional[str]):

        #asignamos las variables
        op = config.get('op')
        dt1 = self.df[config.get('dt1')]
        dt2 = None

        # Solo intentamos traer dt2 si existe en el diccionario
        if config.get('res'):
            res = config.get('res')
        else:
            res = None

        if config.get('dt2'):
            dt2 = self.df[config.get('dt2')]

        match op:

            case "=":

                try:
                    #transformamos el texto en fecha
                    dt1 = config.get('dt1')
                    date = pd.to_datetime(dt1)    
                except Exception as e:
                    print(f"❌ Error inesperado al convertir formato: {e}")
                    date = None

            case "+":

                try:
                    #realizamos la suma
                    date = dt1 + dt2
                except Exception as e:
                    print(f"❌ Error inesperado al sumar fechas: {e}")
                    date = None
                
            case "-":

                try:
                    ##realizamos la resta
                    date = dt1 - dt2
                except Exception as e:
                    print(f"❌ Error inesperado al restar fechas: {e}")
                    date = None
                
            case "D":

                try:
                    ## Extraemos el número (0-6) - Atributo sin ()
                    col_fecha = pd.to_datetime(dt1, errors='coerce')
                    date = col_fecha.dt.dayofweek
                except Exception as e:
                    print(f"❌ Error inesperado al extraer dias: {e}")
                    date = None
                
            case "D2":

                try:
                    ## Extraemos el nombre (Texto) - Función con ()
                    col_fecha = pd.to_datetime(dt1, errors='coerce')
                    date = col_fecha.dt.day_name()
                except Exception as e:
                    print(f"❌ Error inesperado al extraer dias: {e}")
                    date = None
                
            case "S":

                try:
                    ## Extraemos el número de semana del año (1-53)
                    col_fecha = pd.to_datetime(dt1, errors='coerce')
                    date = col_fecha.dt.isocalendar().week
                except Exception as e:
                    print(f"❌ Error inesperado al extraer semanas: {e}")
                    date = None
                
            case "M":

                try:
                    ## Extraemos el número del mes (1-12)
                    col_fecha = pd.to_datetime(dt1, errors='coerce')
                    date = col_fecha.dt.month
                except Exception as e:
                    print(f"❌ Error inesperado al extraer meses: {e}")
                    date = None
                
            case "H":

                try:
                    ## Extraemos el número del mes (1-12)
                    hora = pd.to_datetime(dt1, errors='coerce')
                    date = hora.dt.hour
                except Exception as e:
                    print(f"❌ Error inesperado al extraer las horas: {e}")
                    date = None
                    
            case "Y":

                try:
                    ## Extraemos el año (ej. 2024, 2025)
                    fecha = pd.to_datetime(dt1, errors='coerce')
                    date = fecha.dt.year
                except Exception as e:
                    print(f"❌ Error inesperado al al extraer por fecha: {e}")
                    date = None
                
            case _:
                print("❌ Operación no válida: no se especifico operacion")

        if(res):

            self.df[res] = date
            print(f"✅ Columna '{res}' creada en el DataFrame.")
            self.Reporte(f"OPERACION REALIZADA: {op} || COLUMNA CREADA: {res}")
            return date # <--- Retorna el resultado para operaciones encadenadas

        else:
            print(f"✅ Operacion realizada.")
            self.Reporte(f"OPERACION  REALIZADA: {op}")
            return date # <--- Retorna el resultado para operaciones encadenadas

    #operaciones con fecha
    def TimePlus(self, **kwargs:Optional[str]):
