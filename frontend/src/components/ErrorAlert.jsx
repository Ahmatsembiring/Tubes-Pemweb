"use client"
import "./ErrorAlert.css"

function ErrorAlert({ message, onClose }) {
  return (
    <div className="error-alert">
      <div className="error-content">
        <span className="error-icon">✕</span>
        <p>{message}</p>
      </div>
      {onClose && (
        <button className="error-close" onClick={onClose}>
          ×
        </button>
      )}
    </div>
  )
}

export default ErrorAlert
