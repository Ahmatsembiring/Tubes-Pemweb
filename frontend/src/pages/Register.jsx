"use client"

import { useState } from "react"
import { useNavigate, Link } from "react-router-dom"
import { useAuth } from "../hooks/useAuth"
import api from "../services/api"
import FormInput from "../components/FormInput"
import ErrorAlert from "../components/ErrorAlert"
import LoadingSpinner from "../components/LoadingSpinner"
import "./AuthPages.css"

function Register() {
  const navigate = useNavigate()
  const { login } = useAuth()
  const [formData, setFormData] = useState({
    email: "",
    password: "",
    confirmPassword: "",
    role: "job_seeker",
    name: "",
  })
  const [errors, setErrors] = useState({})
  const [loading, setLoading] = useState(false)
  const [apiError, setApiError] = useState("")
  const [step, setStep] = useState(1)

  const validateForm = () => {
    const newErrors = {}

    if (!formData.name.trim()) {
      newErrors.name = "Name is required"
    }

    if (!formData.email.trim()) {
      newErrors.email = "Email is required"
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = "Invalid email format"
    }

    if (!formData.password) {
      newErrors.password = "Password is required"
    } else if (formData.password.length < 8) {
      newErrors.password = "Password must be at least 8 characters"
    }

    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = "Passwords do not match"
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }))
    if (errors[name]) {
      setErrors((prev) => ({
        ...prev,
        [name]: "",
      }))
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setApiError("")

    if (!validateForm()) return

    setLoading(true)

    try {
      const response = await api.post("/auth/register", {
        email: formData.email,
        password: formData.password,
        role: formData.role,
        name: formData.name,
      })

      if (response.data.token) {
        login(response.data.token, response.data.user)
        navigate("/profile")
      } else {
        setStep(2)
      }
    } catch (error) {
      setApiError(error.response?.data?.message || "Registration failed")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-container">
      <div className="auth-box">
        <h1>Create Account</h1>
        <p className="auth-subtitle">
          {step === 1 ? "Sign up to find your next opportunity" : "Verify your email to complete registration"}
        </p>

        {apiError && <ErrorAlert message={apiError} onClose={() => setApiError("")} />}

        {step === 1 ? (
          <form onSubmit={handleSubmit} className="auth-form">
            <FormInput
              label="Full Name"
              value={formData.name}
              onChange={handleChange}
              name="name"
              placeholder="John Doe"
              error={errors.name}
              required
            />

            <FormInput
              label="Email"
              type="email"
              value={formData.email}
              onChange={handleChange}
              name="email"
              placeholder="your@email.com"
              error={errors.email}
              required
            />

            <div className="form-group">
              <label className="form-label">
                Account Type <span className="required">*</span>
              </label>
              <select name="role" value={formData.role} onChange={handleChange} className="form-input">
                <option value="job_seeker">Job Seeker</option>
                <option value="employer">Employer</option>
              </select>
            </div>

            <FormInput
              label="Password"
              type="password"
              value={formData.password}
              onChange={handleChange}
              name="password"
              placeholder="••••••••"
              error={errors.password}
              required
            />

            <FormInput
              label="Confirm Password"
              type="password"
              value={formData.confirmPassword}
              onChange={handleChange}
              name="confirmPassword"
              placeholder="••••••••"
              error={errors.confirmPassword}
              required
            />

            <button type="submit" className="auth-button" disabled={loading}>
              {loading ? <LoadingSpinner size="sm" /> : "Create Account"}
            </button>
          </form>
        ) : (
          <div className="verification-box">
            <p>
              A verification email has been sent to <strong>{formData.email}</strong>
            </p>
            <p>Please check your email and click the verification link to activate your account.</p>
            <button className="auth-button" onClick={() => navigate("/login")}>
              Go to Login
            </button>
          </div>
        )}

        <div className="auth-footer">
          Already have an account? <Link to="/login">Login here</Link>
        </div>
      </div>
    </div>
  )
}

export default Register
