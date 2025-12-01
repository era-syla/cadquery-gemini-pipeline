import cadquery as cq

# Dimensions
length = 80.0
width = 60.0
height = 20.0
thickness = 2.0

# Create a box and shell it to create the open container
result = (
    cq.Workplane("XY")
    .box(length, width, height)
    .faces(">Z")
    .shell(-thickness, kind="intersection")
)