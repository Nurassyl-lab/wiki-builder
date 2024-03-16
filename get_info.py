"ALL IN ONE FILE"

from rdflib import Graph, Namespace, Literal
import requests
import argparse
import pandas as pd
import urllib.parse

def wikipedia_to_dbpedia(wikipedia_url):
    title = wikipedia_url.split('/')[-1]
    title_encoded = urllib.parse.quote(title)
    dbpedia_uri = f'http://dbpedia.org/resource/{title_encoded}'
    return dbpedia_uri

# Example usage
#wikipedia_link = 'https://en.wikipedia.org/wiki/Python_(programming_language)'
#dbpedia_link = wikipedia_to_dbpedia(wikipedia_link)

def parse_arguments():
    parser = argparse.ArgumentParser(description='Extract RDF predicates and objects from a given URL.')
    parser.add_argument('--wiki_url', default='skip', help='The URL of the RDF resource to extract data from.')
    args = parser.parse_args()
    return args


#url = 'http://dbpedia.org/resource/Frunthorn'
args = parse_arguments()
url = wikipedia_to_dbpedia(args.wiki_url)
print(url)

# You can add more namespaces (aka predicates)
DBP = Namespace('http://dbpedia.org/property/')
DBO = Namespace('http://dbpedia.org/ontology/')
RDFS = Namespace('http://www.w3.org/2000/01/rdf-schema#')
PROV = Namespace('http://www.w3.org/ns/prov#')
OWL = Namespace('http://www.w3.org/2002/07/owl#')
FOAF = Namespace('http://xmlns.com/foaf/0.1/')
GEO = Namespace('http://www.w3.org/2003/01/geo/wgs84_pos#')
RDF = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')

namespaces = {
    DBP: 'dbp',
    DBO: 'dbo',
    RDFS: 'rdfs',
    PROV: 'prov',
    OWL: 'owl',
    FOAF: 'foaf',
    GEO: 'geo',
    RDF: 'rdf'
} 

headers = {'Accept': 'text/turtle'}
response = requests.get(url, headers=headers)

res_file = {
    'title':url,
    'relation':'direct',
    'predicate':[],
    'str':[]
}

if response.status_code == 200:
    g = Graph()
    g.parse(data=response.text, format='turtle')
    for predicate, obj in g.predicate_objects():
        predicate_short = predicate
        for ns, prefix in namespaces.items():
            if predicate.startswith(ns):
                predicate_short = f'{prefix}:{predicate[len(ns):]}'
                break
        obj_str = f'{obj}'
        if isinstance(obj, Literal):
            if obj.datatype:
                obj_str += f' ({obj.datatype})'
            if obj.language:
                obj_str += f' (@{obj.language})'

        #print(f'{predicate_short}\t{obj_str}')
        res_file['predicate'].append(predicate_short)
        res_file['str'].append(obj_str)
else:
    print(f'Failed to retrieve RDF data from {url}. Status code: {response.status_code}')

pd.DataFrame.from_dict(res_file).to_csv('info.csv', index=False)
