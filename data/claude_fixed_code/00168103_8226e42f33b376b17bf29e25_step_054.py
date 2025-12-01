import cadquery as cq
from math import cos, sin, pi

# --- Parameters ---
# Estimated based on visual proportions of the ring image
od = 25.0             # Outer Diameter
id_minor = 17.0       # Inner Diameter (Minor diameter of thread)
height = 12.0         # Height of the ring
pitch = 1.5           # Thread pitch
thread_depth = 1.0    # Depth of the cut (Standard metric is approx 0.6*pitch, exaggerated slightly for visual)
chamfer_size = 0.8    # Size of the top inner chamfer

# --- 1. Base Geometry ---
# Create the main cylinder and cut the central hole
result = (
    cq.Workplane("XY")
    .circle(od / 2.0)
    .circle(id_minor / 2.0)
    .extrude(height)
)

# --- 2. Chamfer ---
# Apply a chamfer to the top inner edge before threading
result = (
    result
    .faces(">Z")
    .edges("<R")
    .chamfer(chamfer_size)
)

# --- 3. Internal Threading ---
# To create the threads, we generate a helical path and sweep a triangular profile along it.

# Parametric function for the helix curve
def helix(t):
    # t ranges from 0 to 1
    # Extend the path slightly above and below the solid to ensure a clean cut
    extension = pitch * 1.5
    total_h = height + 2 * extension
    
    # Calculate current Z height
    z = (t * total_h) - extension
    
    # Calculate angle (Total vertical travel / pitch = number of turns)
    turns = total_h / pitch
    angle = 2 * pi * turns * t
    
    # Helix radius matches the inner hole surface
    r = id_minor / 2.0
    
    x = r * cos(angle)
    y = r * sin(angle)
    return (x, y, z)

# Generate the path wire (High N for smooth curve)
path = cq.Workplane("XY").parametricCurve(helix, N=400)

# Calculate parameters to define the profile plane at the start of the helix (t=0)
# Start position
extension = pitch * 1.5
total_h = height + 2 * extension
start_pt = (id_minor / 2.0, 0, -extension)

# Tangent vector at t=0
# dx/dt = 0 (since sin(0)=0), so the tangent lies in the YZ plane.
# We construct a vector aligned with the helix slope.
turns = total_h / pitch
dy = (id_minor / 2.0) * 2 * pi * turns
dz = total_h
tangent = (0, dy, dz)

# Define a plane at the start point, with normal aligned to the tangent.
# We set xDir=(1,0,0) so the local X-axis points radially outward (into the material).
profile_plane = cq.Plane(origin=start_pt, normal=tangent, xDir=(1, 0, 0))

# Draw the triangular cutter profile on this plane
# Shape: Triangle pointing into the wall (+X direction in local coords)
thread_profile = (
    cq.Workplane(profile_plane)
    .moveTo(0, 0)                        # Start at surface of hole
    .lineTo(thread_depth, pitch / 2.3)   # Top corner of triangle
    .lineTo(thread_depth, -pitch / 2.3)  # Bottom corner of triangle
    .close()
)

# Sweep the profile along the path to create the thread solid
# isFrenet=True keeps the profile properly oriented along the 3D curve
thread_cut_solid = thread_profile.sweep(path, isFrenet=True)

# Subtract the thread solid from the main body
result = result.cut(thread_cut_solid)