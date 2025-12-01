import cadquery as cq

# --- Object Dimensions and Parameters ---
height = 50.0           # Total height of the object
diameter = 14.0         # Outer diameter
radius = diameter / 2.0
hole_diameter = 4.0     # Diameter of the center hole
chamfer_size = 0.5      # Size of the edge chamfers

# Knurling Parameters
knurl_depth = 0.4       # Depth of the grooves
num_starts = 10         # Number of helical grooves in each direction
twist_angle = 90.0      # Total rotation of the helix over the height (degrees)

# --- 1. Base Geometry ---
# Create the main cylinder centered on the XY plane
result = cq.Workplane("XY").circle(radius).extrude(height)

# Apply chamfers to the top and bottom edges before knurling
# Select edges that are not parallel to the Z axis (the circular rims)
result = result.edges("|Z").chamfer(chamfer_size)

# Create the central hole (through hole)
result = result.faces(">Z").workplane().hole(hole_diameter)

# --- 2. Knurling Tool Generation ---
# To create the knurl, we define a V-shaped cutter profile and twist-extrude it.
# We create one cutter for the clockwise (CW) direction and one for counter-clockwise (CCW).

# Extend the cutter slightly beyond the part height to ensure clean cuts at ends
cutter_ext = 5.0
cut_height = height + 2 * cutter_ext
# Adjust twist angle for the extended height to maintain constant pitch
cut_twist = twist_angle * (cut_height / height)

# Define the 2D V-shape profile for the cutter
# Positioned at Z start level, pointing towards the center
p_tip = (radius - knurl_depth, 0)       # Deepest point of the cut
p_out_top = (radius + 2.0, 1.5)         # Outer point (clear of the cylinder)
p_out_bot = (radius + 2.0, -1.5)        # Outer point

# Create the profile wire
cutter_wire = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(0, 0, -cutter_ext))
    .polyline([p_out_top, p_tip, p_out_bot])
    .close()
)

# Generate the solid helical cutters (CW and CCW)
cutter_cw = cutter_wire.twistExtrude(cut_height, cut_twist)
cutter_ccw = cutter_wire.twistExtrude(cut_height, -cut_twist)

# --- 3. Apply Knurling Pattern ---
# Rotate and subtract the cutters from the base cylinder
for i in range(num_starts):
    angle = (360.0 / num_starts) * i
    
    # Rotate the master cutters to the current angle
    c_cw = cutter_cw.rotate((0, 0, 0), (0, 0, 1), angle)
    c_ccw = cutter_ccw.rotate((0, 0, 0), (0, 0, 1), angle)
    
    # Subtract both cutters from the result
    result = result.cut(c_cw).cut(c_ccw)

# The 'result' variable now contains the final knurled object