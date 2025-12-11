"use client"

import { useState } from "react"
import { useNavigate } from "react-router-dom"
import api from "../services/api"
import FormInput from "../components/FormInput"
import ErrorAlert from "../components/ErrorAlert"
import LoadingSpinner from "../components/LoadingSpinner"
import "./PostJob.css"

function PostJob() {
  const navigate = useNavigate()
  const [formData, setFormData] = useState({
    title: "",
    description: "",
    requirements: "",
    salary: "",
    location: "",
    type: "Full-time",
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

  const validateForm = () => {
    const newErrors = {}
    if (!formData.title.trim()) newErrors.title = "Job title is required"
    if (!formData.description.trim()) newErrors.description = "Description is required"
    if (!formData.requirements.trim()) newErrors.requirements = "Requirements are required"
    if (!formData.salary) newErrors.salary = "Salary is required"
    if (!formData.location.trim()) newErrors.location = "Location is required"

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setApiError("")

    if (!validateForm()) return

    setLoading(true)

    try {
      await api.post("/jobs", {
        ...formData,
        salary: Number.parseInt(formData.salary),
      })
      navigate("/manage-jobs")
    } catch (error) {
      setApiError(error.response?.data?.message || "Failed to post job")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="post-job-page">
      <div className="container">
        <h1>Post a New Job</h1>

        <div className="form-container">
          {apiError && <ErrorAlert message={apiError} onClose={() => setApiError("")} />}

          <form onSubmit={handleSubmit} className="job-form">
            <FormInput
              label="Job Title"
              value={formData.title}
              onChange={handleChange}
              name="title"
              placeholder="e.g., Senior React Developer"
              error={errors.title}
              required
            />

            <div className="form-group">
              <label className="form-label">
                Description <span className="required">*</span>
              </label>
              <textarea
                name="description"
                value={formData.description}
                onChange={handleChange}
                placeholder="Describe the job role and responsibilities"
                className={`form-textarea ${errors.description ? "error" : ""}`}
                rows="6"
              ></textarea>
              {errors.description && <span className="error-message">{errors.description}</span>}
            </div>

            <div className="form-group">
              <label className="form-label">
                Requirements <span className="required">*</span>
              </label>
              <textarea
                name="requirements"
                value={formData.requirements}
                onChange={handleChange}
                placeholder="List requirements (one per line)"
                className={`form-textarea ${errors.requirements ? "error" : ""}`}
                rows="6"
              ></textarea>
              {errors.requirements && <span className="error-message">{errors.requirements}</span>}
            </div>

            <div className="form-row">
              <FormInput
                label="Salary (IDR)"
                type="number"
                value={formData.salary}
                onChange={handleChange}
                name="salary"
                placeholder="e.g., 5000000"
                error={errors.salary}
                required
              />

              <FormInput
                label="Location"
                value={formData.location}
                onChange={handleChange}
                name="location"
                placeholder="e.g., Jakarta"
                error={errors.location}
                required
              />
            </div>

            <div className="form-group">
              <label className="form-label">Job Type</label>
              <select name="type" value={formData.type} onChange={handleChange} className="form-input">
                <option value="Full-time">Full-time</option>
                <option value="Part-time">Part-time</option>
                <option value="Contract">Contract</option>
                <option value="Internship">Internship</option>
              </select>
            </div>

            <button type="submit" className="btn btn-primary btn-large" disabled={loading}>
              {loading ? <LoadingSpinner size="sm" /> : "Post Job"}
            </button>
          </form>
        </div>
      </div>
    </div>
  )
}

export default PostJob
