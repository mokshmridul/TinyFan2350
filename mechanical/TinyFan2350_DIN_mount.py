# TinyFan2350 DIN rail tray for 1x Voron Trident PCB DIN clip.
# The board's long side (89 mm) sits across the rail, so the rail runs along the board's short side (Y).
# Run with CadQuery 2.x:  python3 TinyFan2350_DIN_mount.py  -> writes .step and .stl
# Coordinates: X/Y = PCB outline (Y up, origin at a PCB corner), Z = up from the clip face.
# GPL-3.0, part of https://github.com/mokshmridul/TinyFan2350
import cadquery as cq
# ---- parameters (mm) ----
BW,BH=89.0,58.1           # PCB outline
HOLE=[(3.5,3.5),(85.5,3.5),(3.5,54.6),(85.5,54.6)]   # PCB M3 holes (mount coords, Y up)
T=3.0                      # base plate thickness
SO=7.0                     # standoff height above plate (clearance for THT leads)
SO_D=8.5; INS_D=4.3; INS_DEP=6.0     # M3 heat-set insert (Robu M3x4, 4.8 OD)
RIM=5.0
CY=BH/2                    # clip centre line along the rail (board centre)
CX=BW/2-10.0               # clip top-face centre; the latch reaches 20 mm further in +X, so the whole clip is centred under the tray
CLIP_L=42.0                # clip top-face length along X, across the rail (+0.2 clearance)
CLIP_W=10.4                # clip width along Y, along the rail
POCKET=0.5
SCREW_X=[CX+17.41,CX-14.09]  # clip pilot holes (31.5 mm apart)
PAD_W=14.0; PAD_H=2.0      # raised screw pad on top of the plate
# ---- base ----
m=cq.Workplane('XY').box(BW,BH,T,centered=False).edges('|Z').fillet(3.0)
# vent windows (two each side of the clip pad)
ya,yb=CY-PAD_W/2-2.5,CY+PAD_W/2+2.5
for (x0,x1) in [(12.0,BW/2-3.0),(BW/2+3.0,BW-12.0)]:
    for (y0,y1) in [(RIM,ya),(yb,BH-RIM)]:
        m=m.cut(cq.Workplane('XY').box(x1-x0,y1-y0,T,centered=False).translate((x0,y0,0)).edges('|Z').fillet(2.0))
# raised pad over the clip
m=m.union(cq.Workplane('XY').box(CLIP_L+4,PAD_W,PAD_H,centered=False).translate((CX-CLIP_L/2-2,CY-PAD_W/2,T)).edges('|Z').fillet(2.0))
# standoffs
for (x,y) in HOLE:
    m=m.union(cq.Workplane('XY').circle(SO_D/2).extrude(SO).translate((x,y,T)))
    m=m.cut(cq.Workplane('XY').circle(INS_D/2).extrude(INS_DEP).translate((x,y,T+SO-INS_DEP)))
# clip locating pocket + screw holes
m=m.cut(cq.Workplane('XY').box(CLIP_L,CLIP_W,POCKET,centered=False).translate((CX-CLIP_L/2,CY-CLIP_W/2,0)))
for x in SCREW_X:
    m=m.cut(cq.Workplane('XY').circle(1.2).extrude(T+PAD_H).translate((x,CY,0)))      # M2 clearance
    m=m.cut(cq.Workplane('XY').circle(2.2).extrude(1.6).translate((x,CY,T+PAD_H-1.6)))  # head seat
cq.exporters.export(m,'TinyFan2350_DIN_mount.step'); cq.exporters.export(m,'TinyFan2350_DIN_mount.stl',tolerance=0.02,angularTolerance=0.1)
bb=m.val().BoundingBox(); print('bbox',bb.xmin,bb.ymin,bb.zmin,bb.xmax,bb.ymax,bb.zmax,'vol',round(m.val().Volume(),1),'valid',m.val().isValid())
