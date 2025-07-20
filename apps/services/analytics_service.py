import pandas as pd
from django.db import connection
from apps.services.assignment_service import AssignmentService


class AnalyticsService:
    @staticmethod
    def get_hierarchy_dataframe():
        """
        Get current hierarchy as pandas DataFrame for analytics
        """
        hierarchy_data = AssignmentService.get_current_hierarchy()
        return pd.DataFrame(hierarchy_data)

    @staticmethod
    def get_assignment_history_df(start_date=None, end_date=None):
        """
        Get assignment history for trend analysis
        """
        query = """
                SELECT s.store_id, \
                       s.store_name, \
                       rc.employee_code                                                    as rc_code, \
                       rc.first_name + ' ' + rc.last_name                                  as regional_coach, \
                       rca.start_date, \
                       rca.end_date, \
                       CASE WHEN rca.end_date IS NULL THEN 'Current' ELSE 'Historical' END as status
                FROM RegionalCoachAssignments rca
                         JOIN Stores s ON rca.store_id = s.id
                         JOIN RegionalCoaches rc ON rca.regional_coach_id = rc.id
                WHERE 1 = 1 \
                """

        params = []
        if start_date:
            query += " AND rca.start_date >= %s"
            params.append(start_date)
        if end_date:
            query += " AND (rca.end_date IS NULL OR rca.end_date <= %s)"
            params.append(end_date)

        return pd.read_sql_query(query, connection, params=params)