import json

from ckanext.scheming.validation import scheming_validator
from ckantoolkit import _

@scheming_validator
def composite_group2json(field, schema):
    print schema
    print field
    def validator(key, data, errors, context):
        print("VALIDATOR data: {}".format(data))
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
        data[key] = json.dumps(found)

    return validator
