import cadquery as cq

# --- Model Parameters ---
width = 50.0            # Total width of the base (X-axis)
depth = 30.0            # Total depth of the base (Y-axis)
base_thickness = 6.0    # Thickness of the base plate
upright_height = 32.0   # Total height of the uprights from the bottom
upright_width = 8.0     # Thickness of the uprights (X dimension)
upright_depth = 14.0    # Depth of the uprights (Y dimension)
hole_diameter = 6.0     # Diameter of the holes in the uprights
slot_length = 24.0      # Length of the slot in the base
slot_width = 8.0        # Width of the slot in the base
front_radius = 8.0      # Fillet radius for the front corners
root_fillet = 3.0       # Fillet radius at the connection of uprights and base

# --- Geometry Construction ---

# 1. Create the Base Plate
# Oriented on the XY plane, centered at origin.
result = cq.Workplane("XY").box(width, depth, base_thickness)

# 2. Fillet Front Corners
# Select edges parallel to Z axis that are on the front face (+Y)
result = result.edges("|Z and >Y").fillet(front_radius)

# 3. Create Uprights
# Calculate the position for the uprights (back corners)
# Center X: Offset from center by (Width/2 - UprightWidth/2)
# Center Y: Back edge (-Depth/2) + Half Upright Depth
x_offset = width/2 - upright_width/2
y_offset = -depth/2 + upright_depth/2

# Sketch rectangles on top of the base and extrude
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([(-x_offset, y_offset), (x_offset, y_offset)])
    .rect(upright_width, upright_depth)
    .extrude(upright_height - base_thickness)
)

# 4. Round the Top of Uprights
# Fillet the top edges parallel to X to create a full round top.
# Radius is half of the upright_depth.
top_radius = upright_depth / 2.0
# Using a slightly smaller radius avoids potential geometry kernel issues with self-intersection
result = result.faces(">Z").edges("|X").fillet(top_radius - 0.01)

# 5. Cut Holes in Uprights
# Position is centered on the rounded top.
hole_z_center = upright_height - top_radius
# Cut holes at both uprights
result = (
    result.faces(">Y")
    .workplane(centerOption="CenterOfBoundBox")
    .pushPoints([(-x_offset, hole_z_center), (x_offset, hole_z_center)])
    .circle(hole_diameter / 2.0)
    .cutThruAll()
)

# 6. Cut Slot in Base
# Position the slot in the available space in front of the uprights.
# Let's position it slightly forward from the center.
slot_y_pos = 5.0
result = (
    result.faces(">Z")
    .workplane()
    .center(0, slot_y_pos)
    .slot2D(slot_length, slot_width)
    .cutBlind(-base_thickness)
)

# 7. Apply Inner Fillets (Upright to Base transition)
# Select edges at the base of the uprights on the inner side
try:
    # Select horizontal edges at the base-upright junction
    result = result.edges("|X and >Z[-2]").fillet(root_fillet)
except Exception:
    # Fallback if fillet fails
    pass