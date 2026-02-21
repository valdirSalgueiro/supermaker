import xml.etree.ElementTree as ET

NS = {"t": "http://www.w3.org/1999/xhtml"}

SRC_W = 77
SRC_H = 14

OUT_W = 60
OUT_H = 14

tree = ET.parse("map.tmx")
root = tree.getroot()

layer = root.find(".//t:layer[@name='BG1']", NS)
if layer is None:
    raise RuntimeError("BG1 layer not found")

data = layer.find("t:data", NS)
if data is None:
    raise RuntimeError("BG1 data node not found")

tiles = data.findall("t:tile", NS)

if len(tiles) != SRC_W * SRC_H:
    raise RuntimeError(f"Unexpected tile count: {len(tiles)}")

lines = []

for y in range(OUT_H):
    row_start = y * SRC_W
    row = tiles[row_start : row_start + SRC_W]

    slice_ = row[:OUT_W]  # leftmost 60 columns

    line = ",".join(str(int(t.attrib["gid"])) for t in slice_)
    lines.append(line)

with open("bg1_left_60x14.txt", "w", newline="\n") as f:
    for i, l in enumerate(lines):
        if i < OUT_H - 1:
            f.write(l + ",\n")
        else:
            f.write(l)

print("bg1_left_60x14.txt written successfully")
