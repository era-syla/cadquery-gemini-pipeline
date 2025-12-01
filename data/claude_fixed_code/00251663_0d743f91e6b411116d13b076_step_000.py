import cadquery as cq

# Parametric dimensions
length = 50.0    # Dimension along X axis
width = 40.0     # Dimension along Y axis
height = 40.0    # Dimension along Z axis
hole_dia = 20.0  # Diameter of the circular hole

# Create the model
# 1. Start with a base workplane (XY)
# 2. Create a solid box centered at the origin
# 3. Select a face to drill the hole (e.g., the face along positive Y)
# 4. Initialize a new workplane on that face
# 5. Create a through-hole centered on the face
result = (
    cq.Workplane("XY")
    .box(length, width, height)
    .faces(">Y")
    .workplane()
    .hole(hole_dia, depth=length)
)