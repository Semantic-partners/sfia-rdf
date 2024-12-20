import csv
import os

import pytest
from rdflib import Graph

from sfia_rdf import namespaces
from sfia_rdf.parsers import skills_parser


@pytest.fixture
def skills_graph():
    g = Graph()
    namespaces.bind_namespaces(g)
    with open(os.path.dirname(__file__) + "/test_files/skills_test.csv") as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        reader.__next__()  # skip header
        for row in reader:
            triples = skills_parser.parse_row(row)
            [g.add(triple) for triple in triples]
    return g


def test_properties(skills_graph):
    ress = skills_graph.query("""
        select ?skill
        where {
            ?skill a sfia:Skill
        }
        order by ?skill
    """)
    assert [str(res.skill) for res in ress] == ["https://rdf.sfia-online.org/9/skills/ISCO",
                                                "https://rdf.sfia-online.org/9/skills/ITSP"]
    ress = skills_graph.query("""
    select ?skillLevel
    where {
        skills:ISCO sfia:definedAtLevel ?skillLevel
    }
    order by ?skillLevel
    """)
    assert [str(res.skillLevel) for res in ress] == ["https://rdf.sfia-online.org/9/skilllevels/ISCO_6",
                                                     "https://rdf.sfia-online.org/9/skilllevels/ISCO_7"]


def test_categories(skills_graph):
    ress = skills_graph.query("""
        select ?cat
        where {
            ?cat a sfia:Category
        }
        order by ?cat
    """)
    print(str(len([res.cat for res in ress])))
    assert [str(res.cat) for res in ress] == [
        'https://rdf.sfia-online.org/9/categories/strategy_and_architecture',
        'https://rdf.sfia-online.org/9/categories/strategy_and_planning'
    ]
