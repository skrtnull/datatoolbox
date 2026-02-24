from kit import DataToolBox
import pandas as pd

# 1. EXTRACCIÓN (Constructor)
print("🚀 Iniciando Pipeline de Pruebas...")
old_db = DataToolBox("bandeja/caos_total.csv")
db = DataToolBox("bandeja/caos_total.csv")

##----------------LIMPIEZA-----------------

#Nomrmalizamos lista
db.Clean("structure")
db.Clean("numb","id")
db.Clean("id","id",1,4)
db.Clean("text","nombre_cliente", 2)
db.Clean("text","producto")
db.Clean("numb","precio",2)
db.Clean("numb","cantidad")
db.Clean("date","fecha_compra")
db.Clean("extract","email") 

# #----------------CALCULO-------------------

#Calculamos subtotal
db.CalculadoraPlus(**{
            'tipo': 'subtotal',       # Define qué bloque del match-case entrará
            'col1': 'precio',          # Primera columna
            'col2': 'cantidad'        # Segunda columna
        })
#Calculamos IVA
db.CalculadoraPlus(**{
            'tipo': 'iva',       # Define qué bloque del match-case entrará
            'col1': 'Subtotal',          # Primera columna
        })
db.Clean("decimal","IVA",1,2)
#Calculamos estacionalidad
db.TimePlus(**{
    "tipo": "estacionalidad",
    "date1": "fecha_compra"
})

# #--------------VISULAIZACION-----------------

#Antes
print("\n" + "—" * 40)
print("❌ ANTES DE LA TUBERÍA (Raw Data)")
print("—" * 40)
old_db.View(filas=100)
#Despues
print("\n" + "—" * 40)
print("✅ DESPUÉS DE LA TUBERÍA (Processed Data)")
print("—" * 40)
db.View(filas=100)
print("\n𝕏 Pipeline finalizado con éxito.")

# #---------------EXPORTACION------------------

#Exportación final
db.Export("dataset_limpio")
