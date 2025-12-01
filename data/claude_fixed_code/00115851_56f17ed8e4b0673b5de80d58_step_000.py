import cadquery as cq

# Base parameters
base_length = 150
base_width = 100
base_height = 10

# Support parameters
support_height = 70
support_diameter = 15
support_base_diameter = 25
support_base_height = 5

# Wheel parameters
wheel_diameter = 100
wheel_thickness = 5

# Blade parameters
blade_length = 40
blade_width = 5
blade_thickness = 2

# Axle parameters
axle_diameter = 5
axle_length = 20


# Create base
base = cq.Workplane("XY").box(base_length, base_width, base_height)

# Create support
def create_support(x_pos):
    support_base = cq.Workplane("XY").center(x_pos, base_width / 4).circle(support_base_diameter / 2).extrude(support_base_height)
    support_cylinder = cq.Workplane("XY").workplane(offset=support_base_height).center(x_pos, base_width / 4).circle(support_diameter / 2).extrude(support_height - support_base_height)
    return support_base.union(support_cylinder)

# Add supports to base
support1 = create_support(base_length / 4)
support2 = create_support(base_length * 3 / 4)

base = base.union(support1).union(support2)

# Create wheel
wheel = cq.Workplane("YZ").workplane(offset=base_length / 2).center(base_width / 4, support_height).circle(wheel_diameter / 2).extrude(wheel_thickness)

# Create blades
def create_blade(angle):
    blade = cq.Workplane("YZ").workplane(offset=base_length / 2).center(base_width / 4, support_height).rect(blade_length, blade_width).extrude(blade_thickness)
    blade = blade.rotate((base_length / 2, base_width / 4, support_height), (base_length / 2, base_width / 4, support_height + 1), angle)
    return blade

blade1 = create_blade(0)
blade2 = create_blade(90)


# Create axle
axle = cq.Workplane("YZ").workplane(offset=base_length / 2).center(base_width / 4, support_height).circle(axle_diameter / 2).extrude(axle_length)

# Combine all parts
result = base.union(wheel).union(blade1).union(blade2).union(axle)