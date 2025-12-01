import cadquery as cq

# --- Parametric Dimensions ---
width = 440.0         # Main chassis body width (excluding ears)
depth = 400.0         # Chassis depth
height = 88.0         # Chassis height (approx 2U)
thickness = 1.5       # Sheet metal thickness
ear_width = 25.0      # Width of rack mount ears
ear_thickness = 3.0   # Thickness of rack mount ears

# --- 1. Main Chassis Body ---
# Create the base solid block
# We orient the box such that Width=X, Depth=Y, Height=Z
result = cq.Workplane("XY").box(width, depth, height)

# Shell the box inwards to create the walls, removing the top face (+Z)
result = result.faces("+Z").shell(-thickness)

# --- 2. Rack Mounting Ears ---
# We attach flanges to the front face (at -Y)
# Create Right Ear
ear_r = (
    cq.Workplane("XZ")
    .workplane(offset=-depth/2)  # Move to front face plane
    .center(width/2 + ear_width/2, 0) # Move to right side
    .box(ear_width, ear_thickness, height) # Create ear geometry (correct order: width, depth, height in XZ plane)
)

# Create Left Ear
ear_l = (
    cq.Workplane("XZ")
    .workplane(offset=-depth/2)
    .center(-(width/2 + ear_width/2), 0)
    .box(ear_width, ear_thickness, height)
)

# Join ears to the main body
result = result.union(ear_r).union(ear_l)

# --- 3. Rack Ear Mounting Slots ---
# Add standard oval mounting slots to the ears
result = (
    result.faces("<Y").workplane()
    .pushPoints([
        (width/2 + ear_width/2, height/2 - 15),
        (width/2 + ear_width/2, -(height/2 - 15)),
        (-(width/2 + ear_width/2), height/2 - 15),
        (-(width/2 + ear_width/2), -(height/2 - 15))
    ])
    .slot2D(10, 6, 90) # Length, diameter, rotation (vertical)
    .cutThruAll()
)

# --- 4. Front Panel Cutouts ---
# Add rectangular cutouts on the left side of the front panel
result = (
    result.faces("<Y").workplane()
    .pushPoints([
        (-width/2 + 45, 20),
        (-width/2 + 45, -20)
    ])
    .rect(35, 18)
    .cutBlind(-thickness * 3) # Cut only through the front wall
)

# Add connector cutouts on the center/right of front panel
result = (
    result.faces("<Y").workplane()
    .pushPoints([(20, 0), (60, 0)])
    .rect(14, 14)
    .cutBlind(-thickness * 3)
)

# --- 5. Side Ventilation Slots ---
# Add a row of vertical slots on the right side wall (>X face)
slot_w = 3.0
slot_h = height * 0.65
slot_pitch = 8.0
# Calculate number of slots to fit the depth
num_slots = int((depth - 60) / slot_pitch)

result = (
    result.faces(">X").workplane()
    # Create linear array along the length of the face
    .rarray(1, slot_pitch, 1, num_slots)
    .rect(slot_w, slot_h)
    .cutBlind(-thickness * 3) # Cut only through the side wall
)

# --- 6. Base Mounting Holes ---
# Add a grid of mounting holes on the floor of the chassis
result = (
    result.faces("<Z").workplane()
    .rarray(100, 100, 3, 3)
    .circle(2.0) # M4 clearance hole approx
    .cutBlind(-thickness * 3)
)