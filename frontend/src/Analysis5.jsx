import React from "react"
import "./styles/Analysis5.css"

export default function Analysis5(props) {
	const [simulationImage, setSimulationImage] = React.useState(null)

	function decodeImages() {
		const decodedImage = atob(props.pageData.simulationImage)

		setSimulationImage(decodedImage)	
	}

	React.useEffect(() => {
		decodeImages()
	}, [])

	function renderStressWarning() {
		const stress = props.pageData.stressExcess
		const n = stress.length

		let warningNeeded = false
		for (let i = 0; i < n; i++) {
			if (stress[i] == 1) {
				warningNeeded = true
				break
			}
		}

		if (warningNeeded) {
			const warningMessages = []

			for (let i = 0; i < n; i++) {
				if (stress[i] == 1) {
					warningMessages.push(<p key={i} className="warning-message">Stress at node {i + 1} exceeds safe limit!</p>)
				}
			}

			return (
				<div className="warning-message-container">
					<h4>Warnings</h4>
					{warningMessages}
				</div>
			)
		}

		else {
			return <></>
		}
	}

	function getTableRows() {
		const results = props.pageData.resultTable
		const tableRows = []

		for (let i = 0; i < results.length; i++) {
			const tableData = []

			for (let j = 0; j < results[i].length; j++) {
				tableData.push(<td key={j}>{results[i][j]}</td>)
			}

			tableRows.push(<tr key={i}>{tableData}</tr>)
		}

		return tableRows
	}

	function renderTable() {
		// console.log(props.pageData.resultTable)

		return (
			<table>
				<thead>
				<tr>
					<th>Node position</th>
					<th>Force (Newtons)</th>
					<th>Stress (Newton/mm^2)</th>
					<th>Displacement (mm)</th>
				</tr>
				</thead>

				<tbody>
					{getTableRows()}
				</tbody>
			</table>
		)
	}

	return (
		<div className="analysis5-container">
			<h3 className="analysis5__title">Simulation Results</h3>
			<img className="simulation-image" alt="decoded image" src={`data:image/png;base64,${props.pageData.simulationImage}`} />

			{renderStressWarning()}
			{renderTable()}
		</div>
	)
}