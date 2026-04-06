"""
API Blueprint – JSON endpoint'leri (SRP).
"""

from flask import Blueprint, request, jsonify

from db_manager import get_db_connection
from app.decorators import login_required

api_bp = Blueprint('api', __name__)


@api_bp.route('/student_lookup')
@login_required
def api_student_lookup():
    no = request.args.get('no', '').strip()
    if not no or len(no) < 3:
        return {'found': False}
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT OgrenciNo, AdSoyad FROM Ogrenciler WHERE OgrenciNo = %s", (no,))
    row = cursor.fetchone()
    if row:
        return {'found': True, 'ad_soyad': row.AdSoyad or ''}
    return {'found': False}


@api_bp.route('/bolum_ogrenciler')
@login_required
def api_bolum_ogrenciler():
    bolum_id = request.args.get('bolum_id', '').strip()
    if not bolum_id:
        return {'ogrenciler': []}
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT OgrenciNo, AdSoyad FROM Ogrenciler WHERE BolumID = %s ORDER BY OgrenciNo",
        (bolum_id,)
    )
    rows = cursor.fetchall()
    return {'ogrenciler': [{'no': r.OgrenciNo, 'ad': r.AdSoyad or ''} for r in rows]}


@api_bp.route('/bolumler_list')
@login_required
def api_bolumler_list():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT BolumID, BolumAdi, OgretimTuru FROM Bolumler ORDER BY BolumAdi")
    rows = cursor.fetchall()
    return jsonify([{'id': r.BolumID, 'adi': f"{r.BolumAdi} ({r.OgretimTuru})"} for r in rows])


@api_bp.route('/takvim_events')
@login_required
def api_takvim_events():
    bolum_id = request.args.get('bolum_id', '')
    tur = request.args.get('tur', '')
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        SELECT sp.SunumID, sp.HaftaNo, k.KonuAdi, sp.OgretimTuru, sp.SunumTarihi,
               STRING_AGG(DISTINCT o.AdSoyad, ', ') AS Atananlar
        FROM SunumProgrami sp
        JOIN Konular k ON k.KonuID=sp.KonuID
        LEFT JOIN SunumGorevlileri sg ON sg.SunumID=sp.SunumID
        LEFT JOIN Ogrenciler o ON o.OgrenciID=sg.OgrenciID
    """
    params = []
    where = []
    if bolum_id:
        where.append("sp.BolumID=%s")
        params.append(bolum_id)
    if tur:
        where.append("sp.OgretimTuru=%s")
        params.append(tur)
    if where:
        query += " WHERE " + " AND ".join(where)
    query += " GROUP BY sp.SunumID, sp.HaftaNo, k.KonuAdi, sp.OgretimTuru, sp.SunumTarihi ORDER BY sp.HaftaNo"
    cursor.execute(query, params)
    rows = cursor.fetchall()
    events = []
    for row in rows:
        if not row.SunumTarihi:
            continue
        event_date = row.SunumTarihi
        color = '#3b82f6' if row.OgretimTuru == 'Örgün' else '#8b5cf6'
        if row.Atananlar:
            color = '#10b981'
        events.append({
            'id': row.SunumID,
            'title': f"H{row.HaftaNo}: {row.KonuAdi}",
            'start': event_date.isoformat(),
            'color': color,
            'extendedProps': {
                'konu': row.KonuAdi,
                'hafta': row.HaftaNo,
                'tur': row.OgretimTuru,
                'atananlar': row.Atananlar or '—',
                'sunum_id': row.SunumID,
            }
        })
    return jsonify(events)
