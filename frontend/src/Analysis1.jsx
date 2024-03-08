import React from "react"
import "./styles/Analysis1.css"

export default function Analysis1(props) {
	const [XYImage, setXYImage] = React.useState(null)
	const [YZImage, setYZImage] = React.useState(null)
	const [XZImage, setXZImage] = React.useState(null)

	function decodeImages() {
		const decodedXY = atob(props.pageData.xyImage)
		const decodedYZ = atob(props.pageData.yzImage)
		const decodedXZ = atob(props.pageData.xzImage)

		setXYImage(decodedXY)	
		setYZImage(decodedYZ)
		setXZImage(decodedXZ)
	}

	function renderImages() {
		return (
			<div className="plane-image-container" >
				<img className="plane-image" alt="decoded image" src={`data:image/png;base64,${props.pageData.xyImage}`} />
				<img className="plane-image" alt="decoded image" src={`data:image/png;base64,${props.pageData.yzImage}`} />
				<img className="plane-image" alt="decoded image" src={`data:image/png;base64,${props.pageData.xzImage}`} />
			</div>
		)
	}

	React.useEffect(() => {
		decodeImages()
	}, [])

	function handleClick(e) {
		let planeImage
		let crossSection
		const planeName = e.target.value

		if (planeName == "xy") {
			planeImage = props.pageData.xyImage
			crossSection = props.pageData.xyCross
		}

		if (planeName == "yz") {
			planeImage = props.pageData.yzImage
			crossSection = props.pageData.yzCross
		}

		if (planeName == "xz") {
			planeImage = props.pageData.xzImage
			crossSection = props.pageData.xzCross
		}

		const pageData = {
			planeName, 
			planeImage, 
			crossSection, 
			xDim: props.pageData.xDim,
			yDim: props.pageData.yDim,
			zDim: props.pageData.zDim
		}

		props.changePage({number: 2, pageData})
	}

	return (
		<div className="analysis1-wrapper" >
			<h3>Select a plane to apply load on:</h3>
			{renderImages()}

			<div className="plane-selection-container">
				<button value="xy" className={`plane-selection-container__button`} onClick={handleClick}>XY Plane</button>
				<button value="yz" className={`plane-selection-container__button`} onClick={handleClick}>YZ Plane</button>
				<button value="xz" className={`plane-selection-container__button`} onClick={handleClick}>XZ Plane</button>
			</div>
		</div>
	)
}