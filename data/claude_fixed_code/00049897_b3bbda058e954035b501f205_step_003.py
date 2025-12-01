import cadquery as cq

# Geometric parameters estimated from the image
cube_size = 50.0          # Size of the cube sides
hole_diameter = 20.0      # Diameter of the through holes
chamfer_size = 1.5        # Size of the chamfer on the hole edges

# 1. Create the base cube
# We create a box centered on the XY plane.
result = cq.Workplane("XY").box(cube_size, cube_size, cube_size)

# 2. Create the intersecting holes
# We select the faces on the positive Z, X, and Y axes.
# We create a workplane on each face and drill a hole.
# The hole() method automatically cuts through the part material.
result = (
    result
    .faces(">Z").workplane().hole(hole_diameter)
    .faces(">X").workplane().hole(hole_diameter)
    .faces(">Y").workplane().hole(hole_diameter)
)

# 3. Apply Chamfers
# The image shows chamfers on the rims of the holes.
# We select edges using the ">Z or >X or >Y" selector to get edges on outer faces
# and filter by type Circle to get hole edges
result = result.edges("|Z or |X or |Y").edges("%Circle").chamfer(chamfer_size)