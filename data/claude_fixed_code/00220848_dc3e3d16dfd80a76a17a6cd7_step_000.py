import cadquery as cq

# Parameter definitions based on visual analysis of the geometry
base_width = 40.0       # Width of the square base plate
base_height = 40.0      # Height of the square base plate
base_thickness = 6.0    # Thickness of the base plate
boss_diameter = 25.0    # Outer diameter of the cylindrical boss
boss_length = 20.0      # Length of the boss extending from the base
hole_diameter = 15.0    # Diameter of the through-hole

# Generate the 3D object
result = (
    cq.Workplane("XY")
    # 1. Create the square base plate centered at the origin
    .box(base_width, base_height, base_thickness)
    
    # 2. Select the top face of the base to add the boss
    .faces(">Z")
    .workplane()
    
    # 3. Draw the outer circle of the boss and extrude it
    .circle(boss_diameter / 2.0)
    .extrude(boss_length)
    
    # 4. Cut a through-hole through the entire part
    .faces(">Z")
    .workplane()
    .circle(hole_diameter / 2.0)
    .cutThruAll()
)