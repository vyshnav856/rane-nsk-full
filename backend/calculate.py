import numpy as np 
from stl import mesh
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull

def save_xy_plane(file_path):
	stl_mesh = mesh.Mesh.from_file(file_path)

	vertices = stl_mesh.vectors

	# Flatten vertices and calculate depth
	flattened_vertices = vertices.reshape(-1, 3)
	depths = flattened_vertices[:, 2]

	# Plot the 2D view
	plt.figure(figsize=(8, 6))
	plt.scatter(flattened_vertices[:, 0], flattened_vertices[:, 1], c=depths, cmap='viridis', s=1)
	plt.xlabel('X')
	plt.ylabel('Y')
	plt.title('2D View of STL Model (XY Plane)')
	plt.gca().set_aspect('equal', adjustable='box')
	
	filename = "xy-plane.png"
	plt.savefig(filename)
	return filename

def save_yz_plane(file_path):
	# Load the STL file
	stl_mesh = mesh.Mesh.from_file(file_path)

	# Extract vertices
	vertices = stl_mesh.vectors

	# Flatten vertices and calculate depth
	flattened_vertices = vertices.reshape(-1, 3)
	depths = flattened_vertices[:, 0]

	# Plot the 2D view on the YZ plane
	plt.figure(figsize=(8, 6))
	plt.scatter(flattened_vertices[:, 1], flattened_vertices[:, 2], c=depths, cmap='viridis', s=1)
	plt.xlabel('Y')
	plt.ylabel('Z')
	plt.title('2D View of STL Model (YZ Plane)')
	plt.gca().set_aspect('equal', adjustable='box')
	
	filename = "yz-plane.png"
	plt.savefig(filename)
	return filename

def save_xz_plane(file_path):
	# Load the STL file
	stl_mesh = mesh.Mesh.from_file(file_path)

	# Extract vertices
	vertices = stl_mesh.vectors

	# Flatten vertices and calculate depth
	flattened_vertices = vertices.reshape(-1, 3)
	depths = flattened_vertices[:, 1]

	# Plot the 2D view on the XZ plane
	plt.figure(figsize=(8, 6))
	plt.scatter(flattened_vertices[:, 0], flattened_vertices[:, 2], c=depths, cmap='viridis', s=1)
	plt.xlabel('X')
	plt.ylabel('Z')
	plt.title('2D View of STL Model (XZ Plane)')
	plt.gca().set_aspect('equal', adjustable='box')
	
	filename = "xz-plane.png"
	plt.savefig(filename)
	return filename

def calculate_cross_section_area(file_path):
	# Load the STL file
	stl_mesh = mesh.Mesh.from_file(file_path)

	# Extract vertices
	vertices = stl_mesh.vectors

	# Flatten vertices
	flattened_vertices = vertices.reshape(-1, 3)

	# Calculate cross-sectional areas on XY, YZ, and XZ planes
	xy_area = np.ptp(flattened_vertices[:, 0]) * np.ptp(flattened_vertices[:, 1])
	yz_area = np.ptp(flattened_vertices[:, 1]) * np.ptp(flattened_vertices[:, 2])
	xz_area = np.ptp(flattened_vertices[:, 0]) * np.ptp(flattened_vertices[:, 2])

	return xy_area, yz_area, xz_area

def visualize_xy_plane(file_path):
	stl_mesh = mesh.Mesh.from_file(file_path)

	vertices = stl_mesh.vectors

	# Flatten vertices and calculate depth
	flattened_vertices = vertices.reshape(-1, 3)
	depths = flattened_vertices[:, 2]

	# Plot the 2D view
	plt.figure(figsize=(8, 6))
	plt.scatter(flattened_vertices[:, 0], flattened_vertices[:, 1], c=depths, cmap='viridis', s=1)
	plt.xlabel('X')
	plt.ylabel('Y')
	plt.title('2D View of STL Model (XY Plane)')
	plt.gca().set_aspect('equal', adjustable='box')
	return plt

def visualize_yz_plane(file_path):
	# Load the STL file
	stl_mesh = mesh.Mesh.from_file(file_path)

	# Extract vertices
	vertices = stl_mesh.vectors

	# Flatten vertices and calculate depth
	flattened_vertices = vertices.reshape(-1, 3)
	depths = flattened_vertices[:, 0]

	# Plot the 2D view on the YZ plane
	plt.figure(figsize=(8, 6))
	plt.scatter(flattened_vertices[:, 1], flattened_vertices[:, 2], c=depths, cmap='viridis', s=1)
	plt.xlabel('Y')
	plt.ylabel('Z')
	plt.title('2D View of STL Model (YZ Plane)')
	plt.gca().set_aspect('equal', adjustable='box')
	return plt

