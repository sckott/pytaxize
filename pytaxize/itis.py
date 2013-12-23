import sys
import requests
from lxml import etree

def itis_ping():
    '''
    Ping the ITIS API

    Usage:
    >>> import pytaxize
    >>> pytaxize.itis_ping()
    u'<ns:getDescriptionResponse xmlns:ns="http://itis_service.itis.usgs.gov"><ns:return xmlns:ax21="http://data.itis_service.itis.usgs.gov/xsd" xmlns:ax26="http://itis_service.itis.usgs.gov/xsd" xmlns:ax23="http://metadata.itis_service.itis.usgs.gov/xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="ax26:SvcDescription"><ax26:description>This is the ITIS Web Service, providing access to the data behind www.itis.gov. The database contains 641,468 scientific names (486,232 of them valid/accepted) and 118,145 common names.</ax26:description></ns:return></ns:getDescriptionResponse>'
    '''
    r = requests.get('http://www.itis.gov/ITISWebService/services/ITISService/getDescription')
    r.raise_for_status()
    return r.text

if __name__ == "__main__":
    import doctest
    doctest.testmod()