from rdflib import Graph

from sfia_rdf import namespaces
from sfia_rdf.parsers.skills_parser import hash_name


def test_hash():
    assert hash_name("My, category") == "my__category"


def test_bind_namespaces():
    g = Graph()
    namespaces.bind_namespaces(g)
    assert g.qname("https://rdf.sfia-online.org/9/lor/2") == "levels:2"
