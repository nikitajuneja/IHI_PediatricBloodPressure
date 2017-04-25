from fhirclient import client
import datetime
import csv

settings = {
    'app_id': 'my_web_app',
##    'api_base': 'https://fhir-open-api-dstu2.smarthealthit.org' # 'http://35.185.78.58:9070/api/smartdstu2/open'
##    'api_base': 'http://35.185.78.58:9070/api/smartdstu2/open'
##    'api_base': 'http://52.72.172.54:8080/fhir/baseDstu2'
##    'api_base':'https://sandbox.smarthealthit.org/smartdstu2/open'
##    'api_base': 'https://sb-fhir-dstu2.smarthealthit.org/api/smartdstu2/data'
##    'api_base': 'https://fhir.careevolution.com/Master.Adapter1.WebClient/api/fhir/open'
    'api_base': 'https://sb-fhir-dstu2.smarthealthit.org/api/smartdstu2/open'
##    'api_base': 'https://api.hspconsortium.org/BP2/open'
}

smart = client.FHIRClient(settings=settings)

import fhirclient.models.bundle as b
import fhirclient.models.patient as p
import fhirclient.models.observation as o

def iterentries(qry):
    """ Generator to provide the entries in a paged bundle. Hides the
        process of pages being passed.
        input:
            qry is the portion of the REST URL after the server
        yields:
            a tuble containing
            entry - a single entry from the bundle
            blob - the most recent portion of the bundle downloaded
        Note:  had trouble nesting loops, probably because of
            a timeout between page fetches.
    """
    bund = b.Bundle.read_from(qry,smart.server)
    have_page = bund.entry
    while have_page:
        for item in bund.entry:
            yield item,bund
        next_link = next((item.url for item in bund.link if item.relation == 'next'),None)
        if next_link:
            qry = next_link.rpartition('?')[2]
            bund = b.Bundle.read_from('?'+qry,smart.server)
        else:
            have_page = False


# Get all the patients as a list
pats = []
for pat,blob in iterentries('Patient?_format=json):#&_count=10'):
    pats.append(pat)

# Get all of the observations of vital signs. Find youngest reading and count
# BP readings under age 20 per patient to find the useful ones for project

# Use the python csv library for file output
with open('pat.csv', 'wb') as patfile,open('vitals.csv','wb') as vitfile:
    pwriter = csv.writer(patfile,delimiter="\t",quotechar='"',quoting=csv.QUOTE_MINIMAL)
    owriter = csv.writer(vitfile,delimiter="\t",quotechar='"',quoting=csv.QUOTE_MINIMAL)
    for pat in pats:
        youngestBP = 1000000
        bpUnder20 = 0
        for ob,blob2 in iterentries('Observation?patient='+pat.resource.id+'&category=vital-signs&_format=json'):
            # Had to jump through hoops because dates are intemixed with datetimes
            edt = ob.resource.effectiveDateTime.date
            edtiso = ob.resource.effectiveDateTime.isostring
            if isinstance(edt,datetime.datetime):
                edt = edt.date()
            obAge = (edt-pat.resource.birthDate.date).days/1  # age in days
            # Look for Loinc code for BP pair and count these
            if ob.resource.code.coding[0].code == '55284-4':
                if  obAge < youngestBP:
                    youngestBP = obAge
                if obAge < 20*365.25:
                    bpUnder20 += 1
            # Some observations are lists of several different values
            # Others are singletons.  Make singletons 1 entry lists to simplify
                ll = ob.resource.component
            else:
                ll = [ob.resource]
            for meas in ll:
                ovec = [ pat.resource.id, #pt id
                        obAge, #age at observation (days)
                        edtiso, #date of observation
                        meas.code.coding[0].display, #what was measured
                        meas.valueQuantity.value, #the result
                        meas.valueQuantity.unit] #units
                owriter.writerow(ovec)
        # Output the patients - id, name, # BP before age 20, age at first BP (in days)
        pvec = [pat.resource.id,smart.human_name(pat.resource.name[0]),bpUnder20,youngestBP]
        pwriter.writerow(pvec)
        # Print the interesting ones (data starts before age 20) to stdout
        if youngestBP < 20*365.25:
            print pvec




