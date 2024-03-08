import React from "react"
import axios from "axios"
import "./styles/FileUpload.css"

export default function FileUpload(props) {
	const [file, setFile] = React.useState("none")

	function handleChange(event) {
		setFile(event.target.files[0])
	}

	function renderFileName() {
		if (file != "none")
			return <p>Uploaded file: <span className="highlight-blue">{file.name}</span></p>;
	}

	function gotoAnalysis1(data) {
		props.setLoading(false)
		props.changePage({number: 1, pageData: data})
	}

	function handleSubmit(e) {
		props.setLoading(true)
		e.preventDefault()

		const reader = new FileReader()
		reader.onload = () => {
			const base64String = btoa(reader.result)
			
			axios.post("http://127.0.0.1:5000/send", {base64String})
			.then(response => gotoAnalysis1(response.data))
			.catch(error => console.log(error))
		}

		reader.readAsBinaryString(file)
	}

	function renderSubmitButton() {
		if (file != "none") {
			return <button className="button-enabled button-stick-left">Submit</button>
		}

		else return <button disabled className="button-disabled button-stick-left">Submit</button>
	}

	return (
		<form className="file-upload__wrapper" onSubmit={handleSubmit} >
				<h3 className="file-upload__title">Upload your STL file</h3>

				<label className="file-upload__select-button">Select file to upload
					<input onChange={handleChange} accept=".stl" type="file" className="file-upload__input"/>
				</label>

				{renderFileName()}
				{renderSubmitButton()}
		</form>	
	)
}