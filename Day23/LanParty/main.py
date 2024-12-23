from collections import namedtuple
from copy import deepcopy
from enum import unique

Node = namedtuple("Node", ["From", "To"])


def process_file(filename):
    """Read the file and split into list."""
    with open(filename, "r") as file:
        connections = file.read().splitlines()
        return [Node(*connection.split("-")) for connection in connections]


def find_connected_nodes(computers):
    node_matches = []
    for computer in computers:
        # Considering computer.From and search from computer.To
        connected_nodes = [
            comp.To if comp.From == computer.To else comp.From
            for comp in computers
            if comp.From == computer.To or comp.To == computer.To
        ]
        for node in connected_nodes:
            last_nodes = [
                comp.To if comp.From == node else comp.From
                for comp in computers
                if comp.From == node or comp.To == node
            ]
            if computer.From in last_nodes:
                node_matches.append([computer.From, computer.To, node])

    unique_node_matches = list({tuple(sorted(match)) for match in node_matches})
    return unique_node_matches


def find_connected_nodes_startswith(computers, letter):
    connected_nodes = find_connected_nodes(computers)
    filtered_node_matches = [
        list(match)
        for match in connected_nodes
        if any(node.startswith(letter) for node in match)
    ]

    return len(filtered_node_matches)


# Main execution
if __name__ == "__main__":
    computers = process_file("dummydata.txt")
    assert len(find_connected_nodes(computers)) == 12
    assert find_connected_nodes_startswith(computers, "t") == 7
    computers = process_file("data.txt")
    print("Part 1", find_connected_nodes_startswith(computers, "t"))
