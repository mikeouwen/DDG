# import library of plotting and drawing rectangles
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.collections import LineCollection
from matplotlib.patches import Rectangle

import random
import math

# headpq for priority queue
import heapq

# deque for double-ended queue
from collections import deque

# import the image processing library for generating level map
from PIL import Image

# for specifying relative file path
from pathlib import Path


# number of cells on the x axis
grid_size_x = 50
# number of cells on the y axis
grid_size_y = 50

# tile size of the tile image in pixels
tile_size_x = 16
tile_size_y = 16


def initializeWeight(index):
    # generate a random weight matrix
    # weight matrix of horizontal edges
    horizontal_weight = [
        [random.randint(1, 100) for x in range(grid_size_x - 1)]
        for y in range(grid_size_y)
    ]

    vertical_weight = [
        [random.randint(1, 100) for x in range(grid_size_x)]
        for y in range(grid_size_y - 1)
    ]

    drawWeightMap(horizontal_weight, vertical_weight, index)

    return horizontal_weight, vertical_weight

    # find the path from a destination node to the starting node


def findPath(path, parents, start_node, destination_node):
    # enque the node from left
    path.appendleft(destination_node)
    # check if this node is the starting node
    if destination_node == start_node:
        print("Pathfinding finished. Here is the path")
        print(path)
    # if not, trace back and put in the parent node of the current node as the next node to check.
    else:
        findPath(path, parents, start_node, parents[destination_node])

    return path


def dijkstraSearch(start_node, end_node, image, index):

    # initialize the graph weight
    horizontal_weight, vertical_weight = initializeWeight(index)

    # set up graph
    # set up the graph representation of the dungeon using a hash table. Key will be grid cell as tuple e.g. (x,y)
    # Values will be the cell's neighbor and the movement cost ((x,y),cost)

    graph = {}

    # 4 corner cases
    # top left corner
    graph[(0, 0)] = [(1, 0, horizontal_weight[0][0]), (0, 1, vertical_weight[0][0])]

    # top right corner
    graph[(grid_size_x - 1, 0)] = [
        (grid_size_x - 2, 0, horizontal_weight[0][-1]),
        (grid_size_x - 1, 1, vertical_weight[0][-1]),
    ]

    # bottom left corner
    graph[(0, grid_size_y - 1)] = [
        (1, grid_size_y - 1, horizontal_weight[-1][0]),
        (0, grid_size_y - 2, vertical_weight[-1][0]),
    ]

    # bottom right corner
    graph[(grid_size_x - 1, grid_size_y - 1)] = [
        (grid_size_x - 2, grid_size_y - 1, horizontal_weight[-1][-1]),
        (grid_size_x - 1, grid_size_y - 2, vertical_weight[-1][-1]),
    ]

    # top and bottom row cell

    for x in range(1, grid_size_x - 1):
        # top row
        graph[(x, 0)] = [
            (x - 1, 0, horizontal_weight[0][x - 1]),
            (x + 1, 0, horizontal_weight[0][x]),
            (x, 1, vertical_weight[0][x]),
        ]

        # bottom row
        graph[(x, grid_size_y - 1)] = [
            (x - 1, grid_size_y - 1, horizontal_weight[-1][x - 1]),
            (x + 1, grid_size_y - 1, horizontal_weight[-1][x]),
            (x, grid_size_y - 2, vertical_weight[-1][x]),
        ]

    # left and right row cell

    for y in range(1, grid_size_y - 1):
        # Left row
        graph[(0, y)] = [
            (0, y - 1, vertical_weight[y - 1][0]),
            (0, y + 1, vertical_weight[y][0]),
            (1, y, horizontal_weight[y][0]),
        ]

        # right row
        graph[(grid_size_x - 1, y)] = [
            (grid_size_x - 1, y - 1, vertical_weight[y - 1][-1]),
            (grid_size_x - 1, y + 1, vertical_weight[y][-1]),
            (grid_size_x - 2, y, horizontal_weight[y][-1]),
        ]

    # all other cell

    for x in range(1, grid_size_x - 1):
        for y in range(1, grid_size_y - 1):
            graph[(x, y)] = [
                (x - 1, y, horizontal_weight[y][x - 1]),
                (x, y - 1, vertical_weight[y - 1][x]),
                (x + 1, y, horizontal_weight[y][x]),
                (x, y + 1, vertical_weight[y][x]),
            ]

    # let's start writing the Dijkstra's algorithm
    # we first need the graph, the current cost hash table, the costs priority queue and the parent hash table
    # we already have graph

    # set a random starting node

    # set up the current cost hash table
    costs = {}

    for x in range(grid_size_x):
        for y in range(grid_size_y):
            costs[(x, y)] = math.inf

    # the starting node should have a cost 0
    costs[start_node] = 0

    # set up the pq
    # push the starting node into pq with cost zero
    pq = []
    heapq.heappush(pq, (0, start_node))
    # print(pq)

    # set up the parent hash table
    parents = {}

    # set up the processed set
    processed = set()

    # the core Dijkstra loop starts here
    # Step 1 find the cheapest node in the queue and explore its neighbor

    while pq:
        # retrieve the node
        cost, node = heapq.heappop(pq)

        for neighbor in graph[node]:
            # calculate the new cost to this neighbor
            if (neighbor[0], neighbor[1]) not in processed:
                new_cost = cost + neighbor[2]

                # if the new cost is lower than current best cost. Update the current best cost
                if new_cost < costs[(neighbor[0], neighbor[1])]:
                    costs[(neighbor[0], neighbor[1])] = new_cost

                    # put the neighbor into the pq
                    heapq.heappush(pq, (new_cost, (neighbor[0], neighbor[1])))

                    # update parent table
                    parents[(neighbor[0], neighbor[1])] = node

        # add this node to the processed set
        processed.add(node)

    # draw cost map
    drawCostMap(costs, index)

    # set up a double ended queue

    # test a destination node
    path = deque()
    path = findPath(path, parents, start_node, end_node)

    # Draw the path
    drawPath(image, path, index)

    return path


