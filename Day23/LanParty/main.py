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


def find_connected_nodes_startswith(connection, letter):
    connected_nodes = find_connected_nodes(connection)
    filtered_node_matches = [
        list(match)
        for match in connected_nodes
        if any(node.startswith(letter) for node in match)
    ]

    return len(filtered_node_matches)


def find_maximum_connected_nodes(connections):
    sets = set()  # Use a set to prevent duplicates

    def search(node, required):
        key = tuple(sorted(required))
        if key in sets:
            return
        sets.add(key)
        for neighbor_node in connections[node]:
            if neighbor_node in required:
                continue
            if not all(neighbor_node in connections[query] for query in required):
                continue
            search(neighbor_node, required | {neighbor_node})

    for connection in connections:
        search(connection, {connection})

    required_nodes = sorted(max(sets, key=len))
    return ",".join(required_nodes)


# Main execution
if __name__ == "__main__":
    connections = process_file("dummydata.txt")
    assert len(find_connected_nodes(connections)) == 12
    assert find_connected_nodes_startswith(connections, "t") == 7
    print(find_maximum_connected_nodes(connections))
    connections = process_file("data.txt")
    print("Part 1", find_connected_nodes_startswith(connections, "t"))
    print("Part 2", find_maximum_connected_nodes(connections))
