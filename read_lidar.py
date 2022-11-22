import laspy
import open3d as o3d
import numpy as np
las = laspy.read(“data/lidar.las”)
buildings = laspy.create(point_format=las.header.point_format, file_version=las.header.version)
buildings.points = las.points[las.classification == 6]
buildings.write(‘buildings.las’)
geom = o3d.geometry.PointCloud()
geom.points = o3d.utility.Vector3dVector(point_data)
o3d.visualization.draw_geometries([geom])