def drawPath(image, path, index):

    path_tile = Image.open(BASE_DIR / "images/path.png")

    for node in path:
        x = node[0] * tile_size_x
        y = node[1] * tile_size_y
        image.paste(path_tile, (x, y))

    image.save(f"Path_{index}.png")


def drawCostMap(costs, index):
    # let plot!
    fig, ax = plt.subplots(figsize=(15, 15))

    # find the max cost to properly set up the color scale
    max_cost = max(value for value in costs.values() if value != math.inf)

    # make a color map
    cmap = plt.cm.coolwarm

    # draw every cell

    for y in range(grid_size_y):
        for x in range(grid_size_x):
            value = costs[(x, y)]

            # Convert cost to 0~1 for the colormap
            if value == math.inf:
                color = "gray"
            else:
                normalized = value / max_cost
                color = cmap(normalized)

            # Rectangle
            rect = Rectangle((x, y), 1, 1, facecolor=color, edgecolor="black")
            ax.add_patch(rect)

            # Number in center
            if value != math.inf:
                ax.text(
                    x + 0.5, y + 0.5, str(value), ha="center", va="center", fontsize=4
                )
            else:
                ax.text(x + 0.5, y + 0.5, "∞", ha="center", va="center", fontsize=4)

    # Make cells square
    ax.set_aspect("equal")

    # Set the boundaries
    ax.set_xlim(0, grid_size_x)
    ax.set_ylim(0, grid_size_y)

    # Remove axes/ticks
    ax.axis("off")
    # Top left be origin
    ax.invert_yaxis()

    # Save
    plt.savefig(f"cell_cost_map_{index}.png", dpi=300, bbox_inches="tight")


