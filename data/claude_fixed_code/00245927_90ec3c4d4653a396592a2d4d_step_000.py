import cadquery as cq

# Parameters defining the object geometry
total_height = 120.0
tube_od = 20.0
wall_thickness = 1.5
tube_id = tube_od - (2 * wall_thickness)
flange_od = 26.0
flange_height = 2.0
slot_width = 6.0
slot_length = 14.0
slot_center_z = 12.0  # Height of the slot center from the bottom

# 1. Create the Base Flange
# Start with a simple disk on the XY plane
result = cq.Workplane("XY").circle(flange_od / 2.0).extrude(flange_height)

# 2. Create the Main Tube Body
# Select the top face of the base and extrude the tube cylinder
# We subtract the flange height from total height so the overall height is exact
result = result.faces(">Z").workplane().circle(tube_od / 2.0).extrude(total_height - flange_height)

# 3. Hollow out the assembly
# Select the top face of the tube and cut a bore all the way through to the bottom
# Depth is negative to cut downwards, greater than total height to ensure a clean through-hole
result = result.faces(">Z").workplane().circle(tube_id / 2.0).cutBlind(-total_height)

# 4. Create the Slot Feature
# We define a workplane parallel to the front (XZ plane), offset outwards
# so we can cut back into the tube wall.
# Offset distance ensures we start outside the tube geometry.
plane_offset = tube_od + 10.0

# Create the slot profile and cut
# Use rect instead of slot2D for the slot shape
result = (
    cq.Workplane("XZ")
    .workplane(offset=plane_offset)
    .center(0, slot_center_z)
    .rect(slot_length, slot_width)
    .cutBlind(-plane_offset)
)

result = result.union(cq.Workplane("XY").circle(flange_od / 2.0).extrude(flange_height).union(cq.Workplane("XY").workplane(offset=flange_height).circle(tube_od / 2.0).extrude(total_height - flange_height).faces(">Z").workplane().circle(tube_id / 2.0).cutBlind(-total_height)))