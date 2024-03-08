import numpy as np
from stl import mesh
import matplotlib.pyplot as pltd
from scipy.spatial import ConvexHull

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

# Provide the path to your STL file
stl_file = "D:/Ranensk.stl"

# Assign images to variables a, b, and c for XY, YZ, and XZ planes respectively
visualize_xy_plane(stl_file)
visualize_yz_plane(stl_file)
visualize_xz_plane(stl_file)

# Show the plots
plt.show()


# In[2]:


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

# Provide the path to your STL file
stl_file = "D:/Ranensk.stl"

# Calculate cross-sectional areas
xy_area, yz_area, xz_area = calculate_cross_section_area(stl_file)

print("Cross-sectional area on XY plane:", xy_area)
print("Cross-sectional area on YZ plane:", yz_area)
print("Cross-sectional area on XZ plane:", xz_area)


# In[3]:




x_dim = 10 
y_dim = 100
z_dim = 10
x_min = 0
x_max = 10
y_min = 0 
y_max = 100
z_min = 10
z_max = 20

def calculate_cross_section_area(file_path, plane):
	# Load the STL file
	stl_mesh = mesh.Mesh.from_file(file_path)

	# Extract vertices
	vertices = stl_mesh.vectors.reshape(-1, 3)

	# Project vertices onto the specified plane
	if plane == 'xy':
		# Project onto the XY plane (z = 0)
		projected_vertices = vertices[:, [0, 1]]
	elif plane == 'yz':
		# Project onto the YZ plane (x = 0)
		projected_vertices = vertices[:, [1, 2]]
	elif plane == 'xz':
		# Project onto the XZ plane (y = 0)
		projected_vertices = vertices[:, [0, 2]]
	else:
		raise ValueError("Invalid plane specified. Choose 'xy', 'yz', or 'xz'.")

	# Calculate the convex hull of the projected vertices
	hull = ConvexHull(projected_vertices)

	# Calculate the area of the convex hull
	area = hull.volume

	return area

# Prompt user for plane selection
plane = input("Enter the plane in which the load is applied (xy, yz, xz): ")

# Prompt user for the number of nodes
num_nodes = int(input("Enter the number of nodes required for the model: "))

if plane == 'xy':
	visualize_xy_plane(stl_file)
	plt.show()
	print(xy_area)
	print("Dimensions in x direction: ",x_dim)
	print("Dimensions in y direction: ",y_dim)
	# Calculate the longitudinal distance
	longitudinal_distance = input("Enter the direction in which the nodes should be arranged (x or y): ")
	# Calculate the distance between nodes
	if longitudinal_distance == 'x':
		node_distance = x_dim / (num_nodes-1)
	else:
		node_distance = y_dim / (num_nodes-1)
	print("Distance between nodes in the", plane, "plane:", node_distance)
	
	if longitudinal_distance == 'x':
		x_nodes = np.arange(x_min, x_max, node_distance)
		y_nodes = np.full_like(x_nodes, (y_max + y_min) / 2)  # Place nodes at the middle of the y-axis
		z_nodes = np.full_like(x_nodes, (z_max + z_min) / 2)  # Place nodes at the middle of the z-axis
	elif longitudinal_distance == 'y':
		y_nodes = np.arange(y_min, y_max, node_distance)
		x_nodes = np.full_like(y_nodes, (x_max + x_min) / 2)  # Place nodes at the middle of the x-axis
		z_nodes = np.full_like(y_nodes, (z_max + z_min) / 2)  # Place nodes at the middle of the z-axis
	else:
		print("Invalid direction. Please choose 'x', 'y', or 'z'.")
		# Add additional error handling if needed
		exit()

#################################################################################################
	
elif plane == 'yz':
	visualize_yz_plane(stl_file)
	plt.show()
	print(yz_area)
	print("Dimensions in y direction: ",y_dim)
	print("Dimensions in z direction: ",z_dim)
	# Calculate the longitudinal distance
	longitudinal_distance = input("Enter the direction in which the nodes should be arranged (y or z): ")
	# Calculate the distance between nodes
	if longitudinal_distance == 'y':
		node_distance = y_dim / (num_nodes-1)
	else:
		node_distance = z_dim / (num_nodes-1)
	print("Distance between nodes in the", plane, "plane:", node_distance)
	
	if longitudinal_distance == 'z':
		z_nodes = np.arange(z_min, z_max, node_distance)
		y_nodes = np.full_like(z_nodes, (y_max + y_min) / 2)  # Place nodes at the middle of the y-axis
		x_nodes = np.full_like(z_nodes, (x_max + x_min) / 2)  # Place nodes at the middle of the z-axis
	elif longitudinal_distance == 'y':
		y_nodes = np.arange(y_min, y_max, node_distance)
		x_nodes = np.full_like(y_nodes, (x_max + x_min) / 2)  # Place nodes at the middle of the x-axis
		z_nodes = np.full_like(y_nodes, (z_max + z_min) / 2)  # Place nodes at the middle of the z-axis
	else:
		print("Invalid direction. Please choose 'x', 'y', or 'z'.")
		# Add additional error handling if needed
		exit()
		
############################################################################################################	
elif plane == 'xz':
	visualize_xz_plane(stl_file)
	plt.show()
	print(xz_area)
	print("Dimensions in x direction: ",x_dim)
	print("Dimensions in z direction: ",z_dim)
	# Calculate the longitudinal distance
	longitudinal_distance = input("Enter the direction in which the nodes should be arranged (x or z): ")
	# Calculate the distance between nodes
	if longitudinal_distance == 'x':
		node_distance = x_dim / (num_nodes)
	else:
		node_distance = z_dim / (num_nodes-1)
	print("Distance between nodes in the", plane, "plane:", node_distance)
	
	if longitudinal_distance == 'z':
		z_nodes = np.arange(z_min, z_max, node_distance)
		y_nodes = np.full_like(z_nodes, (y_max + y_min) / 2)  # Place nodes at the middle of the y-axis
		x_nodes = np.full_like(z_nodes, (x_max + x_min) / 2)  # Place nodes at the middle of the z-axis
	elif longitudinal_distance == 'x':
		x_nodes = np.arange(x_min, x_max, node_distance)
		y_nodes = np.full_like(x_nodes, (y_max + y_min) / 2)  # Place nodes at the middle of the y-axis
		z_nodes = np.full_like(x_nodes, (z_max + z_min) / 2)  # Place nodes at the middle of the z-axis
	else:
		print("Invalid direction. Please choose 'x', 'y', or 'z'.")
		# Add additional error handling if needed
		exit()
else:
	print("Invalid plane selection. Please choose 'xy', 'yz', or 'xz'.")

# Prompt user for load applied
load = float(input("Enter the value of load applied (in Newtons): "))

# Calculate cross-sectional area on the selected plane
area = calculate_cross_section_area(stl_file, plane)
print("Cross-sectional area on the", plane, "plane:", area)


# Plot the red dots for nodes
plt.scatter(x_nodes, y_nodes, z_nodes, color='red', marker='X')

# Show the updated plot
plt.show()


# In[ ]:




