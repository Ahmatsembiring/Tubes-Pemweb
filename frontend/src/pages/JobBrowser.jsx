"use client"

import { useState } from "react"
import { Link } from "react-router-dom"
import { useFetch } from "../hooks/useFetch"
import LoadingSpinner from "../components/LoadingSpinner"
import ErrorAlert from "../components/ErrorAlert"
import "./JobBrowser.css"

function JobBrowser() {
  const [filters, setFilters] = useState({
    search: "",
    location: "",
    jobType: "",
    salaryMin: "",
    salaryMax: "",
  })
  const [page, setPage] = useState(1)

  const queryParams = new URLSearchParams()
  if (filters.search) queryParams.append("search", filters.search)
  if (filters.location) queryParams.append("location", filters.location)
  if (filters.jobType) queryParams.append("type", filters.jobType)
  if (filters.salaryMin) queryParams.append("salary_min", filters.salaryMin)
  if (filters.salaryMax) queryParams.append("salary_max", filters.salaryMax)
  queryParams.append("page", page)

  const { data, loading, error } = useFetch(`/jobs?${queryParams}`)

  const handleFilterChange = (e) => {
    const { name, value } = e.target
    setFilters((prev) => ({
      ...prev,
      [name]: value,
    }))
    setPage(1)
  }

  return (
    <div className="job-browser">
      <div className="container">
        <h1>Job Opportunities</h1>

        <div className="browser-layout">
          <aside className="filters-sidebar">
            <h3>Filters</h3>

            <div className="filter-group">
              <label>Search</label>
              <input
                type="text"
                name="search"
                value={filters.search}
                onChange={handleFilterChange}
                placeholder="Job title, skills..."
                className="filter-input"
              />
            </div>

            <div className="filter-group">
              <label>Location</label>
              <select name="location" value={filters.location} onChange={handleFilterChange} className="filter-input">
                <option value="">All Locations</option>
                <option value="Jakarta">Jakarta</option>
                <option value="Surabaya">Surabaya</option>
                <option value="Bandung">Bandung</option>
                <option value="Remote">Remote</option>
              </select>
            </div>

            <div className="filter-group">
              <label>Job Type</label>
              <select name="jobType" value={filters.jobType} onChange={handleFilterChange} className="filter-input">
                <option value="">All Types</option>
                <option value="Full-time">Full-time</option>
                <option value="Part-time">Part-time</option>
                <option value="Contract">Contract</option>
                <option value="Internship">Internship</option>
              </select>
            </div>

            <div className="filter-group">
              <label>Salary Range</label>
              <div className="salary-inputs">
                <input
                  type="number"
                  name="salaryMin"
                  value={filters.salaryMin}
                  onChange={handleFilterChange}
                  placeholder="Min"
                  className="filter-input"
                />
                <span>-</span>
                <input
                  type="number"
                  name="salaryMax"
                  value={filters.salaryMax}
                  onChange={handleFilterChange}
                  placeholder="Max"
                  className="filter-input"
                />
              </div>
            </div>

            <button className="btn btn-primary" style={{ width: "100%" }} onClick={() => setPage(1)}>
              Apply Filters
            </button>
          </aside>

          <main className="jobs-list">
            {error && <ErrorAlert message={error} />}

            {loading ? (
              <div className="loading-center">
                <LoadingSpinner size="lg" />
              </div>
            ) : data?.jobs?.length > 0 ? (
              <>
                <div className="jobs-count">Found {data.total} jobs</div>
                {data.jobs.map((job) => (
                  <Link key={job.id} to={`/jobs/${job.id}`} className="job-item">
                    <div className="job-header">
                      <h3>{job.title}</h3>
                      <span className="job-type-badge">{job.type}</span>
                    </div>
                    <p className="job-company">{job.company_name}</p>
                    <p className="job-description">{job.description.substring(0, 150)}...</p>
                    <div className="job-footer">
                      <div className="job-info">
                        <span className="job-location">{job.location}</span>
                        <span className="job-salary">Rp{job.salary.toLocaleString("id-ID")}</span>
                      </div>
                      <div className="job-date">{new Date(job.created_at).toLocaleDateString()}</div>
                    </div>
                  </Link>
                ))}

                {data.pages > 1 && (
                  <div className="pagination">
                    <button onClick={() => setPage(Math.max(1, page - 1))} disabled={page === 1}>
                      Previous
                    </button>
                    <span>
                      Page {page} of {data.pages}
                    </span>
                    <button onClick={() => setPage(Math.min(data.pages, page + 1))} disabled={page === data.pages}>
                      Next
                    </button>
                  </div>
                )}
              </>
            ) : (
              <div className="empty-state">
                <p>No jobs found. Try adjusting your filters.</p>
              </div>
            )}
          </main>
        </div>
      </div>
    </div>
  )
}

export default JobBrowser
