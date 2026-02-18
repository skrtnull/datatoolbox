from kit import DataToolBox
import pandas as pd

# 1. EXTRACCIÓN (Constructor)
print("🚀 Iniciando Pipeline de Pruebas...")
old_db = DataToolBox("bandeja/caos_total.csv")
db = DataToolBox("bandeja/caos_total.csv")

##----------------LIMPIEZA-----------------

#Nomrmalizamos lista
db.CleanStruct()
db.CleanNumb("id")
db.CleanText("nombre_cliente")
db.CleanText("producto", False)
db.CleanNumb("precio")
db.CleanNumb("cantidad")
db.CleanDate("fecha_compra")
db.ExtractInfo("email")

#----------------CALCULO-------------------

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
db.CleanDecimal("IVA")
#Calculamos estacionalidad
db.TimePlus(**{
    "tipo": "estacionalidad",
    "date1": "fecha_compra"
})

#--------------VISULAIZACION-----------------

#Antes
print("\n" + "—" * 40)
print("❌ ANTES DE LA TUBERÍA (Raw Data)")
print("—" * 40)
old_db.View(filas=10)
#Despues
print("\n" + "—" * 40)
print("✅ DESPUÉS DE LA TUBERÍA (Processed Data)")
print("—" * 40)
db.View(filas=10)
print("\n𝕏 Pipeline finalizado con éxito.")

#---------------EXPORTACION------------------

#Exportación final
db.Export("dataset_limpio")