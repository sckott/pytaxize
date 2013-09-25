import sys
import requests

def tacks():
	print "some shit"

def joke():
    return (u'Wenn ist das Nunst\u00fcck git und Slotermeyer? Ja! ... '
            u'Beiherhund das Oder die Flipperwaldt gersput.')

def itisPing():
	r = requests.get('http://www.itis.gov/ITISWebService/services/ITISService/getDescription')
  	return r.text

def gnrResolve(names='Homo sapiens', source=None, format='json', resolve_once='false', 
	with_context='false', best_match_only='false', header_only='false', preferred_data_sources='false'):
	'''
	E.g.: pytaxize.gnrResolve('Helianthus annus')
	'''
	url = 'http://resolver.globalnames.org/name_resolvers'
	payload = {'names': names, 'data_source_ids': source, 'format': format, 'resolve_once': resolve_once, 
			   'with_context': with_context, 'best_match_only': best_match_only, 'header_only': header_only, 
			   'preferred_data_sources': preferred_data_sources}
	out = requests.get(url, params = payload)
	data = out.json()['data'][0]['results']
	return data

def gniParse(names):
	'''
	E.g.: pytaxize.gniParse(names = ['Cyanistes caeruleus','Helianthus annuus'])
	'''
	url = 'http://gni.globalnames.org/parsers.json'
	names = '|'.join(names)
	out = requests.get(url, params = {'names': names})
	return out.json()

def gniSearch(search_term='ani*', per_page=30, page=1):
	'''
	E.g.: pytaxize.gniSearch(search_term = 'ani*')
	'''
	url = 'http://gni.globalnames.org/name_strings.json'
	out = requests.get(url, params = {'search_term': search_term, 'per_page': per_page, 'page': page})
	return out.json()

def gniDetails(id=17802847, all_records=1):
	'''
	E.g,: pytaxize.gniDetails(id = 17802847)
	'''
	url = 'http://gni.globalnames.org/name_strings/'
	mylist = [url, str(id), '.json']
	url2 = ''.join(mylist)
	out = requests.get(url2, params = {'all_records': all_records})
	return out.json()