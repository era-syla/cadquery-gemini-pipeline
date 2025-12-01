import cadquery as cq

# Parametric dimensions
board_width = 100
board_length = 65
board_thickness = 1.6

connector_height = 8
connector_width = 10
connector_depth = 5

# Create the main board
result = cq.Workplane("XY").box(board_width, board_length, board_thickness)

# Add connectors (example: two connectors)
connector1 = cq.Workplane("XY").center(board_width / 4, -board_length/2+5).box(connector_width, connector_depth, connector_height)
result = result.union(connector1.translate((0, 0, board_thickness/2 + connector_height/2)))

connector2 = cq.Workplane("XY").center(-board_width / 4, -board_length/2+5).box(connector_width, connector_depth, connector_height)
result = result.union(connector2.translate((0, 0, board_thickness/2 + connector_height/2)))

# Add the cutout on the left side
connector3 = cq.Workplane("XY").center(-board_width/2+5, board_length/2-5).box(connector_depth, connector_depth, connector_height)
result = result.union(connector3.translate((0, 0, board_thickness/2 + connector_height/2)))

cutout = cq.Workplane("YZ").center(board_length/2-connector_depth/2, 0).box(connector_depth, connector_depth, board_thickness)
result = result.cut(cutout.translate((-board_width/2, 0, 0)))