# drawWeightMap
def drawWeightMap(horizontal_weight, vertical_weight, index):

    fig, ax = plt.subplots(figsize=(15, 15))

    # 1. Draw nodes
    x = []
    y = []

    for row in range(50):
        for col in range(50):
            x.append(col)
            y.append(row)

    ax.scatter(x, y, color="black", s=15, zorder=5)

    # 2. Create edges and collect weights
    segments = []
    weights = []

    # Horizontal edges
    for row in range(50):
        for col in range(49):
            weight = horizontal_weight[row][col]

            segments.append([(col, row), (col + 1, row)])

            weights.append(weight)

            ax.text(col + 0.5, row, str(weight), ha="center", va="center", fontsize=5)

    # Vertical edges
    for row in range(49):
        for col in range(50):
            weight = vertical_weight[row][col]

            segments.append([(col, row), (col, row + 1)])

            weights.append(weight)

            ax.text(col, row + 0.5, str(weight), ha="center", va="center", fontsize=5)

    # 3. Weight → color
    norm = mpl.colors.Normalize(vmin=min(weights), vmax=max(weights))

    cmap = plt.cm.coolwarm
    colors = cmap(norm(weights))

    # 4. Weight → line width
    linewidths = [0.5 + weight * 0.05 for weight in weights]

    # 5. Draw all edges
    edge_collection = LineCollection(segments, colors=colors, linewidths=linewidths)

    ax.add_collection(edge_collection)

    # 6. Appearance
    ax.set_aspect("equal")
    ax.set_xlim(-1, 50)
    ax.set_ylim(50, -1)

    ax.set_xticks([])
    ax.set_yticks([])

    plt.tight_layout()
    plt.savefig(f"edge_weight_map_{index}.png", dpi=200)


# output map
image = Image.new("RGB", (grid_size_x * tile_size_x, grid_size_y * tile_size_y))
# draw level map
BASE_DIR = Path(__file__).parent

# left and right edge nodes count
left_edge_node_counts = 3
right_edge_node_counts = 3

# Sample start node, end node as well all other dead-end node
left_edge_node_y = random.sample(range(grid_size_y - 1), left_edge_node_counts)
left_edge_nodes = [(0, y) for y in left_edge_node_y]

right_edge_node_y = random.sample(range(grid_size_y - 1), right_edge_node_counts)
right_edge_nodes = [(grid_size_x - 1, y) for y in right_edge_node_y]


# specify the number of main path connecting start and end
connection_counts = 3

paths: list[list] = []

for i, left_node in enumerate(left_edge_nodes):
    for j, right_node in enumerate(right_edge_nodes):
        paths.append(list(dijkstraSearch(left_node, right_node, image, f"{i}{j}")))


# let's get a set of all pathway cells
pathway_cells = set()

for path in paths:
    pathway_cells.update(path)

# now draw the wall cells
all_cells = {(x, y) for x in range(grid_size_x) for y in range(grid_size_y)}

wall_cells = all_cells - pathway_cells

wall_tile = Image.open(BASE_DIR / "images/wall.png")

for cell in wall_cells:
    x = cell[0] * tile_size_x
    y = cell[1] * tile_size_y
    image.paste(wall_tile, (x, y))


# let's draw the start and the end cell
start_node = paths[0][0]
end_node = paths[0][-1]

start_tile = Image.open(BASE_DIR / "images/start.png").convert("RGBA")
end_tile = Image.open(BASE_DIR / "images/end.png").convert("RGBA")
image.paste(
    start_tile, (start_node[0] * tile_size_x, start_node[1] * tile_size_y), start_tile
)
image.paste(end_tile, (end_node[0] * tile_size_x, end_node[1] * tile_size_y), end_tile)


# now let's draw the treasure boxes. They are scattered at the edges. Some are guarded.
# get all left and right edge nodes into one set
all_edge_nodes = set(left_edge_nodes + right_edge_nodes)
# remove the start and end node from the set
all_edge_nodes.discard(start_node)
all_edge_nodes.discard(end_node)
# now this is a suitable set for locations for treasures
nodes_for_treasure = all_edge_nodes

print(f"Nodes for treasure {nodes_for_treasure}")

