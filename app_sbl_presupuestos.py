import streamlit as st
import datetime
import urllib.parse

st.set_page_config(page_title="SBL Presupuestos Premium", page_icon="⚡", layout="centered")

# ==========================================
#       SISTEMA DE SEGURIDAD PRIVADO
# ==========================================
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("🔒 Acceso Restringido - SBL")
    clave = st.text_input("Contraseña de acceso:", type="password")
    if st.button("Iniciar Sesión"):
        if clave == "SBL2026*":
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("❌ Contraseña incorrecta")
    st.stop()

# ==========================================
#       CÓDIGO DE LA APLICACIÓN (SBL)
# ==========================================
st.title("⚡ SBL Seguridad Informática")
st.subheader("Generador de Presupuestos Oficiales")

# Panel lateral de configuración básica
st.sidebar.header("⚙️ Configuración")
num_presupuesto = st.sidebar.text_input("N° de Presupuesto", "0001-0026")
fecha = st.sidebar.date_input("Fecha de Emisión", datetime.date.today())
cbu_alias = st.sidebar.text_input("CBU / Alias Bancario", "SBL.SEGURIDAD.TUC")
condicion_pago = st.sidebar.selectbox("Condición de Pago", ["Contado / Transferencia", "50% Anticipo - 50% Saldo", "A Convenir"])

# Formulario Central Principal
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

# Precios fijos de SBL
P_BOCA, P_TERMICA, P_AIRE = 45000, 32000, 60000
P_CAMARA, P_DVR, P_MANTENIMIENTO, P_METRO, P_KIT = 35000, 40000, 15000, 2000, 368000

# Cálculos comerciales
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
#       NUEVO MÉTODOS TOTALMENTE FIJOS
# ==========================================
st.subheader("📥 Generación de Documento")

# Plantilla de texto limpia estructurada (Reemplaza al HTML/PDF pesado que colgaba el servidor)
texto_documento = f"""⚡ SBL SEGURIDAD INFORMÁTICA
=========================================
PRESUPUESTO OFICIAL N° {num_presupuesto}
Fecha de Emisión: {fecha.strftime('%d/%m/%Y')}
Validez del Presupuesto: 15 días
=========================================

👤 DATOS DEL CLIENTE / OBRA:
-----------------------------------------
Cliente: {cliente}
Ubicación de la Obra: {domicilio}

🛠️ DESGLOSE DETALLADO DE CONCEPTOS:
-----------------------------------------
• Mano de obra Eléctrica: ${tot_electricidad:,}
• Mano de obra Seguridad y Mantenimiento: ${tot_seguridad:,}
• Materiales, Kit y Equipamiento: ${tot_materiales:,}

-----------------------------------------
🔥 VALOR TOTAL CONTADO NETO: ${total_general:,}
-----------------------------------------

📝 TÉRMINOS Y CONDICIONES COMERCIALES:
-----------------------------------------
• Forma de Pago: {condicion_pago}.
• Garantía: Equipamiento con 1 año de garantía oficial. Mano de obra por 90 días.
• Transferencia Bancaria: Cuenta Corriente SBL | CBU/Alias: {cbu_alias}

Muchas gracias por elegir SBL Seguridad Informática."""

# BOTÓN DE DESCARGA NATIVO DE STREAMLIT (Imposible de ocultar o romper)
st.download_button(
    label="📥 Descargar Documento de Presupuesto Formal",
    data=texto_documento,
    file_name=f"Presupuesto_{num_presupuesto}_{cliente.replace(' ', '_')}.txt",
    mime="text/plain",
    use_container_width=True
)

st.markdown("---")
st.subheader("📲 Panel de Envío por WhatsApp")

# CASILLA DE TELÉFONO FIJA EN EL CENTRO DE LA APP
telefono_cliente = st.text_input("Celular del Cliente (Escribir números seguidos con código de área, Ej: 543816083885)", "543816083885")

texto_wa = f"*⚡ SBL SEGURIDAD INFORMÁTICA *\n *Presupuesto Oficial N° {num_presupuesto}*\n📅 *Fecha:* {fecha.strftime('%d/%m/%Y')}\n👤 *Cliente:* {cliente}\n📍 *Obra:* {domicilio}\n-----------------------------------------\n*DESGLOSE DEL SERVICIO:* \n"
if tot_electricidad > 0: texto_wa += f"💡 *Mano de obra Eléctrica:* ${tot_electricidad:,}\n"
if tot_seguridad > 0: texto_wa += f"🛡️ *Mano de obra Seguridad y Manto.:* ${tot_seguridad:,}\n"
if tot_materiales > 0: texto_wa += f"📦 *Materiales y Equipos:* ${tot_materiales:,}\n"

texto_wa += f"-----------------------------------------\n🔥 *TOTAL NETO: ${total_general:,}*\n-----------------------------------------\n📝 *Términos Comerciales:*\n• Pago: {condicion_pago}.\n• Garantía: Equipos 1 año, Mano de obra 90 días.\n🏦 *Datos de Transferencia:* \n• CBU/Alias: {cbu_alias}\n\n¡Muchas gracias por elegirnos!"
texto_url = urllib.parse.quote(texto_wa)

num_limpio = telefono_cliente.replace("+", "").replace("-", "").replace(" ", "").replace("(", "").replace(")", "")
whatsapp_url = f"https://wa.me{num_limpio}?text={texto_url}"

# ENLACE DE WHATSAPP TOTALMENTE FIJO ABAJO DEL TODO
st.markdown(f"👉 **[HACÉ CLIC AQUÍ PARA ENVIAR EL RESUMEN POR WHATSAPP]({whatsapp_url})**")
