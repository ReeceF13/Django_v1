from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

class BaseModel(models.Model):
    """
    Abstract base model with common audit fields
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='created_%(class)s_set'
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='updated_%(class)s_set'
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # Handle user tracking for updates
        if not self.pk and hasattr(self, '_current_user'):
            self.created_by = self._current_user
            self.updated_by = self._current_user
        elif hasattr(self, '_current_user'):
            self.updated_by = self._current_user
        super().save(*args, **kwargs)

    def set_current_user(self, user):
        """Set the current user for audit tracking"""
        self._current_user = user