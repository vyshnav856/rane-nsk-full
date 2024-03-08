import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors
import tkinter as tk
import sys
	# Function to display material properties 
def on_material_selected(material):
	global youngs_modulus, poissons_ratio, ultimate_strength
	youngs_modulus, poissons_ratio, ultimate_strength = material_properties[material]
	youngs_modulus_label.config(text=f"Young's Modulus: {youngs_modulus} GPa")
	poissons_ratio_label.config(text=f"Poisson's Ratio: {poissons_ratio}")
	ultimate_tensile_stress_label.config(text=f"Ultimate Tensile Stress: {ultimate_strength} GPa")

# Function to get material properties
def get_material_properties(material):
	global youngs_modulus, poissons_ratio, ultimate_strength
	youngs_modulus, poissons_ratio, ultimate_strength = material_properties[material]
	return youngs_modulus, poissons_ratio, ultimate_strength

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
	stress_matrix = np.diag(force / area)
	displacement_matrix = np.zeros(N)
	for i in range(N):
		displacement_matrix[i] = np.array(force[i] * nodes[i] / (area * youngs_modulus))
	# Calculate the stress and displacement arrays
	stresses = np.dot(stress_matrix, np.ones(N))
	return nodes, stresses, displacement_matrix

# material_properties = {
#	 "Aluminum": (70.35, 0.33, 0.31),
#	 "Steel": (210, 0.3, 0.75),
#	 "Concrete": (32.2, 0.2, 0.005),
#	 "Glass": (80, 0.22, 0.15),
#	 "Wood": (18.4, 0.40, 0.1),  
#	 "Rubber": (0.0033, 0.45, 0.025),
#	 "Plastic": (3.5, 0.4, 0.11),
#	 "Copper": (120, 0.38, 0.21),
#	 "Bronze": (65, 0.35, 0.5),
#	 "Titanium": (110, 0.34, 1.26)
# }

# plane = input("Enter plane - xy, yz or zx: ")
# length = int(input("Enter length in mm: "))
# breadth = int(input("Enter breadth in mm: "))
# height = int(input("Enter height in mm: "))
# N = int(input("Enter number of nodes: "))
# choice = input("Do you want to select material from material library (Y/N): ")

# if(choice == 'Y' or choice == 'y'):
#	 root = tk.Tk()
#	 root.geometry("400x200")

#	 # Create dropdown menu
#	 material_var = tk.StringVar(root)
#	 material_var.set("Select Material")
#	 material_dropdown = tk.OptionMenu(root, material_var, *material_properties.keys(), command=on_material_selected)
#	 material_dropdown.pack()

#	 # Create labels to display material properties
#	 youngs_modulus_label = tk.Label(root, text="Young's Modulus: ")
#	 youngs_modulus_label.pack()
#	 poissons_ratio_label = tk.Label(root, text="Poisson's Ratio: ")
#	 poissons_ratio_label.pack()
#	 ultimate_tensile_stress_label = tk.Label(root, text="Ultimate Tensile Stress: ")
#	 ultimate_tensile_stress_label.pack()

#	 # Run tkinter main loop
#	 root.mainloop()

# elif(choice == 'N' or choice == 'n'):
#	 youngs_modulus = int(input("Enter Young's Modulus in GPa: "))
#	 poissons_ratio = float(input("Enter poisson's ratio: "))
#	 ultimate_strength = float(input("Enter ultimate tensile strength: "))

# safety_factor = float(input("Enter safety factor between 1 and 2.5: "))

# if(safety_factor<1):
#	 print("Design is unsafe. Please enter safety factor equal to or greater than 1.")
# elif(safety_factor>2.5):
#	 print("Design becomes over-engineered. Please enter safety factor less than 2.5")

# permissible_stress = float(ultimate_strength/safety_factor)
# print("Permissible stress: ", permissible_stress, "GPa")
# answer = input("Is force constant at all nodes? (Y/N): ")

# if(answer == 'Y' or answer == 'y'):
#	 force = int(input("Enter force value: "))
#	 force = [force]*N
# elif(answer == 'N' or answer == 'n'):
#	 force = np.array([int(input(f"Enter force at node {i}: ")) for i in range(N)])
# else:
#	 print("Invalid Input. Choose Y or N")

# if (plane == 'xy' or plane == 'XY'):
#	 area = breadth * height
# elif (plane == 'yz' or plane == 'YZ'):
#	 area = length * height
# else:
#	 area = length * breadth

nodes, stresses, displacements = nodes_stress_displacement(plane, force, area, length, breadth, height, N, youngs_modulus, poissons_ratio)

for i in range(N):
	if(stresses[i]>permissible_stress):
		print(f"Stress at node {i} is exceeding safe stress limit. Please change material or area or loading conditions.\n Exiting Program")
		sys.exit()

print("\nNode\tForce\tStress\tDisplacement")
for i in range(N):
	print(f"{nodes[i]:.1f}\t{force[i]:.0f}\t{stresses[i]:.4f}\t{displacements[i]:.8f}")

# Create a figure and two subplots
fig, axs = plt.subplots(1, 2, figsize=(6.4, 4.8))

# Normalize the stress values to [0, 1] range
stress_norm = colors.Normalize()
stress_norm.autoscale(np.abs(stresses))

# Visualize the stress
im = axs[0].imshow(stress_norm(stresses.reshape(N, 1)), cmap=cm.coolwarm, aspect='auto', origin='lower', extent=[nodes[0], nodes[-1], 0, N], vmin=0, vmax=1)
cbar = fig.colorbar(im, ax=axs[0], orientation='vertical', pad=0.02)
cbar.set_label('Stress (GPa)')
axs[0].set_title('Stress Distribution')
axs[0].set_xlabel('Node')
axs[0].set_ylabel('Force')
axs[0].set_xticks(nodes)
axs[0].xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.1f}'))

# Normalize the displacement values to [0, 1] range
disp_norm = colors.Normalize()
disp_norm.autoscale(np.abs(displacements))

# Visualize the displacement
im = axs[1].imshow(disp_norm(displacements.reshape(N, 1)), cmap=cm.coolwarm, aspect='auto', origin='lower', extent=[nodes[0], nodes[-1], 0, N], vmin=0, vmax=1)
cbar = fig.colorbar(im, ax=axs[1], orientation='vertical', pad=0.02)
cbar.set_label('Displacement (m)')
axs[1].set_title('Displacement Distribution')
axs[1].set_xlabel('Node')
axs[1].set_ylabel('Force')
axs[1].set_xticks(nodes)
axs[1].xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.1f}'))

plt.savefig("final_image.png")
plt.show()