import cadquery as cq

# Parameters derived from image analysis
height = 60.0       # Total height of the object
width = 40.0        # Total width across flanges
depth = 25.0        # Depth (extrusion length)
web_thickness = 12.0
flange_thickness = 12.0
fillet_radius = 6.0 # Radius of the fillet between web and flanges
top_sag = 3.5       # Depth of the concave curve on the top surface

# 1. Create the base block
# We start with a rectangular block extruded along the Y-axis.
# Using both=True creates the object centered on the origin in Y.
result = cq.Workplane("XZ").rect(width, height).extrude(depth, both=True)

# 2. Create the I-beam profile (Side Cuts)
# Calculate dimensions for the rectangular cutouts on the left and right
cutout_w = (width - web_thickness) / 2.0
cutout_h = height - 2 * flange_thickness
# Offset center of cutouts from X origin
cutout_offset_x = (web_thickness + cutout_w) / 2.0

# Perform the cuts on the side to shape the web and flanges
# We select the front face (>Y), draw the cutouts, and cut through the entire depth
result = (
    result.faces(">Y")
    .workplane()
    .pushPoints([(-cutout_offset_x, 0), (cutout_offset_x, 0)])
    .rect(cutout_w, cutout_h)
    .cutThruAll()
)

# 3. Add Fillets
# Fillet the vertical internal edges where the web meets the flanges.
# We select edges parallel to Y (|Y) and filter for the inner ones 
# (those whose X coordinate is closer to 0 than the outer width).
result = result.edges("|Y").fillet(fillet_radius)

# 4. Top Surface Concave Cut
# The top surface is curved downwards (saddle shape). 
# This corresponds to subtracting a large cylinder with an axis parallel to X.
# Calculate the radius of the cylinder based on the chord (depth) and the sag height.
# Formula: R = (chord^2 + 4*sag^2) / (8*sag)
R_top = (depth**2 + 4 * top_sag**2) / (8 * top_sag)

# Calculate the center position of the cutter cylinder.
# We want the lowest point of the cylinder to be at (height/2 - top_sag).
# Center_Z - R = height/2 - top_sag  =>  Center_Z = height/2 + R - top_sag
cut_center_z = height / 2.0 + R_top - top_sag

# Create the cutter tool
# A cylinder oriented along the X-axis (created on YZ plane and extruded)
cutter = (
    cq.Workplane("YZ")
    .center(0, cut_center_z)
    .circle(R_top)
    .extrude(width * 2, both=True) # Make sure it covers the full width
)

# Subtract the cylinder from the main body
result = result.cut(cutter)