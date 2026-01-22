from sys import argv


def find_costs(route, costs):
    rows, columns = len(route), len(route[0])
    # Create a 2D list with all zeros, same as the size of the given route
    cost_route = [[0 for column in range(columns)] for row in range(rows)]

    for i in range(rows):
        for j in range(columns):
            # For every 1 in route check neighbors and get its cost
            if route[i][j] == 1:
                horizontal_vertical_neighbors = []
                diagonal_neighbors = []

                # Check all neighbors (vertical, horizontal and diagonal - one hop away)
                for row_offset in range(-1, 2):
                    for column_offset in range(-1, 2):
                        # Skip the current cell
                        if row_offset == 0 and column_offset == 0:
                            continue

                        # Get the neighbor's row and column
                        neighbor_row, neighbor_column = i + row_offset, j + column_offset
                        # Make sure that neighbor is not over the bounds of the route
                        if 0 <= neighbor_row < rows and 0 <= neighbor_column < columns:
                            # Check if it is horizontal and vertical or diagonal neighbor
                            # it is horizontal or vertical when column or row are the same as of the current cell
                            if (row_offset == 0 and column_offset != 0) or (row_offset != 0 and column_offset == 0):
                                horizontal_vertical_neighbors.append(route[neighbor_row][neighbor_column])
                            else:
                                diagonal_neighbors.append(route[neighbor_row][neighbor_column])

                # Assign costs according to the neighbors
                if all(neighbor == 1 for neighbor in horizontal_vertical_neighbors + diagonal_neighbors):
                    cost_route[i][j] = int(costs[0])
                elif (
                        any(neighbor == 0 for neighbor in diagonal_neighbors) and
                        all(neighbor == 1 for neighbor in horizontal_vertical_neighbors)
                ):
                    cost_route[i][j] = int(costs[1])
                else:
                    cost_route[i][j] = int(costs[2])

    return cost_route


def find_path(cost_route, i, j,
              current_cost, visited_cells, current_path,
              min_cost, min_cost_path):
    rows, columns = len(cost_route), len(cost_route[0])

    # Base case: Check if rightmost cell has been reached
    if j == columns - 1:
        # Compare new cost and update min_cost and min_cost_path if it is less than previously found
        if current_cost < min_cost:
            min_cost = current_cost
            min_cost_path.clear()
            min_cost_path.extend(current_path)
        return min_cost, min_cost_path

    # Recursive case: Check  possible moves(right, up, down, left)
    # Make sure the next cell is valid (within the bounds, not visited, not a sinkhole (0))
    # Check right
    if j + 1 < columns and (i, j + 1 ) not in visited_cells and cost_route[i][j + 1] != 0:
        new_cost = current_cost + cost_route[i][j + 1]
        # Check if next move will increase cost so it is bigger than min cost so far
        if new_cost < min_cost:
            # Mark this cell as visited and add its indexes to path
            # current_path and min_cost_path are used to track indexes of the path with min cost
            # so it will be reused later for output
            visited_cells.append((i, j + 1))
            current_path.append((i, j + 1))
            min_cost, min_cost_path = find_path(
                cost_route, i, j + 1, new_cost,
                visited_cells, current_path, min_cost, min_cost_path
            )
            # After finishing this call remove it from visited cells and current_path
            visited_cells.remove((i, j + 1))
            current_path.pop()

    # Same logic is also used for other moves (up, down, left)
    # Check up
    if i - 1 >= 0 and (i - 1, j) not in visited_cells and cost_route[i - 1][j] != 0:
        new_cost = current_cost + cost_route[i - 1][j]
        if new_cost < min_cost:
            visited_cells.append((i - 1, j))
            current_path.append((i - 1, j))
            min_cost, min_cost_path = find_path(
                cost_route, i - 1, j, new_cost,
                visited_cells, current_path, min_cost, min_cost_path
            )
            visited_cells.remove((i - 1, j))
            current_path.pop()

    # Check down
    if i + 1 < rows and (i + 1, j) not in visited_cells and cost_route[i + 1][j] != 0:
        new_cost = current_cost + cost_route[i + 1][j]
        if new_cost < min_cost:
            visited_cells.append((i + 1, j))
            current_path.append((i + 1, j))
            min_cost, min_cost_path = find_path(
                cost_route, i + 1, j, new_cost,
                visited_cells, current_path, min_cost, min_cost_path
            )
            visited_cells.remove((i + 1, j))
            current_path.pop()

    # Check left
    if j - 1 >= 0 and (i, j - 1) not in visited_cells and cost_route[i][j - 1] != 0:
        new_cost = current_cost + cost_route[i][j - 1]
        if new_cost < min_cost:
            visited_cells.append((i, j - 1))
            current_path.append((i, j - 1))
            min_cost, min_cost_path = find_path(
                cost_route, i, j - 1, new_cost,
                visited_cells, current_path, min_cost, min_cost_path
            )
            visited_cells.remove((i, j - 1))
            current_path.pop()

    return min_cost, min_cost_path


def main():
    if len(argv) != 3:
        print("It should be: python route_finder.py <input_file> <output_file>")
        return

    try:
        with open(argv[1], "r") as file_input:
            # Check if input is empty
            if not file_input.readlines():
                print("Input file is empty")
                return

            file_input.seek(0)

            # Check if number of costs is not less or bigger than 3
            try:
                costs = file_input.readline().strip().split(" ")
                if len(costs) != 3:
                    raise ValueError("There should be exactly 3 positive integers that represent costs.")
            except ValueError as e:
                print(e)
                return

            try:
                route = []
                for line in file_input:
                    route.append([int(x) for x in line.split()])
                # Make sure all rows have the same length
                row_length = len(route[0])
                if not all(len(row) == row_length for row in route):
                    raise ValueError("All rows in the input file should have the same length.")
            except ValueError as e:
                print(e)
                return

            route_with_costs = find_costs(route, costs)
            min_cost = float('inf')
            min_cost_path = []

            # Check path for every first leftmost row
            for i in range(len(route_with_costs)):
                # Make sure it is not a sinkhole (0)
                if route_with_costs[i][0] != 0:
                    visited_cells = [(i, 0)]
                    current_path = [(i, 0)]
                    min_cost, min_cost_path = find_path(
                        route_with_costs, i, 0, route_with_costs[i][0],
                        visited_cells, current_path, min_cost, min_cost_path
                    )

            with open(argv[2], "w") as output_file:
                if min_cost == float('inf'):
                    output_file.write("There is no possible route!")
                else:
                    output_file.write(f"Cost of the route: {min_cost}\n")
                    for i in range(len(route)):
                        for j in range(len(route[i])):
                            # Mark the shortest path with "X"
                            if (i, j) in min_cost_path:
                                route[i][j] = 'X'
                            output_file.write(f"{route[i][j]}")
                            if j < len(route[i]) - 1:
                                output_file.write(" ")
                        if i < len(route) - 1:
                            output_file.write("\n")

    except FileNotFoundError:
        print("Input file not found")
        return
    except PermissionError:
        print("Permission denied")
        return


if __name__ == '__main__':
   main()