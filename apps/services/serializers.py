from rest_framework import serializers
from django.contrib.auth.models import User
from apps.models.core import (
    Region, Store, RegionalCoach, AreaCoach, BusinessPartner, Employee)
from apps.models.assignments import AreaCoachAssignment, BusinessPartnerAssignment, RegionalCoachAssignment

class UserSerializer(serializers.ModelSerializer):
    """
    Basic user serializer for audit fields
    """
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'full_name', 'email']
        read_only_fields = ['id']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()


class RegionSerializer(serializers.ModelSerializer):
    """
    Region serializer with store count
    """
    store_count = serializers.ReadOnlyField()
    total_employees = serializers.ReadOnlyField()
    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)

    class Meta:
        model = Region
        fields = [
            'id', 'region_name', 'store_count', 'total_employees',
            'created_at', 'updated_at', 'created_by', 'updated_by'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by', 'updated_by']


class StoreListSerializer(serializers.ModelSerializer):
    """
    Simplified store serializer for lists
    """
    region_name = serializers.CharField(source='region.region_name', read_only=True)
    employee_count = serializers.ReadOnlyField()

    class Meta:
        model = Store
        fields = [
            'id', 'store_id', 'store_name', 'region', 'region_name',
            'is_head_office', 'employee_count'
        ]


class StoreDetailSerializer(serializers.ModelSerializer):
    """
    Detailed store serializer with hierarchy information
    """
    region = RegionSerializer(read_only=True)
    region_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    employee_count = serializers.ReadOnlyField()
    current_regional_coach = serializers.SerializerMethodField()
    hierarchy_chain = serializers.SerializerMethodField()
    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)

    class Meta:
        model = Store
        fields = [
            'id', 'store_id', 'store_name', 'region', 'region_id', 'is_head_office',
            'employee_count', 'current_regional_coach', 'hierarchy_chain',
            'created_at', 'updated_at', 'created_by', 'updated_by'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by', 'updated_by']

    def get_current_regional_coach(self, obj):
        rc = obj.current_regional_coach
        return RegionalCoachListSerializer(rc).data if rc else None

    def get_hierarchy_chain(self, obj):
        chain = obj.get_hierarchy_chain()
        if not chain:
            return None

        return {
            'regional_coach': RegionalCoachListSerializer(chain['regional_coach']).data if chain[
                'regional_coach'] else None,
            'area_coach': AreaCoachListSerializer(chain['area_coach']).data if chain['area_coach'] else None,
            'business_partner': BusinessPartnerListSerializer(chain['business_partner']).data if chain[
                'business_partner'] else None,
        }


class RegionalCoachListSerializer(serializers.ModelSerializer):
    """
    Simplified regional coach serializer for lists
    """
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = RegionalCoach
        fields = [
            'id', 'first_name', 'last_name', 'full_name',
            'employee_code', 'email_address', 'is_active'
        ]


class RegionalCoachDetailSerializer(serializers.ModelSerializer):
    """
    Detailed regional coach serializer
    """
    full_name = serializers.ReadOnlyField()
    current_stores = serializers.SerializerMethodField()
    current_area_coach = serializers.SerializerMethodField()
    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)

    class Meta:
        model = RegionalCoach
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 'cell_phone',
            'email_address', 'employee_code', 'is_active', 'current_stores',
            'current_area_coach', 'created_at', 'updated_at', 'created_by', 'updated_by'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by', 'updated_by']

    def get_current_stores(self, obj):
        stores = obj.current_stores
        return StoreListSerializer(stores, many=True).data

    def get_current_area_coach(self, obj):
        ac = obj.current_area_coach
        return AreaCoachListSerializer(ac).data if ac else None


class AreaCoachListSerializer(serializers.ModelSerializer):
    """
    Simplified area coach serializer for lists
    """
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = AreaCoach
        fields = [
            'id', 'first_name', 'last_name', 'full_name',
            'employee_code', 'email_address', 'is_active'
        ]


class AreaCoachDetailSerializer(serializers.ModelSerializer):
    """
    Detailed area coach serializer
    """
    full_name = serializers.ReadOnlyField()
    current_regional_coaches = serializers.SerializerMethodField()
    current_business_partner = serializers.SerializerMethodField()
    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)

    class Meta:
        model = AreaCoach
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 'cell_phone',
            'email_address', 'employee_code', 'is_active', 'current_regional_coaches',
            'current_business_partner', 'created_at', 'updated_at', 'created_by', 'updated_by'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by', 'updated_by']

    def get_current_regional_coaches(self, obj):
        coaches = obj.current_regional_coaches
        return RegionalCoachListSerializer(coaches, many=True).data

    def get_current_business_partner(self, obj):
        bp = obj.current_business_partner
        return BusinessPartnerListSerializer(bp).data if bp else None


class BusinessPartnerListSerializer(serializers.ModelSerializer):
    """
    Simplified business partner serializer for lists
    """
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = BusinessPartner
        fields = [
            'id', 'first_name', 'last_name', 'full_name',
            'employee_code', 'email_address', 'is_active'
        ]


