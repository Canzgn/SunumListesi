"""
Yetkilendirme decorator'ları – Open/Closed Principle.
Yeni roller eklendiğinde mevcut kod değişmez, yeni decorator yazılır.
"""

from functools import wraps
from flask import session, redirect, url_for


def role_required(*roles):
    """Belirtilen rollerden birine sahip olmayanı login'e yönlendirir."""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if session.get('user_role') not in roles:
                return redirect(url_for('auth.login'))
            return f(*args, **kwargs)
        return wrapper
    return decorator


def admin_required(f):
    """admin veya hoca rolü gerektirir."""
    return role_required('admin', 'hoca')(f)


def hoca_required(f):
    """hoca veya admin rolü gerektirir."""
    return role_required('hoca', 'admin')(f)


def student_required(f):
    """student rolü gerektirir."""
    return role_required('student')(f)


def kontrolcu_required(f):
    """kontrolcu rolü gerektirir."""
    return role_required('kontrolcu')(f)


def login_required(f):
    """Herhangi bir rol ile giriş yapmış olmayı gerektirir."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get('user_role'):
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return wrapper
