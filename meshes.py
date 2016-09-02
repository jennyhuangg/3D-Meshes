"""
HW3: 3D Meshes
Comp 630 W'16 - Computer Graphics
Phillips Academy
2015-1-8

By Jenny Huang
"""

from gfx_helper_mayavi import *

def main():
  """
  Plots several 3D shapes in different octants of space.
  """
  fig = setUpFigure()

  (cubeVerts, cubeTris) = cube()
  (ellVerts, ellTris) = ell()
  (prismVerts, prismTris) = prism(5)
  (cylinderVerts, cylinderTris) = prism(12)
  (sphereVerts, sphereTris) = sphere(6)
  (torusVerts, torusTris) = torus(4)

  drawTriMesh(cubeVerts + np.array([[2.5, 2.5, 2.5]]).T, cubeTris, fig,
       edges=True, normals=True)
  drawTriMesh(ellVerts + np.array([[-2.5, 2.5, 2.5]]).T, ellTris, fig,
       edges=True, normals=True)
  drawTriMesh(prismVerts + np.array([[-2.5, -2.5, 2.5]]).T, prismTris, fig,
       edges=True, normals=True)
  drawTriMesh(cylinderVerts + np.array([[2.5, -2.5, 2.5]]).T, cylinderTris, fig,
       edges=True, normals=True)
  drawTriMesh(sphereVerts + np.array([[2.5, 2.5, -2.5]]).T, sphereTris, fig,
       edges=True, normals=True)
  drawTriMesh(torusVerts + np.array([[-2.5, 2.5, -2.5]]).T, torusTris, fig,
       edges=True, normals=True)

  showFigure(fig)

  fig2 = setUpFigure()
  (jhuangVerts, jhuangTris) = jhuang_shape(4)
  drawTriMesh(jhuangVerts, jhuangTris, fig2, edges=True, normals=True)
  showFigure(fig2)


def cube():
  """
  Returns a 2-tuple (verts, tris) representing a triangle mesh of the surface
of a "unit cube".  verts is 3x8 and tris is 12x3.  See cubeVerts().
  """
  tris = np.array([[0,1,2],
                   [0,2,3],
                   [5,6,1],
                   [6,2,1],
                   [4,6,5],
                   [7,6,4],
                   [0,7,4],
                   [0,3,7],
                   [5,1,4],
                   [1,0,4],
                   [2,6,3],
                   [3,6,7]])
  return (cubeVerts(), tris)


def cubeVerts():
  """
  Returns a 3x8 array of the eight vertices of the "unit cube".  In analogy with
the unit circle, it has "radius" 1 --- that is, the edges all have length 2.
  """
  return np.array([[ 1, 1, 1],
                   [-1, 1, 1],
                   [-1,-1, 1],
                   [ 1,-1, 1],
                   [ 1, 1,-1],
                   [-1, 1,-1],
                   [-1,-1,-1],
                   [ 1,-1,-1]]).T

def ell():
  """
  Returns a 2-tuple (verts, tris) representing a triangle mesh of the surface of
an L shape.  verts is 3x12 and tris is 20x3.  See ellVerts().
  """
  tris = np.array([[0,1,2],
                   [0,2,3],
                   [0,3,4],
                   [0,4,5],
                   [8,7,6],
                   [9,8,6],
                   [10,9,6],
                   [11,10,6],
                   [7,8,1],
                   [8,2,1],
                   [9,2,8],
                   [3,2,9],
                   [4,9,10],
                   [3,9,4],
                   [10,11,4],
                   [4,11,5],
                   [5,11,6],
                   [5,6,0],
                   [6,7,1],
                   [6,1,0]])
  return (ellVerts(), tris)


