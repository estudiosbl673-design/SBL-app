import streamlit as st
import datetime
import urllib.parse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

st.set_page_config(page_title="SBL Presupuestos Profesionales", page_icon="⚡", layout="centered")

# ==========================================
#       SISTEMA DE SEGURIDAD PRIVADO
# ==========================================
def comprobar_contrasenia():
    if "autenticado" not in st.session_state:
        st.session_state.autenticado = False
    if st.session_state.autenticado:
        return True

    st.title("🔒 Acceso Restringido - SBL")
    st.subheader("Por favor, identifíquese para usar el generador profesional.")
    
    clave = st.text_input("Contraseña de acceso:", type="password")
    if st.button("Iniciar Sesión"):
        if clave == "SBL2026*":
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("❌ Contraseña incorrecta. Intente nuevamente.")
    return False

if not comprobar_contrasenia():
    st.stop()

# ==========================================
#       CÓDIGO DE LA APLICACIÓN (SBL)
# ==========================================
st.title("⚡ SBL Seguridad Informática")
st.subheader("Generador de Presupuestos Premium")

# Datos del Presupuesto
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

# Categoría 1: Electricidad
st.subheader("💡 1. Instalación Eléctrica")
c_bocas = st.number_input("Cantidad de Bocas Completas ($45.000 c/u)", min_value=0, value=0)
c_termicas = st.number_input("Instalación de Térmicas/Disyuntores ($32.000 c/u)", min_value=0, value=0)
c_aires = st.number_input("Líneas Exclusivas para A/A ($60.000 c/u)", min_value=0, value=0)

# Categoría 2: Cámaras y Mantenimiento
st.subheader("🛡️ 2. Seguridad, CCTV y Mantenimiento")
c_camaras = st.number_input("Instalación y Cableado de Cámaras Analógicas ($35.000 c/u)", min_value=0, value=4)
c_dvr = st.number_input("Configuración de DVR/NVR + Celulares ($40.000 c/u)", min_value=0, value=1)
c_mantenimiento = st.number_input("Mantenimiento Técnico / Limpieza de Cámaras ($15.000 c/u)", min_value=0, value=0)
c_metros = st.number_input("Metros de cableado excedente ($2.000 por metro)", min_value=0, value=0)

# Categoría 3: Materiales
st.subheader("📦 3. Materiales y Equipos")
incluye_materiales = st.checkbox("¿Incluir Kit de 4 Cámaras HD + Disco 1TB ($368.000)?", value=True)
otros_materiales = st.number_input("Otros materiales / Adicionales (Pesos $)", min_value=0, value=0)

# Datos de Pago Opcionales para el PDF
st.sidebar.markdown("---")
st.sidebar.header("🏦 Datos de Cobro (PDF)")
cbu_alias = st.sidebar.text_input("CBU / Alias Bancario", "SBL.SEGURIDAD.TUC")

# Entrada de Teléfono para WhatsApp en barra lateral
st.sidebar.markdown("---")
st.sidebar.header("📲 Enviar por WhatsApp")
telefono_cliente = st.sidebar.text_input("Celular del Cliente (Ej: 3816083885)", "")

# Precios Unitarios fijos para cálculos
P_BOCA = 45000
P_TERMICA = 32000
P_AIRE = 60000
P_CAMARA = 35000
P_DVR = 40000
P_MANTENIMIENTO = 15000
P_METRO = 2000
P_KIT = 368000

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

def generar_pdf():
    import io
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    
    styles = getSampleStyleSheet()
    style_normal = ParagraphStyle('Normal', parent=styles['Normal'], fontSize=10, leading=14, textColor=colors.HexColor('#2C3E50'))
    style_bold = ParagraphStyle('Bold', parent=style_normal, fontName='Helvetica-Bold')
    
    style_title = ParagraphStyle('DocTitle', fontName='Helvetica-Bold', fontSize=22, leading=26, textColor=colors.HexColor('#1A365D'))
    style_right_text = ParagraphStyle('RightText', parent=style_normal, alignment=2, fontSize=9, leading=13)
    style_section_h = ParagraphStyle('SecH', fontName='Helvetica-Bold', fontSize=12, leading=16, textColor=colors.HexColor('#1A365D'), spaceBefore=12, spaceAfter=6)
    
    style_cell = ParagraphStyle('Cell', parent=style_normal, fontSize=9, leading=12)
    style_cell_bold = ParagraphStyle('CellB', parent=style_bold, fontSize=9, leading=12)
    style_cell_right = ParagraphStyle('CellR', parent=style_cell, alignment=2)
    style_cell_right_bold = ParagraphStyle('CellRB', parent=style_bold, alignment=2)
    
    story = []
    
    header_data = [
        [
            Paragraph("<b>⚡ SBL SEGURIDAD INFORMÁTICA</b><br/><font size=9 color='#4A5568'>Soluciones Tecnológicas e Integrales</font>", style_title),
            Paragraph("<b>PRESUPUESTO OFICIAL</b><br/>"
                      f"<b>N°:</b> {num_presupuesto}<br/>"
                      f"<b>Fecha:</b> {fecha.strftime('%d/%m/%Y')}<br/>"
                      "<b>Validez:</b> 15 días", style_right_text)
        ]
    ]
    t_header = Table(header_data, colWidths=[330, 210])
    t_header.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
    story.append(t_header)
    
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#1A365D'), spaceAfter=15))
    
    info_data = [
        [Paragraph("<b>PROVEEDOR:</b>", style_cell_bold), Paragraph("<b>CLIENTE / OBRA:</b>", style_cell_bold)],
        [Paragraph("SBL Seguridad Informática<br/>San Miguel de Tucumán<br/>Email: info@sblseguridad.com", style_cell),
         Paragraph(f"<b>Nombre:</b> {cliente}<br/><b>Ubicación:</b> {domicilio}<br/><b>Estado:</b> Pendiente de Aprobación", style_cell)]
    ]
    t_info = Table(info_data, colWidths=[270, 270])
    t_info.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2D3748')),
        ('PADDING', (0,0), (-1,-1), 6),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor('#F7FAFC')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(t_info)
    
    story.append(Spacer(1, 15))
    story.append(Paragraph("DESGLOSE DETALLADO DE CONCEPTOS", style_section_h))
    
    th_style = ParagraphStyle('TH', parent=style_cell_bold, textColor=colors.whitesmoke)
    th_style_r = ParagraphStyle('THR', parent=style_cell_right_bold, textColor=colors.whitesmoke)
    
    items_table_data = [
        [Paragraph("Descripción del Ítem / Servicio Técnico", th_style), Paragraph("Cant.", th_style_r), Paragraph("P. Unitario", th_style_r), Paragraph("Subtotal", th_style_r)]
    ]
    
    # Estructura plana (Sin bloques if indentados para evitar errores del servidor)
    if c_bocas > 0:
        items_table_data.append([Paragraph("Mano de obra: Instalación de Bocas Eléctricas Completas", style_cell), Paragraph(str(c_bocas), style_cell_right), Paragraph(f"${P_BOCA:,}", style_cell_right), Paragraph(f"${c_bocas*P_BOCA:,}", style_cell_right)])
    if c_termicas > 0:
        items_table_data.append([Paragraph("Mano de obra: Montaje y conexión de Térmicas/Disyuntores", style_cell), Paragraph(str(c_termicas), style_cell_right), Paragraph(f"${P_TERMICA:,}", style_cell_right), Paragraph(f"${c_termicas*P_TERMICA:,}", style_cell_right)])
    if c_aires > 0:
        items_table_data.append([Paragraph("Mano de obra: Tendido de líneas exclusivas para Aire Acondicionado", style_cell), Paragraph(str(c_aires), style_cell_right), Paragraph(f"${P_AIRE:,}", style_cell_right), Paragraph(f"${c_aires*P_AIRE:,}", style_cell_right)])
    if c_camaras > 0:
        items_table_data.append([Paragraph("Mano de obra: Instalación, montaje y cableado de Cámaras Analógicas HD", style_cell), Paragraph(str(c_camaras), style_cell_right), Paragraph(f"${P_CAMARA:,}", style_cell_right), Paragraph(f"${c_camaras*P_CAMARA:,}", style_cell_right)])
    if c_dvr > 0:
        items_table_data.append([Paragraph("Servicio Técnico: Configuración de DVR/NVR + Enlace a celulares", style_cell), Paragraph(str(c_dvr), style_cell_right), Paragraph(f"${P_DVR:,}", style_cell_right), Paragraph(f"${c_dvr*P_DVR:,}", style_cell_right)])
    if c_mantenimiento > 0:
        items_table_data.append([Paragraph("Servicio Técnico: Mantenimiento correctivo, limpieza de lentes y calibración de Cámaras", style_cell), Paragraph(str(c_mantenimiento), style_cell_right), Paragraph(f"${P_MANTENIMIENTO:,}", style_cell_right), Paragraph(f"${c_mantenimiento*P_MANTENIMIENTO:,}", style_cell_right)])
    if c_metros > 0:
        items_table_data.append([Paragraph("Materiales: Metros de cableado estructurado/excedente de CCTV", style_cell), Paragraph(str(c_metros), style_cell_right), Paragraph(f"${P_METRO:,}", style_cell_right), Paragraph(f"${c_metros*P_METRO:,}", style_cell_right)])
    if incluye_materiales:
