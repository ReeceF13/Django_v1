from celery.utils.sysinfo import df
from django.shortcuts import render

from apps.db.stores.store_query import fetch_store_data
##FORMS
from apps.pages.forms import *
##TESTING
from apps.db.tests.tests_ import fetch_test_data
from apps.pages.frontend_forms.forms import *
#CLASS IMPORTS

from apps.db.connections.connection_string import conn_str
from apps.db.dict_fetch.fetch_data import dictfetchall
import pyodbc
import pandas as pd
from datetime import datetime


conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

def test(request):
    store_one = fetch_store_data()
    store_ = store_one.store_data()
    context = {'html_table': store_}

    return render(request, 'pages/pages/testing/test_table.html', context)


from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
@csrf_exempt
def handle_click(request):
    if request.method == 'POST':
        # Get data from AJAX request

        data = json.loads(request.body)
        cell_value = data.get('value')
        # print(cell_value)
        params = cell_value
        try:
            cursor.execute("SELECT s.store_id, s.store_name, r.region_name, "
                           "rc.first_name + ' ' + rc.last_name as regional_coach_name, "
                           "ac.first_name + ' ' + ac.last_name as area_coach_name, "
                           "bp.first_name + ' ' + bp.last_name as business_partner_name "
                           "FROM Stores s "
                           "LEFT JOIN Regions r ON s.region_id = r.id "
                           "LEFT JOIN RegionalCoachAssignments rca ON s.id = rca.store_id "
                           "LEFT JOIN RegionalCoaches rc ON rca.regional_coach_id = rc.id "
                           "LEFT JOIN AreaCoachAssignments aca ON rc.id = aca.regional_coach_id "
                           "LEFT JOIN AreaCoaches ac ON aca.area_coach_id = ac.id "
                           "LEFT JOIN BusinessPartnerAssignments bpa ON ac.id = bpa.area_coach_id "
                           "LEFT JOIN BusinessPartners bp ON bpa.business_partner_id = bp.id WHERE store_name=?", params)
            rs1 = dictfetchall(cursor)
            df = pd.DataFrame(rs1)
            print(df)

        except:
            df = "No Data Found"
            return df

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
