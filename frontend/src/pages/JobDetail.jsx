"use client"

import { useState } from "react"
import { useParams, useNavigate } from "react-router-dom"
import { useAuth } from "../hooks/useAuth"
import { useFetch } from "../hooks/useFetch"
import api from "../services/api"
import LoadingSpinner from "../components/LoadingSpinner"
import ErrorAlert from "../components/ErrorAlert"
import "./JobDetail.css"

function JobDetail() {
  const { id } = useParams()
  const navigate = useNavigate()
  const { auth } = useAuth()
  const { data: job, loading, error } = useFetch(`/jobs/${id}`)
  const [applying, setApplying] = useState(false)
  const [applied, setApplied] = useState(false)
  const [apiError, setApiError] = useState("")

  const handleApply = async () => {
    if (!auth?.isAuthenticated) {
      navigate("/login")
      return
    }

    setApplying(true)
    setApiError("")

    try {
      await api.post(`/jobs/${id}/apply`)
      setApplied(true)
    } catch (error) {
      setApiError(error.response?.data?.message || "Failed to apply")
    } finally {
      setApplying(false)
    }
  }

  if (loading)
    return (
      <div className="loading-center">
        <LoadingSpinner size="lg" />
      </div>
    )

  if (error) return <ErrorAlert message={error} />

  if (!job)
    return (
      <div className="error-container">
        <p>Job not found</p>
      </div>
    )

  return (
    <div className="job-detail">
      <div className="container">
        <button className="back-button" onClick={() => navigate("/jobs")}>
          ← Back to Jobs
        </button>

        <div className="detail-layout">
          <main className="detail-content">
            <header className="detail-header">
              <h1>{job.title}</h1>
              <span className="job-type-badge">{job.type}</span>
            </header>

            <div className="detail-meta">
              <div className="meta-item">
                <span className="meta-label">Company</span>
                <span className="meta-value">{job.company_name}</span>
              </div>
              <div className="meta-item">
                <span className="meta-label">Location</span>
                <span className="meta-value">{job.location}</span>
              </div>
              <div className="meta-item">
                <span className="meta-label">Salary</span>
                <span className="meta-value">Rp{job.salary.toLocaleString("id-ID")}/month</span>
              </div>
              <div className="meta-item">
                <span className="meta-label">Posted</span>
                <span className="meta-value">{new Date(job.created_at).toLocaleDateString()}</span>
              </div>
            </div>

            <section className="detail-section">
              <h2>Description</h2>
              <p>{job.description}</p>
            </section>

            <section className="detail-section">
              <h2>Requirements</h2>
              <ul className="requirements-list">
                {job.requirements?.split("\n").map((req, idx) => (
                  <li key={idx}>{req}</li>
                ))}
              </ul>
            </section>
          </main>

          <aside className="detail-sidebar">
            {apiError && <ErrorAlert message={apiError} />}

            {applied ? (
              <div className="success-box">
                <h3>Application Submitted</h3>
                <p>Your application has been submitted successfully. The employer will review it soon.</p>
              </div>
            ) : (
              <>
                {auth?.isAuthenticated && auth.user.role === "job_seeker" ? (
                  <button className="btn btn-primary apply-button" onClick={handleApply} disabled={applying}>
                    {applying ? <LoadingSpinner size="sm" /> : "Apply Now"}
                  </button>
                ) : auth?.isAuthenticated && auth.user.role === "employer" ? (
                  <div className="info-box">
                    <p>You are viewing this as an employer. You cannot apply to this job.</p>
                  </div>
                ) : (
                  <button className="btn btn-primary apply-button" onClick={() => navigate("/register")}>
                    Sign Up to Apply
                  </button>
                )}
              </>
            )}

            <div className="info-box">
              <h3>About This Role</h3>
              <ul className="info-list">
                <li>
                  <strong>Type:</strong> {job.type}
                </li>
                <li>
                  <strong>Level:</strong> {job.level || "Not specified"}
                </li>
              </ul>
            </div>
          </aside>
        </div>
      </div>
    </div>
  )
}

export default JobDetail
