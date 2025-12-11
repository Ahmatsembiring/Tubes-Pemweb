"use client"

import { useState, useEffect } from "react"
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom"
import AuthContext from "./context/AuthContext"
import Navbar from "./components/Navbar"
import ProtectedRoute from "./components/ProtectedRoute"

// Pages
import Home from "./pages/Home"
import Register from "./pages/Register"
import Login from "./pages/Login"
import JobBrowser from "./pages/JobBrowser"
import JobDetail from "./pages/JobDetail"
import PostJob from "./pages/PostJob"
import ManageJobs from "./pages/ManageJobs"
import MyApplications from "./pages/MyApplications"
import ManageApplications from "./pages/ManageApplications"
import Profile from "./pages/Profile"
import NotFound from "./pages/NotFound"

import "./App.css"

function App() {
  const [auth, setAuth] = useState(null)
  const [loading, setLoading] = useState(true)

  // Load auth from localStorage on mount
  useEffect(() => {
    const token = localStorage.getItem("token")
    const user = localStorage.getItem("user")

    if (token && user) {
      setAuth({
        token,
        user: JSON.parse(user),
        isAuthenticated: true,
      })
    }

    setLoading(false)
  }, [])

  const login = (token, user) => {
    localStorage.setItem("token", token)
    localStorage.setItem("user", JSON.stringify(user))
    setAuth({
      token,
      user,
      isAuthenticated: true,
    })
  }

  const logout = () => {
    localStorage.removeItem("token")
    localStorage.removeItem("user")
    setAuth(null)
  }

  if (loading) {
    return (
      <div className="loading-container">
        <div className="spinner"></div>
      </div>
    )
  }

  return (
    <BrowserRouter>
      <AuthContext.Provider value={{ auth, login, logout }}>
        <Navbar />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/register" element={auth?.isAuthenticated ? <Navigate to="/jobs" /> : <Register />} />
            <Route path="/login" element={auth?.isAuthenticated ? <Navigate to="/jobs" /> : <Login />} />

            <Route path="/jobs" element={<JobBrowser />} />
            <Route path="/jobs/:id" element={<JobDetail />} />

            <Route
              path="/post-job"
              element={
                <ProtectedRoute role="employer">
                  <PostJob />
                </ProtectedRoute>
              }
            />
            <Route
              path="/manage-jobs"
              element={
                <ProtectedRoute role="employer">
                  <ManageJobs />
                </ProtectedRoute>
              }
            />
            <Route
              path="/manage-applications"
              element={
                <ProtectedRoute role="employer">
                  <ManageApplications />
                </ProtectedRoute>
              }
            />

            <Route
              path="/my-applications"
              element={
                <ProtectedRoute role="job_seeker">
                  <MyApplications />
                </ProtectedRoute>
              }
            />
            <Route
              path="/profile"
              element={
                <ProtectedRoute>
                  <Profile />
                </ProtectedRoute>
              }
            />

            <Route path="*" element={<NotFound />} />
          </Routes>
        </main>
      </AuthContext.Provider>
    </BrowserRouter>
  )
}

export default App
