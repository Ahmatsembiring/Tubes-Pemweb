import "./LoadingSpinner.css"

function LoadingSpinner({ size = "md" }) {
  return <div className={`spinner spinner-${size}`}></div>
}

export default LoadingSpinner
