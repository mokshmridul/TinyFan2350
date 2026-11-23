"""
Regenerate all TinyFan2350 production files from the KiCad board.

Run with KiCad's bundled Python (it provides the pcbnew module):

    "C:\\Program Files\\KiCad\\10.0\\bin\\python.exe" PCB\\make_production_files.py

Outputs (PCB/ProductionFiles):
    GERBER-TinyFan2350.zip              Gerbers + Excellon drill files
    JLC-Economic-BOM-bottom.csv         JLCPCB BOM, bottom-side SMD parts only
    JLC-Economic-CPL-bottom.csv         JLCPCB CPL (pick & place), bottom-side SMD parts only
    POS-TinyFan2350.csv                 KiCad position file (all SMD parts)
"""
import csv
import os
import shutil
import subprocess
import tempfile
import zipfile
from collections import OrderedDict

import pcbnew

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.dirname(HERE)
BOARD = os.path.join(PROJECT, "TinyFan2350.kicad_pcb")
OUT = os.path.join(HERE, "ProductionFiles")
KICAD_CLI = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"

# Value -> (LCSC part, JLC library type). Checked against lcsc.com / jlcpcb.com.
LCSC = {
    "AO3400A": ("C20917", "Basic"),
    "2N7002": ("C8545", "Basic"),
    "B5819W": ("C8598", "Basic"),
    "SS54": ("C22452", "Basic"),
    "1N4148WS": ("C2128", "Basic"),
    "P6SMB6.8CA": ("C78395", "Basic"),
    "4.7k": ("C23162", "Basic"),
    "330": ("C23138", "Basic"),
    "470": ("C23179", "Basic"),
    "100nF": ("C14663", "Basic"),
}


def is_assembled_smd(fp):
    attrs = fp.GetAttributes()
    if not attrs & pcbnew.FP_SMD:
        return False
    if attrs & pcbnew.FP_EXCLUDE_FROM_POS_FILES or attrs & pcbnew.FP_EXCLUDE_FROM_BOM:
        return False
    if hasattr(fp, "IsDNP") and fp.IsDNP():
        return False
    return True


def jlc_bottom_rotation(fp):
    # JLC views bottom parts from the top: mirror the KiCad angle about the Y axis
    return (180.0 - fp.GetOrientationDegrees()) % 360.0


def main():
    os.makedirs(OUT, exist_ok=True)
    board = pcbnew.LoadBoard(BOARD)
    parts = []
    for fp in board.GetFootprints():
        if not is_assembled_smd(fp):
            continue
        if not fp.IsFlipped():
            raise SystemExit(f"{fp.GetReference()} is an SMD part on the TOP side - this board expects SMD on the bottom only")
        parts.append(fp)
    parts.sort(key=lambda f: (f.GetReference().rstrip("0123456789"), int("".join(c for c in f.GetReference() if c.isdigit()) or 0)))

    # BOM grouped by value + footprint
    groups = OrderedDict()
    missing = set()
    for fp in parts:
        key = (fp.GetValue(), fp.GetFPID().GetLibItemName().wx_str())
        groups.setdefault(key, []).append(fp.GetReference())
        if fp.GetValue() not in LCSC:
            missing.add(fp.GetValue())
    if missing:
        raise SystemExit("No LCSC number for: " + ", ".join(sorted(missing)))
    with open(os.path.join(OUT, "JLC-Economic-BOM-bottom.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Comment", "Designator", "Footprint", "LCSC Part #", "Quantity", "JLC Library"])
        for (value, footprint), refs in groups.items():
            lcsc, lib = LCSC[value]
            w.writerow([value, ",".join(refs), footprint, lcsc, len(refs), lib])

    # CPL, coordinates in the Gerber coordinate system (Y up)
    with open(os.path.join(OUT, "JLC-Economic-CPL-bottom.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Designator", "Mid X", "Mid Y", "Layer", "Rotation"])
        for fp in parts:
            pos = fp.GetPosition()
            w.writerow([fp.GetReference(), f"{pcbnew.ToMM(pos.x):.3f}mm", f"{-pcbnew.ToMM(pos.y):.3f}mm",
                        "Bottom", f"{jlc_bottom_rotation(fp):.0f}"])

    # Gerbers + drill
    tmp = tempfile.mkdtemp()
    try:
        subprocess.run([KICAD_CLI, "pcb", "export", "gerbers", "--output", tmp + os.sep, "--layers",
                        "F.Cu,B.Cu,F.Paste,B.Paste,F.Silkscreen,B.Silkscreen,F.Mask,B.Mask,Edge.Cuts",
                        "--subtract-soldermask", BOARD], check=True, capture_output=True)
        subprocess.run([KICAD_CLI, "pcb", "export", "drill", "--output", tmp + os.sep, "--format", "excellon",
                        "--excellon-separate-th", "--generate-map", "--map-format", "gerberx2", BOARD],
                       check=True, capture_output=True)
        with zipfile.ZipFile(os.path.join(OUT, "GERBER-TinyFan2350.zip"), "w", zipfile.ZIP_DEFLATED) as z:
            for name in sorted(os.listdir(tmp)):
                z.write(os.path.join(tmp, name), name)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    subprocess.run([KICAD_CLI, "pcb", "export", "pos", "--side", "both", "--format", "csv", "--units", "mm",
                    "--smd-only", "-o", os.path.join(OUT, "POS-TinyFan2350.csv"), BOARD], check=True, capture_output=True)

    extended = sorted({LCSC[v][0] for (v, _), _r in groups.items() if LCSC[v][1] == "Extended"})
    print(f"{len(parts)} bottom SMD parts in {len(groups)} BOM lines; extended parts: {len(extended)} ({', '.join(extended)})")


if __name__ == "__main__":
    main()
