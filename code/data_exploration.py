"""
Scripting for loading the data

Usage: python 
"""
import logging
import os
from argparse import ArgumentParser

import debugpy
from SPARQLWrapper import JSON, SPARQLWrapper

# Load DBPedia and Wikipedia Together

query_wiki_id = """
PREFIX xmlns: <http://xmlns.com/foaf/0.1/>
PREFIX wiki: <http://en.wikipedia.org/wiki/>

SELECT ?s ?anypreedicate ?object
WHERE {
  GRAPH <http://huginns.io/graph/wikipedia-links_lang=en> { 
    { VALUES ?predicate { xmlns:primaryTopic }
      wiki:<val> ?predicate ?o .}
    UNION
    {VALUES ?predicate { xmlns:isPrimaryTopicOf }
      wiki:<val> ?predicate ?o .}
  }

  ?s ?anypreedicate ?object .
} LIMIT 10

"""

related_objects = """
PREFIX xmlns: <http://xmlns.com/foaf/0.1/>
PREFIX wiki: <http://en.wikipedia.org/wiki/>

SELECT ?object ?anyPredicate ?relatedObject
WHERE {
  {
    SELECT ?object WHERE
    {
        GRAPH <http://huginns.io/graph/wikipedia-links_lang=en> { 
          { VALUES ?predicate { xmlns:primaryTopic }
            wiki:<val> ?predicate ?object .}
          UNION
          {VALUES ?predicate { xmlns:isPrimaryTopicOf }
            wiki:<val> ?predicate ?object .}
        } 
    } LIMIT 1
  }

  GRAPH <http://huginns.io/graph/infobox-properties_lang=en> {
    ?object ?anyPredicate ?relatedObject .
  }

} LIMIT 10

"""

# Define the Fuseki server endpoint


def setup_logger(name: str, level):
    entryp_path = os.path.dirname(os.path.abspath(__file__))
    logs_dir = os.path.join(entryp_path, "logs/")
    os.makedirs(logs_dir, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    sh.setLevel(logging.INFO)

    fh = logging.FileHandler(os.path.join(logs_dir, name + ".log"))
    fh.setFormatter(formatter)
    fh.setLevel(level)

    logger.addHandler(fh)
    logger.addHandler(sh)

    return logger


class Graph:
    """
    Will represent a returned graph from a query.
    """

    def __init__(self):
        pass


def explore_ttl_data(endpoint: str):
    """
    Use Parql
    """
    sparql = SPARQLWrapper(fuseki_endpoint)
    # Define your SPARQL query
    query = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX wiki: <https://en.wikipedia.org/wiki/>
    PREFIX 
    SELECT ?subject ?predicate ?object
    WHERE {
       ?predicate ?object
    }
    LIMIT 10
    """
    # Set the query to the SPARQLWrapper
    sparql.setQuery(query)
    # Select the return format (e.g., JSON or XML)
    sparql.setReturnFormat(JSON)
    # Execute the query and convert the response to a Python dictionary
    try:
        response = sparql.query().convert()
        for result in response["results"]["bindings"]:  # type:ignore
            print(result)
    except Exception as e:
        print(f"An error occurred: {e}")


def explore_local(
    file_path: str,
):
    cwd = os.getcwd()
    full_path = os.path.join(cwd, file_path)
    if not os.path.exists(full_path) or not file_path.endswith("ttl"):
        raise ValueError("Provided does not exist or is incorrect")

    graph = Graph()
    graph.parse(full_path, format="ttl")

    qres = graph.query(
        """ SELECT DISTINCT
           ?subject ?predicate ?object
           WHERE {
           ?subject ?predicate ?object .
           } LIMIT 10
        """
    )
    for row in qres:
        print(f"S: {row.subject} P: {row.predicate} O: {row.object}")  # type:ignore


def argsies():
    ap = ArgumentParser()
    ap.add_argument("--port", default=3030, type=int)
    ap.add_argument("--host", default="localhost", type=str)
    ap.add_argument("--wiki_id", required=True)
    ap.add_argument("--debug", action="store_true")

    parsed = ap.parse_args()

    # Sanitized

    return parsed


"http://xmlns.com/foaf/0.1/isPrimaryTopicOf"
"http://xmlns.com/foaf/0.1/primaryTopic"


def explore_fuseki(wiki_id: str):
    query = related_objects.replace("<val>", wiki_id)
    logger.info(f"We are using query:\n{query}")
    sparql = SPARQLWrapper(fuseki_endpoint)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    try:
        response = sparql.query().convert()
        # logger.info(f"Response is {response}")
        # logger.info("Prettier")

        for result in response["results"]["bindings"]:  # type:ignore
            logger.info(result)
    except Exception as e:
        print(f"An error occurred: {e}")


global logger
if __name__ == "__main__":
    # Take args
    args = argsies()
    logger = setup_logger(__name__, logging.INFO)
    # Take he
    if args.debug:
        logger.info("Debugging is enabled, waiting for client")
        debugpy.listen(42019)
        debugpy.wait_for_client()
        logger.info("Client connected continuing with debuggin session")

    # Send Fuseki the request

    fuseki_endpoint = "http://localhost:3030/fusekiservice/query"
    explore_fuseki(args.wiki_id)
