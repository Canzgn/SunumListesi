from app import create_app
app = create_app()

with app.test_client() as c:
    with c.session_transaction() as sess:
        sess['user_role'] = 'admin'
        sess['admin_id'] = 1
        sess['admin_name'] = 'Test Admin'
    
    resp = c.get('/admin/panel')
    print('Status:', resp.status_code)
    if resp.status_code == 302:
        print('Redirect to:', resp.location)
    elif resp.status_code == 500:
        print('500 ERROR — ilk 500 karakter:')
        print(resp.data.decode('utf-8')[:500])
    else:
        print('OK - render başarılı')

# Hoca panel testi
with app.test_client() as c:
    with c.session_transaction() as sess:
        sess['user_role'] = 'hoca'
        sess['hoca_id'] = 1
        sess['hoca_name'] = 'Test Hoca'
    
    resp = c.get('/hoca/panel')
    print('Hoca panel status:', resp.status_code)
    if resp.status_code == 500:
        print('HOCA 500 ERROR:')
        print(resp.data.decode('utf-8')[:500])
    elif resp.status_code == 302:
        print('Hoca redirect to:', resp.location)
    else:
        print('Hoca panel OK')
