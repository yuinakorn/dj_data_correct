from django.db import models
from django.contrib.auth.models import User

class DataCategory(models.Model):
    """หมวดหมู่ข้อมูลที่ตรวจสอบ"""
    name = models.CharField(max_length=100, verbose_name="ชื่อหมวดหมู่")
    description = models.TextField(blank=True, verbose_name="คำอธิบาย")
    is_active = models.BooleanField(default=True, verbose_name="สถานะใช้งาน")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "หมวดหมู่ข้อมูล"
        verbose_name_plural = "หมวดหมู่ข้อมูล"
    
    def __str__(self):
        return self.name

class Province(models.Model):
    """จังหวัด"""
    code = models.CharField(max_length=10, unique=True, verbose_name="รหัสจังหวัด")
    name = models.CharField(max_length=100, verbose_name="ชื่อจังหวัด")
    region = models.CharField(max_length=50, verbose_name="ภูมิภาค")
    
    class Meta:
        verbose_name = "จังหวัด"
        verbose_name_plural = "จังหวัด"
    
    def __str__(self):
        return self.name

class District(models.Model):
    """อำเภอ"""
    province = models.ForeignKey(Province, on_delete=models.CASCADE, verbose_name="จังหวัด")
    code = models.CharField(max_length=10, verbose_name="รหัสอำเภอ")
    name = models.CharField(max_length=100, verbose_name="ชื่ออำเภอ")
    
    class Meta:
        verbose_name = "อำเภอ"
        verbose_name_plural = "อำเภอ"
        unique_together = ['province', 'code']
    
    def __str__(self):
        return f"{self.name}, {self.province.name}"

class HealthFacility(models.Model):
    """หน่วยบริการสุขภาพ"""
    FACILITY_TYPES = [
        ('hospital', 'โรงพยาบาล'),
        ('health_center', 'ศูนย์สุขภาพชุมชน'),
        ('clinic', 'คลินิก'),
        ('other', 'อื่นๆ'),
    ]
    
    hcode = models.CharField(max_length=10, unique=True, verbose_name="รหัสหน่วยบริการ")
    name = models.CharField(max_length=200, verbose_name="ชื่อหน่วยบริการ")
    district = models.ForeignKey(District, on_delete=models.CASCADE, verbose_name="อำเภอ")
    facility_type = models.CharField(max_length=20, choices=FACILITY_TYPES, verbose_name="ประเภทหน่วยบริการ")
    is_active = models.BooleanField(default=True, verbose_name="สถานะใช้งาน")
    
    class Meta:
        verbose_name = "หน่วยบริการสุขภาพ"
        verbose_name_plural = "หน่วยบริการสุขภาพ"
    
    def __str__(self):
        return self.name

class DataAnomaly(models.Model):
    """ข้อมูลความผิดปกติ"""
    SEVERITY_LEVELS = [
        ('low', 'ต่ำ'),
        ('medium', 'ปานกลาง'),
        ('high', 'สูง'),
        ('critical', 'วิกฤติ'),
    ]
    
    STATUS_CHOICES = [
        ('new', 'ใหม่'),
        ('investigating', 'กำลังตรวจสอบ'),
        ('resolved', 'แก้ไขแล้ว'),
        ('ignored', 'ยกเลิก'),
    ]
    
    category = models.ForeignKey(DataCategory, on_delete=models.CASCADE, verbose_name="หมวดหมู่")
    facility = models.ForeignKey(HealthFacility, on_delete=models.CASCADE, verbose_name="หน่วยบริการ")
    patient_id = models.CharField(max_length=20, verbose_name="รหัสผู้ป่วย", blank=True)
    
    # ข้อมูลความผิดปกติ
    anomaly_type = models.CharField(max_length=100, verbose_name="ประเภทความผิดปกติ")
    description = models.TextField(verbose_name="รายละเอียด")
    data_field = models.CharField(max_length=50, verbose_name="ฟิลด์ข้อมูล")
    expected_value = models.CharField(max_length=100, verbose_name="ค่าที่คาดหวัง", blank=True)
    actual_value = models.CharField(max_length=100, verbose_name="ค่าที่ได้จริง")
    
    # การจัดการ
    severity = models.CharField(max_length=10, choices=SEVERITY_LEVELS, default='medium', verbose_name="ระดับความรุนแรง")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='new', verbose_name="สถานะ")
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="มอบหมายให้")
    
    # วันที่
    detected_at = models.DateTimeField(auto_now_add=True, verbose_name="วันที่ตรวจพบ")
    resolved_at = models.DateTimeField(null=True, blank=True, verbose_name="วันที่แก้ไข")
    
    # หมายเหตุ
    notes = models.TextField(blank=True, verbose_name="หมายเหตุ")
    
    class Meta:
        verbose_name = "ข้อมูลความผิดปกติ"
        verbose_name_plural = "ข้อมูลความผิดปกติ"
        ordering = ['-detected_at']
    
    def __str__(self):
        return f"{self.anomaly_type} - {self.facility.name}"
