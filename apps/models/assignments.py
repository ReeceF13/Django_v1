from django.db import models
from django.core.exceptions import ValidationError
from .base import BaseModel
from .core import Store, RegionalCoach, AreaCoach, BusinessPartner


class RegionalCoachAssignment(BaseModel):
    """
    Historical tracking of regional coach to store assignments
    """
    regional_coach = models.ForeignKey(
        RegionalCoach,
        on_delete=models.CASCADE,
        related_name='store_assignments'
    )
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name='regional_coach_assignments'
    )
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True, help_text="Leave blank for current assignment")

    class Meta:
        db_table = 'RegionalCoachAssignments'
        unique_together = ['regional_coach', 'store', 'start_date']
        indexes = [
            models.Index(fields=['regional_coach', 'end_date']),
            models.Index(fields=['store', 'end_date']),
            models.Index(fields=['start_date', 'end_date']),
        ]

    def __str__(self):
        status = "Current" if self.end_date is None else f"Ended {self.end_date}"
        return f"{self.regional_coach} -> {self.store} ({status})"

    def clean(self):
        """Validate date ranges and prevent overlapping current assignments"""
        super().clean()

        if self.end_date and self.end_date < self.start_date:
            raise ValidationError("End date cannot be before start date")

        # Check for overlapping current assignments for the same store
        if self.end_date is None:  # This is a current assignment
            existing_current = RegionalCoachAssignment.objects.filter(
                store=self.store,
                end_date__isnull=True
            ).exclude(pk=self.pk)

            if existing_current.exists():
                raise ValidationError(f"Store {self.store.store_id} already has a current regional coach assignment")

    @property
    def is_current(self):
        return self.end_date is None

    @property
    def duration_days(self):
        """Calculate duration of assignment in days"""
        from django.utils import timezone
        end = self.end_date or timezone.now().date()
        return (end - self.start_date).days


class AreaCoachAssignment(BaseModel):
    """
    Historical tracking of area coach to regional coach assignments
    """
    area_coach = models.ForeignKey(
        AreaCoach,
        on_delete=models.CASCADE,
        related_name='regional_coach_assignments'
    )
    regional_coach = models.ForeignKey(
        RegionalCoach,
        on_delete=models.CASCADE,
        related_name='area_coach_assignments'
    )
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'AreaCoachAssignments'
        unique_together = ['area_coach', 'regional_coach', 'start_date']
        indexes = [
            models.Index(fields=['area_coach', 'end_date']),
            models.Index(fields=['regional_coach', 'end_date']),
        ]

    def __str__(self):
        status = "Current" if self.end_date is None else f"Ended {self.end_date}"
        return f"{self.area_coach} -> {self.regional_coach} ({status})"

    def clean(self):
        """Validate date ranges"""
        super().clean()
        if self.end_date and self.end_date < self.start_date:
            raise ValidationError("End date cannot be before start date")

    @property
    def is_current(self):
        return self.end_date is None


class BusinessPartnerAssignment(BaseModel):
    """
    Historical tracking of business partner to area coach assignments
    """
    business_partner = models.ForeignKey(
        BusinessPartner,
        on_delete=models.CASCADE,
        related_name='area_coach_assignments'
    )
    area_coach = models.ForeignKey(
        AreaCoach,
        on_delete=models.CASCADE,
        related_name='business_partner_assignments'
    )
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'BusinessPartnerAssignments'
        unique_together = ['business_partner', 'area_coach', 'start_date']
        indexes = [
            models.Index(fields=['business_partner', 'end_date']),
            models.Index(fields=['area_coach', 'end_date']),
        ]

    def __str__(self):
        status = "Current" if self.end_date is None else f"Ended {self.end_date}"
        return f"{self.business_partner} -> {self.area_coach} ({status})"

    def clean(self):
        """Validate date ranges"""
        super().clean()
        if self.end_date and self.end_date < self.start_date:
            raise ValidationError("End date cannot be before start date")

    @property
    def is_current(self):
        return self.end_date is None