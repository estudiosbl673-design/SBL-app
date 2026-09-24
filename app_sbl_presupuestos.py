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
#       GENERACIÓN DE INFORME DETALLADO
# ==========================================
plantilla_informe = f"""⚡ SBL SEGURIDAD INFORMÁTICA
=========================================
PRESUPUESTO OFICIAL N° {num_presupuesto}
Fecha de Emisión: {fecha.strftime('%d/%m/%Y')}
Validez del Presupuesto: 15 días
=========================================

👤 DATOS DEL CLIENTE / OBRA:
-----------------------------------------
Cliente: {cliente}
Ubicación de la Obra: {domicilio}
Estado: Pendiente de Aprobación

🛠️ DESGLOSE DETALLADO DE CONCEPTOS:
-----------------------------------------"""

if c_bocas > 0: plantilla_informe += f"\n• Inst. Bocas Eléctricas Completas ({c_bocas} u.): ${c_bocas*P_BOCA:,}"
if c_termicas > 0: plantilla_informe += f"\n• Montaje Térmicas/Disyuntores ({c_termicas} u.): ${c_termicas*P_TERMICA:,}"
if c_aires > 0: plantilla_informe += f"\n• Líneas exclusivas para A/A ({c_aires} u.): ${c_aires*P_AIRE:,}"
if c_camaras > 0: plantilla_informe += f"\n• Inst. Cámaras Analógicas HD ({c_camaras} u.): ${c_camaras*P_CAMARA:,}"
if c_dvr > 0: plantilla_informe += f"\n• Configuración DVR y enlace celular ({c_dvr} u.): ${c_dvr*P_DVR:,}"
if c_mantenimiento > 0: plantilla_informe += f"\n• Mantenimiento correctivo y limpieza ({c_mantenimiento} u.): ${c_mantenimiento*P_MANTENIMIENTO:,}"
if c_metros > 0: plantilla_informe += f"\n• Cableado estructurado excedente CCTV ({c_metros} m.): ${c_metros*P_METRO:,}"
if incluye_materiales: plantilla_informe += f"\n• Kit 4 Cámaras HD + Disco Rígido 1TB (1 u.): ${P_KIT:,}"
if otros_materiales > 0: plantilla_informe += f"\n• Componentes o accesorios adicionales: ${otros_materiales:,}"

plantilla_informe += f"""\n-----------------------------------------
🔥 VALOR TOTAL CONTADO NETO: ${total_general:,}
-----------------------------------------

📝 TÉRMINOS Y CONDICIONES COMERCIALES:
-----------------------------------------
• Forma de Pago: {condicion_pago}.
• Garantía: Equipamiento con 1 año de garantía de fábrica. Mano de obra por 90 días.
• Transferencia Bancaria: Cuenta Corriente SBL | CBU/Alias: {cbu_alias}

Muchas gracias por elegir SBL Seguridad Informática."""

# Botón Nativo para Descargar la Propuesta Estructurada
st.download_button(
    label="📥 Descargar Documento Comercial",
    data=plantilla_informe,
    file_name=f"Presupuesto_{num_presupuesto}_{cliente.replace(' ', '_')}.txt",
    mime="text/plain",
    use_container_width=True
)

# Mensaje para WhatsApp optimizado
texto_wa = f"*⚡ SBL SEGURIDAD INFORMÁTICA *\n *Presupuesto Oficial N° {num_presupuesto}*\n📅 *Fecha:* {fecha.strftime('%d/%m/%Y')}\n👤 *Cliente:* {cliente}\n📍 *Obra:* {domicilio}\n-----------------------------------------\n*DESGLOSE DEL SERVICIO:* \n"
if tot_electricidad > 0: texto_wa += f"💡 *Mano de obra Eléctrica:* ${tot_electricidad:,}\n"
if tot_seguridad > 0: texto_wa += f"🛡️ *Mano de obra Seguridad y Manto.:* ${tot_seguridad:,}\n"
if tot_materiales > 0: texto_wa += f"📦 *Materiales y Equipos:* ${tot_materiales:,}\n"

texto_wa += f"-----------------------------------------\n🔥 *TOTAL NETO: ${total_general:,}*\n-----------------------------------------\n📝 *Términos Comerciales:*\n• Pago: {condicion_pago}.\n• Garantía: Equipos 1 año, Mano de obra 90 días.\n🏦 *Datos de Transferencia:* \n• CBU/Alias: {cbu_alias}\n\n¡Muchas gracias por elegirnos!"
texto_url = urllib.parse.quote(texto_wa)

if telefono_cliente:
    num_limpio = telefono_cliente.replace("+", "").replace("-", "").replace(" ", "").replace("(", "").replace(")", "")
    if not num_limpio.startswith("54"): num_limpio = "54" + num_limpio
    whatsapp_url = f"https://wa.me{num_limpio}?text={texto_url}"
    st.success("✅ ¡Propuesta comercial generada de forma exitosa!")
    st.markdown(f"👉 **[HACÉ CLIC AQUÍ PARA ENVIAR POR WHATSAPP]({whatsapp_url})**")
else:
    st.info("💡 Ingresá el celular del cliente en el panel izquierdo para habilitar el envío directo por WhatsApp.")
