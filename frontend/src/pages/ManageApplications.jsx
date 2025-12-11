"use client"

import { useState } from "react"
import { useFetch } from "../hooks/useFetch"
import api from "../services/api"
import LoadingSpinner from "../components/LoadingSpinner"
import ErrorAlert from "../components/ErrorAlert"
import "./Applications.css"

function ManageApplications() {
  const { data, loading, error, refetch } = useFetch("/applications/employer/applicants")
  const [updating, setUpdating] = useState(null)
  const [updateError, setUpdateError] = useState("")

  const handleStatusUpdate = async (appId, status) => {
    setUpdating(appId)
    setUpdateError("")

    try {
      await api.put(`/applications/${appId}`, { status })
      refetch()
    } catch (error) {
      setUpdateError(error.response?.data?.message || "Failed to update status")
    } finally {
      setUpdating(null)
    }
  }

  if (loading)
    return (
      <div className="loading-center">
        <LoadingSpinner size="lg" />
      </div>
    )

  return (
    <div className="applications-page">
      <div className="container">
        <h1>Manage Applications</h1>

        {error && <ErrorAlert message={error} />}
        {updateError && <ErrorAlert message={updateError} onClose={() => setUpdateError("")} />}

        {data?.length > 0 ? (
          <div className="applications-list employer">
            {data.map((app) => (
              <div key={app.id} className="application-card employer">
                <div className="app-header">
                  <div className="app-title">
                    <h3>{app.seeker_name}</h3>
                    <p>{app.job_title}</p>
                  </div>
                  <div className="app-email">{app.seeker_email}</div>
                </div>
                <div className="app-actions">
                  <button
                    className="action-btn accept"
                    onClick={() => handleStatusUpdate(app.id, "accepted")}
                    disabled={updating === app.id}
                  >
                    Accept
                  </button>
                  <button
                    className="action-btn shortlist"
                    onClick={() => handleStatusUpdate(app.id, "shortlisted")}
                    disabled={updating === app.id}
                  >
                    Shortlist
                  </button>
                  <button
                    className="action-btn reject"
                    onClick={() => handleStatusUpdate(app.id, "rejected")}
                    disabled={updating === app.id}
                  >
                    Reject
                  </button>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="empty-state">
            <p>No applications yet.</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default ManageApplications
