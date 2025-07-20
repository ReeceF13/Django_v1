from django.db import transaction
from django.utils import timezone

from apps.models import assignments
from apps.models.core import Store, RegionalCoach
from apps.models.assignments import AreaCoachAssignment, BusinessPartnerAssignment, RegionalCoachAssignment


class AssignmentService:
    @staticmethod
    @transaction.atomic
    def assign_regional_coach_to_store(regional_coach, store, start_date, user):
        """
        Assign a regional coach to a store, ending any existing assignment
        """
        # End existing assignment
        existing = RegionalCoachAssignment.objects.filter(
            store=store,
            end_date__isnull=True
        ).first()

        if existing:
            existing.end_date = start_date - timezone.timedelta(days=1)
            existing.set_current_user(user)
            existing.save()

        # Create new assignment
        assignment = RegionalCoachAssignment.objects.create(
            regional_coach=regional_coach,
            store=store,
            start_date=start_date
        )
        assignment.set_current_user(user)
        assignment.save()

        return assignment

    @staticmethod
    def get_current_hierarchy():
        """
        Get current complete hierarchy for analytics
        """
        from django.db import connection

        query = """
                SELECT s.store_id, \
                       s.store_name, \
                       r.region_name, \
                       rc.first_name + ' ' + rc.last_name as regional_coach_name, \
                       ac.first_name + ' ' + ac.last_name as area_coach_name, \
                       bp.first_name + ' ' + bp.last_name as business_partner_name
                FROM Stores s
                         LEFT JOIN Regions r ON s.region_id = r.id
                         LEFT JOIN RegionalCoachAssignments rca ON s.id = rca.store_id AND rca.end_date IS NULL
                         LEFT JOIN RegionalCoaches rc ON rca.regional_coach_id = rc.id
                         LEFT JOIN AreaCoachAssignments aca ON rc.id = aca.regional_coach_id AND aca.end_date IS NULL
                         LEFT JOIN AreaCoaches ac ON aca.area_coach_id = ac.id
                         LEFT JOIN BusinessPartnerAssignments bpa ON ac.id = bpa.area_coach_id AND bpa.end_date IS NULL
                         LEFT JOIN BusinessPartners bp ON bpa.business_partner_id = bp.id \
                """

        with connection.cursor() as cursor:
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]