class BusinessPartnerDetailSerializer(serializers.ModelSerializer):
    """
    Detailed business partner serializer
    """
    full_name = serializers.ReadOnlyField()
    current_area_coaches = serializers.SerializerMethodField()
    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)

    class Meta:
        model = BusinessPartner
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 'cell_phone',
            'email_address', 'employee_code', 'is_active', 'current_area_coaches',
            'created_at', 'updated_at', 'created_by', 'updated_by'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by', 'updated_by']

    def get_current_area_coaches(self, obj):
        coaches = obj.current_area_coaches
        return AreaCoachListSerializer(coaches, many=True).data


class EmployeeSerializer(serializers.ModelSerializer):
    """
    Employee serializer
    """
    full_name = serializers.ReadOnlyField()
    store_info = StoreListSerializer(source='store', read_only=True)
    store_id = serializers.IntegerField(write_only=True)
    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)

    class Meta:
        model = Employee
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 'cell_phone',
            'email_address', 'employee_code', 'store', 'store_id', 'store_info',
            'employee_type', 'is_active', 'created_at', 'updated_at', 'created_by', 'updated_by'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by', 'updated_by']


# Assignment Serializers
class RegionalCoachAssignmentSerializer(serializers.ModelSerializer):
    """
    Regional coach assignment serializer
    """
    regional_coach_info = RegionalCoachListSerializer(source='regional_coach', read_only=True)
    store_info = StoreListSerializer(source='store', read_only=True)
    regional_coach_id = serializers.IntegerField(write_only=True)
    store_id = serializers.IntegerField(write_only=True)
    is_current = serializers.ReadOnlyField()
    duration_days = serializers.ReadOnlyField()
    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)

    class Meta:
        model = RegionalCoachAssignment
        fields = [
            'id', 'regional_coach', 'regional_coach_id', 'regional_coach_info',
            'store', 'store_id', 'store_info', 'start_date', 'end_date',
            'is_current', 'duration_days', 'created_at', 'updated_at', 'created_by', 'updated_by'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by', 'updated_by']


class AreaCoachAssignmentSerializer(serializers.ModelSerializer):
    """
    Area coach assignment serializer
    """
    area_coach_info = AreaCoachListSerializer(source='area_coach', read_only=True)
    regional_coach_info = RegionalCoachListSerializer(source='regional_coach', read_only=True)
    area_coach_id = serializers.IntegerField(write_only=True)
    regional_coach_id = serializers.IntegerField(write_only=True)
    is_current = serializers.ReadOnlyField()
    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)

    class Meta:
        model = AreaCoachAssignment
        fields = [
            'id', 'area_coach', 'area_coach_id', 'area_coach_info',
            'regional_coach', 'regional_coach_id', 'regional_coach_info',
            'start_date', 'end_date', 'is_current',
            'created_at', 'updated_at', 'created_by', 'updated_by'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by', 'updated_by']


class BusinessPartnerAssignmentSerializer(serializers.ModelSerializer):
    """
    Business partner assignment serializer
    """
    business_partner_info = BusinessPartnerListSerializer(source='business_partner', read_only=True)
    area_coach_info = AreaCoachListSerializer(source='area_coach', read_only=True)
    business_partner_id = serializers.IntegerField(write_only=True)
    area_coach_id = serializers.IntegerField(write_only=True)
    is_current = serializers.ReadOnlyField()
    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)

    class Meta:
        model = BusinessPartnerAssignment
        fields = [
            'id', 'business_partner', 'business_partner_id', 'business_partner_info',
            'area_coach', 'area_coach_id', 'area_coach_info',
            'start_date', 'end_date', 'is_current',
            'created_at', 'updated_at', 'created_by', 'updated_by'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by', 'updated_by']


# Analytics Serializers
class HierarchyAnalyticsSerializer(serializers.Serializer):
    """
    Serializer for current hierarchy analytics data
    """
    store_id = serializers.CharField()
    store_name = serializers.CharField()
    region_name = serializers.CharField(allow_null=True)
    regional_coach_name = serializers.CharField(allow_null=True)
    area_coach_name = serializers.CharField(allow_null=True)
    business_partner_name = serializers.CharField(allow_null=True)


class AssignmentHistorySerializer(serializers.Serializer):
    """
    Serializer for assignment history analytics
    """
    store_id = serializers.CharField()
    store_name = serializers.CharField()
    rc_code = serializers.CharField()
    regional_coach = serializers.CharField()
    start_date = serializers.DateField()
    end_date = serializers.DateField(allow_null=True)
    status = serializers.CharField()


# Bulk Operations Serializers
class BulkAssignmentSerializer(serializers.Serializer):
    """
    Serializer for bulk assignment operations
    """
    regional_coach_id = serializers.IntegerField()
    store_ids = serializers.ListField(
        child=serializers.IntegerField(),
        min_length=1
    )
    start_date = serializers.DateField()
    end_existing = serializers.BooleanField(default=True)


class AssignmentCreateSerializer(serializers.Serializer):
    """
    Simplified serializer for creating assignments through services
    """
    regional_coach_id = serializers.IntegerField()
    store_id = serializers.IntegerField()
    start_date = serializers.DateField()

    def validate(self, data):
        """Validate that the coach and store exist"""
        from apps.models.core import RegionalCoach, Store

        try:
            RegionalCoach.objects.get(id=data['regional_coach_id'], is_active=True)
        except RegionalCoach.DoesNotExist:
            raise serializers.ValidationError("Regional coach not found or inactive")

        try:
            Store.objects.get(id=data['store_id'])
        except Store.DoesNotExist:
            raise serializers.ValidationError("Store not found")

        return data