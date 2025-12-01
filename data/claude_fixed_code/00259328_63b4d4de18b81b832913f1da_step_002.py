import cadquery as cq

width = 120
depth = 60
height = 75
tube_width = 2
shelf_height = 25
shelf_depth = 30

# Legs
leg1 = cq.Workplane("XY").box(tube_width, tube_width, height)
leg2 = cq.Workplane("XY").box(tube_width, tube_width, height).translate((width - tube_width, 0, 0))
leg3 = cq.Workplane("XY").box(tube_width, tube_width, height).translate((0, depth - tube_width, 0))
leg4 = cq.Workplane("XY").box(tube_width, tube_width, height).translate((width - tube_width, depth - tube_width, 0))

# Horizontal supports
support1 = cq.Workplane("XY").box(width - 2*tube_width, tube_width, tube_width).translate((tube_width, 0, shelf_height))
support2 = cq.Workplane("XY").box(width - 2*tube_width, tube_width, tube_width).translate((tube_width, depth - tube_width, shelf_height))
support3 = cq.Workplane("XY").box(tube_width, depth - 2*tube_width, tube_width).translate((0, tube_width, shelf_height))
support4 = cq.Workplane("XY").box(tube_width, depth - 2*tube_width, tube_width).translate((width - tube_width, tube_width, shelf_height))
support5 = cq.Workplane("XY").box(width - 2*tube_width, tube_width, tube_width).translate((tube_width, 0, height - tube_width))
support6 = cq.Workplane("XY").box(width - 2*tube_width, tube_width, tube_width).translate((tube_width, depth - tube_width, height - tube_width))
support7 = cq.Workplane("XY").box(tube_width, depth - 2*tube_width, tube_width).translate((0, tube_width, height - tube_width))
support8 = cq.Workplane("XY").box(tube_width, depth - 2*tube_width, tube_width).translate((width - tube_width, tube_width, height - tube_width))
support9 = cq.Workplane("XY").box(width - 2*tube_width, tube_width, tube_width).translate((tube_width, depth - tube_width, height/2 - tube_width/2))

# Left side shelf supports
left_support1 = cq.Workplane("XY").box(tube_width, shelf_depth - tube_width, tube_width).translate((0, tube_width, shelf_height))
left_support2 = cq.Workplane("XY").box(tube_width, shelf_depth - tube_width, tube_width).translate((0, tube_width, 2*shelf_height - tube_width))
left_support3 = cq.Workplane("XY").box(tube_width, shelf_depth - tube_width, tube_width).translate((0, tube_width, 3*shelf_height - 2*tube_width))
left_support4 = cq.Workplane("XY").box(tube_width, shelf_depth - tube_width, tube_width).translate((0, tube_width, height - tube_width))
left_vertical_support = cq.Workplane("XY").box(tube_width, tube_width, height - tube_width - shelf_height).translate((0, shelf_depth - tube_width, shelf_height))

# Shelves
shelf1 = cq.Workplane("XY").box(width/2 - tube_width, shelf_depth - tube_width, tube_width).translate((tube_width, tube_width, shelf_height + tube_width))
shelf2 = cq.Workplane("XY").box(width/2 - tube_width, shelf_depth - tube_width, tube_width).translate((tube_width, tube_width, 2*shelf_height))

# Table Top
table_top = cq.Workplane("XY").box(width, depth, tube_width).translate((0, 0, height))

# Assemble the parts
result = leg1.union(leg2).union(leg3).union(leg4).union(support1).union(support2).union(support3).union(support4).union(support5).union(support6).union(support7).union(support8).union(support9).union(left_support1).union(left_support2).union(left_support3).union(left_support4).union(left_vertical_support).union(shelf1).union(shelf2).union(table_top)