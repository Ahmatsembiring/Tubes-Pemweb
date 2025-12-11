"use client"

import { useState } from "react"
import { useNavigate, Link } from "react-router-dom"
import { useAuth } from "../hooks/useAuth"
import api from "../services/api"
import FormInput from "../components/FormInput"
import ErrorAlert from "../components/ErrorAlert"
import LoadingSpinner from "../components/LoadingSpinner"
import "./AuthPages.css"

function Login() {
  const navigate = useNavigate()
  const { login } = useAuth()
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  })
  const [errors, setErrors] = useState({})
  const [loading, setLoading] = useState(false)
  const [apiError, setApiError] = useState("")

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

    const newErrors = {}
    if (!formData.email) newErrors.email = "Email is required"
    if (!formData.password) newErrors.password = "Password is required"

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors)
      return
    }

    setLoading(true)

    try {
      const response = await api.post("/auth/login", formData)
      login(response.data.token, response.data.user)
      navigate(response.data.user.role === "employer" ? "/manage-jobs" : "/jobs")
    } catch (error) {
      setApiError(error.response?.data?.message || "Login failed")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-container">
      <div className="auth-box">
        <h1>Welcome Back</h1>
        <p className="auth-subtitle">Login to access your account</p>

        {apiError && <ErrorAlert message={apiError} onClose={() => setApiError("")} />}

        <form onSubmit={handleSubmit} className="auth-form">
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

          <button type="submit" className="auth-button" disabled={loading}>
            {loading ? <LoadingSpinner size="sm" /> : "Login"}
          </button>
        </form>

        <div className="auth-footer">
          Don't have an account? <Link to="/register">Register here</Link>
        </div>
      </div>
    </div>
  )
}

export default Login
