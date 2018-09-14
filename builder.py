#from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from io import BytesIO
import xmltodict
import json
import wget
import os

__author__ = 'Luiz Fernando Surian Filho'
file_path  = './bin/files/'
file_main  = f'{file_path}main.json'
file_xml   = f'{file_path}nist800-53-controls.xml'
url_nist   = 'https://nvd.nist.gov/download/800-53/800-53-controls.xml'
        
# Nist Handler
def build():
    # Verify Nist files
    nist_main = {}
    print('building dependencies')
    # Check XML
    if (Path(file_xml).is_file() == False):
        print('nist xml file not found, downloading')
        
        try:
            wget.download(url_nist, out=file_xml)
        except:
            print('couldn\'t download file')
            return False
    else:
        print('nist xml file ok')

    # Check JSON
    if (Path(file_main).is_file() == False):
        print('json file not found, parsing xml file')
        doc = {}
        
        with open(file_xml, 'rb') as fd:
            doc = xmltodict.parse(fd.read())
            
        for item in doc['ns3:controls']['ns3:control']:
            # Parse XML
            control_class = item['control-class']
            family        = item['family']
            number        = item['number']
            title         = item['title']
            try:
              priority = item['priority']
            except:
              priority = False
            try:
              baseline_impact = item['baseline-impact']
            except:
              baseline_impact = False
            try:
              description = item['description']
            except:
              description = False
            try:
              supplemental_guidance = item['supplemental-guidance']
            except:
              supplemental_guidance = False
            try:
              references = item['references']['reference']
            except:
              references = False
            try:
              control_enhancements = item['control-enhancements']['control-enhancement']
            except:
              control_enhancements = False
              

            # Build main dict
            if control_class not in nist_main:
                nist_main[control_class] = {}

            if family not in nist_main[control_class]:
                nist_main[control_class][family] = {}

            nist_main[control_class][family].update( { number: { 'title': title,
                                                                 'priority': priority } } )

            # Make individual item JSON
            file_current = f'{file_path}nist/{number}.json'
            content = { 'title': title,
                        'priority': priority,
                        'baseline_impact': baseline_impact,
                        'description': description,
                        'supplemental_guidance': supplemental_guidance,
                        'references': references,
                        'control_enhancements': control_enhancements }
            
            with open(file_current, 'wb') as f:
                #print('building', file_current)
                f.write( bytes(str( json.dumps(content) ), "utf-8") )

            # Make main JSON
            with open(file_main, 'wb') as f:
                #print('building', file_main)
                f.write( bytes(str( json.dumps(nist_main) ), "utf-8") )

    else:
        print('nist json file ok')

    
    print('build successfull')
    return True

if __name__ == "__main__":
    if build():
        print('exiting')
    else:
        print('stopping')
        os.system('pause')
