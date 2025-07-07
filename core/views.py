from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from datetime import datetime, timedelta

def home(request):
    return render(request, 'core/home.html', {'title': 'หน้าแรก'})


def login_view(request):
    """หน้า login ที่ใช้ Provider ID แทน username/password"""
    if request.user.is_authenticated:
        return redirect('core:home')
    
    # ตรวจสอบ JWT token จาก URL parameter
    jwt_token = request.GET.get('t')
    if jwt_token:
        try:
            # ตรวจสอบและ validate JWT token
            user = authenticate(request, providerid_token=jwt_token)
            
            if user:
                login(request, user)
                messages.success(request, f'เข้าสู่ระบบสำเร็จด้วย Provider ID - {user.first_name} {user.last_name}')
                return redirect('core:home')
            else:
                messages.error(request, 'การยืนยันตัวตนด้วย Provider ID ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง')
                return redirect('core:login')
        except Exception as e:
            messages.error(request, f'เกิดข้อผิดพลาดในการตรวจสอบ Provider ID: {str(e)}')
            return redirect('core:login')
    
    if request.method == 'POST':
        # จำลองการ login ด้วย Provider ID
        # ในระบบจริงจะต้องเชื่อมต่อกับ Provider ID API
        providerid_response = request.POST.get('providerid_response')
        
        if providerid_response:
            # จำลองการตรวจสอบ Provider ID
            # ในระบบจริงจะต้องตรวจสอบกับ Provider ID server
            user = authenticate(request, providerid_token=providerid_response)
            
            if user:
                login(request, user)
                messages.success(request, 'เข้าสู่ระบบสำเร็จด้วย Provider ID')
                return redirect('core:home')
            else:
                messages.error(request, 'การยืนยันตัวตนด้วย Provider ID ไม่สำเร็จ')
        else:
            messages.error(request, 'กรุณาเข้าสู่ระบบด้วย Provider ID')
    
    return render(request, 'core/login.html')


def logout_view(request):
    """ออกจากระบบ"""
    logout(request)
    messages.success(request, 'ออกจากระบบสำเร็จ')
    return redirect('core:home')


@login_required
def dashboard(request):
    """หน้า dashboard สำหรับผู้ใช้ที่ login แล้ว"""
    
    # สำหรับตอนนี้ใช้ข้อมูล mock เพื่อแสดงตัวอย่าง
    # ในอนาคตจะดึงจากฐานข้อมูลจริง
    
    context = {
        'total_anomalies': 1247,
        'critical_issues': 43,
        'resolved_count': 892,
        'affected_facilities': 127,
        'total_facilities': 450,
        'categories': [
            {
                'name': 'ข้อมูลเด็กนักเรียน',
                'description': 'น้ำหนัก/ส่วนสูงผิดปกติ',
                'count': 324,
                'new_count': 18,
                'icon_color': 'orange'
            },
            {
                'name': 'ข้อมูลผู้สูงอายุ',
                'description': 'อายุเกิน 150 ปี',
                'count': 89,
                'new_count': 5,
                'icon_color': 'purple'
            },
            {
                'name': 'ข้อมูลการฉีดวัคซีน',
                'description': 'วันที่ไม่สมเหตุสมผล',
                'count': 156,
                'new_count': 3,
                'icon_color': 'green'
            },
            {
                'name': 'ข้อมูลการรักษา',
                'description': 'ข้อมูลไม่สอดคล้องกัน',
                'count': 234,
                'new_count': 12,
                'icon_color': 'red'
            }
        ],
        'recent_alerts': [
            {
                'severity': 'critical',
                'title': 'ข้อมูลวิกฤติ',
                'description': 'เด็กอายุ 5 ปี น้ำหนัก 250 กก.',
                'facility': 'โรงพยาบาลเชียงใหม่'
            },
            {
                'severity': 'high',
                'title': 'ต้องตรวจสอบ',
                'description': 'ผู้สูงอายุ 180 ปี',
                'facility': 'ศูนย์สุขภาพบ้านแม่ริม'
            },
            {
                'severity': 'medium',
                'title': 'ข้อมูลผิดปกติ',
                'description': 'ส่วนสูง 300 ซม.',
                'facility': 'คลินิกหางดง'
            }
        ]
    }
    
    return render(request, 'core/dashboard.html', context)


@login_required
def profile(request):
    """หน้าโปรไฟล์ของผู้ใช้"""
    return render(request, 'core/profile.html')


@login_required
def file_correct(request):
    """หน้าแก้ไขแฟ้มข้อมูล"""
    return render(request, 'core/file_correct.html')
