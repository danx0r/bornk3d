import sys, time, os
from xml.dom import minidom

def fix(n):
    return "%8.6f" % n

name = sys.argv[1]
fmodel = name + "/models/" + name + ".mesh.xml"
print >> sys.stderr, "model:", fmodel

x = minidom.parse(fmodel)

mesh = x.getElementsByTagName("mesh")[0]
submeshes = x.getElementsByTagName("submeshes")[0]
submesh = submeshes.getElementsByTagName("submesh")[0]
material = submesh.getAttribute("material")
print >> sys.stderr, "material:", material
fscript = name + "/materials/scripts/" + name + ".os"
print >> sys.stderr, "script:", fscript
f=open(fscript)
lins = f.readlines()
f.close()
uvsets = {}
for i, lin in enumerate(lins):
    lin = lin.strip()
    if lin[:13]=="texture_unit ":
        unit = lin[13:]
    if ".dds" in lin and lin[:8]=="texture ":
        print >> sys.stderr, "  texture unit:", unit
        print >> sys.stderr, "    color texture:", lin.strip()[8:]
        nxt = lins[i+1].strip()
        if nxt[:14]=="tex_coord_set ":
            uvsets[unit] = int(nxt[14])
            print >> sys.stderr, "    uv set for this texture:", uvsets[unit]
        else:
            print >> sys.stderr, "expected tex_coord_set..."
            0/0
uvset = uvsets["Diffuse"]
print >> sys.stderr, "capturing Diffuse uvset (" + str(uvset) + ")"

faces = submesh.getElementsByTagName("faces")[0]
geometry = submesh.getElementsByTagName("geometry")[0]
vertexcount = int(geometry.getAttribute("vertexcount"))
vertexbuffer = geometry.getElementsByTagName("vertexbuffer")[0]
verts = vertexbuffer.getElementsByTagName("vertex")
positions = []
normals = []
uvs = []

for v in verts:
    pos = v.getElementsByTagName("position")[0]
    norm = v.getElementsByTagName("normal")[0]
    uv = v.getElementsByTagName("texcoord")[uvset]
    px = pos.getAttribute("x")
    py = pos.getAttribute("y")
    pz = pos.getAttribute("z")
    nx = norm.getAttribute("x")
    ny = norm.getAttribute("y")
    nz = norm.getAttribute("z")
    u = uv.getAttribute("u")
    v = uv.getAttribute("v")
    positions += [float(px), float(py), float(pz)]
    normals += [float(nx), float(ny), float(nz)]
    uvs += [float(u), float(v)]

indices = []
triangles = faces.getElementsByTagName("face")
for t in triangles:
    v1 = t.getAttribute("v1")
    v2 = t.getAttribute("v2")
    v3 = t.getAttribute("v3")
    indices += [int(v1), int(v2), int(v3)]

##print "positions:", positions
##print "normals:", normals
##print "uvs:", uvs
##print "indices:", indices

print '<mesh id="' + name + '">'
print "<positions>",
for i, p in enumerate(positions):
    if i==len(positions)-1:
        print fix(p),
    else:
        print fix(p) + ",",
print "</positions>"
print "<normals>",
for i, n in enumerate(normals):
    if i==len(normals)-1:
        print fix(n),
    else:
        print fix(n) + ",",
print "</normals>"
print "<uv1>",
for i, j in enumerate(uvs):
    if i==len(uvs)-1:
        print fix(j),
    else:
        print fix(j) + ",",
print "</uv1>"
print "<faces>",
for i, j in enumerate(indices):
    if i==len(indices)-1:
        print j,
    else:
        print str(j) + ",",
print "</faces>"
print "</mesh>"

