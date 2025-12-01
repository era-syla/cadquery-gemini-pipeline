import cadquery as cq

# Dimensions estimated from visual analysis
base_diameter = 40.0
base_height = 10.0
tooth_diameter = 8.0
num_teeth = 12
hub_diameter = 24.0
hub_height = 5.0
hole_diameter = 10.0

# 1. Create the base cylinder
# Start on the XY plane and extrude the main disk
result = cq.Workplane("XY").circle(base_diameter / 2.0).extrude(base_height)

# 2. Create the teeth (lobes)
# Create teeth using a loop for polar array
import math
for i in range(num_teeth):
    angle = (360.0 / num_teeth) * i
    angle_rad = math.radians(angle)
    x = (base_diameter / 2.0) * math.cos(angle_rad)
    y = (base_diameter / 2.0) * math.sin(angle_rad)
    tooth = cq.Workplane("XY").center(x, y).circle(tooth_diameter / 2.0).extrude(base_height)
    result = result.union(tooth)

# 4. Create the top hub
# Select the top face of the current object to sketch the hub
result = (
    result.faces(">Z")
    .workplane()
    .circle(hub_diameter / 2.0)
    .extrude(hub_height)
)

# 5. Create the central through-hole
# Cut a hole through the entire assembly
result = (
    cq.Workplane("XY")
    .circle(hole_diameter / 2.0)
    .extrude(base_height + hub_height)
)

result = (
    cq.Workplane("XY").circle(base_diameter / 2.0).extrude(base_height)
)

import math
for i in range(num_teeth):
    angle = (360.0 / num_teeth) * i
    angle_rad = math.radians(angle)
    x = (base_diameter / 2.0) * math.cos(angle_rad)
    y = (base_diameter / 2.0) * math.sin(angle_rad)
    tooth = cq.Workplane("XY").center(x, y).circle(tooth_diameter / 2.0).extrude(base_height)
    result = result.union(tooth)

result = (
    result.faces(">Z")
    .workplane()
    .circle(hub_diameter / 2.0)
    .extrude(hub_height)
)

result = result.faces(">Z").workplane().hole(hole_diameter, base_height + hub_height)