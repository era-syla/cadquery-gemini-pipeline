import cadquery as cq

# Parameters derived from visual estimation
cyl_radius = 6.0         # Radius of the two main cylinders
cyl_height = 24.0        # Height of the vertical columns
base_height = 4.0        # Thickness of the connecting base
center_dist = 18.0       # Distance between the centers of the two columns
hole_diam = 5.0          # Diameter of the hole in the right cylinder
slot_width = 3.0         # Width of the slot cut into the left cylinder

# 1. Create the Base
# The base is the hull of two circles positioned at the centers of the features
base = (
    cq.Workplane("XY")
    .circle(cyl_radius)
    .workplane(offset=0)
    .center(center_dist, 0)
    .circle(cyl_radius)
    .consolidateWires()
    .extrude(base_height)
)

# 2. Add the Vertical Columns
# We extrude two circles from the top face of the base
columns = (
    base.faces(">Z")
    .workplane()
    .pushPoints([(0, 0), (center_dist, 0)])
    .circle(cyl_radius)
    .extrude(cyl_height)
)

# 3. Cut the Slot in the Left Cylinder
# The slot is located at (0,0). We align it along the X-axis (connecting the centers).
# We cut downwards from the top of the columns to the top of the base.
# Dimensions: Length must exceed diameter, Width determines the gap size.
with_slot = (
    columns.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(cyl_radius * 2.5, slot_width)
    .cutBlind(-cyl_height)
)

# 4. Cut the Hole in the Right Cylinder
# A through-hole centered at the right column (center_dist, 0).
# cutThruAll() ensures it goes through the base as well.
result = (
    with_slot.faces(">Z")
    .workplane()
    .center(center_dist, 0)
    .circle(hole_diam / 2.0)
    .cutThruAll()
)