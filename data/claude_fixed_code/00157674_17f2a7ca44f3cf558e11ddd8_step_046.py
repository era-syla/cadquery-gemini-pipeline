import cadquery as cq

# ------------------------------------------------------------------
# Parameters (Defaulting to an M6 x 25mm Socket Head Cap Screw)
# ------------------------------------------------------------------
major_dia = 6.0          # Major diameter of the screw (M6)
pitch = 1.0              # Thread pitch
total_length = 25.0      # Length of the shaft
head_dia = 10.0          # Diameter of the head
head_height = 6.0        # Height of the head
hex_size = 5.0           # Size of the hex key (across flats)
hex_depth = 3.5          # Depth of the hex socket
thread_length = 22.0     # Length of the threaded portion

# Derived Dimensions
# Calculate core diameter (approximate for modeling)
# Standard ISO thread depth is roughly 0.61 * pitch, so major - 1.22*pitch
# For visual clarity and robust union, we use slightly simpler math.
tooth_height = 0.55 * pitch
core_radius = (major_dia / 2.0) - tooth_height

# ------------------------------------------------------------------
# 1. Create the Head
# ------------------------------------------------------------------
# Build from the XY plane upwards
result = (
    cq.Workplane("XY")
    .circle(head_dia / 2.0)
    .extrude(head_height)
    # Cut the Hexagonal Socket
    .faces(">Z")
    .workplane()
    .polygon(6, hex_size)
    .cutBlind(-hex_depth)
    # Add a chamfer to the top edge of the head
    .faces(">Z")
    .edges()
    .chamfer(0.5)
)

# ------------------------------------------------------------------
# 2. Create the Shaft Core
# ------------------------------------------------------------------
# Extrude from the bottom of the head downwards
# Selecting the bottom face (<Z) sets the workplane normal to -Z
# So a positive extrude distance goes downwards in global space
result = (
    result.faces("<Z")
    .workplane()
    .circle(core_radius)
    .extrude(total_length)
)

# ------------------------------------------------------------------
# 3. Generate Helical Threads
# ------------------------------------------------------------------
# To make a robust thread, we sweep a profile along a helix
# and union it to the core shaft.

# A. Create the Helix Path
# We generate a helix wire centered on the Z axis.
helix_wire = cq.Wire.makeHelix(
    pitch=pitch,
    height=thread_length,
    radius=core_radius
)

# B. Position the Helix
# The screw shaft goes from Z=0 to Z=-25.
# Threads should end at the tip (-25) and go up.
# Calculate the center Z position for the helix to align it correctly.
# Center of shaft threaded area = -(total_length - thread_length/2)
helix_center_z = -(total_length - thread_length / 2.0)
helix_path = helix_wire.translate(cq.Vector(0, 0, helix_center_z))

# C. Create the Thread Profile
# We define a trapezoidal profile (ISO style) on the XZ plane.
# This profile must be positioned at the start of the helix.
# Based on makeHelix defaults, the start is at angle 0.
z_start = helix_center_z - (thread_length / 2.0)

# Profile dimensions
root_width = 0.75 * pitch  # Width at base
tip_width = 0.15 * pitch   # Width at tip

# Points for the trapezoid (Counter-Clockwise)
# Drawn relative to the start point (core_radius, 0, z_start)
p1 = (core_radius, z_start - root_width/2)
p2 = (core_radius + tooth_height, z_start - tip_width/2)
p3 = (core_radius + tooth_height, z_start + tip_width/2)
p4 = (core_radius, z_start + root_width/2)

profile_wire = (
    cq.Workplane("XZ")
    .polyline([p1, p2, p3, p4])
    .close()
    .vals()[0]
)

# D. Sweep the Profile
# isFrenet=True ensures the profile rotates correctly with the helix
thread_solid = (
    cq.Workplane("XY")
    .add(profile_wire)
    .sweep(helix_path, isFrenet=True)
)

# ------------------------------------------------------------------
# 4. Final Assembly
# ------------------------------------------------------------------
# Union the threads to the main body
result = result.union(thread_solid)

# Add a chamfer to the tip of the screw (bottom-most edges)
result = result.faces("<Z").edges().chamfer(0.75)