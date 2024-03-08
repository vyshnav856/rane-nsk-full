import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors

def short(num):
	return f"{num:.6f}"

def nodes_stress_displacement(plane, force, area, length, breadth, height, N, youngs_modulus, poissons_ratio):
	E = youngs_modulus
	nu = poissons_ratio
	# Define the dimensions of the cuboidal beam element
	L = length
	B = breadth
	H = height
	# Define the nodal coordinates based on the plane
	if (plane == 'xy' or plane == 'XY'):
		nodes = np.linspace(0, L, N)
	elif (plane == 'yz' or plane == 'YZ'):
		nodes = np.linspace(0, B, N)
	elif (plane == 'zx' or plane == 'ZX'):
		nodes = np.linspace(0, H, N)
	else:
		raise ValueError("Invalid plane")
	# Convert area to a 1-dimensional array
	area = np.array([area])
	# Calculate the stress and displacement matrices
	force = np.asarray(force, dtype=int)
	stress_matrix = np.diag(force / area)
	displacement_matrix = np.zeros(N)
	for i in range(N):
		displacement_matrix[i] = np.array(force[i] * nodes[i] / (area * youngs_modulus))
	# Calculate the stress and displacement arrays
	stresses = np.dot(stress_matrix, np.ones(N))
	return nodes, stresses, displacement_matrix

def get_simulation(data, length, breadth, height):
	num_nodes = int(data.get("nodes"))
	N = num_nodes
	youngs_modulus = float(data.get("youngs"))
	poissons_ratio = float(data.get("poisson"))
	ultimate_strength = float(data.get("tensile"))
	safety_factor = float(data.get("safetyFactor"))
	is_force_constant = int(data.get("isForceConstant"))
	force = ""

	permissible_stress = float(ultimate_strength/safety_factor)

	if is_force_constant == 1:
		force = int(data.get("force"))
		force = [force] * num_nodes

	else:
		force = data.get("force")

	plane = data.get("plane")

	area = ''
	if (plane == 'xy' or plane == 'XY'):
		area = breadth * height
	elif (plane == 'yz' or plane == 'YZ'):
		area = length * height
	else:
		area = length * breadth

	nodes, stresses, displacements = nodes_stress_displacement(plane, force, area, length, breadth, height, num_nodes, youngs_modulus, poissons_ratio)

	stress_excess = []
	for i in range(num_nodes):
		stress_excess.append(0)

	for i in range(num_nodes):
		if(stresses[i]>permissible_stress):
			stress_excess[i] = 1

	result_table = []
	for i in range(num_nodes):
		result_table.append([nodes[i], (force[i]), (stresses[i]), short(displacements[i])])

	fig, axs = plt.subplots(1, 2, figsize=(6.4, 4.8))
	stress_norm = colors.Normalize()
	stress_norm.autoscale(np.abs(stresses))
	im = axs[0].imshow(stress_norm(stresses.reshape(N, 1)), cmap=cm.coolwarm, aspect='auto', origin='lower', extent=[nodes[0], nodes[-1], 0, N], vmin=0, vmax=1)
	cbar = fig.colorbar(im, ax=axs[0], orientation='vertical', pad=0.02)
	cbar.set_label('Stress (GPa)')
	axs[0].set_title('Stress Distribution')
	axs[0].set_xlabel('Node')
	axs[0].set_ylabel('Force')
	axs[0].set_xticks(nodes)
	axs[0].xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.1f}'))
	disp_norm = colors.Normalize()
	disp_norm.autoscale(np.abs(displacements))
	im = axs[1].imshow(disp_norm(displacements.reshape(N, 1)), cmap=cm.coolwarm, aspect='auto', origin='lower', extent=[nodes[0], nodes[-1], 0, N], vmin=0, vmax=1)
	cbar = fig.colorbar(im, ax=axs[1], orientation='vertical', pad=0.02)
	cbar.set_label('Displacement (m)')
	axs[1].set_title('Displacement Distribution')
	axs[1].set_xlabel('Node')
	axs[1].set_ylabel('Force')
	axs[1].set_xticks(nodes)
	axs[1].xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.1f}'))

	plt.savefig("final_image.png")
	with open("output.txt", "w") as file:
		file.writelines("\n".join(map(str, result_table)))

	return result_table, stress_excess