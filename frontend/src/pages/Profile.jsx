"use client"

import { useState, useEffect } from "react"
import { useAuth } from "../hooks/useAuth"
import api from "../services/api"
import FormInput from "../components/FormInput"
import ErrorAlert from "../components/ErrorAlert"
import LoadingSpinner from "../components/LoadingSpinner"
import "./Profile.css"

function Profile() {
  const { auth } = useAuth()
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    skills: "",
    experience: "",
    cv_url: "",
  })
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [apiError, setApiError] = useState("")
  const [successMessage, setSuccessMessage] = useState("")
  const [uploadingFile, setUploadingFile] = useState(false)

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await api.get("/profile")
        setFormData({
          name: response.data.name || "",
          email: response.data.email || "",
          skills: response.data.skills || "",
          experience: response.data.experience || "",
          cv_url: response.data.cv_url || "",
        })
      } catch (error) {
        setApiError("Failed to load profile")
      } finally {
        setLoading(false)
      }
    }

    fetchProfile()
  }, [])

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }))
  }

  const handleFileUpload = async (e) => {
    const file = e.target.files?.[0]
    if (!file) return

    setUploadingFile(true)
    setApiError("")

    try {
      // Upload to Vercel Blob
      const formDataObj = new FormData()
      formDataObj.append("file", file)

      const response = await api.post("/profile/upload-cv", formDataObj, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })

      setFormData((prev) => ({
        ...prev,
        cv_url: response.data.cv_url,
      }))
      setSuccessMessage("CV uploaded successfully")
    } catch (error) {
      setApiError(error.response?.data?.message || "Failed to upload CV")
    } finally {
      setUploadingFile(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setApiError("")
    setSuccessMessage("")
    setSaving(true)

    try {
      await api.put("/profile", formData)
      setSuccessMessage("Profile updated successfully")
    } catch (error) {
      setApiError(error.response?.data?.message || "Failed to update profile")
    } finally {
      setSaving(false)
    }
  }

  if (loading)
    return (
      <div className="loading-center">
        <LoadingSpinner size="lg" />
      </div>
    )

  return (
    <div className="profile-page">
      <div className="container">
        <h1>My Profile</h1>

        <div className="profile-container">
          {apiError && <ErrorAlert message={apiError} onClose={() => setApiError("")} />}
          {successMessage && (
            <div className="success-alert">
              <p>{successMessage}</p>
            </div>
          )}

          <form onSubmit={handleSubmit} className="profile-form">
            <div className="form-section">
              <h2>Personal Information</h2>

              <FormInput
                label="Full Name"
                value={formData.name}
                onChange={handleChange}
                name="name"
                placeholder="Your name"
              />

              <FormInput
                label="Email"
                type="email"
                value={formData.email}
                onChange={handleChange}
                name="email"
                placeholder="your@email.com"
                disabled
              />
            </div>

            {auth?.user?.role === "job_seeker" && (
              <>
                <div className="form-section">
                  <h2>Professional Information</h2>

                  <div className="form-group">
                    <label className="form-label">Skills</label>
                    <textarea
                      name="skills"
                      value={formData.skills}
                      onChange={handleChange}
                      placeholder="List your skills (one per line)"
                      className="form-textarea"
                      rows="4"
                    ></textarea>
                  </div>

                  <div className="form-group">
                    <label className="form-label">Experience</label>
                    <textarea
                      name="experience"
                      value={formData.experience}
                      onChange={handleChange}
                      placeholder="Describe your work experience"
                      className="form-textarea"
                      rows="4"
                    ></textarea>
                  </div>
                </div>

                <div className="form-section">
                  <h2>Resume/CV</h2>

                  <div className="file-upload">
                    <input
                      type="file"
                      accept=".pdf,.doc,.docx"
                      onChange={handleFileUpload}
                      disabled={uploadingFile}
                      id="cv-upload"
                    />
                    <label htmlFor="cv-upload" className="upload-label">
                      {uploadingFile ? (
                        <>
                          <LoadingSpinner size="sm" /> Uploading...
                        </>
                      ) : (
                        "Choose CV/Resume File"
                      )}
                    </label>
                    {formData.cv_url && (
                      <p className="file-info">
                        <strong>Current CV:</strong> <a href={formData.cv_url}>View CV</a>
                      </p>
                    )}
                  </div>
                </div>
              </>
            )}

            <button type="submit" className="btn btn-primary btn-large" disabled={saving}>
              {saving ? <LoadingSpinner size="sm" /> : "Save Profile"}
            </button>
          </form>
        </div>
      </div>
    </div>
  )
}

export default Profile
