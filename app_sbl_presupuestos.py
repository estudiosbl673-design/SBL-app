import streamlit as st
import datetime
import urllib.parse

st.set_page_config(page_title="SBL Presupuestos Premium", page_icon="⚡", layout="centered")

# ==========================================
#       SISTEMA DE SEGURIDAD PRIVADO
# ==========================================
def comprobar_contrasenia():
    if "autenticado" not in st.session_state:
        st.session_state.autenticado = False
    if st.session_state.autenticado:
        return True
    st.title("🔒 Acceso Restringido - SBL")
    clave = st.text_input("Contraseña de acceso:", type="password")
    if st.button("Iniciar Sesión"):
        if clave == "SBL2026*":
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("❌ Contraseña incorrecta")
    return False

if not comprobar_contrasenia():
    st.stop()

# ==========================================
#       CÓDIGO DE LA APLICACIÓN (SBL)
# ==========================================
st.title("⚡ SBL Seguridad Informática")
st.subheader("Generador de Presupuestos Premium")

st.sidebar.header("⚙️ Configuración")
num_presupuesto = st.sidebar.text_input("N° de Presupuesto", "0001-0026")
fecha = st.sidebar.date_input("Fecha de Emisión", datetime.date.today())
cbu_alias = st.sidebar.text_input("CBU / Alias Bancario", "SBL.SEGURIDAD.TUC")
condicion_pago = st.sidebar.selectbox("Condición de Pago", ["Contado / Transferencia", "50% Anticipo - 50% Saldo", "A Convenir"])

st.header("👤 Datos del Cliente")
col1, col2 = st.columns(2)
with col1:
    cliente = st.text_input("Nombre del Cliente / Empresa", "Cliente Ejemplo")
with col2:
    domicilio = st.text_input("Domicilio de la Obra", "San Miguel de Tucumán")

st.header("🛠️ Detalle del Servicio")
st.subheader("💡 1. Instalación Eléctrica")
c_bocas = st.number_input("Cantidad de Bocas Completas ($45.000 c/u)", min_value=0, value=0)
c_termicas = st.number_input("Instalación de Térmicas/Disyuntores ($32.000 c/u)", min_value=0, value=0)
c_aires = st.number_input("Líneas Exclusivas para A/A ($60.000 c/u)", min_value=0, value=0)

st.subheader("🛡️ 2. Seguridad, CCTV y Mantenimiento")
c_camaras = st.number_input("Instalación de Cámaras Analógicas ($35.000 c/u)", min_value=0, value=4)
c_dvr = st.number_input("Configuración de DVR/NVR + Celulares ($40.000 c/u)", min_value=0, value=1)
c_mantenimiento = st.number_input("Mantenimiento Técnico / Limpieza de Cámaras ($15.000 c/u)", min_value=0, value=0)
c_metros = st.number_input("Metros de cableado excedente ($2.000 por metro)", min_value=0, value=0)

st.subheader("📦 3. Materiales y Equipos")
incluye_materiales = st.checkbox("¿Incluir Kit de 4 Cámaras HD + Disco 1TB ($368.000)?", value=True)
otros_materiales = st.number_input("Otros materiales / Adicionales (Pesos $)", min_value=0, value=0)

P_BOCA, P_TERMICA, P_AIRE = 45000, 32000, 60000
P_CAMARA, P_DVR, P_MANTENIMIENTO, P_METRO, P_KIT = 35000, 40000, 15000, 2000, 368000

tot_electricidad = (c_bocas * P_BOCA) + (c_termicas * P_TERMICA) + (c_aires * P_AIRE)
tot_seguridad = (c_camaras * P_CAMARA) + (c_dvr * P_DVR) + (c_mantenimiento * P_MANTENIMIENTO) + (c_metros * P_METRO)
tot_materiales = (P_KIT if incluye_materiales else 0) + otros_materiales
total_general = tot_electricidad + tot_seguridad + tot_materiales

st.markdown("---")
st.header("💰 Resumen del Presupuesto")
st.write(f"**Total Electricidad (Mano de Obra):** ${tot_electricidad:,}")
st.write(f"**Total Seguridad y Mantenimiento:** ${tot_seguridad:,}")
st.write(f"**Total Materiales y Equipos:** ${tot_materiales:,}")
st.markdown(f"### 🔥 **TOTAL A PRESUPUESTAR: ${total_general:,}**")
st.markdown("---")

