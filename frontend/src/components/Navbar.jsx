"use client"

import { useState } from "react"
import { Link, useNavigate } from "react-router-dom"
import { useAuth } from "../hooks/useAuth"
import "./Navbar.css"

function Navbar() {
  const { auth, logout } = useAuth()
  const navigate = useNavigate()
  const [showMenu, setShowMenu] = useState(false)

  const handleLogout = () => {
    logout()
    setShowMenu(false)
    navigate("/")
  }

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-brand">
          <span className="logo">JobPortal</span>
        </Link>

        <button className="menu-toggle" onClick={() => setShowMenu(!showMenu)}>
          <span></span>
          <span></span>
          <span></span>
        </button>

        <div className={`nav-menu ${showMenu ? "active" : ""}`}>
          <Link to="/jobs" className="nav-link" onClick={() => setShowMenu(false)}>
            Browse Jobs
          </Link>

          {auth?.isAuthenticated ? (
            <>
              {auth.user.role === "employer" && (
                <>
                  <Link to="/post-job" className="nav-link" onClick={() => setShowMenu(false)}>
                    Post Job
                  </Link>
                  <Link to="/manage-jobs" className="nav-link" onClick={() => setShowMenu(false)}>
                    My Jobs
                  </Link>
                  <Link to="/manage-applications" className="nav-link" onClick={() => setShowMenu(false)}>
                    Applications
                  </Link>
                </>
              )}

              {auth.user.role === "job_seeker" && (
                <Link to="/my-applications" className="nav-link" onClick={() => setShowMenu(false)}>
                  My Applications
                </Link>
              )}

              <div className="user-menu">
                <Link to="/profile" className="nav-link" onClick={() => setShowMenu(false)}>
                  Profile
                </Link>
                <span className="user-email">{auth.user.email}</span>
                <button className="logout-btn" onClick={handleLogout}>
                  Logout
                </button>
              </div>
            </>
          ) : (
            <>
              <Link to="/login" className="nav-link login-link" onClick={() => setShowMenu(false)}>
                Login
              </Link>
              <Link to="/register" className="nav-link signup-link" onClick={() => setShowMenu(false)}>
                Sign Up
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  )
}

export default Navbar
