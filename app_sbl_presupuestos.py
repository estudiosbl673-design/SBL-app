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
st.subheader("Generador de Presupuestos Desglosados")

st.sidebar.header("⚙️ Configuración")
num_presupuesto = st.sidebar.text_input("N° de Presupuesto", "0001-0026")
fecha = st.sidebar.date_input("Fecha de Emisión", datetime.date.today())

st.header("👤 Datos del Cliente")
col1, col2 = st.columns(2)
with col1:
    cliente = st.text_input("Nombre del Cliente / Empresa", "Cliente Ejemplo")
with col2:
    domicilio = st.text_input("Domicilio de la Obra", "San Miguel de Tucumán")

st.header("🛠️ Desglose del Trabajo Técnico")

st.subheader("💡 1. Trabajos de Instalación Eléctrica")
c_bocas = st.number_input("Cantidad de Bocas Completas ($45.000 c/u)", min_value=0, value=0)
c_tomas = st.number_input("Colocación de Tomas / Módulos ($15.000 c/u)", min_value=0, value=0)
c_termicas = st.number_input("Colocación de Térmicas / Disyuntores ($32.000 c/u)", min_value=0, value=0)

st.subheader("🛡️ 2. Trabajos de Seguridad y CCTV")
c_camaras = st.number_input("Montaje de Cámaras ($35.000 c/u)", min_value=0, value=4)
c_cableado = st.number_input("Tendido de Cableado de Cámaras ($12.000 c/u)", min_value=0, value=4)
c_caneria = st.number_input("Instalación de Cañerías / Conducción ($18.000 c/u)", min_value=0, value=0)
c_dvr = st.number_input("Configuración de DVR / NVR + Enlace Celular ($40.000 c/u)", min_value=0, value=1)
c_mantenimiento = st.number_input("Mantenimiento Técnico / Limpieza General ($15.000 c/u)", min_value=0, value=0)

st.subheader("📦 3. Materiales y Equipos")
incluye_materiales = st.checkbox("¿Incluir Kit de 4 Cámaras HD + Disco 1TB ($368.000)?", value=True)
otros_materiales = st.number_input("Otros materiales / Equipos Adicionales (Pesos $)", min_value=0, value=0)

P_BOCA, P_TOMA, P_TERMICA = 45000, 15000, 32000
P_CAMARA, P_CABLEADO, P_CANERIA, P_DVR, P_MANTENIMIENTO, P_KIT = 35000, 12000, 18000, 40000, 15000, 368000

tot_mano_obra = (c_bocas * P_BOCA) + (c_tomas * P_TOMA) + (c_termicas * P_TERMICA) + \
                 (c_camaras * P_CAMARA) + (c_cableado * P_CABLEADO) + (c_caneria * P_CANERIA) + \
                 (c_dvr * P_DVR) + (c_mantenimiento * P_MANTENIMIENTO)

tot_materiales = (P_KIT if incluye_materiales else 0) + otros_materiales
total_general = tot_mano_obra + tot_materiales

st.markdown("---")
st.header("💰 Resumen del Presupuesto")
st.write(f"**Total Mano de Obra Desglosada:** ${tot_mano_obra:,}")
st.write(f"**Total Materiales y Equipos:** ${tot_materiales:,}")
st.markdown(f"### 🔥 **TOTAL A PRESUPUESTAR: ${total_general:,}**")
st.markdown("---")

