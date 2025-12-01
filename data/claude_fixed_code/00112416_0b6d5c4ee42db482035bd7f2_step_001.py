import cadquery as cq

# Parametric dimensions
height = 80
width = 20
depth = 20
tube_outer_diameter = 25
tube_inner_diameter = 15
flange_diameter = 40
flange_thickness = 10
hole_diameter = 6


# Create the base rectangular prism
base = cq.Workplane("XY").box(width, depth, height)

# Create the bottom flange
bottom_flange = (
    cq.Workplane("XY")
    .workplane(offset=height / 4 - flange_thickness / 2)
    .circle(flange_diameter / 2)
    .extrude(flange_thickness)
)

# Cut a hole through the bottom flange
bottom_flange = bottom_flange.faces(">Z").workplane().circle(tube_inner_diameter / 2).cutThruAll()

# Add the bottom flange to the base
base = base.union(bottom_flange)


# Cut holes in bottom flange
hole_distance = flange_diameter / 2 * 0.8
base = (
    base.faces("<Z")
    .workplane()
    .moveTo(hole_distance, 0)
    .hole(hole_diameter)
    .moveTo(-2 * hole_distance, 0)
    .hole(hole_diameter)
)


# Create the top tube
top_tube = (
    cq.Workplane("XY")
    .workplane(offset=height / 2 + flange_thickness / 2)
    .circle(tube_outer_diameter / 2)
    .extrude(height / 4)
)

# Cut a hole through the top tube
top_tube = top_tube.faces(">Z").workplane().circle(tube_inner_diameter / 2).cutThruAll()

# Add the top tube to the base
base = base.union(top_tube)

#Create top flange
top_flange = (
    cq.Workplane("XY")
    .workplane(offset=height * 0.75 - flange_thickness / 2)
    .circle(flange_diameter / 2)
    .extrude(flange_thickness)
)

# Cut a hole through the top flange
top_flange = top_flange.faces(">Z").workplane().circle(tube_inner_diameter / 2).cutThruAll()

# Add the top flange to the base
base = base.union(top_flange)

# Create the circular protrusion
protrusion_diameter = 8
protrusion_offset = 15

protrusion = (
    cq.Workplane("YZ")
    .workplane(offset=height / 2 + protrusion_offset)
    .moveTo(0,width/2)
    .circle(protrusion_diameter/2)
    .extrude(depth/2)
)

# Add the protrusion to the base
base = base.union(protrusion)

# Create support
support_diameter = 4
support_offset = 7

support = (
    cq.Workplane("XZ")
    .workplane(offset=height / 2 + support_offset)
    .moveTo(width/2, tube_outer_diameter*0.75)
    .circle(support_diameter/2)
    .extrude(depth/5)
)

# Add the support to the base
base = base.union(support)

# Cut a slot in flange
slot = (
    cq.Workplane("XZ")
    .workplane(offset=height * 0.75)
    .center(width/2, -flange_thickness/2)
    .rect(6, 4)
    .extrude(flange_thickness)
)

# Subtract the slot
base = base.cut(slot)


result = base