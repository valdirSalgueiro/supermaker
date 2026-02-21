import xml.etree.ElementTree as ET

NS = {"t": "http://www.w3.org/1999/xhtml"}

SRC_W = 77
SRC_H = 14

PATTERN_W = 16
OUT_W = 48
OUT_H = 8
REPEAT = OUT_W // PATTERN_W  # = 3

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

for y in range(OUT_H):  # top 8 rows
    row_start = y * SRC_W
    row = tiles[row_start : row_start + SRC_W]

    # extract the 16-tile pattern (top-right)
    pattern = row[SRC_W - PATTERN_W : SRC_W]

    # repeat pattern horizontally
    out_row = pattern * REPEAT

    line = ",".join(str(int(t.attrib["gid"])) for t in out_row)
    lines.append(line)

with open("bg1_topright_repeat_48x8.txt", "w", newline="\n") as f:
    for i, l in enumerate(lines):
        if i < OUT_H - 1:
            f.write(l + ",\n")
        else:
            f.write(l)

print("bg1_topright_repeat_48x8.txt written successfully")
