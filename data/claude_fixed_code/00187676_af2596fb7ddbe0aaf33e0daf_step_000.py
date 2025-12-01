import cadquery as cq
import math

# --- Parameters ---
# Dimensions estimated from the image
od = 60.0              # Outer Diameter of the main body
id = 54.0              # Inner Diameter (Wall thickness = 3mm)
height = 15.0          # Total height of the cap
floor_thickness = 2.0  # Thickness of the perforated bottom
rib_height = 11.0      # Height of the ribbed section (skirt)
lug_angle_width = 40.0 # Angular width of the smooth locking tabs
num_rib_slots = 36     # Total number of rib slots for a full circle pattern
slot_depth = 1.2       # Depth of the vertical rib cuts
slot_width = 2.5       # Width of the vertical rib cuts
hole_diameter = 2.5    # Diameter of holes in the bottom grid
hole_pitch = 4.0       # Center-to-center spacing of holes
num_top_notches = 12   # Number of small notches on the top rim
notch_width = 2.0      # Width of top notches
notch_depth = 3.0      # Radial depth of top notches
notch_height = 1.2     # Vertical depth of top notches

# --- 1. Base Body ---
# Create the main cylinder
result = cq.Workplane("XY").circle(od / 2.0).extrude(height)

# Hollow out the cylinder to create the cup shape
# Cut from the top face down to the floor thickness
result = result.faces(">Z").workplane().circle(id / 2.0).cutBlind(-(height - floor_thickness))

# --- 2. Outer Ribs (Grip Pattern) ---
# Calculate the locations for the vertical rib cuts.
# We create a radial pattern but skip the angles where the "Lugs" (smooth tabs) are located.
# Lugs are positioned at 0 and 180 degrees.

angle_step = 360.0 / num_rib_slots

for i in range(num_rib_slots):
    angle = i * angle_step
    norm_angle = angle % 360
    
    # Check if the current angle falls within the lug regions
    # Lug 1: Centered at 0 degrees
    in_lug_1 = (norm_angle < (lug_angle_width / 2.0)) or (norm_angle > (360.0 - lug_angle_width / 2.0))
    # Lug 2: Centered at 180 degrees
    in_lug_2 = (norm_angle > (180.0 - lug_angle_width / 2.0)) and (norm_angle < (180.0 + lug_angle_width / 2.0))
    
    if not (in_lug_1 or in_lug_2):
        # Calculate position on the outer edge
        rad = math.radians(angle)
        x = (od / 2.0) * math.cos(rad)
        y = (od / 2.0) * math.sin(rad)
        
        # Create a cutting box at this location
        cutter = (
            cq.Workplane("XY")
            .center(x, y)
            .rect(slot_depth * 2, slot_width)
            .extrude(rib_height)
        )
        result = result.cut(cutter)

# --- 3. Floor Perforations ---
# Create a grid of holes on the bottom plate
hole_points = []
grid_limit = int(od / hole_pitch)
max_r = (id / 2.0) - 1.0 # Margin to ensure holes don't cut into the wall

for i in range(-grid_limit, grid_limit + 1):
    for j in range(-grid_limit, grid_limit + 1):
        x = i * hole_pitch
        y = j * hole_pitch
        # Circular clipping for the grid
        if x**2 + y**2 < max_r**2:
            hole_points.append((x, y))

# Cut the holes
if hole_points:
    result = (
        result.faces("<Z").workplane()
        .pushPoints(hole_points)
        .circle(hole_diameter / 2.0)
        .cutBlind(floor_thickness)
    )

# --- 4. Top Rim Notches ---
# Cut small rectangular notches into the top rim
for i in range(num_top_notches):
    angle = i * (360.0 / num_top_notches)
    rad = math.radians(angle)
    x = (od / 2.0) * math.cos(rad)
    y = (od / 2.0) * math.sin(rad)
    
    result = (
        result.faces(">Z").workplane()
        .center(x, y)
        .rect(notch_depth * 2, notch_width)
        .cutBlind(-notch_height)
    )

# Return the result
# result