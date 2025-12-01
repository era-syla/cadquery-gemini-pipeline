import cadquery as cq
import math

# Parameters for the socket model
socket_od = 24.0          # Outer diameter of the top cylindrical part
socket_height = 20.0      # Height of the top cylindrical part
drive_od = 14.0           # Outer diameter of the bottom cylindrical part
drive_height = 12.0       # Height of the bottom cylindrical part
hex_across_flats = 15.0   # Size of the hex opening (flat-to-flat)
hex_depth = 12.0          # Depth of the hex pocket

# Calculate the circumscribed diameter of the hexagon for the polygon function
# Relation: Across_Flats = Circum_Diameter * cos(30 degrees)
# Therefore: Circum_Diameter = Across_Flats / (sqrt(3) / 2)
hex_circum_diameter = hex_across_flats / (math.sqrt(3) / 2.0)

# Construct the geometry
result = (
    cq.Workplane("XY")
    # 1. Create the bottom cylinder (drive shaft)
    .circle(drive_od / 2.0)
    .extrude(drive_height)
    
    # 2. Create the top cylinder on top of the bottom one
    .faces(">Z")
    .workplane()
    .circle(socket_od / 2.0)
    .extrude(socket_height)
    
    # 3. Cut the hexagonal socket into the top face
    .faces(">Z")
    .workplane()
    .polygon(6, hex_circum_diameter)
    .cutBlind(-hex_depth)
)