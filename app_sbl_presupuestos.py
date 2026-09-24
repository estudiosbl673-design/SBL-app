import streamlit as st
import datetime
import urllib.parse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

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

def generar_pdf_nativo():
    import io
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    style_n = styles['Normal']
    style_t = ParagraphStyle('T', parent=styles['Heading1'], fontSize=22, textColor=colors.HexColor('#1E3D59'), spaceAfter=15)
    style_sub = ParagraphStyle('S', parent=styles['Heading3'], fontSize=11, textColor=colors.HexColor('#17B890'), spaceAfter=15)
    style_r = ParagraphStyle('R', parent=style_n, alignment=2)
    
    story = []
    story.append(Paragraph("<b>⚡ SBL Seguridad Informática</b>", style_t))
    story.append(Paragraph(f"<b>Presupuesto N°:</b> {num_presupuesto} &nbsp;&nbsp;|&nbsp;&nbsp; <b>Fecha:</b> {fecha.strftime('%d/%m/%Y')}", style_sub))
    story.append(Spacer(1, 10))
    
    datos_c = [[Paragraph(f"<b>Cliente:</b> {cliente}", style_n), Paragraph(f"<b>Ubicación:</b> {domicilio}", style_n)]]
    t_c = Table(datos_c, colWidths=[3.75 * inch, 3.75 * inch])
    t_c.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F5F7FA')), ('PADDING', (0,0), (-1,-1), 8)]))
    story.append(t_c)
    story.append(Spacer(1, 20))
    
    tabla_data = [[Paragraph("<b>Detalle del Servicio / Concepto</b>", style_n), Paragraph("<b>Subtotal</b>", style_r)]]
    if tot_electricidad > 0: tabla_data.append([Paragraph("Mano de obra: Instalación Eléctrica Integral", style_n), Paragraph(f"${tot_electricidad:,}", style_r)])
    if tot_seguridad > 0: tabla_data.append([Paragraph("Mano de obra: Seguridad y Mantenimiento Técnico", style_n), Paragraph(f"${tot_seguridad:,}", style_r)])
    if tot_materiales > 0: tabla_data.append([Paragraph("Equipamiento: Materiales y Kits de Cámaras/Discos", style_n), Paragraph(f"${tot_materiales:,}", style_r)])
    tabla_data.append([Paragraph("<b>TOTAL A PRESUPUESTAR</b>", style_n), Paragraph(f"<b>${total_general:,}</b>", style_r)])
    
    t_d = Table(tabla_data, colWidths=[5.5 * inch, 2.0 * inch])
    t_d.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E3D59')), ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke), ('PADDING', (0,0), (-1,-1), 10), ('GRID', (0,0), (-1,-2), 0.5, colors.lightgrey), ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#E8F1F5'))]))
    story.append(t_d)
    story.append(Spacer(1, 20))
    
    terminos = f"• <b>Condición de Pago:</b> {condicion_pago}.<br/>• <b>Garantía:</b> Equipos con 1 año de garantía oficial de fábrica. Mano de obra por 90 días.<br/>• <b>Datos Bancarios:</b> Cuenta SBL | CBU/Alias: {cbu_alias}"
    story.append(Paragraph(terminos, style_n))
    
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

st.subheader("📥 Generación de Documento")

try:
    archivo_pdf = generar_pdf_nativo()
    st.download_button(
        label="📥 Descargar PDF Profesional Real",
        data=archivo_pdf,
        file_name=f"Presupuesto_{num_presupuesto}_{cliente.replace(' ', '_')}.pdf",
        mime="application/pdf",
        use_container_width=True
    )
except Exception as e:
    st.info("💡 Complete los datos de cantidad arriba para activar la descarga del archivo PDF.")

st.markdown("---")
st.subheader("📲 Panel de Envío por WhatsApp")

telefono_cliente = st.text_input("Celular del Cliente (Escribir números seguidos con código de área, Ej: 543816083885)", "543816083885")

# TEXTO DE WHATSAPP CORREGIDO: Dice 'Mano de obra Seguridad' sin la abreviatura 'manto.'
texto_wa = f"*⚡ SBL SEGURIDAD INFORMÁTICA *\n *Presupuesto Oficial N° {num_presupuesto}*\n📅 *Fecha:* {fecha.strftime('%d/%m/%Y')}\n👤 *Cliente:* {cliente}\n📍 *Obra:* {domicilio}\n-----------------------------------------\n*DESGLOSE DEL SERVICIO:* \n"
if tot_electricidad > 0: texto_wa += f"💡 *Mano de obra Eléctrica:* ${tot_electricidad:,}\n"
if tot_seguridad > 0: texto_wa += f"🛡️ *Mano de obra Seguridad:* ${tot_seguridad:,}\n"
if tot_materiales > 0: texto_wa += f"📦 *Materiales y Equipos:* ${tot_materiales:,}\n"

texto_wa += f"-----------------------------------------\n🔥 *TOTAL NETO: ${total_general:,}*\n-----------------------------------------\n📝 *Términos Comerciales:*\n• Pago: {condicion_pago}.\n• Garantía: Equipos 1 año, Mano de obra 90 días.\n🏦 *Datos de Transferencia:* \n• CBU/Alias: {cbu_alias}\n\n¡Muchas gracias por elegirnos!"
texto_url = urllib.parse.quote(texto_wa)

num_limpio = telefono_cliente.replace("+", "").replace("-", "").replace(" ", "").replace("(", "").replace(")", "")
whatsapp_url = f"https://wa.me{num_limpio}?text={texto_url}"

st.markdown(f"👉 **[HACÉ CLIC AQUÍ PARA ENVIAR EL RESUMEN POR WHATSAPP]({whatsapp_url})**")
