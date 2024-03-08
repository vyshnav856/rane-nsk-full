import React from "react"
import axios from "axios"
import "./styles/Analysis4.css"

export default function Analysis4(props) {
	const [nodesImage, setNodesImage] = React.useState(null)
	const [selectFromLibrary, setSelectFromLibrary] = React.useState(true)
	const [selectedMaterial, setSelectedMaterial] = React.useState("aluminium")
	const [safetyFactor, setSafetyFactor] = React.useState(1.5)
	const [constantForce, setConstantForce] = React.useState(true)
	const [constantForceValue, setConstantForceValue] = React.useState(10)
	const [ultimateTensile, setUltimateTensile] = React.useState(0)
	const [manualProperties, setManualProperties] = React.useState({
		young: 70.35,
		poisson: 0.33,
		tensile: 0.31
	})
	const [customForce, setCustomForce] = React.useState(new Array(props.pageData.numNodes).fill(1))

	const materialProperties = {
		aluminium: [70.35, 0.33, 0.31],
		steel: [210, 0.3, 0.75],
		concrete: [32.2, 0.2, 0.005],
		glass: [80, 0.22, 0.15],
		wood: [18.4, 0.40, 0.1],  
		rubber: [0.0033, 0.45, 0.025],
		plastic: [3.5, 0.4, 0.11],
		copper: [120, 0.38, 0.21],
		bronze: [65, 0.35, 0.5],
		titanium: [110, 0.34, 1.26]
	}

	function decodeImages() {
		const decodedImage = atob(props.pageData.nodesImage)

		setNodesImage(decodedImage)	
	}

	React.useEffect(() => {
		decodeImages()
		setUltimateTensile(materialProperties.aluminium[2])
	}, [])

	function changeMaterialSelection() {
		setSelectFromLibrary(prev => !prev)
	}

	function changeSelectedMaterial(event) {
		setSelectedMaterial(event.target.value)
		setUltimateTensile(materialProperties[event.target.value][2])
	}

	function handleManualPropertyChange(event) {
		const {name, value} = event.target

		setManualProperties(prev => {
			return {...prev, [name]: value}
		})

		console.log(manualProperties)
	}

	function renderMaterialSelector() {
		if (selectFromLibrary) {
			return (
				<div className="library-select">
						<h4 className="library-select__title">Select Materials</h4>

						<select className="library-select__materials" value={selectedMaterial} onChange={changeSelectedMaterial}>
							<option value="aluminium" >Aluminium</option>
							<option value="steel" >Steel</option>
							<option value="concrete" >Concrete</option>
							<option value="glass" >Glass</option>
							<option value="wood" >Wood</option>
							<option value="rubber" >Rubber</option>
							<option value="plastic" >Plastic</option>
							<option value="copper" >Copper</option>
							<option value="bronze" >Bronze</option>
							<option value="titanium" >Titanium</option>
						</select>

						<h4 className="library-select__properties-title">Material Properties</h4>

						<div className="library-select__properties-container">
							<p>Young's modulus: {materialProperties[selectedMaterial][0]} GPa</p>
							<p>Poisson's ratio: {materialProperties[selectedMaterial][1]}</p>
							<p>Ultimate tensile strengh: {ultimateTensile} GPa</p>
						</div>
				</div>
			)
		}

		return (
			<div className="manual-select">
				<h4>Enter Material Properties</h4>	

				<label>
					Young's Modulus 
					<input min="1" onChange={handleManualPropertyChange} name="young" type="number" value={manualProperties.young} /> GPa
				</label>
				<br />
				<label>
					Poisson's ratio 
					<input min="1" onChange={handleManualPropertyChange} name="poisson" type="number" value={manualProperties.poisson} />
				</label>
				<br />
				<label>
					Ultimate tensile strength 
					<input min="1" onChange={handleManualPropertyChange} name="tensile" type="number" value={manualProperties.tensile} /> GPa
				</label>
			</div>
		)
	}

	function changeSafetyFactor(event) {
		setSafetyFactor(event.target.value)
	}

	function renderMaxPermissibleStress() {
		if (safetyFactor < 1 || safetyFactor > 2.5) {
			return <p className="warning">Safety factor value is outside of allowed range</p>
		}

		else {
			const maxPermissibleStress = ultimateTensile/ safetyFactor
			return <p>Maximum permissible stress: {maxPermissibleStress.toFixed(3)} GPa</p>
		}
	}

	function changeConstantForce() {
		setConstantForce(prev => !prev)
	}

	function changeConstantForceValue(event) {
		setConstantForceValue(event.target.value)
	}

	function changeCustomForce(event) {
		const {value, name} = event.target

		const newCustomForce = [...customForce]
		newCustomForce[name] = value

		setCustomForce(newCustomForce)

	}

	function renderForceNodes() {
		if (constantForce) {
			return (
				<label>
					Enter force value (in Newtons)
					<input onChange={changeConstantForceValue} value={constantForceValue} type="number" />
				</label>
			)
		}

		else {
			const numNodes = props.pageData.numNodes
			const forceInputs = []

			for (let i = 0; i < numNodes; i++) {
				forceInputs.push(<label className="force-input" key={i}>Node {i + 1} <input type="number" name={i} value={customForce[i]} onChange={changeCustomForce} /></label>)
			}

			return (<div className="force-inputs-container">
						<h5>Enter force values for each node (in Newtons)</h5>
						{forceInputs}
					</div>)
		}
	}

	function handleSimulateClick() {
		const apiData = {}

		apiData.plane = props.pageData.plane
		apiData.nodes = props.pageData.numNodes

		if (selectFromLibrary) {
			apiData.youngs = materialProperties[selectedMaterial][0]
			apiData.poisson = materialProperties[selectedMaterial][1]
			apiData.tensile = ultimateTensile
		}

		else {
			apiData.youngs = manualProperties.young
			apiData.poisson = manualProperties.poisson
			apiData.tensile = manualProperties.tensile
		}

		apiData.safetyFactor = safetyFactor


		if (constantForce) {
			apiData.isForceConstant = 1
			apiData.force = constantForceValue
		}

		else {
			apiData.isForceConstant = 0
			apiData.force = customForce
		}

		axios.post("http://127.0.0.1:5000/simulate", apiData)
			.then(response => props.changePage({number: 5, pageData: response.data}))
			.catch(error => console.log(error))
	}

	return (
		<div className="analysis4-container">
			<h3>Select Material Properties</h3>

			<div className="sections-container">
				<div className="image-container">
					<img className="nodes-image" alt="decoded image" src={`data:image/png;base64,${props.pageData.nodesImage}`} />
				</div>

				<div className="form-container">
					<label className="checkbox-label">
						<input type="checkbox" checked={selectFromLibrary} onChange={changeMaterialSelection} />
						Select material from materials library
					</label>

					{renderMaterialSelector()}

					<div className="safety-factor-container">
						<label className="safety-factor-input checkbox-label">
							Safety factor (between 1 and 2.5)
							<input step="any" type="number" min="1" max="2.5" value={safetyFactor} onChange={changeSafetyFactor}/>
						</label>

						{renderMaxPermissibleStress()}
					</div>

					<div className="force-check-container">
					<label className="checkbox-label">
						<input type="checkbox" checked={constantForce} onChange={changeConstantForce} />
						Force is constant at all nodes
					</label>

					{renderForceNodes()}
					</div>
					
					<br />
					<button className="simulate-button button-stick-left" onClick={handleSimulateClick}>Simulate</button>
				</div>
			</div>

		</div>
	)
}