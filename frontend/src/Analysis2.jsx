import React from "react"
import axios from "axios"
import "./styles/Analysis2.css"

export default function Analysis2(props) {
	let nodeDistance

	const [direction, setDirection] = React.useState("none")
	const [formData, setFormData] = React.useState({
		nodes: 5,
		load: 10,

	})

	function submitPage() {
		const apiData = {
			plane: props.pageData.planeName,
			direction,
			nodes: formData.nodes,
			distance: nodeDistance
		}

		console.log(apiData)

		axios.post("http://127.0.0.1:5000/send2", apiData)
			.then(response => props.changePage({number: 3, pageData: response.data}))
			.catch(error => console.log(error))
	}

	function renderDimensions() {
		const plane = props.pageData.planeName

		if (plane == "xy") {
			return (
				<>
					<p>Length in x direction: {props.pageData.xDim}</p>
					<p>Length in y direction: {props.pageData.yDim}</p>
				</>
			)
		}

		if (plane == "xz") {
			return (
				<>
					<p>Length in x direction: {props.pageData.xDim}</p>
					<p>Length in z direction: {props.pageData.zDim}</p>
				</>
			)
		}

		if (plane == "yz") {
			return (
				<>
					<p>Length in y direction: {props.pageData.yDim}</p>
					<p>Length in z direction: {props.pageData.zDim}</p>
				</>
			)
		}
	}

	function handleDirectionChange(e) {
		setDirection(e.target.value)
	}

	function renderSubmitButton() {
		if (direction != "none") {
			return <button onClick={submitPage} className="" >Submit</button>
		}

		else return <button disabled className="button-disabled">Submit</button>
	}

	function renderDirectionButtons() {
		const [plane1, plane2] = props.pageData.planeName.split("")

		return (
			<div className="analysis2__buttons-container">
				<button value={plane1} onClick={handleDirectionChange} className={`analysis2__direction ${direction == plane1 ? "selected" : ""}`} >{plane1}</button>
				<button value={plane2} onClick={handleDirectionChange} className={`analysis2__direction ${direction == plane2 ? "selected" : ""}`} >{plane2}</button>
			</div>
		)
	}

	function handleFormChange(event) {
		const {name, value} = event.target

		setFormData(prev => {
			return {...prev, [name]: value}
		})
	}

	function renderNodeDistance() {
		if (direction == "none") return <></>

		if (direction == "x") {
			nodeDistance = props.pageData.xDim / (formData.nodes)
		}

		if (direction == "y") {
			nodeDistance = props.pageData.yDim / (formData.nodes)
		}

		if (direction == "z") {
			nodeDistance = props.pageData.zDim / (formData.nodes)
		}

		return (
			<p>Distance between nodes in the plane: {nodeDistance}</p>
		)
	}

	return (
		<div className="analysis2-container">
			<h3>Pre-processing</h3>

			<div className="image-details-container">
				<img className="plane-image-2" alt="decoded image" src={`data:image/png;base64,${props.pageData.planeImage}`} />
				<p>Cross section area: {props.pageData.crossSection}</p>
				<br />
				<h5>Dimensions</h5>
				{renderDimensions()}
			</div>

			<div className="analysis2__inputs">
				<h4>Select direction to place nodes in</h4>
				{renderDirectionButtons()}

				<div className="analysis2__input-group">
					<label>Enter the number of nodes:</label>
					<input min="1" max="9999" name="nodes" onChange={handleFormChange} type="number" value={formData.nodes} />
				</div>
				
				{/* <div className="analysis2__input-group">
					<label>{"Enter load to apply (in Newtons): "}</label>
					<input min="1" max="9999" name="load" onChange={handleFormChange} type="number" value={formData.load} />
				</div> */}

				{renderNodeDistance()}

				{renderSubmitButton()}
				
			</div>
		</div>
	)
}