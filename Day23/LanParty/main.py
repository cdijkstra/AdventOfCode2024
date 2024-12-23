def process_file(filename):
    """Read the file and split into list."""
    conns = {}
    with open(filename, "r") as file:
        connections = [line.strip().split("-") for line in file.readlines()]
        for left, right in connections:
            if left not in conns:
                conns[left] = set()
            if right not in conns:
                conns[right] = set()
            conns[left].add(right)
            conns[right].add(left)
        return conns


def find_connected_nodes(connections):
    node_matches = []
    for initial_node, connected_nodes in connections.items():
        for second_node in connected_nodes:
            for third_node in connections[second_node]:
                if initial_node not in connections[third_node]:
                    continue
                node_matches.append([initial_node, second_node, third_node])

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

    # Every node is connected to two other nodes
    # Those nodes are connected to other nodes as well
