import cadquery as cq

# Define dimensions
height = 50.0
width = 60.0
depth = 40.0
extension_width = 30.0
extension_depth = 20.0

# Create the base block
base = cq.Workplane("XY").box(width, depth, height)

# Create the extension block
extension = cq.Workplane("XY").center(0, depth/2 + extension_depth/2).box(extension_width, extension_depth, height)

# Combine the base and extension
result = base.union(extension)

#show_object(result)