'''
Dictionary enveloping utility.
'''
from typing import Optional, List, Dict


def envelope(data: Dict,
             key: str,
             excludes: Optional[List[str]] = None
             ) -> Dict:
    '''
    Reformats the data dictionary to push any keys that aren't described in the
    excludes list into the filters sub-object.

    Args:
        data (dict):
            The data dictionary to modify
        key (str):
            The dictionary key to wrap the data within.
        excludes (list[str], optional):
            A list of keys to exclude from the enveloping process.

    Returns:
        dict:
            The modified data dictionary.
    '''
    resp = {}

    # for each excluded item, we will move it into the response dictionary
    # using the same key.
    if excludes:
        for item in excludes:
            if item in data:
                resp[item] = data.pop(item)

    # add the remaining attributes in the data dictionary to the response
    # object within the envelope key.
    resp[key] = data

    # Return the response object to the caller.
    return resp
