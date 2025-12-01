import cadquery as cq

# Dimensions based on visual analysis
base_width = 40.0       # Width of the square base
top_diameter = 26.0     # Diameter of the top circular opening
height = 40.0           # Height of the transition
wall_thickness = 2.0    # Thickness of the walls

# Create the square-to-round transition object
result = (
    cq.Workplane("XY")
    # 1. Create the square base geometry
    .rect(base_width, base_width)
    # 2. Establish the top plane offset by the height
    .workplane(offset=height)
    # 3. Create the circular top geometry
    .circle(top_diameter / 2.0)
    # 4. Loft between the square and the circle to create the solid form
    .loft(combine=True)
    # 5. Select top and bottom faces to remove them, creating openings
    .faces(">Z or <Z")
    # 6. Shell inwards (negative thickness) to create the hollow walls
    .shell(-wall_thickness)
)