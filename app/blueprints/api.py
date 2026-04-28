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


@api_bp.route('/search_students')
@login_required
def api_search_students():
    """Öğrenci numarası veya adına göre anlık arama (autocomplete için).
    sunum_id verilirse: aynı OgretimTuru + sunum sahiplerini hariç tut."""
    q = request.args.get('q', '').strip()
    sunum_id = request.args.get('sunum_id', '').strip()
    if len(q) < 2:
        return jsonify([])
    conn = get_db_connection()
    cursor = conn.cursor()

    extra_filters = ""
    params: list = [f'%{q}%', f'%{q}%']

    if sunum_id:
        # Aynı öğretim türünden öğrenciler — Bolumler üzerinden güvenli join
        extra_filters += """
            AND EXISTS (
                SELECT 1 FROM Bolumler b
                WHERE b.BolumID = o.BolumID
                  AND b.OgretimTuru = (
                      SELECT OgretimTuru FROM SunumProgrami WHERE SunumID = %s LIMIT 1
                  )
            )
        """
        params.append(sunum_id)
        # Sunum sahiplerini hariç tut
        extra_filters += """
            AND o.OgrenciNo NOT IN (
                SELECT o2.OgrenciNo FROM SunumGorevlileri sg
                JOIN Ogrenciler o2 ON o2.OgrenciID = sg.OgrenciID
                WHERE sg.SunumID = %s
            )
        """
        params.append(sunum_id)

    cursor.execute(f"""
        SELECT o.OgrenciNo, o.AdSoyad
        FROM Ogrenciler o
        WHERE (o.OgrenciNo ILIKE %s OR o.AdSoyad ILIKE %s)
          AND o.IsApproved = TRUE
          {extra_filters}
        ORDER BY o.OgrenciNo
        LIMIT 10
    """, params)
    rows = cursor.fetchall()
    return jsonify([{'no': r.OgrenciNo, 'ad': r.AdSoyad or ''} for r in rows])


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


@api_bp.route('/tatil_gunleri')
def api_tatil_gunleri():
    donem_id = request.args.get('donem_id', type=int)
    conn = get_db_connection()
    cursor = conn.cursor()
    if donem_id:
        cursor.execute(
            "SELECT tarih, aciklama, eylemtipi FROM TatilGunleri WHERE donemid=%s ORDER BY tarih",
            (donem_id,)
        )
    else:
        cursor.execute("SELECT tarih, aciklama, eylemtipi FROM TatilGunleri ORDER BY tarih")
    events = []
    for t in cursor.fetchall():
        events.append({
            "title": t.aciklama or "Tatil",
            "start": t.tarih.isoformat(),
            "display": "background",
            "color": "#ef4444" if t.eylemtipi == 'kaydir' else "#f59e0b",
            "extendedProps": {"eylemtipi": t.eylemtipi}
        })
    return jsonify(events)