def ellVerts():
  """
  Returns a 3x12 array of the 12 vertices of an L shape, like three cubes
attached to each other.  The edge length of each cube is 1, the whole shape is
centered on the origin, and the L lies parallel to the X-Y plane.
  """
  L = np.array([[ 0, 0, 0.5],
                [ 0, 1, 0.5],
                [-1, 1, 0.5],
                [-1,-1, 0.5],
                [ 1,-1, 0.5],
                [ 1, 0, 0.5]]).T
  return np.concatenate((L, L + np.array([[0,0,-1]]).T), 1)


def prism(K):
  """
  Returns a 2-tuple (verts, tris) representing a triangle mesh of the surface
of a regular K-gon prism.  verts is 3x(2K) and tris is (4K-4)x3.  See
prismVerts().
  """
  top = np.fliplr(fanDiskTriangles(K,0))
  bottom = fanDiskTriangles(K,K)

  sideBot = np.arange(K)
  sideTop = np.arange(K) + K
  preSide = triangleStrip(sideBot, sideTop)
  lastTris = np.array([[2*K-1,K-1,0],[K,2*K-1, 0]])
  side = np.concatenate((preSide, lastTris),0)

  tris = np.concatenate((top, bottom, side), 0)
  return (prismVerts(K), tris)


def prismVerts(K):
  """
  Returns a 3x(2K) array representing vertices of a regular K-gon prism.  The
prism is centered on the origin, has height 2 along an axis parallel to the Y-
axis, and has "radius" 1: all the vertices are a distance 1 from this axis.  The
points (1,1,0) and (1,-1,0) should always be vertices of the prism.
  """
  cap = np.concatenate((
      [np.cos(np.linspace(0, 2*np.pi, K, False))],
      np.ones((1,K)),
      [np.sin(np.linspace(0, 2*np.pi, K, False))]
    ), 0);
  return np.concatenate((cap, cap + np.array([[0,-2,0]]).T), 1)


def sphere(K):
  """
  Returns a 2-tuple (verts, tris) representing a triangle mesh of the surface of
a unit sphere.  verts is 3x(2 + (K+1)(K+3)) and tris is ((2K+2)(K+3))x3.  See
sphereVerts().
  """

  # Top and Bottom of sphere.
  bottom = wheelDiskTriangles(K+3)
  top = np.fliplr(wheelDiskTriangles(K+3, 1+ (K+1)*(K+3), (K+1)*(K+3) -(K+1)-1))

  # Create triangle strip based on top and bottom arrays.
  t = (np.arange(K*(K+3)+1)+1)%(2 + (K+1)*(K+3))
  b = (np.arange(K*(K+3)+1) + K+3 + 1)%(2 + (K+1)*(K+3))
  sides = triangleStrip(b,t)

  # Adjust so the triangles are consistent with the spherical cycle.
  sides = sides[:-1]
  last = (np.array([[K+3, K+4, 1]]))
  sides = np.concatenate((last, sides),0)

  # Combine all together.
  tris = np.concatenate((bottom, sides, top), 0)
  return (sphereVerts(K), tris)


def sphereVerts(K):
  """
  Returns a 3x(2 + (K+1)(K+3)) array representing vertices on the surface of the
unit sphere, centered at the origin.  The sampling on the sphere follows a
"latitude/longitude" pattern: there are K+1 lines of latitude, and K+3 lines of
longitude, equally distributed around the sphere.  There's one vertex at each
pole (2 verts total), plus one more at each lat/lon intersection (that's
(K+1)(K+3) additional verts).
  The north and south poles are at (0,1,0) and (0,-1,0), respectively, and the
"prime meridian" (which should always be included) runs between the poles
through the point (1,0,0).  (This means that your sphere should always include
at least K+3 points whose Z-coordinate is 0 and whose X-coordinate is
non-negative: the poles, plus the K+1 vertices along the prime meridian.)
  """
  grid_XZ = (
      np.concatenate((
        np.cos(np.linspace(0, 2*np.pi, K+3, False))[None, :, None],
        np.sin(np.linspace(0, 2*np.pi, K+3, False))[None, :, None]), 2) *
      np.cos(np.linspace(-np.pi/2, np.pi/2, K+2, False))[1:, None, None]
    ).reshape((-1,2))
  grid_Y = (
      np.ones((1, K+3, 1)) *
      np.sin(np.linspace(-np.pi/2, np.pi/2, K+2, False))[1:, None, None]
    ).reshape((-1,1))
  grid = np.concatenate((grid_XZ[:,0,None], grid_Y, grid_XZ[:,1,None]), 1)
  return np.concatenate(([[0,-1,0]], grid, [[0,1,0]]), 0).T


