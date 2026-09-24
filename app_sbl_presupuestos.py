import streamlit as st
import datetime

st.set_page_config(page_title="SBL Presupuestos", page_icon="⚡", layout="centered")

st.title("⚡ SBL Seguridad Informática")
st.subheader("Generador de Presupuestos Oficiales - Tucumán")

# Datos del Presupuesto
st.sidebar.header("⚙️ Configuración")
num_presupuesto = st.sidebar.text_input("N° de Presupuesto", "0001-0026")
fecha = st.sidebar.date_input("Fecha de Emisión", datetime.date.today())

st.header("👤 Datos del Cliente")
col1, col2 = st.columns(2)
with col1:
    cliente = st.text_input("Nombre del Cliente", "Cliente Ejemplo")
with col2:
    domicilio = st.text_input("Domicilio de la Obra", "San Miguel de Tucumán")

st.header("🛠️ Detalle del Servicio")

# Categoría 1: Electricidad
st.subheader("💡 1. Instalación Eléctrica")
c_bocas = st.number_input("Cantidad de Bocas Completas ($45.000 c/u)", min_value=0, value=0)
c_termicas = st.number_input("Instalación de Térmicas/Disyuntores ($32.000 c/u)", min_value=0, value=0)
c_aires = st.number_input("Líneas Exclusivas para A/A ($60.000 c/u)", min_value=0, value=0)

# Categoría 2: Cámaras
st.subheader("🛡️ 2. Seguridad y CCTV")
c_camaras = st.number_input("Instalación y Cableado de Cámaras Analógicas ($35.000 c/u)", min_value=0, value=4)
c_dvr = st.number_input("Configuración de DVR/NVR + Celulares ($40.000 c/u)", min_value=0, value=1)
c_metros = st.number_input("Metros de cableado excedente ($2.000 por metro)", min_value=0, value=0)

# Categoría 3: Materiales
st.subheader("📦 3. Materiales y Equipos")
incluye_materiales = st.checkbox("¿Incluir Kit de 4 Cámaras HD + Disco 1TB ($368.000)?", value=True)
otros_materiales = st.number_input("Otros materiales (Pesos $)", min_value=0, value=0)

# Cálculos
tot_electricidad = (c_bocas * 45000) + (c_termicas * 32000) + (c_aires * 60000)
tot_seguridad = (c_camaras * 35000) + (c_dvr * 40000) + (c_metros * 2000)
tot_materiales = (368000 if incluye_materiales else 0) + otros_materiales
total_general = tot_electricidad + tot_seguridad + tot_materiales

st.markdown("---")
st.header("💰 Resumen del Presupuesto")
st.write(f"**Total Electricidad (Mano de Obra):** ${tot_electricidad:,}")
st.write(f"**Total Seguridad (Mano de Obra):** ${tot_seguridad:,}")
st.write(f"**Total Materiales y Equipos:** ${tot_materiales:,}")
st.markdown(f"### 🔥 **TOTAL A PRESUPUESTAR: ${total_general:,}**")

# Simulación de generación de PDF
st.markdown("---")
if st.button("🚀 Generar PDF Profesional para WhatsApp"):
    st.success("✅ ¡PDF generado con éxito listo para compartir!")
    st.info("Esta es una vista previa de la interfaz de tu aplicación.")
