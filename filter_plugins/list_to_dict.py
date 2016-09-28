#! /usr/bin/env python

from ansible import errors


def list_to_dict(data, key):
    '''Key must be passed in when calling from a Jinja template
    '''

    new_obj = {}

    for item in data:
        try:
            key_elem = item.get(key)
        except Exception, e:
            raise errors.AnsibleFilterError(str(e))
        if key_elem:
            if new_obj.get(key_elem):
                new_obj[key_elem].append(item)
            else:
                new_obj[key_elem] = []
                new_obj[key_elem].append(item)

    return new_obj

class FilterModule(object):
    '''Convert a list of dictionaries to a dictionary provided a
       key that exists in all dicts.  If it does not, that dict is omitted
    '''
    def filters(self):
        return {
            'list_to_dict': list_to_dict
        }
