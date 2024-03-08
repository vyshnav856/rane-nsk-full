import React from "react"
import "./styles/Analysis3.css"

export default function Analysis3(props) {
	const [nodesImage, setNodesImage] = React.useState(null)

	function decodeImages() {
		const decodedImage = atob(props.pageData.nodesImage)

		setNodesImage(decodedImage)	
	}

	React.useEffect(() => {
		decodeImages()
	}, [])

	function handleClick() {
		const nextPageData = {
			nodesImage: props.pageData.nodesImage,
			numNodes: props.pageData.numNodes,
			plane: props.pageData.plane
		}

		props.changePage({number: 4, pageData: nextPageData})
	}

	return (
		<div className="analysis3-container">
			<h3>Mesh Generation (Placement of Nodes)</h3>

			<img className="nodes-image" alt="decoded image" src={`data:image/png;base64,${props.pageData.nodesImage}`} />
			
			<p>Number of nodes: {props.pageData.numNodes}</p>
			<p>Distance between nodes: {props.pageData.nodeDistance}mm</p>

			<button onClick={handleClick} >Go to post processing and simulation results</button>
		</div>
	)
}