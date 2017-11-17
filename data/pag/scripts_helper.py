def scrape_record(csv, i):
    """ Scrape data regarding a single listed company. """
    record = http_get(ISSUER, i).get('GetIssuerResult')
    if not record.get('LongName'):
        return
    log.info('Scraping: %s', record.get('LongName'))
    nob = http_get(BUSINESS, i).get('GetIssuerNatureOfBusinessResult')
    record['NatureOfBusiness'] = nob
    res = http_get(ASSOCIATED, i)
    assocs = res.get('GetIssuerAssociatedRolesResult', [])
    record['source_url'] = SOURCE_URL % i
    record.pop('Contacts', None)
    csv.write('jse_entities.csv', record)
    for assoc in assocs:
        assoc.pop('Contacts', None)
        assoc['source_url'] = record['source_url']
        csv.write('jse_entities.csv', assoc)
        link = {
            'SourceName': assoc.get('LongName'),
            'TargetName': record.get('LongName'),
            'Role': assoc.get('RoleDescription'),
            'source_url': record['source_url']
        }
        csv.write('jse_links.csv', link)




import requests
URL_PATTERN = 'https://www.ppaghana.org/contractdetail.asp?Con_ID=%s'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
url = URL_PATTERN % 432
try: 
    res = requests.get(url, headers=HEADERS)
except ConnectionError as e:
    z = e

print z



try:
    res = requests.get(url, headers=HEADERS)
except requests.exceptions.Timeout:
    # Maybe set up for a retry, or continue in a retry loop
except requests.exceptions.HTTPError:
    # Tell the user their URL was bad and try a different one
except requests.exceptions.RequestException as e:
    # catastrophic error. bail.
    print e
    sys.exit(1)





import pandas as pd
f3 = pd.read_csv("ppa_contracts3.csv")
f4 = pd.read_csv("ppa_contracts4.csv")
f5 = pd.read_csv("ppa_contracts5.csv")
f6 = pd.read_csv("ppa_contracts6.csv")
f7 = pd.read_csv("ppa_contracts7.csv")
f8 = pd.read_csv("ppa_contracts8.csv")
f = pd.concat([f3, f4, f5, f6, f7, f8])



import pandas as pd
ppa_contracts = pd.read_csv("ppa_contracts.csv")
f = pd.read_csv("f.csv")
f = pd.concat([f, ppa_contracts])
f.sort_values(['contract_id'], ascending=[True], inplace=True)
f["contract_signed_on"] = pd.to_datetime(f["contract_signed_on"])
f["estimated_contract_completion_date"] = pd.to_datetime(f["estimated_contract_completion_date"])
orig_len = len(f)
f.drop_duplicates(keep='first', inplace=True)
dedu_len = len(f)
print("Original length = %s ----- Deduplicate length = %s and de difference is: %s " % (orig_len, dedu_len, orig_len - dedu_len))
orig_len - dedu_len
f.to_csv("f.csv", index=False)
all = pd.Index(range(0,5067))
l = all.difference(f.contract_id)
len(l)


f = pd.read_csv("f.csv")
f["contract_id"].astype('category').describe()
f["contract_awarded_to"].astype('category').describe()
f["awarding_agency"].astype('category').describe()
f["awarding_ministry"].astype('category').describe()
f["tender_type"].astype('category').describe()



s = "Mr. Seth Adjei - Chairman\n\nMr. E. Kwasi Okoh - Managing Director\n\nTogbe Afede XIV - Member\n\nMr. Victor K. Djangmah - Member\n\nMr. Anthony Ebow Spio - Member\n\nProf. Lade Wosornu - Member\n\nMr. Kingsley O. Ofosu Obeng - Member\n\nMr.Joseph Simple Siilo - Member"
def remove_el(l, el):
   return [v for v in l if v != el]


s = s.split('\n')
s = remove_el(s, '')
s


persons = []
for el in s :
    p = {}
    p['name'] = el.split('-')[0].strip()
    p['position'] = el.split('-')[1].strip()
    persons.append(p)






ngos = pd.read_csv("ghanayello_ngos4.csv")
ngos_m = pd.read_csv("ghanayello_ngos.csv")
f2 = pd.concat([ngos, ngos_m])
f2.to_csv("f2.csv", index=False)

def diff(first, second):
    second = set(second)
    return [item for item in first if item not in second]


