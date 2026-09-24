import streamlit as st
import datetime
import urllib.parse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

st.set_page_config(page_title="SBL Presupuestos", page_icon="⚡", layout="centered")

# ==========================================
#       SISTEMA DE SEGURIDAD PRIVADO
# ==========================================
def comprobar_contrasenia():
    if "autenticado" not in st.session_state:
        st.session_state.autenticado = False
    if st.session_state.autenticado:
        return True

    st.title("🔒 Acceso Restringido - SBL")
    st.subheader("Por favor, identifíquese para usar el generador.")
    
    clave = st.text_input("Contraseña de acceso:", type="password")
    if st.button("Iniciar Sesión"):
        if clave == "SBL2026*":  # <-- AQUÍ CAMBIÁS TU CONTRASEÑA
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("❌ Contraseña incorrecta. Intente nuevamente.")
    return False

# Si no está autenticado, detiene la aplicación aquí
if not comprobar_contrasenia():
    st.stop()

# ==========================================
#       CÓDIGO DE LA APLICACIÓN (SBL)
# ==========================================
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

# Entrada de Teléfono para WhatsApp en barra lateral
st.sidebar.markdown("---")
st.sidebar.header("📲 Enviar por WhatsApp")
telefono_cliente = st.sidebar.text_input("Celular del Cliente (Ej: 3815551234)", "")

# Cálculos de Totales
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

st.markdown("---")

def generar_pdf():
    import io
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40, title=f"Presupuesto_{num_presupuesto}")
    
    styles = getSampleStyleSheet()
    style_normal = styles['Normal']
    style_title = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=24, textColor=colors.HexColor('#1E3D59'), spaceAfter=15)
    style_subtitle = ParagraphStyle('SubTitleStyle', parent=styles['Heading3'], fontSize=12, textColor=colors.HexColor('#17B890'), spaceAfter=15)
    style_header = ParagraphStyle('HeaderStyle', parent=styles['Heading2'], fontSize=14, textColor=colors.HexColor('#1E3D59'), spaceAfter=10, spaceBefore=10)
    style_right = ParagraphStyle('RightStyle', parent=style_normal, alignment=2)
    style_bold_right = ParagraphStyle('BoldRightStyle', parent=style_normal, fontName='Helvetica-Bold', alignment=2)
    
    story = []
    story.append(Paragraph("<b>⚡ SBL Seguridad Informática</b>", style_title))
    story.append(Paragraph(f"<b>N° de Presupuesto:</b> {num_presupuesto} &nbsp;&nbsp;|&nbsp;&nbsp; <b>Fecha:</b> {fecha.strftime('%d/%m/%Y')}", style_subtitle))
    story.append(Spacer(1, 10))
    
    datos_cliente = [
        [Paragraph(f"<b>Cliente:</b> {cliente}", style_normal), Paragraph(f"<b>Domicilio de Obra:</b> {domicilio}", style_normal)]
    ]
    t_cliente = Table(datos_cliente, colWidths=[260, 260])
    t_cliente.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F5F7FA')),
        ('PADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_cliente)
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("<b>🛠️ Detalle del Presupuesto</b>", style_header))
    
    style_th = ParagraphStyle('TH', parent=style_normal, textColor=colors.whitesmoke, fontName='Helvetica-Bold')
    style_th_r = ParagraphStyle('THR', parent=style_right, textColor=colors.whitesmoke, fontName='Helvetica-Bold')
    
    tabla_datos = [
        [Paragraph("Descripción del concepto / Servicio", style_th), Paragraph("Subtotal", style_th_r)]
    ]
    
    if tot_electricidad > 0:
        desc_elec = f"Mano de obra Instalación Eléctrica ({c_bocas} bocas, {c_termicas} térmicas, {c_aires} líneas A/A)"
        tabla_datos.append([Paragraph(desc_elec, style_normal), Paragraph(f"${tot_electricidad:,}", style_right)])
        
    if tot_seguridad > 0:
        desc_seg = f"Mano de obra Seguridad y CCTV ({c_camaras} cámaras, {c_dvr} DVR, {c_metros}m cable)"
        tabla_datos.append([Paragraph(desc_seg, style_normal), Paragraph(f"${tot_seguridad:,}", style_right)])
        
    if tot_materiales > 0:
        desc_mat = "Materiales y Equipamiento"
        if incluye_materiales:
            desc_mat += " (Kit 4 Cámaras HD + Disco 1TB)"
        if otros_materiales > 0:
            desc_mat += " + Adicionales"
        tabla_datos.append([Paragraph(desc_mat, style_normal), Paragraph(f"${tot_materiales:,}", style_right)])
        
    tabla_datos.append([Paragraph("<b>TOTAL A PRESUPUESTAR</b>", style_normal), Paragraph(f"<b>${total_general:,}</b>", style_bold_right)])
    
    t_detalle = Table(tabla_datos, colWidths=[400, 120])
    t_detalle.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E3D59')),
        ('PADDING', (0,0), (-1,-1), 10),
        ('GRID', (0,0), (-1,-2), 0.5, colors.lightgrey),
        ('LINEABOVE', (0,-1), (-1,-1), 1.5, colors.HexColor('#1E3D59')),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#E8F1F5')),
    ]))
    
    story.append(t_detalle)
    story.append(Spacer(1, 30))
    story.append(Paragraph("<i>Este presupuesto tiene una validez de 15 días a partir de la fecha de emisión. Precios sujetos a variaciones de mercado.</i>", style_normal))
    
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

pdf_data = generar_pdf()

st.download_button(
    label="📥 Descargar PDF Profesional",
    data=pdf_data,
    file_name=f"Presupuesto_{num_presupuesto}_{cliente.replace(' ', '_')}.pdf",
    mime="application/pdf"
)

# ... (deja todo lo de arriba del PDF exactamente igual)

texto_wa = f"*⚡ SBL Seguridad Informática*\n" \
           f"Hola {cliente}, te adjuntamos el resumen del *Presupuesto N° {num_presupuesto}*.\n\n" \
           f"💡 Mano de Obra Eléctrica: ${tot_electricidad:,}\n" \
           f"🛡️ Mano de Obra Seguridad: ${tot_seguridad:,}\n" \
           f"📦 Materiales y Equipos: ${tot_materiales:,}\n" \
           f"🔥 *TOTAL A PRESUPUESTAR: ${total_general:,}*\n\n" \
           f"Te enviamos el documento PDF formal por este medio."

texto_url = urllib.parse.quote(texto_wa)

if telefono_cliente:
    num_limpio = telefono_cliente.replace("+", "").replace("-", "").replace(" ", "").replace("(", "").replace(")", "")
    if not num_limpio.startswith("54"):
        num_limpio = "54" + num_limpio
    
    whatsapp_url = f"https://wa.me{num_limpio}?text={texto_url}"

    
    # NUEVO MÉTODO SEGURO: Enlace directo en Markdown que salta los bloqueos del navegador
    st.markdown(f'<a href="{whatsapp_url}" target="_self" style="text-decoration: none;"><button style="background-color: #25D366; color: white; border: none; padding: 10px 20px; border-radius: 5px; font-size: 16px; font-weight: bold; cursor: pointer; width: 100%;">💬 Enviar Resumen por WhatsApp</button></a>', unsafe_allow_html=True)
else:
    st.info("💡 Ingresá el celular del cliente en el panel izquierdo para habilitar el botón de envío directo por WhatsApp.")

