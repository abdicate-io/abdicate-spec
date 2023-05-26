import networkx as nx

from pydantic import BaseModel

from pathlib import Path
from ruamel.yaml import YAML
from abdicate.assembly import read_directory

from abdicate.weave import WeaveModel
from abdicate.model_1_1 import ServiceIdentifier


class BuildOrderModel(BaseModel):
    services: list[ServiceIdentifier]

    @classmethod
    def from_model(cls, woven: WeaveModel) -> "BuildOrderModel":
        g_list = []
        for name, weavable in woven.weavable.items():
            for s in weavable.services:
                g_list.append((weavable.providers[0].service, s.service))

        for name, provisionable in woven.provisionable.items():
            for s in provisionable.services:
                g_list.append((name, s.service))

        for name, required in woven.required.items():
            for s in required.services:
                g_list.append((name, s.service))


        graph = nx.DiGraph()
        #NetworkX does not like special chars in the node names, so quote them
        g_list = list(map(lambda x: (_quote(x[0]), _quote(x[1])), g_list))

        graph.add_edges_from(g_list)
        order = list(list(nx.topological_sort(graph)))

        order = list(map(lambda x: _unquote(x), order))

        return cls(**{
            'services': order,
            })


def _quote(string: str) -> str:
    return '"{}"'.format(string)

def _unquote(string: str) -> str:
    return string.strip('"')