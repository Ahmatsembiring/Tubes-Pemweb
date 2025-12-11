"use client"

import { useState } from "react"
import { Link } from "react-router-dom"
import { useFetch } from "../hooks/useFetch"
import api from "../services/api"
import LoadingSpinner from "../components/LoadingSpinner"
import ErrorAlert from "../components/ErrorAlert"
import "./ManageJobs.css"

function ManageJobs() {
  const { data, loading, error, refetch } = useFetch("/jobs/employer/my-jobs")
  const [deleting, setDeleting] = useState(null)
  const [deleteError, setDeleteError] = useState("")

  const handleDelete = async (jobId) => {
    if (!window.confirm("Are you sure you want to delete this job?")) return

    setDeleting(jobId)
    setDeleteError("")

    try {
      await api.delete(`/jobs/${jobId}`)
      refetch()
    } catch (error) {
      setDeleteError(error.response?.data?.message || "Failed to delete job")
    } finally {
      setDeleting(null)
    }
  }

  if (loading)
    return (
      <div className="loading-center">
        <LoadingSpinner size="lg" />
      </div>
    )

  return (
    <div className="manage-jobs">
      <div className="container">
        <div className="manage-header">
          <h1>My Jobs</h1>
          <Link to="/post-job" className="btn btn-primary">
            Post New Job
          </Link>
        </div>

        {error && <ErrorAlert message={error} />}
        {deleteError && <ErrorAlert message={deleteError} onClose={() => setDeleteError("")} />}

        {data?.length > 0 ? (
          <div className="jobs-table">
            <table>
              <thead>
                <tr>
                  <th>Title</th>
                  <th>Location</th>
                  <th>Type</th>
                  <th>Salary</th>
                  <th>Posted</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {data.map((job) => (
                  <tr key={job.id}>
                    <td className="title-cell">
                      <strong>{job.title}</strong>
                    </td>
                    <td>{job.location}</td>
                    <td>
                      <span className="type-badge">{job.type}</span>
                    </td>
                    <td>Rp{job.salary.toLocaleString("id-ID")}</td>
                    <td>{new Date(job.created_at).toLocaleDateString()}</td>
                    <td>
                      <div className="action-buttons">
                        <button className="btn-small btn-edit">Edit</button>
                        <button
                          className="btn-small btn-delete"
                          onClick={() => handleDelete(job.id)}
                          disabled={deleting === job.id}
                        >
                          {deleting === job.id ? "Deleting..." : "Delete"}
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="empty-state">
            <p>No jobs posted yet.</p>
            <Link to="/post-job" className="btn btn-primary">
              Post Your First Job
            </Link>
          </div>
        )}
      </div>
    </div>
  )
}

export default ManageJobs
