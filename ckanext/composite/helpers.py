import json
import re

import logging


logger = logging.getLogger(__name__)

def _json2dict_or_empty(value, field_name = ""):
    try:
        json_dict = json.loads(value)
    except Exception as e:
        logger.warn("Field " + field_name + "('" + str(value) + "') could not be parsed: " + str(e))
        json_dict = {}
    return (json_dict)

def composite_get_as_dict(value):
    '''
    Template helper funciton.
    Returns the value as a dictionary. If if is already
    a dictionary, the original value is returned. If it is
    a json dump, it will be parsed into a dictionary. Otherwise
    an empty dictionary is returned.
    '''
    if isinstance(value, dict):
        return value
    else:
        return(_json2dict_or_empty(value))

def composite_get_label_dict(field_list):
    '''
    Converts a list of dictionaries containing the keys
    "field_name" and "label" into asingle dictionary
    with "field_name" value as key and "label" as value.
    If label is not defined, the field name is used as
    label. 
    '''

    label_dict = {}
    for field in field_list:
        name = field.get('field_name', '')
        label_dict[name] = field.get('label', name)
    return label_dict

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
            if data[field] is not None:
                subfield = field.split("-",1)[1]
                value_dict[subfield] = data[field]
        return value_dict

    value_dict = {}

    form_value = build_value_dict()

    if form_value:
       value_dict = form_value
    else:
       db_value = data.get(field_name)
       if db_value:
           if isinstance(db_value, dict):
               value_dict = db_value
           else:
               value_dict = _json2dict_or_empty(db_value)

    return value_dict
