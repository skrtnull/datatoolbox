from __future__ import annotations
from typing import Optional, Any, Union
import pandas as pd
import os
import time
import numpy as np
from datetime import datetime
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

class DataToolBox:

    def __init__(self, file:Optional[str] =None):

        # 1. Definimos las variables con valores por defecto SIEMPRE al principio
        self.df = pd.DataFrame()
        self.ruta = "" 
        self.engine = None

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

    #----------------------------SQL---------------------------------------

    #conectamos con la base de datos
    def Conexion(self, **kwargs:Optional[str]):

        if self.engine is not None:
            print("⚡ Conexión ya establecida. Saltando configuración...")
            return

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
    def ExportSQL(self, nombre_tabla:str, modo:str ='append'):
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
            print("⚠️ ERROR: El DataFrame está vacío. No hay nada que exportar.")
            return

        try:
            # 2. Ejecutar la exportación usando el motor de la instancia
            self.df.to_sql(nombre_tabla, con=self.engine, if_exists=modo, index=False)
            print(f"✅ ¡Éxito! Datos exportados a la tabla '{nombre_tabla}' (Modo: {modo}).")
            self.Reporte(f"EXPORTACIÓN SQL: Tabla '{nombre_tabla}' actualizada satisfactoriamente.")
            
        except Exception as e:
            print(f"❌ ERROR al exportar a SQL: {e}")
            self.Reporte(f"FALLO EXPORTACIÓN SQL: {e}")

    #---------------------------Utilieria-------------------------------

    #Ver lista
    def View(self, filas:int =10, portable:bool =False, list:Optional[list] =None):

        if (portable == True):
            """Imprime el DataFrame de forma segura y rápida"""
            print(f"\n>>> Mostrando {filas} filas de {list.shape[0]} totales:")
            print(list.head(filas))
            print("-" * 30)
        else:
            """Imprime el DataFrame de forma segura y rápida"""
            print(f"\n>>> Mostrando {filas} filas de {self.df.shape[0]} totales:")
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
    def Refresh(self, archivo:str):

        try:

            print(f"📂 Cargando CSV: {archivo}.")
            self.df = pd.read_csv(f"{archivo}")

        except Exception as e:
            print(f"❌ Error al al cargar archivo: {e}")
            return []
    
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

    #Limpiar texto
    def CleanText(self, columna:str, drop:bool= True):

        if drop:

            # 2. 🔥 NUEVO: Eliminar símbolos (solo deja letras y espacios)
            self.df[columna] = self.df[columna].str.replace(r'[^a-zA-Z\s]', '', regex=True)
        
        else:

            # 2. 🔥 NUEVO: Eliminar símbolos (solo deja letras, números y espacios)
            self.df[columna] = self.df[columna].str.replace(r'[^a-zA-Z0-9\s]', '', regex=True)

        # A. Limpiar espacios vacíos en los nombres y poner la primera en Mayúscula
        # Quita espacios, pone todo en minúsculas y elimina acentos
        self.df[columna] = self.df[columna].astype(str).str.strip().str.lower().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
        
        # .str.strip() quita espacios, .str.capitalize() pone la primera en mayúscula
        self.df[columna] = self.df[columna].str.strip().str.capitalize()

        print(f"✅ Columna '{columna}' normalizada al estilo estándar.")
        print("✅ Texto limpiado")

        return self.df

    #Limpiar numeros
    def CleanNumb(self, columna:str ,sib:str=None, drop:bool= True):

        #limpiamos los numeros de simbolos
        if sib is not None:
            if self.df[columna].dtype == 'object':
                self.df[columna] = self.df[columna].str.replace(sib, '', regex=False)
        #eliminamos cualquier presencia de letra
        # Extrae solo los números (0-9) y los une.
        self.df[columna] = self.df[columna].astype(str).str.extract(r'(\d+)').astype(float)
        #transformamor caracteres en numeros
        self.df[columna] = pd.to_numeric(self.df[columna], errors='coerce')

        if drop:
            #eliminamos nulos
            self.df[columna] = self.df[columna].fillna(0)
        
        #convertir en entero
        self.df[columna] = self.df[columna].round(0).astype(int)

        print("✅ Numeros limpiados")

        return self.df
    
    #limpiar datos mentirosos o con valores fuera de las metricas
    def CleanFalse(self, columna:str):
        
        #normalizamos en caso que no se haya echo ya
        self.df[columna] = pd.to_numeric(self.df[columna], errors='coerce')

        #limpieza de lvl2
        Q1 = self.df[columna].quantile(0.25)
        Q3 = self.df[columna].quantile(0.75)
        IQR = Q3 - Q1
        # Solo deja los datos que están en el rango normal
        self.df = self.df[~((self.df[columna] < (Q1 - 1.5 * IQR)) | (self.df[columna] > (Q3 + 1.5 * IQR)))]
        print(f"💀 Outliers eliminados en {columna}. Los datos mentirosos han muerto.")

        return self.df

    #Acomodar fechas
    def CleanDate(self, fecha:str, drop:str= True):
        
        ##Eliminamos espacios
        self.df[fecha] = self.df[fecha].astype(str).str.strip() # Quita espacios
        # Convierte a Fecha
        self.df[fecha] = pd.to_datetime(self.df[fecha], errors='coerce')

        if drop:

            # ahora donde haya NaT El subset asegura que SOLO eliminara solo esas fechas inexistentes
            self.df = self.df .dropna(subset=[fecha])

        print("✅ Fechas acomodadas")
        
        return self.df

    #Limitar o eliminar
    def CleanDecimal(self, columna, decimales:int = 2):
        # En kit.py, dentro de un nuevo método o en CalculadoraPlus
        self.df[columna] = pd.to_numeric(self.df[columna], errors='coerce').round(decimales)
            
        print(f"🎯 Columna '{columna}' redondeada a {decimales} decimales.")

    # Limpieza estructural: Eliminar filas inservibles o con todo nulos
    def CleanStruct(self):

        # 1. Eliminamos filas donde TODOS los valores sean nulos
        antes = len(self.df)
        self.df = self.df.dropna(how='all')
        
        # 2. Eliminamos filas que tengan nulos en columnas críticas (ej. Producto)
        despues = len(self.df)
        print(f"🧹 Estructura limpiada: Se eliminaron {antes - despues} filas vacías.")

    #recuperar correo y numeros cuando la informacion en la columna sea ilegible
    def ExtractInfo(self, columna:str, patron:str=r"[\w\.-]+@[\w\.-]+"): 

        # Por defecto busca emails, pero puedes pasarle cualquier patron
        self.df[columna] = self.df[columna].str.findall(patron).str[0]
        print("📧 Información extraída mediante patrones complejos.")
          
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
                    input("Pulse cualquier tecla pra continuar: ")
                else:
                    print ("Error inesperado")
                    input("Pulse cualquier tecla pra continuar: ")
            
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
        val1 = self.df[c1] if c1 in self.df.columns else c1
        val2 = self.df[c2] if c2 in self.df.columns else c2

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
                    #Subtotal: cantidad vendida + cantidad total 

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
                    "col2" : kwargs.get('col2', 0.16),             
                    "pass" : True                
                    })
                    
                case "descuento":
                    # Fórmula: Precio * (1 - pct) (donde 0.10 son como 10%)

                    pct = self.Calculadora({
                    "op" : "-",
                    "res" : "",
                    "col1" : 1,              
                    "col2" : kwargs.get('col2', 0.10),              
                    })

                    self.Calculadora({
                    "op" : "*",
                    "res" : "Descuento",
                    "col1" : kwargs.get('col1'),              
                    "col2" : pct,              
                    })

                case "precio_final":
                    # Fórmula: Precio Final: Subtotal + Impuestos - Descuentos
                    
                    op1=self.Calculadora({
                    "op" : "+",
                    "res" : "",
                    "col1" : kwargs.get('col1'),
                    "col2" : kwargs.get('col2')                
                    })

                    self.Calculadora({
                    "op" : "-",
                    "res" : "Precio_final",
                    "col1" : op1,
                    "col2" : kwargs.get('col3', 0.10)                
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
