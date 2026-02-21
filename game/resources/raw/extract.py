import xml.etree.ElementTree as ET

NS = {"t": "http://www.w3.org/1999/xhtml"}

tree = ET.parse("map.tmx")
root = tree.getroot()

layer = root.find(".//t:layer[@name='BG1']", NS)
if layer is None:
    raise RuntimeError("BG1 layer not found")

data = layer.find("t:data", NS)
if data is None:
    raise RuntimeError("BG1 data node not found")

tiles = data.findall("t:tile", NS)

SRC_W = 77
DST_W = 48
H = 14

lines = []

for y in range(H):
    start = y * SRC_W
    row = tiles[start:start + DST_W]
    line = ",".join(str(int(t.attrib["gid"])) for t in row)
    lines.append(line)

with open("bg1_48x14.txt", "w", newline="\n") as f:
    for i, l in enumerate(lines):
        if i < H - 1:
            f.write(l + ",\n")
        else:
            f.write(l)

print("bg1_48x14.txt written successfully")