def torus(K):
  """
  Returns a 2-tuple (verts, tris) representing a triangle mesh of the surface of
a torus.  verts is 3x((K+3)^2) and tris is (2(K+3)^2)x3.  See torusVerts().
  """
  t = (np.arange((K+3)**2+1))%((K+3)**2)
  b = (np.arange((K+3)**2+1) + K+3)%((K+3)**2)
  tris = triangleStrip(b, t)
  return (torusVerts(K), tris)


def torusVerts(K):
  """
  Returns a 3x((K+3)^2) array representing vertices on the surface of a torus
lying parallel to the X-Y plane, centered at the origin.  The overall diameter
is 2, and the diameter of the inner hole is 2/3.  The point (1,0,0) should
always be included --- this is the intersection of two circles, other points on
which should also be included in the torus surface.  One circle is the unit
circle in the X-Y plane, and the other is perpendicular to it, in the X-Z plane,
with radius 1/3.
  """
  wand = np.concatenate((
      (np.cos(np.linspace(0, 2*np.pi, K+3, False))[None, :, None] + 2)/3,
      (np.cos(np.linspace(0, 2*np.pi, K+3, False))[None, :, None] + 2)/3,
      np.sin(np.linspace(0, 2*np.pi, K+3, False))[None, :, None]/3
    ), 2)
  sweep = np.concatenate((
      np.cos(np.linspace(0, 2*np.pi, K+3, False))[:, None, None],
      np.sin(np.linspace(0, 2*np.pi, K+3, False))[:, None, None],
      np.ones((K+3, 1, 1))
    ), 2)
  return (wand * sweep).reshape((-1,3)).T

def jhuang_shape(K):
  """
  Returns a 2-tuple (verts, tris) representing a triangle mesh of the surface of
a J shape.  verts is 3x(2K+14) and tris is (4K+16)x3.  See jhuang_verts().
  """
  # Triangles for straight edge sections.
  edges = np.array([[0,1,6],
                   [6,1,5],
                   [1,2,3],
                   [1,3,4],
                   [7,0,6],
                   [7,8,0],
                   [0,8,1],
                   [8,9,1],
                   [9,2,1],
                   [2,9,10],
                   [2,10,3],
                   [10,11,4],
                   [3,10,4],
                   [6,5,13],
                   [13,5,12],
                   [13,12,7],
                   [7,12,8],
                   [9,8,10],
                   [8,11,10],
                   [7,6,13]])

  # Triangles for curve section.
  # Wheel that does not loop around.
  front = wheelDiskTriangles(K,1,14)[:-1]
  back = np.fliplr(wheelDiskTriangles(K, 8, K+14))[:-1]

  # Side triangle strip.
  sideBot = np.arange(K) + 14
  sideTop = np.arange(K) + K+14
  side = np.fliplr(triangleStrip(sideBot, sideTop))

  tris = np.concatenate((edges, front, back, side), 0)
  return (jhuang_verts(K), tris)


