"use client"

import { useFetch } from "../hooks/useFetch"
import LoadingSpinner from "../components/LoadingSpinner"
import ErrorAlert from "../components/ErrorAlert"
import "./Applications.css"

function MyApplications() {
  const { data, loading, error } = useFetch("/applications/my-applications")

  const getStatusColor = (status) => {
    switch (status) {
      case "accepted":
        return "#00a854"
      case "rejected":
        return "#f5222d"
      case "shortlisted":
        return "#faad14"
      default:
        return "#1890ff"
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
        <h1>My Applications</h1>

        {error && <ErrorAlert message={error} />}

        {data?.length > 0 ? (
          <div className="applications-list">
            {data.map((app) => (
              <div key={app.id} className="application-card">
                <div className="app-header">
                  <div className="app-title">
                    <h3>{app.job_title}</h3>
                    <p>{app.company_name}</p>
                  </div>
                  <span className="app-status" style={{ backgroundColor: getStatusColor(app.status) }}>
                    {app.status.charAt(0).toUpperCase() + app.status.slice(1)}
                  </span>
                </div>
                <div className="app-details">
                  <span>Applied: {new Date(app.applied_date).toLocaleDateString()}</span>
                  <span>{app.location}</span>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="empty-state">
            <p>You haven't applied to any jobs yet.</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default MyApplications
