import json

from ckanext.scheming.validation import scheming_validator
from ckantoolkit import _

@scheming_validator
def composite_group2json(field, schema):

    def validator(key, data, errors, context):

        value = ""

	for name,text in data.iteritems():
            if name[-1] == key[-1]:
               if text:
                   value = text
                   
        if not value:

           found = {}
           prefix = key[-1] + '-'
           extras = data.get(key[:-1] + ('__extras',), {})

           for name, text in extras.iteritems():
               if not name.startswith(prefix):
                  continue
               if not text:
                  continue
               subfield = name.split('-', 1)[1]
               found[subfield] = text
           data[key] = json.dumps(found, ensure_ascii=False)

    return validator

def composite_group2json_output(value):
    """
    Return stored json representation as a dictionary, if
    value is already a dictionary just pass it through.
    """
    if isinstance(value, dict):
        return value
    if value is None:
        return {}
    try:
        return json.loads(value)
    except ValueError:
        print "composite_group2json_output: VALUE ERROR!" + str(value)
        return {}
