"use client"
import { Navigate } from "react-router-dom"
import { useAuth } from "../hooks/useAuth"

function ProtectedRoute({ children, role }) {
  const { auth } = useAuth()

  if (!auth?.isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  if (role && auth.user.role !== role) {
    return <Navigate to="/" replace />
  }

  return children
}

export default ProtectedRoute
