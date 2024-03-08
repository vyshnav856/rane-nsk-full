import { useState } from 'react'
import './App.css'

import FileUpload from "./FileUpload.jsx"
import Analysis1 from "./Analysis1.jsx"
import Analysis2 from "./Analysis2.jsx"
import Analysis3 from "./Analysis3.jsx"
import Analysis4 from "./Analysis4.jsx"
import Analysis5 from "./Analysis5.jsx"
import Error from "./Error.jsx"

function App() {
	const [page, setPage] = useState({number: -1, pageData: {}});
	const [loading, setLoading] = useState(false);

	function renderComponent() {
		if (page.number == -1) {
			return (
				<video className="background-video" autoPlay muted loop>
					<source src="/background.mp4" type="video/mp4" />
				</video>
			)
		}

		else if (page.number == 0) 
			return <FileUpload setLoading={setLoading} changePage={setPage} />

		else if (page.number == 1) 
			return <Analysis1 setLoading={setLoading} changePage={setPage} pageData={page.pageData} />

		else if (page.number == 2)
			return <Analysis2 setLoading={setLoading} changePage={setPage} pageData={page.pageData} />

		else if (page.number == 3)
			return <Analysis3 setLoading={setLoading} changePage={setPage} pageData={page.pageData} />

		else if (page.number == 4)
			return <Analysis4 setLoading={setLoading} changePage={setPage} pageData={page.pageData} />

		else if (page.number == 5)
			return <Analysis5 setLoading={setLoading} changePage={setPage} pageData={page.pageData} />

		else 
			return <Error />
	}

	function showLoading() {
		if (loading) return <div className="loading-box"><p>Loading, please wait</p></div>
		else return <></>
	}

	function handleButtonClick() {
		setPage({number: 0, pageData: {}})
	}

	function renderUploadButton() {
		return <button className="upload-next-button" onClick={handleButtonClick} >Upload STL File</button>
	}

	return (
		<div className="page-wrapper">
			<header>
				{page.number != -1 && <a href="/"><h1>2D Analysis Software</h1></a>}
			</header>

			<main>
				<div className="component-wrapper">
					{renderComponent()}
				</div>

				{page.number == -1 && renderUploadButton()}
			</main>

			<img className="team-logo" src="/logo.png" alt="team logo" />
		</div>
	)
}

export default App
