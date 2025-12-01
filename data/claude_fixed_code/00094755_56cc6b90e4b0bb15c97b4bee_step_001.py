import cadquery as cq

# Dimensions
base_len = 45.0
base_width = 30.0
base_height = 6.0
base_fillet_r = 3.0

cyl_radius = 12.0
cyl_height = 20.0

hump_len = 30.0
hump_width = 18.0
hump_height = 16.0  # Total height from bottom
hump_fillet_r = 14.0 # Radius for the top slope

arch_width = 10.0
arch_straight_h = 4.0
arch_floor_z = base_height

# 1. Create the Cylinder (Right side feature)
# Positioned at origin (0,0,0)
cylinder = cq.Workplane("XY").circle(cyl_radius).extrude(cyl_height)

# 2. Create the Base Plate (Left side feature)
# Extends to the left (negative X) from the cylinder
# Center X is calculated to ensure overlap with cylinder
base_center_x = -base_len / 2.0 + 5
base = (cq.Workplane("XY")
        .workplane(offset=base_height / 2.0)
        .center(base_center_x, 0)
        .box(base_len, base_width, base_height)
        )

# Fillet the far left corners of the base
base = base.edges("|Z").fillet(base_fillet_r)

# 3. Create the Hump (Raised middle section)
# Sits on top of the base
# We calculate height relative to the base top surface
hump_rel_height = hump_height - base_height
hump_center_x = -hump_len / 2.0

hump = (cq.Workplane("XY")
        .workplane(offset=base_height)
        .center(hump_center_x, 0)
        .box(hump_len, hump_width, hump_rel_height)
        )

# Create the curved slope on the top of the hump
# We fillet the top edge at the far left (negative X) end
# The radius creates the smooth transition visible in the image
hump = hump.edges(">Z and <X").fillet(hump_rel_height - 0.1)

# 4. Create the Arch Cutout
# This is a tunnel cut through the hump along the Y axis
# We define the U-shaped profile on the XZ plane
cutter = (cq.Workplane("XZ")
          .center(hump_center_x, arch_floor_z)
          .moveTo(-arch_width / 2.0, 0)
          .lineTo(-arch_width / 2.0, arch_straight_h)
          .threePointArc((0, arch_straight_h + arch_width / 2.0), 
                         (arch_width / 2.0, arch_straight_h))
          .lineTo(arch_width / 2.0, 0)
          .close()
          .extrude(hump_width * 2, both=True) # Cut through both sides
          )

# 5. Combine all parts
# Union the solids and then cut the arch
result = cylinder.union(base).union(hump).cut(cutter)

# Optional: Add a small chamfer to the top of the cylinder for detail
result = result.edges(">Z").chamfer(0.5)