import cadquery as cq

# Create the top rectangular plate
# Dimensions estimated based on visual proportions: 
# Length (X) = 80, Width (Y) = 50, Thickness (Z) = 8
result = cq.Workplane("XY").box(80, 50, 8)

# Create the vertical rectangular leg
# The leg extends downwards from the center of the bottom face of the top plate.
# Leg Width (along X) = 24 (approx 1/3 of top length)
# Leg Thickness (along Y) = 10
# Leg Height (Z extrusion) = 40
result = (result.faces("<Z")
          .workplane()
          .rect(24, 10)
          .extrude(-40))