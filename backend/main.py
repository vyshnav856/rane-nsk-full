from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import calculate
import simulate
import cloud

app = Flask(__name__)
CORS(app)

def save_to_file(encoded_data):
	decoded_data = base64.b64decode(encoded_data)

	with open("current.stl", "wb") as file:
		file.write(decoded_data)

def encode_images(xy_filename, xz_filename, yz_filename):
	xy_encoded = ""
	xz_encoded = ""
	yz_encoded = ""

	with open(xy_filename, "rb") as file:
		xy_encoded = base64.b64encode(file.read())

	with open(xz_filename, "rb") as file:
		xz_encoded = base64.b64encode(file.read())

	with open(yz_filename, "rb") as file:
		yz_encoded = base64.b64encode(file.read())

	xy_encoded = xy_encoded.decode("utf-8")
	xz_encoded = xz_encoded.decode("utf-8")
	yz_encoded = yz_encoded.decode("utf-8")

	return [ xy_encoded, xz_encoded, yz_encoded ]

def encode_single_image(path):
	encoded_image = ""

	with open(path, "rb") as file:
		encoded_image = base64.b64encode(file.read())

	encoded_image = encoded_image.decode("utf-8")

	return encoded_image


x_dim = 10 
y_dim = 100
z_dim = 10

x_min = 0
x_max = 10
y_min = 0
y_max = 100
z_min = 10
z_max = 20	

@app.route('/')
def testing():
	res = {"message": "hello, world!"}
	return jsonify(res)

@app.route("/send", methods=['POST'])
def get_stl_file():
	data = request.get_json()
	encoded_data = data.get("base64String")

	save_to_file(encoded_data)
	path = "current.stl"

	xy_filename = calculate.save_xy_plane(path)
	xz_filename = calculate.save_xz_plane(path)
	yz_filename = calculate.save_yz_plane(path)

	xy_encoded, xz_encoded, yz_encoded = encode_images(xy_filename, xz_filename, yz_filename)

	xy_area, yz_area, xz_area = calculate.calculate_cross_section_area(path)

	res = {	"xyImage": xy_encoded, 
			"xzImage": xz_encoded, 
			"yzImage": yz_encoded,
			"xyCross": str(xy_area),
			"yzCross": str(yz_area),
			"xzCross": str(xz_area),
			"xDim": x_dim,
			"yDim": y_dim,
			"zDim": z_dim
			}

	return jsonify(res)

@app.route("/send2", methods=["POST"])
def get_analysis_details():
	data = request.get_json()

	plane = data.get("plane")
	direction = data.get("direction")
	nodes = data.get("nodes")
	load = data.get("load")
	distance = data.get("distance")

	calculate.get_nodes_image(plane, direction, "current.stl", int(nodes))

	encoded_image = encode_single_image("nodes.png")

	res = {
		"nodesImage": encoded_image,
		"numNodes": nodes,
		"nodeDistance": distance,
		"plane": plane,
	}

	return jsonify(res)

@app.route("/simulate", methods=["POST"])
def do_simulation():
	data = request.get_json()

	length = x_dim
	breadth = y_dim
	height = z_dim

	result_table, stress_excess = simulate.get_simulation(data, length, breadth, height)

	encoded_image = encode_single_image("final_image.png")

	res = {
		"simulationImage": encoded_image,
		"resultTable": result_table,
		"stressExcess": stress_excess
	}

	cloud.save_to_cloud()

	return jsonify(res)

if __name__ == "__main__":
	app.run(debug=True)