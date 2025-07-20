def create_dict():
    headings = ('Region', 'Created At.', 'Updated At', 'Created By', 'Updated By')
    data = ('North', 'South', 'East', 'West', 'North East', 'North West', 'South East', 'South West')
    dict_ = {}
    dict_ = dict(zip(headings, data))
    print(dict_)
create_dict()