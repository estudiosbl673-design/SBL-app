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

st.sidebar.markdown("---")
st.sidebar.header("🏦 Datos de Cobro")
cbu_alias = st.sidebar.text_input("CBU / Alias Bancario", "SBL.SEGURIDAD.TUC")
condicion_pago = st.sidebar.selectbox("Condición de Pago", ["Contado / Transferencia", "50% Anticipo - 50% Saldo", "A Convenir"])

st.sidebar.markdown("---")
st.sidebar.header("📲 Enviar por WhatsApp")
telefono_cliente = st.sidebar.text_input("Celular del Cliente (Ej: 3816083885)", "")

# Precios Unitarios fijos
P_BOCA, P_TERMICA, P_AIRE = 45000, 32000, 60000
P_CAMARA, P_DVR, P_MANTENIMIENTO, P_METRO, P_KIT = 35000, 40000, 15000, 2000, 368000

# Cálculos de Totales
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

# ==========================================
#       GENERACIÓN DE PLANTILLA HTML COLOR
# ==========================================
html_documento = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
    body {{ font-family: 'Segoe UI', Helvetica, Arial, sans-serif; color: #2c3e50; margin: 20px; }}
    .header-table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
    .logo-title {{ font-size: 24px; font-weight: bold; color: #1a365d; }}
    .doc-type {{ text-align: right; font-size: 14px; color: #4a5568; line-height: 1.5; }}
    .divider {{ border-top: 3px solid #1a365d; margin-bottom: 20px; }}
    .info-table {{ width: 100%; border-collapse: collapse; margin-bottom: 25px; }}
    .info-header {{ background-color: #2d3748; color: white; font-weight: bold; font-size: 13px; padding: 8px; }}
    .info-cell {{ padding: 10px; border: 1px solid #e2e8f0; background-color: #f7fafc; font-size: 13px; vertical-align: top; width: 50%; }}
    .section-title {{ font-size: 14px; font-weight: bold; color: #1a365d; border-bottom: 2px solid #e2e8f0; padding-bottom: 5px; margin-top: 25px; margin-bottom: 15px; }}
    .items-table {{ width: 100%; border-collapse: collapse; }}
    .items-th {{ background-color: #1a365d; color: white; font-weight: bold; font-size: 13px; padding: 10px; text-align: left; }}
    .items-th-r {{ background-color: #1a365d; color: white; font-weight: bold; font-size: 13px; padding: 10px; text-align: right; }}
    .items-td {{ padding: 10px; border-bottom: 1px solid #e2e8f0; font-size: 12px; }}
    .items-td-r {{ padding: 10px; border-bottom: 1px solid #e2e8f0; font-size: 12px; text-align: right; }}
    .row-even {{ background-color: #f7fafc; }}
    .total-row {{ background-color: #edf2f7; font-weight: bold; font-size: 14px; color: #1a365d; }}
    .total-td {{ padding: 12px; border-top: 2px solid #1a365d; border-bottom: 2px solid #1a365d; }}
    .total-td-r {{ padding: 12px; border-top: 2px solid #1a365d; border-bottom: 2px solid #1a365d; text-align: right; }}
    .terms {{ font-size: 13px; line-height: 1.6; background-color: #f7fafc; padding: 15px; border-radius: 5px; border-left: 4px solid #1a365d; }}
    .footer-table {{ width: 100%; margin-top: 50px; }}
    .signature {{ text-align: right; font-size: 13px; font-weight: bold; color: #2d3748; line-height: 1.5; }}
</style>
</head>
<body>

<table class="header-table">
    <tr>
        <td class="logo-title">⚡ SBL SEGURIDAD INFORMÁTICA<br/><span style="font-size: 12px; color: #4a5568; font-weight: normal;">Soluciones Tecnológicas e Integrales</span></td>
        <td class="doc-type">
            <span style="font-size: 18px; font-weight: bold; color: #1a365d;">PRESUPUESTO OFICIAL</span><br/>
            <b>N°:</b> {num_presupuesto}<br/>
            <b>Fecha:</b> {fecha.strftime('%d/%m/%Y')}<br/>
            <b>Validez:</b> 15 días
        </td>
    </tr>
</table>

<div class="divider"></div>

<table class="info-table">
    <tr>
        <td class="info-header">PROVEEDOR:</td>
        <td class="info-header">CLIENTE / OBRA:</td>
    </tr>
    <tr>
        <td class="info-cell">
            <b>SBL Seguridad Informática</b><br/>
            San Miguel de Tucumán<br/>
            Email: info@sblseguridad.com
        </td>
        <td class="info-cell">
            <b>Nombre:</b> {cliente}<br/>
            <b>Ubicación:</b> {domicilio}<br/>
            <b>Estado:</b> Pendiente de Aprobación
        </td>
    </tr>
</table>

<div class="section-title">DESGLOSE DETALLADO DE CONCEPTOS</div>

<table class="items-table">
    <tr>
        <th class="items-th">Descripción del Ítem / Servicio Técnico</th>
        <th class="items-th-r">Cant.</th>
        <th class="items-th-r">P. Unitario</th>
        <th class="items-th-r">Subtotal</th>
    </tr>
"""

linea_index = 1
if c_bocas > 0:
    clase_fila = "row-even" if linea_index % 2 == 0 else ""
    html_documento += f'<tr class="{clase_fila}"><td class="items-td">Mano de obra: Instalación de Bocas Eléctricas Completas</td><td class="items-td-r">{c_bocas}</td><td class="items-td-r">${P_BOCA:,}</td><td class="items-td-r">${c_bocas*P_BOCA:,}</td></tr>'
    linea_index += 1
if c_termicas > 0:
    clase_fila = "row-even" if linea_index % 2 == 0 else ""
    html_documento += f'<tr class="{clase_fila}"><td class="items-td">Mano de obra: Montaje y conexión de Térmicas/Disyuntores</td><td class="items-td-r">{c_termicas}</td><td class="items-td-r">${P_TERMICA:,}</td><td class="items-td-r">${c_termicas*P_TERMICA:,}</td></tr>'
    linea_index += 1
if c_aires > 0:
    clase_fila = "row-even" if linea_index % 2 == 0 else ""
    html_documento += f'<tr class="{clase_fila}"><td class="items-td">Mano de obra: Tendido de líneas exclusivas para Aire Acondicionado</td><td class="items-td-r">{c_aires}</td><td class="items-td-r">${P_AIRE:,}</td><td class="items-td-r">${c_aires*P_AIRE:,}</td></tr>'
    linea_index += 1
if c_camaras > 0:
    clase_fila = "row-even" if linea_index % 2 == 0 else ""
    html_documento += f'<tr class="{clase_fila}"><td class="items-td">Mano de obra: Instalación, montaje y cableado de Cámaras Analógicas HD</td><td class="items-td-r">{c_camaras}</td><td class="items-td-r">${P_CAMARA:,}</td><td class="items-td-r">${c_camaras*P_CAMARA:,}</td></tr>'
    linea_index += 1
if c_dvr > 0:
    clase_fila = "row-even" if linea_index % 2 == 0 else ""
    html_documento += f'<tr class="{clase_fila}"><td class="items-td">Servicio Técnico: Configuración de DVR/NVR + Enlace a celulares en red</td><td class="items-td-r">{c_dvr}</td><td class="items-td-r">${P_DVR:,}</td><td class="items-td-r">${c_dvr*P_DVR:,}</td></tr>'
    linea_index += 1
if c_mantenimiento > 0:
    clase_fila = "row-even" if linea_index % 2 == 0 else ""
    html_documento += f'<tr class="{clase_fila}"><td class="items-td">Servicio Técnico: Mantenimiento correctivo, limpieza de lentes y calibración de Cámaras</td><td class="items-td-r">{c_mantenimiento}</td><td class="items-td-r">${P_MANTENIMIENTO:,}</td><td class="items-td-r">${c_mantenimiento*P_MANTENIMIENTO:,}</td></tr>'
    linea_index += 1
if c_metros > 0:
