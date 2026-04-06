"""
Export Blueprint – Excel ve PDF dışa aktarım (SRP).
"""

from flask import Blueprint, request, send_file
from datetime import datetime
import io

from db_manager import get_db_connection
from app.decorators import admin_required, hoca_required
from app.utils import get_admin_bolum_ids

export_bp = Blueprint('export', __name__)


def _get_export_rows(tur, bolum_id=None, bolum_ids=None):
    """Ortak SQL sorgusunu çalıştırır, satırları döner (DRY)."""
    conn = get_db_connection()
    cursor = conn.cursor()
    base_sql = """
        SELECT sp.SunumID, sp.HaftaNo, k.KonuAdi,
               STRING_AGG(DISTINCT o.AdSoyad||' ('||o.OgrenciNo||')', ', ') AS Atananlar
        FROM SunumProgrami sp
        JOIN Konular k ON k.KonuID=sp.KonuID
        LEFT JOIN SunumGorevlileri sg ON sg.SunumID=sp.SunumID
        LEFT JOIN Ogrenciler o ON o.OgrenciID=sg.OgrenciID
        WHERE {condition}
        GROUP BY sp.SunumID, sp.HaftaNo, k.KonuAdi, k.SiraNo
        ORDER BY sp.HaftaNo, k.SiraNo
    """
    if bolum_id:
        cursor.execute(base_sql.format(condition="sp.BolumID=%s"), (bolum_id,))
    elif bolum_ids:
        cursor.execute(base_sql.format(condition="sp.BolumID = ANY(%s)"), (bolum_ids,))
    else:
        cursor.execute(base_sql.format(condition="sp.OgretimTuru=%s"), (tur,))
    return cursor.fetchall()


def _build_excel(tur, bolum_id=None, bolum_ids=None):
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    rows = _get_export_rows(tur, bolum_id, bolum_ids)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Sunum Programı"

    header_fill = PatternFill("solid", fgColor="1e293b")
    header_font = Font(bold=True, color="FFFFFF", size=11)
    thin = Side(style='thin', color="d1d5db")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)

    headers = ["Hafta No", "Konu Adı", "Atanan Öğrenci(ler)", "Durum"]
    ws.column_dimensions['A'].width = 12
    ws.column_dimensions['B'].width = 45
    ws.column_dimensions['C'].width = 45
    ws.column_dimensions['D'].width = 14

    for col, h in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=h)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal='center', vertical='center')
        cell.border = border

    green_fill = PatternFill("solid", fgColor="d1fae5")
    for i, row in enumerate(rows, 2):
        atanan = row.Atananlar or "—"
        durum = "Onaylandı" if row.Atananlar else "Bekliyor"
        values = [row.HaftaNo, row.KonuAdi, atanan, durum]
        fill = green_fill if row.Atananlar else None
        for col, val in enumerate(values, 1):
            cell = ws.cell(row=i, column=col, value=val)
            cell.border = border
            cell.alignment = Alignment(wrap_text=True, vertical='center')
            if fill:
                cell.fill = fill

    ws.freeze_panes = "A2"
    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    return buf


def _build_pdf(tur, bolum_id=None, bolum_ids=None):
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib import colors
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    rows = _get_export_rows(tur, bolum_id, bolum_ids)

    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=landscape(A4),
                            leftMargin=1.5*cm, rightMargin=1.5*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=14, spaceAfter=10)
    cell_style = ParagraphStyle('Cell', parent=styles['Normal'], fontSize=8, leading=11)
    elems = []
    elems.append(Paragraph(f"Sunum Programı – {tur}", title_style))
    elems.append(Paragraph(f"Oluşturma Tarihi: {datetime.now().strftime('%d.%m.%Y %H:%M')}", styles['Normal']))
    elems.append(Spacer(1, 0.5*cm))
    data = [['Hafta No', 'Konu Adı', 'Atanan Öğrenci(ler)', 'Durum']]
    for row in rows:
        atanan = row.Atananlar or '—'
        durum = 'Onaylandı' if row.Atananlar else 'Bekliyor'
        data.append([
            str(row.HaftaNo),
            Paragraph(row.KonuAdi, cell_style),
            Paragraph(atanan, cell_style),
            durum,
        ])
    col_widths = [2*cm, 8*cm, 12*cm, 3*cm]
    table = Table(data, colWidths=col_widths, repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e293b')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elems.append(table)
    doc.build(elems)
    buf.seek(0)
    return buf


# --- Admin Export ---

@export_bp.route('/admin/export/excel')
@admin_required
def admin_export_excel():
    tur = request.args.get('tur', 'Örgün')
    admin_bolum_ids = get_admin_bolum_ids()
    if admin_bolum_ids is not None and len(admin_bolum_ids) > 0:
        buf = _build_excel(tur, bolum_ids=admin_bolum_ids)
    else:
        buf = _build_excel(tur)
    fname = f"sunum_programi_{tur}_{datetime.now().strftime('%Y%m%d')}.xlsx"
    return send_file(buf, as_attachment=True, download_name=fname,
                     mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


@export_bp.route('/admin/export/pdf')
@admin_required
def admin_export_pdf():
    tur = request.args.get('tur', 'Örgün')
    admin_bolum_ids = get_admin_bolum_ids()
    if admin_bolum_ids is not None and len(admin_bolum_ids) > 0:
        buf = _build_pdf(tur, bolum_ids=admin_bolum_ids)
    else:
        buf = _build_pdf(tur)
    fname = f"sunum_programi_{tur}_{datetime.now().strftime('%Y%m%d')}.pdf"
    return send_file(buf, as_attachment=True, download_name=fname, mimetype='application/pdf')


# --- Hoca Export ---

@export_bp.route('/hoca/export/excel')
@hoca_required
def hoca_export_excel():
    bolum_id = request.args.get('bolum_id', '')
    tur = request.args.get('tur', 'Örgün')
    buf = _build_excel(tur, bolum_id=bolum_id or None)
    fname = f"sunum_programi_{datetime.now().strftime('%Y%m%d')}.xlsx"
    return send_file(buf, as_attachment=True, download_name=fname,
                     mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


@export_bp.route('/hoca/export/pdf')
@hoca_required
def hoca_export_pdf():
    bolum_id = request.args.get('bolum_id', '')
    tur = request.args.get('tur', 'Örgün')
    buf = _build_pdf(tur, bolum_id=bolum_id or None)
    fname = f"sunum_programi_{datetime.now().strftime('%Y%m%d')}.pdf"
    return send_file(buf, as_attachment=True, download_name=fname, mimetype='application/pdf')