print(f"Here is all the paths {paths}")


treasure_node_table = {}
# ok let's make a hash table where the keys are the starting and ending node of each path and the values are the nodes list of that path
for path in paths:
    treasure_node_table[path[0]] = path
    treasure_node_table[path[-1]] = path[::-1]

print(f"Treasure node table {treasure_node_table}")

# generate a random permutation of for all nodes for treasue placement
treasure_placement_list = random.sample(
    list(nodes_for_treasure), len(nodes_for_treasure)
)

# make the first two for placing a treasure and a monster guarding them.
treasure_monster_nodes = treasure_placement_list[:2]
treasure_only_nodes = treasure_placement_list[2:]

print(f"treasure monster node {treasure_monster_nodes}")


# set up images to use
monster1_tile = Image.open(BASE_DIR / "images/monster1.png").convert("RGBA")
monster2_tile = Image.open(BASE_DIR / "images/monster2.png").convert("RGBA")
monster3_tile = Image.open(BASE_DIR / "images/monster3.png").convert("RGBA")
monster4_tile = Image.open(BASE_DIR / "images/monster4.png").convert("RGBA")

monster_list = [monster1_tile, monster2_tile, monster3_tile, monster4_tile]

treasure_box_tile = Image.open(BASE_DIR / "images/treasurebox.png").convert("RGBA")

# starting placing treasure boxes and guarding monsters
for node in treasure_monster_nodes:
    # place the monster in the next node after the treasure position
    monster_node = treasure_node_table[node][1]

    # place treasure box at node
    image.paste(
        treasure_box_tile,
        (node[0] * tile_size_x, node[1] * tile_size_y),
        treasure_box_tile,
    )

    # place monster next to the treasure
    chosen_monster_tile = random.choice(monster_list)
    image.paste(
        chosen_monster_tile,
        (monster_node[0] * tile_size_x, monster_node[1] * tile_size_y),
        chosen_monster_tile,
    )

for node in treasure_only_nodes:
    # place treasure box at node
    image.paste(
        treasure_box_tile,
        (node[0] * tile_size_x, node[1] * tile_size_y),
        treasure_box_tile,
    )


# The final piece is to put in random monsters and potions on the pathways that are not immediately close to the left and right edge nodes

# first we need a set of all nodes on the all pathways
all_pathway_nodes = set()

for path in paths:
    all_pathway_nodes.update(path)

# set up a frame inside the grid. Only nodes inside this frame will be eligible for placing monsters and potions in this phase
# frame has 5 grid cell padding
delta_x = 5
delta_y = delta_x


frame_nodes = set(
    filter(
        lambda node: (
            (node[0] > delta_x and node[0] < grid_size_x - 1 - delta_x)
            and (node[1] > delta_y and node[1] < grid_size_y - 1 - delta_y)
        ),
        all_pathway_nodes,
    )
)

nodes_to_place = random.sample(list(frame_nodes), len(frame_nodes) // 10)

monster5_tile = Image.open(BASE_DIR / "images/monster5.png").convert("RGBA")
monster6_tile = Image.open(BASE_DIR / "images/monster6.png").convert("RGBA")
monster7_tile = Image.open(BASE_DIR / "images/monster7.png").convert("RGBA")
monster8_tile = Image.open(BASE_DIR / "images/monster8.png").convert("RGBA")
manapotion_tile = Image.open(BASE_DIR / "images/manapotion.png").convert("RGBA")
healthpotion_tile = Image.open(BASE_DIR / "images/healthpotion.png").convert("RGBA")

# item list to pick from
item_list = [
    monster5_tile,
    monster6_tile,
    monster7_tile,
    monster8_tile,
    manapotion_tile,
    healthpotion_tile,
]

# draw nodes
for node in nodes_to_place:
    tile = random.choice(item_list)
    image.paste(
        tile,
        (node[0] * tile_size_x, node[1] * tile_size_y),
        tile,
    )

image.save("generatedMap.png")
print(len(paths))
