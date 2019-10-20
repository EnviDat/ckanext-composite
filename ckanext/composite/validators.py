import json

import ckanext.scheming.helpers as sh
import ckan.lib.navl.dictization_functions as df

from ckanext.scheming.validation import scheming_validator
from ckantoolkit import _, get_validator
import logging

logger = logging.getLogger(__name__)

StopOnError = df.StopOnError
missing = df.missing

not_empty = get_validator('not_empty')


def composite_not_empty_subfield(key, subfield_label, value, errors):
    ''' Function equivalent to ckan.lib.navl.validators.not_empty
         but for subfields (custom message including subfield)
    '''
    if not value or value is missing:
        errors[key].append(_('Missing value at required subfield ' + subfield_label))
        raise StopOnError

def composite_all_empty(field, item):

    all_empty = True
    for schema_subfield in field['subfields']:
            subfield_value = item.get(schema_subfield.get('field_name', ''), "")
            if subfield_value and not subfield_value is missing:
                all_empty = False
    return all_empty

@scheming_validator
def composite_group2json(field, schema):

    def validator(key, data, errors, context):
        value = ""
        for name,text in data.iteritems():
            if name == key:
                if text:
                    value = text

        # Parse from extras into a dictionary and save it as a json dump
        if not value:
            found = {}
            prefix = key[-1] + '-'
            extras = data.get(key[:-1] + ('__extras',), {})

            extras_to_delete = []
            for name, text in extras.iteritems():
                if not name.startswith(prefix):
                    continue
                #if not text:
                #    continue
                subfield = name.split('-', 1)[1]
                found[subfield] = text
                extras_to_delete += [name]
            if not found:
                data[key] = ""
            else:
                item_is_empty = composite_all_empty(field, found) 
                item_is_empty_and_optional = item_is_empty and not sh.scheming_field_required(field)
                logger.debug('composite_group2json: item_is_empty_and_optional ' + str(key) + ':' + str(item_is_empty_and_optional))
                # Check if there is any mandatory subfield required
                for schema_subfield in field['subfields']:
                    if schema_subfield.get('required', False) and not item_is_empty_and_optional:
                        subfield_label = schema_subfield.get('label', schema_subfield.get('field_name', ''))
                        subfield_value = found.get(schema_subfield.get('field_name', ''), "")
                        composite_not_empty_subfield(key, subfield_label, subfield_value, errors)
                if item_is_empty:
                    found = {}
                data[key] = json.dumps(found, ensure_ascii=False)
                logger.debug('composite_group2json: key = ' + str(key))

                # delete the extras to avoid duplicate fields
                for extra in extras_to_delete:
                    del extras[extra]

        # Check if the field is required
        if sh.scheming_field_required(field):
            not_empty(key, data, errors, context)
    return validator

@scheming_validator
def composite_repeating_group2json(field, schema):

    def validator(key, data, errors, context):

        value = ""

        for name,text in data.iteritems():
            if name == key:
                if text:
                    value = text

        # parse from extra into a list of dictionaries and save it as a json dump
        if not value:
            found = {}
            prefix = key[-1] + '-'
            extras = data.get(key[:-1] + ('__extras',), {})

            extras_to_delete = []
            for name, text in extras.iteritems():
                if not name.startswith(prefix):
                    continue

                #if not text:
                #    continue

                index = int(name.split('-', 2)[1])
                subfield = name.split('-', 2)[2]
                extras_to_delete += [name]

                if not found.has_key(index):
                      found[index] = {}
                found[index][subfield] = text
            found_list = [element[1] for element in sorted(found.items())]

            if not found_list:
                data[key] = ""
            else:
                # check if there are required subfields missing for every item
                for index in found:
                    item = found[index]
                    item_is_empty_and_optional = composite_all_empty(field, item) and not sh.scheming_field_required(field)
                    logger.debug('composite_repeating_group2json: item_is_empty_and_optional ' + str(key) + ':'  + str(index) + ':' + str(item_is_empty_and_optional))
                    for schema_subfield in field['subfields']:
                        if schema_subfield.get('required', False) and not item_is_empty_and_optional:
                            if type(schema_subfield.get('label', '')) is dict:
                                subfield_label = schema_subfield.get('field_name', '') + " " + str(index)
                            else:
                                subfield_label = schema_subfield.get('label', schema_subfield.get('field_name', '')) + " " + str(index)

                            subfield_value = item.get(schema_subfield.get('field_name', ''), "")
                            composite_not_empty_subfield(key, subfield_label, subfield_value, errors)
                            
                # remove empty elements from list
                clean_list = []
                for element in found_list:
                    if not composite_all_empty(field, element):
                        clean_list += [element]
                # dump the list to a string
                data[key] = json.dumps(clean_list, ensure_ascii=False)

                # delete the extras to avoid duplicate fields
                for extra in extras_to_delete:
                    del extras[extra]

        # check if the field is required
        if sh.scheming_field_required(field):
            not_empty(key, data, errors, context)

    return validator

# this method doesn't work so it shouldn't be used
# def composite_group2json_output(value):
#    """
#    Return stored json representation as a dictionary, if
#    value is already a dictionary just pass it through.
#    """
#    if isinstance(value, dict):
#        return value
#    if value is None:
#        return {}
#    try:
#        return json.loads(value)
#    except ValueError:
#        logger.warn ("ValeError: " + str(value))
#    return {}
