import { Link } from "react-router-dom"
import "./Home.css"

function Home() {
  return (
    <div className="home-page">
      <section className="hero">
        <div className="hero-content">
          <h1>Find Your Dream Job</h1>
          <p>Discover thousands of job opportunities from top companies</p>
          <div className="hero-buttons">
            <Link to="/jobs" className="btn btn-primary">
              Browse Jobs
            </Link>
            <Link to="/register" className="btn btn-secondary">
              Get Started
            </Link>
          </div>
        </div>
      </section>

      <section className="features">
        <h2>Why JobPortal?</h2>
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon">1</div>
            <h3>Easy Application</h3>
            <p>Apply to jobs with a single click and track your applications</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">2</div>
            <h3>Smart Matching</h3>
            <p>Get matched with jobs that fit your skills and experience</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">3</div>
            <h3>For Employers</h3>
            <p>Post jobs and find the best candidates for your company</p>
          </div>
        </div>
      </section>
    </div>
  )
}

export default Home
