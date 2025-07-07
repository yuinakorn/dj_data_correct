# Django Project

โครงสร้างโปรเจค Django พร้อมใช้งาน

## วิธีการติดตั้ง

1. สร้างและเปิดใช้งาน virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # บน Windows ใช้ `venv\Scripts\activate`
```

2. ติดตั้ง requirements:
```bash
pip install -r requirements.txt
```

3. รัน migrations:
```bash
python manage.py migrate
```

4. สร้าง superuser (ไม่จำเป็น):
```bash
python manage.py createsuperuser
```

5. รันเซิร์ฟเวอร์:
```bash
python manage.py runserver
```

6. เปิดเบราว์เซอร์ที่: http://127.0.0.1:8000/

## โครงสร้างโปรเจค

- `config/` - การตั้งค่าโปรเจคหลัก
- `core/` - แอปหลักของโปรเจค
- `templates/` - ไฟล์เทมเพลต
- `static/` - ไฟล์ static (CSS, JavaScript, รูปภาพ)
- `media/` - ไฟล์ที่อัปโหลดโดยผู้ใช้

## เริ่มต้นพัฒนา

1. สร้างแอปใหม่:
```bash
python manage.py startapp your_app_name
```

2. อย่าลืมเพิ่มแอปลงใน `INSTALLED_APPS` ในไฟล์ `config/settings.py`
# dj_data_correct