def jhuang_verts(K):
  """
  Returns a 3x(2K+14) array representing vertices on the surface of the letter
J lying parallel to the X-Y plane, centered at the origin. The shape has a
thickness of 1, height of 2, and width of 1.5. The J is made up of a quarter
cylinder at the corner with rectangular prism legs. There are K vertices that
make up the curve from the top/bottom of the quarter cylinder.
  """
  edges = np.array([[ 0.5, 1, 0.5],
                [ 0.5, -0.5, 0.5],
                [-0.5, -0.5, 0.5],
                [-0.5, -1, 0.5],
                [ 0.5, -1, 0.5],
                [ 1, -.5, 0.5],
                [1, 1, 0.5]]).T
  edges = np.concatenate((edges, edges + np.array([[0,0,-1]]).T), 1)

  # Finds equally distributed angles for quarter circle.
  angles = np.linspace(np.pi*3.0/2, 2*np.pi, K)

  # Finds respective points according to angle
  xValues = 0.5*(np.cos(angles)) + 0.5
  yValues = 0.5*np.sin(angles) - 0.5
  zValues = np.repeat([0.5],K).T
  curve = np.concatenate(([xValues], [yValues], [zValues]), 0)
  curve = np.concatenate((curve, curve + np.array([[0,0,-1]]).T), 1)

  return np.concatenate((edges, curve), 1)


def fanDiskTriangles(K, start=0, flip=False):
  """
  Returns a 3x(K-2) array of vertex indices for the triangulation of a K-polygon
in the plane, with indices numbered counterclockwise.  Arguments:
  - K: number of vertices in the polygon.
  - start (default 0): the starting index of the K consecutive indices around
      the polygon.
  - flip (default False): when False, triangles are oriented right-handed /
      counterclockwise; when True, they are left-handed / clockwise.
  """
  row1 = np.repeat(start, K-2).reshape(-1,1)
  a = np.array([start+1,start+2])
  b = np.arange(K-2).reshape(-1,1)
  tris = np.concatenate((row1, a+b), 1)
  if flip:
      tris = np.fliplr(tris)
  return tris

def wheelDiskTriangles(K, hub=0, start=1, flip=False):
  """
  Returns a 3xK array of vertex indices for the triangulation of a K-polygon
in the plane, with a central "hub" vertex and K vertices in a loop around it,
numbered counterclockwise.  Arguments:
  - K: number of vertices around the outside of the polygon.
  - hub (default 0): the index of the vertex in the middle of the disk.
  - start (default 1): the starting index of the K consecutive indices around
      the polygon.
  - flip (default False): when False, triangles are oriented right-handed /
      counterclockwise; when True, they are left-handed / clockwise.
  """
  row1 = np.repeat(hub, K-1).reshape(-1,1)
  a = np.array([start,start+1])
  b = np.arange(K-1).reshape(-1,1)
  notTris = np.concatenate((row1, a+b), 1)
  lastTri = np.array([[hub,K + start-1, start]])
  tris = np.concatenate((notTris, lastTri), 0)
  if flip:
      tris = np.fliplr(tris)
  return tris


def indexLoop(idx):
  """
  Given a 1-D array or list, returns the same as a 1-D array with element #0
repeated at the end.
  """
  return np.concatenate((idx, [idx[0]]), 0)

def triangleStrip(bot, top):
  """
  Given two 1-D arrays or lists (each of length N) of vertex indices (bot and
top), returns a 3x(2(N-1)) array of indices, each row of which is a triangle in
a zigzagging strip between these parallel sets of indices:

          0  1  2  3  4  5
  top ->  *--*--*--*--*--*
          | /| /| /| /| /|
          |/ |/ |/ |/ |/ |
  bot ->  *--*--*--*--*--*
          0  1  2  3  4  5

  The triangles are oriented so that their right-hand-rule outward directions
are all facing out of the page.
  """
  a1 = top[:-1].reshape(-1,1)
  a2 = bot[:-1].reshape(-1,1)
  a3 = top[1:].reshape(-1,1)
  b3 = bot[1:].reshape(-1,1)

  tri1 = np.concatenate((a1, a2, a3), 1)
  tri2 = np.concatenate((a3, a2, b3), 1)

  tris = np.concatenate((tri1, tri2), 0)
  return tris


# This calls main() when the program is invoked from the command line.
if __name__ == "__main__":
  main()
