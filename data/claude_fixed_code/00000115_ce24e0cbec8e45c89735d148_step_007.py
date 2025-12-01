import cadquery as cq
import math

part_diameter = 50.0
part_height = 12.0
base_thickness = 4.0
fin_pitch = 3.0
fin_gap_width = 1.5
center_recess_diameter = 20.0
center_recess_depth = 5.0
center_hole_diameter = 6.0
mount_hole_diameter = 4.0
mount_cbore_diameter = 9.0
mount_pcd = 36.0

result = cq.Workplane("XY").circle(part_diameter / 2.0).extrude(part_height)

fin_cut_height = part_height - base_thickness
num_slots = int(part_diameter / fin_pitch) + 2

for i in range(-num_slots // 2, num_slots // 2 + 1):
    y_pos = i * fin_pitch + (fin_pitch / 2.0)
    result = result.faces(">Z").workplane().center(0, y_pos).rect(part_diameter + 10.0, fin_gap_width).cutBlind(-fin_cut_height)

result = result.faces(">Z").workplane().circle(center_recess_diameter / 2.0).cutBlind(-center_recess_depth)

coord_offset = (mount_pcd / 2.0) * math.cos(math.radians(45))
mount_locations = [
    (coord_offset, coord_offset),
    (coord_offset, -coord_offset),
    (-coord_offset, coord_offset),
    (-coord_offset, -coord_offset)
]

result = result.faces(">Z").workplane().pushPoints(mount_locations).cboreHole(
    mount_hole_diameter, 
    mount_cbore_diameter, 
    fin_cut_height
)

result = result.faces(">Z").workplane().hole(center_hole_diameter)