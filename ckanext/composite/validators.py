import json

from ckanext.scheming.validation import scheming_validator
from ckantoolkit import _
import logging

logger = logging.getLogger(__name__)

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
        logger.warn ("ValeError: " + str(value))
        return {}

@scheming_validator
def composite_repeating_group2json(field, schema):

    def validator(key, data, errors, context):

        value = ""

        for name,text in data.iteritems():
            if name[-1] == key[-1]:
               if text:
                   logger.debug('*' + str(name) + ': ' + str(text))
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
               logger.debug('*(extras) ' + str(name) + ': ' + str(text))


               index = int(name.split('-', 2)[1])
               subfield = name.split('-', 2)[2]

               if not found.has_key(index):
                   found[index] = {}
               found[index][subfield] = text
           found_list = [element[1] for element in sorted(found.items())]

           data[key] = json.dumps(found_list, ensure_ascii=False)

    return validator