def generar_pdf_desglosado():
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
    story.append(Spacer(1, 15))
    
    tabla_data = [[Paragraph("<b>Descripción del Trabajo / Materiales</b>", style_n), Paragraph("<b>Cant.</b>", style_r), Paragraph("<b>Subtotal</b>", style_r)]]
    
    if c_bocas > 0: tabla_data.append([Paragraph("Mano de obra: Instalación de Bocas Eléctricas Completas", style_n), Paragraph(str(c_bocas), style_r), Paragraph(f"${c_bocas*P_BOCA:,}", style_r)])
    if c_tomas > 0: tabla_data.append([Paragraph("Mano de obra: Colocación de Tomas / Módulos", style_n), Paragraph(str(c_tomas), style_r), Paragraph(f"${c_tomas*P_TOMA:,}", style_r)])
    if c_termicas > 0: tabla_data.append([Paragraph("Mano de obra: Colocación de Térmicas / Disyuntores", style_n), Paragraph(str(c_termicas), style_r), Paragraph(f"${c_termicas*P_TERMICA:,}", style_r)])
    if c_camaras > 0: tabla_data.append([Paragraph("Mano de obra: Montaje de Cámaras de Seguridad", style_n), Paragraph(str(c_camaras), style_r), Paragraph(f"${c_camaras*P_CAMARA:,}", style_r)])
    if c_cableado > 0: tabla_data.append([Paragraph("Mano de obra: Tendido de Cableado de Cámaras", style_n), Paragraph(str(c_cableado), style_r), Paragraph(f"${c_cableado*P_CABLEADO:,}", style_r)])
    if c_caneria > 0: tabla_data.append([Paragraph("Mano de obra: Instalación de Cañerías / Conducción", style_n), Paragraph(str(c_caneria), style_r), Paragraph(f"${c_caneria*P_CANERIA:,}", style_r)])
    if c_dvr > 0: tabla_data.append([Paragraph("Mano de obra: Configuración de DVR / NVR + Enlace Celular", style_n), Paragraph(str(c_dvr), style_r), Paragraph(f"${c_dvr*P_DVR:,}", style_r)])
    if c_mantenimiento > 0: tabla_data.append([Paragraph("Mano de obra: Mantenimiento Técnico / Limpieza General", style_n), Paragraph(str(c_mantenimiento), style_r), Paragraph(f"${c_mantenimiento*P_MANTENIMIENTO:,}", style_r)])
    if incluye_materiales: tabla_data.append([Paragraph("Equipamiento: Kit completo de 4 Cámaras HD + Disco Rígido 1TB", style_n), Paragraph("1", style_r), Paragraph(f"${P_KIT:,}", style_r)])
    if otros_materiales > 0: tabla_data.append([Paragraph("Equipamiento: Materiales o componentes adicionales", style_n), Paragraph("1", style_r), Paragraph(f"${otros_materiales:,}", style_r)])
    
    tabla_data.append([Paragraph("<b>TOTAL A PRESUPUESTAR</b>", style_n), Paragraph(""), Paragraph(f"<b>${total_general:,}</b>", style_r)])
    
    t_d = Table(tabla_data, colWidths=[4.5 * inch, 1.0 * inch, 2.0 * inch])
    t_d.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E3D59')), ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke), ('PADDING', (0,0), (-1,-1), 8), ('GRID', (0,0), (-1,-2), 0.5, colors.lightgrey), ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#E8F1F5'))]))
    story.append(t_d)
    story.append(Spacer(1, 20))
    
    terminos = "<b>TÉRMINOS COMERCIALES:</b><br/>" \
               "• Validez del presupuesto: 10 días a partir de la fecha de emisión.<br/>" \
               "• Garantía: Cobertura de 90 días válida exclusivamente para la mano de obra contratada.<br/>" \
               "• Nota sobre dispositivos: La garantía por materiales, cámaras o dispositivos electrónicos corresponde y se rige según los términos provistos por el fabricante de los mismos."
    story.append(Paragraph(terminos, style_n))
    
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

st.subheader("📥 Generación de Documento")

try:
    archivo_pdf = generar_pdf_desglosado()
    st.download_button(
        label="📥 Descargar PDF Detallado Real",
        data=archivo_pdf,
        file_name=f"Presupuesto_{num_presupuesto}_{cliente.replace(' ', '_')}.pdf",
        mime="application/pdf",
        use_container_width=True
    )
except Exception as e:
    st.info("💡 Modifique las cantidades arriba para actualizar el documento de descarga.")

st.markdown("---")
st.subheader("📲 Panel de Envío por WhatsApp")

# CASILLA DE TELÉFONO MOVIDA AL CENTRO DE LA PANTALLA PRINCIPAL ABAJO DEL PDF
telefono_cliente = st.text_input("Celular del Cliente (Escribir números seguidos con código de área, Ej: 543816083885)", "543816083885")

texto_wa = f"*⚡ SBL SEGURIDAD INFORMÁTICA *\n *Presupuesto Oficial N° {num_presupuesto}*\n📅 *Fecha:* {fecha.strftime('%d/%m/%Y')}\n👤 *Cliente:* {cliente}\n📍 *Obra:* {domicilio}\n-----------------------------------------\n*DESGLOSE DEL SERVICIO:* \n"
if tot_mano_obra > 0: texto_wa += f"💡 *Mano de obra:* ${tot_mano_obra:,}\n"
if tot_materiales > 0: texto_wa += f"📦 *Materiales y Equipos:* ${tot_materiales:,}\n"
texto_wa += f"-----------------------------------------\n🔥 *TOTAL NETO: ${total_general:,}*\n-----------------------------------------\n⏳ *Validez del presupuesto:* 10 días.\n🛡️ *Garantía:* Cobertura de 90 días exclusiva para la mano de obra. La garantía por materiales o dispositivos electrónicos rige según el fabricante.\n\n¡Muchas gracias por elegirnos!"

texto_url = urllib.parse.quote(texto_wa)

num_limpio = telefono_cliente.replace("+", "").replace("-", "").replace(" ", "").replace("(", "").replace(")", "")
if not num_limpio.startswith("54"):
    num_limpio = "54" + num_limpio

