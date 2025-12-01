import cadquery as cq

# Object Parameters
width = 80.0        # Total width along X axis
depth = 40.0        # Total thickness along Y axis
height = 60.0       # Total height along Z axis
rail_width = 20.0   # Width of the vertical side legs
web_thickness = 10.0 # Thickness of the central connecting web
notch_height = 20.0 # Height of the rectangular notches on the sides
notch_depth = 10.0  # Depth of the rectangular notches
hole_diameter = 15.0 # Diameter of the central through-hole

# Calculated Parameters
# Width of the central channel to be removed
recess_width = width - (2 * rail_width)
# Depth of the cut required on front and back to leave the web thickness
cut_depth = (depth - web_thickness) / 2.0

# Construction
result = (
    cq.Workplane("XY")
    .box(width, depth, height) # Start with a solid block
    
    # 1. Create the H-profile by cutting the central channel from the Front (>Y)
    .faces(">Y").workplane()
    .center(0, 0)
    .rect(recess_width, height)
    .cutBlind(-cut_depth)
    
    # 2. Cut the central channel from the Back (<Y)
    .faces("<Y").workplane()
    .center(0, 0)
    .rect(recess_width, height)
    .cutBlind(-cut_depth)
    
    # 3. Create the rectangular notch on the Right side (>X)
    .faces(">X").workplane()
    .center(0, 0)
    # Rectangle width is set larger than depth to ensure it cuts through the entire side face
    .rect(depth * 1.5, notch_height) 
    .cutBlind(-notch_depth)
    
    # 4. Create the rectangular notch on the Left side (<X)
    .faces("<X").workplane()
    .center(0, 0)
    .rect(depth * 1.5, notch_height)
    .cutBlind(-notch_depth)
)

# 5. Create the central through-hole
# Using a new workplane on XZ plane ensures exact centering
result = (
    result
    .faces(">Y").workplane(centerOption="CenterOfBoundBox")
    .center(0, 0)
    .circle(hole_diameter / 2.0)
    .cutThruAll()
)