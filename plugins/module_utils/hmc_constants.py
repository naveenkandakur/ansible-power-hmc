from __future__ import absolute_import, division, print_function
__metaclass__ = type


class HmcConstants():
    MTMS_pattern = r'^\d{4}-[A-Z\d]{3}\*[A-Z\d]{7}$'
    USER_AUTHORITY_ERR = "HSCL350B The user does not have the appropriate authority"
    PROFILE_PATTERN = r'^[a-zA-Z0-9][a-zA-Z0-9@#^/;:~,\.\-_=+\{\}]{0,30}$'