# Armado del documento HTML a color
tabla_html_filas = ""
if c_bocas > 0: tabla_html_filas += "<tr><td style='padding:10px;border-bottom:1px solid #e2e8f0;font-size:12px;'>Mano de obra: Instalación de Bocas Eléctricas Completas</td><td style='padding:10px;border-bottom:1px solid #e2e8f0;font-size:12px;text-align:right;'>" + str(c_bocas) + "</td><td style='padding:10px;border-bottom:1px solid #e2e8f0;font-size:12px;text-align:right;'>$" + f"{P_BOCA:,}" + "</td><td style='padding:10px;border-bottom:1px solid #e2e8f0;font-size:12px;text-align:right;'>$" + f"{c_bocas*P_BOCA:,}" + "</td></tr>"
if c_termicas > 0: tabla_html_filas += "<tr><td style='padding:10px;border-bottom:1px solid #e2e8f0;font-size:12px;'>Mano de obra: Montaje y conexión de Térmicas/Disyuntores</td><td style='padding:10px;border-bottom:1px solid #e2e8f0;font-size:12px;text-align:right;'>" + str(c_termicas) + "</td><td style='padding:10px;border-bottom:1px solid #e2e8f0;font-size:12px;text-align:right;'>$" + f"{P_TERMICA:,}" + "</td><td style='padding:10px;border-bottom:1px solid #e2e8f0;font-size:12px;text-align:right;'>$" + f"{c_termicas*P_TERMICA:,}" + "</td></tr>"
if c_aires > 0: tabla_html_filas += "<tr><td style='padding:10px;border-bottom:1px solid #e2e8f0;font-size:12px;'>Mano de obra: Tendido de líneas para Aire Acondicionado</td><td style='padding:10px;border-bottom:1px solid #e2e8f0;font-size:12px;text-align:right;'>" + str(c_aires) + "</td><td style='padding:10px;border-bottom:1px solid #e2e8f0;font-size:12px;text-align:right;'>$" + f"{P_AIRE:,}" + "</td><td style='padding:10px;border-bottom:1px solid #e2e8f0;font-size:12px;text-align:right;'>$" + f"{c_aires*P_AIRE:,}" + "</td></tr>"
if c_camaras > 0: tabla_html_filas += "<tr><td style='padding:10px;border-bottom:1px solid #e2e8f0;font-size:12px;'>Mano de obra: Instalación y cableado de Cámaras Analógicas HD</td><td style='padding:10px;border-bottom:1px solid #e2e8f0;font-size:12px;text-align:right;'>" + str(c_camaras) + "</td><td style='padding:10px;border-bottom:1px solid #e2e8f0;font-size:12px;text-align:right;'>$" + f"{P_CAMARA:,}" + "</td><td style='padding:10px;border-bottom:1px solid #e2e8f0;font-size:12px;text-align:right;'>$" + f"{c_camaras*P_CAMARA:,}" + "</td></tr>"
if c_dvr > 0: tabla_html_filas += "<tr><td style='padding:10px;border-bottom:1px solid #e2e8f0;font-size:12px;'>Servicio Técnico: Configuración de DVR/NVR + Enlace a celulares</td><td style='padding:10px;border-bottom:1px solid #e2e8f0;font-size:12px;text-align:right;'>" + str(c_dvr) + "</td><td style='padding:10px;border-bottom:1px solid #e2e8f0;font-size:12px;text-align:right;'>$" + f"{P_DVR:,}" + "</td><td style='padding:10px;border-bottom:1px solid #e2e8f0;font-size:12px;text-align:right;'>$" + f"{c_dvr*P_DVR:,}" + "</td></tr>"
if c_mantenimiento > 0: tabla_html_filas += "<tr><td style='padding:10px;border-bottom:1px solid #e2e8f0;font-size:12px;'>Servicio Técnico: Mantenimiento y limpieza de Cámaras</td><td style='padding:10px;border-bottom:1px solid #e2e8f0;font-size:12px;text-align:right;'>" + str(c_mantenimiento) + "</td><td style='padding:10px;border-bottom:1px solid #e2e8f0;font-size:12px;text-align:right;'>$" + f"{P_MANTENIMIENTO:,}" + "</td><td style='padding:10px;border-bottom:1px solid #e2e8f0;font-size:12px;text-align:right;'>$" + f"{c_mantenimiento*P_MANTENIMIENTO:,}" + "</td></tr>"
if c_metros > 0: tabla_html_filas += "<tr><td style='padding:10px;border-bottom:1px solid #e2e8f0;font-size:12px;'>Materiales: Metros de cableado excedente CCTV</td><td style='padding:10px;border-bottom:1px solid #e2e8f0;font-size:12px;text-align:right;'>" + str(c_metros) + "</td><td style='padding:10px;border-bottom:1px solid #e2e8f0;font-size:12px;text-align:right;'>$" + f"{P_METRO:,}" + "</td><td style='padding:10px;border-bottom:1px solid #e2e8f0;font-size:12px;text-align:right;'>$" + f"{c_metros*P_METRO:,}" + "</td></tr>"
if incluye_materiales: tabla_html_filas += "<tr><td style='padding:10px;border-bottom:1px solid #e2e8f0;font-size:12px;'>Equipamiento: Kit completo de 4 Cámaras HD + Disco Rígido 1TB</td><td style='padding:10px;border-bottom:1px solid #e2e8f0;font-size:12px;text-align:right;'>1</td><td style='padding:10px;border-bottom:1px solid #e2e8f0;font-size:12px;text-align:right;'>$" + f"{P_KIT:,}" + "</td><td style='padding:10px;border-bottom:1px solid #e2e8f0;font-size:12px;text-align:right;'>$" + f"{P_KIT:,}" + "</td></tr>"
if otros_materiales > 0: tabla_html_filas += "<tr><td style='padding:10px;border-bottom:1px solid #e2e8f0;font-size:12px;'>Materiales: Componentes adicionales o accesorios de montaje</td><td style='padding:10px;border-bottom:1px solid #e2e8f0;font-size:12px;text-align:right;'>1</td><td style='padding:10px;border-bottom:1px solid #e2e8f0;font-size:12px;text-align:right;'>$" + f"{otros_materiales:,}" + "</td><td style='padding:10px;border-bottom:1px solid #e2e8f0;font-size:12px;text-align:right;'>$" + f"{otros_materiales:,}" + "</td></tr>"

