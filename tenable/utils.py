def dict_merge(master, updates):
    '''
    Merge 2 dictionaries together  The updates dictionary will be merged into
    the master, adding/updating any values as needed.

    Args:
        master (dict): The master dictionary to be used as the base.
        updates (dict): The dictionary that will overload the values in the master.

    Returns:
        dict: The merged dictionary
    '''
    for key in updates:
        if key in master and isinstance(master[key], dict) and isinstance(updates[key], dict):
            master[key] = dict_merge(master[key], updates[key])
        else:
            master[key] = updates[key]
    return master


def policy_settings(item):
    '''
    Recursive function to attempt to pull out the various settings from scan
    policy settings in the editor format.
    '''
    resp = dict()
    if 'id' in item and ('default' in item
        or ('type' in item and item['type'] in [
            'file',
            'checkbox',
            'entry',
            'textarea',
            'medium-fixed-entry',
            'password'])):
        # if we find both an 'id' and a 'default' attribute, or if we find
        # a 'type' attribute matching one of the known attribute types, then
        # we will parse out the data and append it to the response dictionary
        if not 'default' in item:
            item['default'] = ""
        resp[item['id']] = item['default']

    for key in item.keys():
        # here we will attempt to recurse down both a list of sub-
        # documents and an explicitly defined sub-document within the
        # editor data-structure.
        if key == 'modes':
            continue
        if (isinstance(item[key], list)
            and len(item[key]) > 0
            and isinstance(item[key][0], dict)):
            for i in item[key]:
                resp = dict_merge(resp, policy_settings(i))
        if isinstance(item[key], dict):
            resp = dict_merge(resp, policy_settings(item[key]))

    # Return the key-value pair.
    return resp