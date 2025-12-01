import cadquery as cq

# -----------------------------------------------------------------------------
# 1. Parameters & Dimensions
# -----------------------------------------------------------------------------
# Base plate dimensions
plate_width = 100.0
plate_height = 100.0
plate_thickness = 10.0

# Mounting hole configuration
hole_diameter = 8.0
hole_margin = 15.0  # Distance from edge to hole center

# Bracket (Support) dimensions
bracket_width = 60.0
bracket_straight_length = 40.0
bracket_radius = bracket_width / 2.0
bracket_height = 60.0  # Vertical height of the bracket
wall_thickness = 5.0

# -----------------------------------------------------------------------------
# 2. Create Base Plate
# -----------------------------------------------------------------------------
# Create a rectangular plate on the YZ plane.
# Thickness will be along the X-axis. Centered at the origin.
base = cq.Workplane("YZ").box(plate_width, plate_height, plate_thickness)

# Add 4 mounting holes
# Calculate offsets from center
offset_y = (plate_width / 2) - hole_margin
offset_z = (plate_height / 2) - hole_margin

base = (
    base.faces(">X")
    .workplane()
    .pushPoints([
        (offset_y, offset_z), 
        (offset_y, -offset_z), 
        (-offset_y, offset_z), 
        (-offset_y, -offset_z)
    ])
    .hole(hole_diameter)
)

# -----------------------------------------------------------------------------
# 3. Create Bracket Structure
# -----------------------------------------------------------------------------
# We build the "plan view" profile on the XY plane and extrude it.

# Part A: Rectangular straight section
# Created at origin, then moved so it starts at X=0 and extends to X=L
rect_part = (
    cq.Workplane("XY")
    .rect(bracket_straight_length, bracket_width)
    .extrude(bracket_height, both=True)
    .translate((bracket_straight_length / 2, 0, 0))
)

# Part B: Semi-circular tip
# A circle centered at the end of the straight section
circ_part = (
    cq.Workplane("XY")
    .circle(bracket_radius)
    .extrude(bracket_height, both=True)
    .translate((bracket_straight_length, 0, 0))
)

# Combine into a single solid
bracket_solid = rect_part.union(circ_part)

# Hollow out the bracket
# We remove the front curved face (at max X) to create the open U-shape with shelves.
# A negative thickness shells inwards.
bracket_hollow = bracket_solid.faces(">X").shell(-wall_thickness)

# -----------------------------------------------------------------------------
# 4. Assembly
# -----------------------------------------------------------------------------
# The base plate's front face is at X = plate_thickness / 2.
# The bracket starts at X = 0.
# Move the bracket to attach to the face of the plate.
bracket_positioned = bracket_hollow.translate((plate_thickness / 2, 0, 0))

# Combine the base plate and the bracket into one object
result = base.union(bracket_positioned)