def visualize_xz_plane(file_path):
	# Load the STL file
	stl_mesh = mesh.Mesh.from_file(file_path)

	# Extract vertices 
	vertices = stl_mesh.vectors

	# Flatten vertices and calculate depth
	flattened_vertices = vertices.reshape(-1, 3)
	depths = flattened_vertices[:, 1]

	# Plot the 2D view on the XZ plane
	plt.figure(figsize=(8, 6))
	plt.scatter(flattened_vertices[:, 0], flattened_vertices[:, 2], c=depths, cmap='viridis', s=1)
	plt.xlabel('X')
	plt.ylabel('Z')
	plt.title('2D View of STL Model (XZ Plane)')
	plt.gca().set_aspect('equal', adjustable='box')
	return plt

x_dim = 10 
y_dim = 100
z_dim = 20

x_min = 0
x_max = 10
y_min = 0
y_max = 100
z_min = 0
z_max = 20

def get_nodes_image(plane, direction, stl_file, num_nodes):
	longitudinal_distance = direction
	x_nodes = ""
	y_nodes = ""
	z_nodes = ""
	node_distance = ""

	if plane == 'xy':
		visualize_xy_plane(stl_file)

		if longitudinal_distance == 'x':
			node_distance = x_dim / (num_nodes)
		else:
			node_distance = y_dim / (num_nodes)

		if longitudinal_distance == 'x':
			x_nodes = np.arange(x_min, x_max, node_distance)
			y_nodes = np.full_like(x_nodes, (y_max + y_min) / 2)  # Place nodes at the middle of the y-axis
			z_nodes = np.full_like(x_nodes, (z_max + z_min) / 2)  # Place nodes at the middle of the z-axis
		elif longitudinal_distance == 'y':
			y_nodes = np.arange(y_min, y_max, node_distance)
			x_nodes = np.full_like(y_nodes, (x_max + x_min) / 2)  # Place nodes at the middle of the x-axis
			z_nodes = np.full_like(y_nodes, (z_max + z_min) / 2)  # Place nodes at the middle of the z-axis

	elif plane == 'yz':
		visualize_yz_plane(stl_file)

		if longitudinal_distance == 'y':
			node_distance = y_dim / (num_nodes)
		else:
			node_distance = z_dim / (num_nodes)
		
		if longitudinal_distance == 'z':
			z_nodes = np.arange(z_min, z_max, node_distance)
			y_nodes = np.full_like(z_nodes, (y_max + y_min) / 2)  # Place nodes at the middle of the y-axis
			x_nodes = np.full_like(z_nodes, (x_max + x_min) / 2)  # Place nodes at the middle of the z-axis
		elif longitudinal_distance == 'y':
			y_nodes = np.arange(y_min, y_max, node_distance)
			x_nodes = np.full_like(y_nodes, (x_max + x_min) / 2)  # Place nodes at the middle of the x-axis
			z_nodes = np.full_like(y_nodes, (z_max + z_min) / 2)  # Place nodes at the middle of the z-axis

	elif plane == 'xz':
		visualize_xz_plane(stl_file)

		if longitudinal_distance == 'x':
			node_distance = x_dim / (num_nodes)
		else:
			node_distance = z_dim / (num_nodes)
		
		if longitudinal_distance == 'z':
			z_nodes = np.arange(z_min, z_max, node_distance)
			y_nodes = np.full_like(z_nodes, (y_max + y_min) / 2)  # Place nodes at the middle of the y-axis
			x_nodes = np.full_like(z_nodes, (x_max + x_min) / 2)  # Place nodes at the middle of the z-axis
		elif longitudinal_distance == 'x':
			x_nodes = np.arange(x_min, x_max, node_distance)
			y_nodes = np.full_like(x_nodes, (y_max + y_min) / 2)  # Place nodes at the middle of the y-axis
			z_nodes = np.full_like(x_nodes, (z_max + z_min) / 2)  # Place nodes at the middle of the z-axis

	plt.scatter(x_nodes, y_nodes, z_nodes, color='red', marker='X')
	# print("\n\n\n\n\n", node_distance)
	# print("\n\n\n\n\n")
	plt.savefig("nodes.png")