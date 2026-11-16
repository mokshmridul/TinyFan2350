# TinyFan2350 DIN rail tray for 2x Voron Trident PCB DIN clips.
# Run with CadQuery 2.x:  python3 TinyFan2350_DIN_mount.py  -> writes .step and .stl
# Coordinates: X/Y = PCB outline (Y up, origin at the PCB corner on the clip-latch edge), Z = up from the clip face.
# GPL-3.0, part of https://github.com/mokshmridul/TinyFan2350
import cadquery as cq
# ---- parameters (mm) ----
BW,BH=93.0,63.0            # PCB outline
HOLE=[(9.5,4.5),(88.5,4.5),(9.5,58.5),(88.5,58.5)]   # PCB M3 holes (mount coords, Y up)
T=3.0                      # base plate thickness
SO=7.0                     # standoff height above plate (clearance for THT leads)
SO_D=8.5; INS_D=4.3; INS_DEP=6.0     # M3 heat-set insert (Robu M3x4, 4.8 OD)
RIM=5.0
CLIPS=[21.5,71.5]          # clip centre X positions
CLIP_Y=(20.1,62.1)         # clip top-face footprint along Y (+0.2 clearance)
CLIP_W=10.4
POCKET=0.5
SCREW_Y=[23.69,55.19]      # clip pilot holes (31.5 mm apart)
PAD_W=14.0; PAD_H=2.0      # raised screw pads on top of the plate
# ---- base ----
m=cq.Workplane('XY').box(BW,BH,T,centered=False).edges('|Z').fillet(3.0)
# vent windows
for (x0,x1,y0,y1) in [(31,62,RIM,BH/2-2.5),(31,62,BH/2+2.5,BH-RIM)]:
    m=m.cut(cq.Workplane('XY').box(x1-x0,y1-y0,T,centered=False).translate((x0,y0,0)).edges('|Z').fillet(2.0))
# raised pads over the clips
for xc in CLIPS:
    m=m.union(cq.Workplane('XY').box(PAD_W,min(CLIP_Y[1]+2,BH)-(CLIP_Y[0]-2),PAD_H,centered=False).translate((xc-PAD_W/2,CLIP_Y[0]-2,T)).edges('|Z').fillet(2.0))
# standoffs
for (x,y) in HOLE:
    m=m.union(cq.Workplane('XY').circle(SO_D/2).extrude(SO).translate((x,y,T)))
    m=m.cut(cq.Workplane('XY').circle(INS_D/2).extrude(INS_DEP).translate((x,y,T+SO-INS_DEP)))
# clip locating pockets + screw holes
for xc in CLIPS:
    m=m.cut(cq.Workplane('XY').box(CLIP_W,CLIP_Y[1]-CLIP_Y[0],POCKET,centered=False).translate((xc-CLIP_W/2,CLIP_Y[0],0)))
    for y in SCREW_Y:
        m=m.cut(cq.Workplane('XY').circle(1.2).extrude(T+PAD_H).translate((xc,y,0)))      # M2 clearance
        m=m.cut(cq.Workplane('XY').circle(2.2).extrude(1.6).translate((xc,y,T+PAD_H-1.6)))  # head seat
cq.exporters.export(m,'TinyFan2350_DIN_mount.step'); cq.exporters.export(m,'TinyFan2350_DIN_mount.stl',tolerance=0.02,angularTolerance=0.1)
bb=m.val().BoundingBox(); print('bbox',bb.xmin,bb.ymin,bb.zmin,bb.xmax,bb.ymax,bb.zmax,'vol',round(m.val().Volume(),1),'valid',m.val().isValid())
