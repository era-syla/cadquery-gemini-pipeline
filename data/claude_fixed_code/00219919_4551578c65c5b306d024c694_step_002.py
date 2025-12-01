import cadquery as cq

# --- Parameters ---
length = 500.0         # Total length of the strut channel
width = 41.3           # Standard width (approx 1-5/8")
depth = 41.3           # Standard depth (approx 1-5/8")
thickness = 2.5        # Wall thickness
lip_width = 7.0        # Width of the inturned lips
lip_return = 6.0       # Depth of the lip return
hole_diam = 11.0       # Diameter of the mounting holes
hole_spacing = 45.0    # Spacing between holes in a pair
end_margin = 35.0      # Distance from end to first hole

# --- 1. Define the Profile ---
# The profile is a "C" shape with inward curving lips (Strut channel).
# We draw this on the XY plane.
# Origin (0,0) is placed at the center of the back outer face.
# - X axis: Width
# - Y axis: Depth
pts = [
    # Start bottom-left outer corner
    (-width/2, 0),
    # Top-left outer corner
    (-width/2, depth),
    # Top-left lip outer edge
    (-width/2 + lip_width, depth),
    # Top-left lip return (downward)
    (-width/2 + lip_width, depth - lip_return),
    # -- Inner Profile --
    # Top-left lip inner return
    (-width/2 + lip_width - thickness, depth - lip_return),
    # Top-left lip inner horizontal
    (-width/2 + lip_width - thickness, depth - thickness),
    # Inner side wall (left)
    (-width/2 + thickness, depth - thickness),
    # Inner back floor
    (-width/2 + thickness, thickness),
    # Inner side wall (right)
    (width/2 - thickness, thickness),
    # Inner side wall (right) top
    (width/2 - thickness, depth - thickness),
    # Top-right lip inner horizontal
    (width/2 - lip_width + thickness, depth - thickness),
    # Top-right lip inner return
    (width/2 - lip_width + thickness, depth - lip_return),
    # -- Outer Profile --
    # Top-right lip return
    (width/2 - lip_width, depth - lip_return),
    # Top-right lip outer edge
    (width/2 - lip_width, depth),
    # Top-right outer corner
    (width/2, depth),
    # Bottom-right outer corner
    (width/2, 0),
    # Close the loop
    (-width/2, 0)
]

# --- 2. Create the Channel Body ---
# Extrude the profile along the Z axis to create the beam
result = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(length)
)

# --- 3. Cut Holes ---
# Holes are located on the back face (the face at Y=0).
# We calculate hole Z-positions for two pairs at the top and bottom.
z_positions = [
    end_margin, 
    end_margin + hole_spacing, 
    length - end_margin - hole_spacing, 
    length - end_margin
]

# We create a cutting tool. 
# We work on the XZ plane (which corresponds to Y=0).
# We create circles at the specified (x, z) coordinates and extrude them 
# along the +Y axis to cut through the back wall.
cutter = (
    cq.Workplane("XZ")
    .transformed(offset=cq.Vector(-5.0, 0, 0))
    .pushPoints([(0, z) for z in z_positions])
    .circle(hole_diam / 2)
    .extrude(thickness + 10.0)
)

# Apply the cut
result = result.cut(cutter)