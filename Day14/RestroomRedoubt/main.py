import copy
from collections import namedtuple

Robot = namedtuple("Coordinate", ["x", "y", "vx", "vy"])


def process_file(filename):
    """Read the file and split into list."""
    robot_dict = {}
    with open(filename, "r") as file:
        for line_number, line in enumerate(file):
            line = line.strip()  # Remove any leading/trailing whitespace
            if line:  # Ensure line is not empty
                # Parse the p and v values from the line
                parts = line.split()
                p_values = parts[0][2:].split(",")  # Extract p=x,y
                v_values = parts[1][2:].split(",")  # Extract v=x,y

                # Create a Robot namedtuple
                robot = Robot(
                    x=int(p_values[0]),
                    y=int(p_values[1]),
                    vx=int(v_values[0]),
                    vy=int(v_values[1]),
                )

                # Add the robot to the dictionary
                robot_dict[line_number] = robot

    return robot_dict


def safety_score_quadrant(grid, x_range, y_range):
    count = 0
    for x in x_range:
        for y in y_range:
            if grid[y][x].isdigit():  # Check if there's a robot count at this position
                count += int(grid[y][x])
    return count


def calculate_safety_score(robots, width, height, seconds):
    grid = update_coordinates(robots, width, height, seconds)
    safety_score = (
        safety_score_quadrant(
            grid, range(0, (width - 1) // 2), range(0, (height - 1) // 2)
        )
        * safety_score_quadrant(
            grid, range((width + 1) // 2, width), range(0, (height - 1) // 2)
        )
        * safety_score_quadrant(
            grid, range(0, (width - 1) // 2), range((height + 1) // 2, height)
        )
        * safety_score_quadrant(
            grid, range((width + 1) // 2, width), range((height + 1) // 2, height)
        )
    )
    return safety_score


def update_coordinates(robots, width, height, seconds):
    updated_robots = copy.deepcopy(robots)
    for key, robot in updated_robots.items():
        updated_robots[key] = robot._replace(
            x=(robot.x + seconds * robot.vx) % width,
            y=(robot.y + seconds * robot.vy) % height,
        )

    return visualize_grid(updated_robots, width, height)


def visualize_grid(robots, width, height):
    # Create a 2D grid initialized with dots
    grid = [["." for _ in range(width)] for _ in range(height)]

    # Count robots at each coordinate
    position_count = {}
    for robot in robots.values():
        pos = (robot.y, robot.x)  # Note: y corresponds to rows, x to columns
        position_count[pos] = position_count.get(pos, 0) + 1

    # Fill the grid with the number of robots at each position
    for (y, x), count in position_count.items():
        grid[y][x] = str(count)

    # Print the grid
    # for row in grid:
    #     print(" ".join(row))
    # print("\n")  # Add spacing between time steps
    return grid


# Main execution
if __name__ == "__main__":
    robots = process_file("dummydata.txt")
    assert calculate_safety_score(robots, width=11, height=7, seconds=100) == 12

    robots = process_file("data.txt")
    print("part 1", calculate_safety_score(robots, width=101, height=103, seconds=100))
