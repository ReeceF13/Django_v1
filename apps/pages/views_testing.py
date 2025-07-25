from django.shortcuts import render

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

    if request.method == 'GET':
        form2 = E_Dropdown(request.GET)
        if form2.is_valid():
            selected_value = form2.cleaned_data['my_choice_field']
            # Process the selected value
    else:
        form2 = E_Dropdown()
    return render(request, 'pages/pages/testing/test_table.html', {'form2': form2})


    # if request.user.is_authenticated:
    #     # User is logged in
    #     current_user = request.user
    #     print(f"Logged in user: {current_user.username}")
    #     print(f"User ID: {current_user.id}")
    #     print(f"User email: {current_user.email}")
    #     # You can access other attributes of the User model as needed
    # else:
    #     # User is not logged in (anonymous user)
    #     print("No user is currently logged in.")

    # region_one = fetch_region_data()
    # region_ = region_one.region_data()
    # context = {'html_table': region_}
    # now_ = datetime.now().replace(microsecond=0)
    # if 'word' in request.GET:
    #     word_input = request.GET['word']
    #     params = word_input
    #     cursor.execute("SELECT * FROM Regions WHERE region_name LIKE '%' + ? + '%'", params)
    #     rs1 = dictfetchall(cursor)
    #     df = pd.DataFrame(rs1)
    #     dfsd = df.to_records(index=False)
    #     for i in dfsd:
    #         i0 = (str(i[0]))
    #         i1 = (str(i[1]))
    #         i2 = (str(i[2]))
    #         i3 = (str(i[3]))
    #         i4 = (str(i[4]))
    #         i5 = (str(i[5]))
    #         # print(i0)
    #     initial_data = {'ID': i0, 'Region_Name': i1, 'Created_At': i2, 'Updated_At': i3, 'Created_By': i4,
    #                     'Updated_By': i5}
    #     form = RegionUpdate(initial=initial_data)
    #     if 'filter' in request.POST:
    #         id_ = request.POST.get('ID')
    #         rn_ = request.POST.get('Region_Name')
    #         updated_at = now_
    #         updated_by = request.POST.get('Updated_By')
    #         dfsp = pd.DataFrame(
    #             columns=['id', 'region_name', 'updated_at', 'updated_by_id'])
    #         dfsp.loc[0] = id_, rn_, updated_at, updated_by
    #         print(rn_)
            # for index, row in dfsp.iterrows():
            #     cursor.execute("UPDATE Regions SET region_name = ?, updated_at = ?, updated_by_id = ? WHERE id = ?",
            #                    (row['region_name'], row['updated_at'], row['updated_by_id'], row['id']))
            #
            #     cursor.commit()
            #     region_one = fetch_region_data_updated()
            #     region_ = region_one.region_data_updated()
            #     context1 = {'html_table': region_}
            #     return render(request, "pages/pages/region_table.html", context1)

    #     return render(request, "pages/pages/edit_records/edit_regions.html",
    #                   {'form': form, 'initial_data': initial_data})
    #
    # return render(request, "pages/pages/region_table.html", context)