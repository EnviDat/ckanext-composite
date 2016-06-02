import json
import re

def _json2dict_or_empty(value):
    try:
        json_dict = json.loads(value)
    except:
        json_dict = {}
    return (json_dict)

def composite_get_as_dict(value):
    if isinstance(value, dict):
        return value
    else:
        return(_json2dict_or_empty(value))

def composite_get_value_dict(field_name, data):
    '''
    Template helper function.
    Get data from composite_text-field from either field_name (if the
    field comes from the database) or construct from several subfields -
    entries in case data wasn't saved yet, i.e. a validation error occurred.
    '''

    def build_value_dict():
        fields = [re.match(field_name + "-.+", key) for key in data.keys()]
        fields = sorted([r.string for r in fields if r])
        value_dict = {}

        for field in fields:
            if data[field]:
                subfield = field.split("-",1)[1]
                value_dict[subfield] = data[field]
        return value_dict
 
    group_value = {}

    form_value = build_value_dict()
    
    if form_value:
       group_value = form_value
    else:
       db_value = data.get(field_name)
       if db_value:
           if isinstance(db_value, dict):
               group_value = db_value
           else:
               group_value = _json2dict_or_empty(db_value)

    return group_value
