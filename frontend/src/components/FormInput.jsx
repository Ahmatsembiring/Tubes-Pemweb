"use client"
import "./FormInput.css"

function FormInput({ label, type = "text", value, onChange, placeholder, error, required = false, ...props }) {
  return (
    <div className="form-group">
      {label && (
        <label className="form-label">
          {label}
          {required && <span className="required">*</span>}
        </label>
      )}
      <input
        type={type}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        className={`form-input ${error ? "error" : ""}`}
        {...props}
      />
      {error && <span className="error-message">{error}</span>}
    </div>
  )
}

export default FormInput
