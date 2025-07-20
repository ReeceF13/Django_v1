
from .base import BaseModel
from django.db import models
from django.core.exceptions import ValidationError
import re

class Region(BaseModel):
    """
    Regions for organizing stores geographically
    """
    region_name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'Regions'
        ordering = ['region_name']

    def __str__(self):
        return self.region_name

    @property
    def store_count(self):
        """Return the number of stores in this region"""
        return self.stores.filter(store_id=True).count()

    @property
    def total_employees(self):
        """Return total employees across all stores in region"""
        return sum(store.employee_count for store in self.stores.all())
def validate_store_id(value):
    """Validate store ID format: 3 letters + 1-5 numbers"""
    pattern = r'^[A-Z]{3}[0-9]{1,5}$'
    if not re.match(pattern, value):
        raise ValidationError(
            'Store ID must be 3 uppercase letters followed by 1-5 numbers (e.g., ADP1, ADP98765)'
        )


class Store(BaseModel):
    """
    Individual stores and head office
    """
    store_id = models.CharField(
        max_length=10,
        unique=True,
        validators=[validate_store_id],
        help_text="Format: 3 letters + 1-5 numbers (e.g., ADP1)"
    )
    store_name = models.CharField(max_length=30)
    region = models.ForeignKey(
        Region,
        on_delete=models.PROTECT,
        related_name='stores',
        null=True,
        blank=True
    )
    is_head_office = models.BooleanField(default=False)

    class Meta:
        db_table = 'Stores'
        ordering = ['store_id']
        indexes = [
            models.Index(fields=['store_id']),
            models.Index(fields=['region', 'created_at']),
        ]

    def __str__(self):
        return f"{self.store_id} - {self.store_name}"

    def clean(self):
        """Custom validation"""
        super().clean()
        self.store_id = self.store_id.upper()

    @property
    def employee_count(self):
        """Return active employee count for this store"""
        return self.employees.filter(is_active=True).count()

    @property
    def current_regional_coach(self):
        """Get current regional coach assigned to this store"""
        current_assignment = self.regional_coach_assignments.filter(end_date__isnull=True).first()
        return current_assignment.regional_coach if current_assignment else None

    def get_hierarchy_chain(self):
        """Get complete coaching hierarchy for this store"""
        rc = self.current_regional_coach
        if not rc:
            return None

        ac_assignment = rc.area_coach_assignments.filter(end_date__isnull=True).first()
        ac = ac_assignment.area_coach if ac_assignment else None

        if ac:
            bp_assignment = ac.business_partner_assignments.filter(end_date__isnull=True).first()
            bp = bp_assignment.business_partner if bp_assignment else None
        else:
            bp = None

        return {
            'regional_coach': rc,
            'area_coach': ac,
            'business_partner': bp
        }
class RegionalCoach(BaseModel):
    """
    Regional coaches who oversee multiple stores
    """
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    cell_phone = models.CharField(max_length=15, blank=True, null=True)
    email_address = models.EmailField(blank=True, null=True)
    employee_code = models.CharField(max_length=20, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'RegionalCoaches'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.employee_code})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def current_stores(self):
        """Get all stores currently assigned to this regional coach"""
        current_assignments = self.store_assignments.filter(end_date__isnull=True)
        return [assignment.store for assignment in current_assignments]

    @property
    def current_area_coach(self):
        """Get current area coach assigned to this regional coach"""
        current_assignment = self.area_coach_assignments.filter(end_date__isnull=True).first()
        return current_assignment.area_coach if current_assignment else None

class AreaCoach(BaseModel):
    """
    Area coaches who oversee regional coaches
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    cell_phone = models.CharField(max_length=15, blank=True, null=True)
    email_address = models.EmailField(blank=True, null=True)
    employee_code = models.CharField(max_length=20, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'AreaCoaches'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.employee_code})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def current_regional_coaches(self):
        """Get all regional coaches currently assigned to this area coach"""
        current_assignments = self.regional_coach_assignments.filter(end_date__isnull=True)
        return [assignment.regional_coach for assignment in current_assignments]

    @property
    def current_business_partner(self):
        """Get current business partner assigned to this area coach"""
        current_assignment = self.business_partner_assignments.filter(end_date__isnull=True).first()
        return current_assignment.business_partner if current_assignment else None

class BusinessPartner(BaseModel):
    """
    Business partners who oversee area coaches
    """
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    cell_phone = models.CharField(max_length=15, blank=True, null=True)
    email_address = models.EmailField(blank=True, null=True)
    employee_code = models.CharField(max_length=20, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'BusinessPartners'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.employee_code})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def current_area_coaches(self):
        """Get all area coaches currently assigned to this business partner"""
        current_assignments = self.area_coach_assignments.filter(end_date__isnull=True)
        return [assignment.area_coach for assignment in current_assignments]

class Employee(BaseModel):
    """
    All employees including those in coaching roles
    """
    EMPLOYEE_TYPES = [
        ('EMPLOYEE', 'Employee'),
        ('REGIONAL_COACH', 'Regional Coach'),
        ('AREA_COACH', 'Area Coach'),
        ('BUSINESS_PARTNER', 'Business Partner'),
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    cell_phone = models.CharField(max_length=15, blank=True, null=True)
    email_address = models.EmailField(blank=True, null=True)
    employee_code = models.CharField(max_length=20, unique=True)
    store = models.ForeignKey(Store, on_delete=models.PROTECT, related_name='employees')
    employee_type = models.CharField(max_length=20, choices=EMPLOYEE_TYPES, default='EMPLOYEE')
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'Employees'
        ordering = ['last_name', 'first_name']
        indexes = [
            models.Index(fields=['store', 'employee_type']),
            models.Index(fields=['employee_code']),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.employee_code}) - {self.store.store_id}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"