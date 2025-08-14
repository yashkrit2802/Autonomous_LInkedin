// pages/login.js
import React from 'react'

export default function Login() {
  const handleLogin = () => {
    window.location.href = 'http://localhost:8000/auth/login'
  }
  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <div className="bg-white rounded-lg shadow-xl p-8 max-w-sm w-full text-center">
        <h2 className="text-2xl font-semibold text-gray-800 mb-4">Login to Influence OS</h2>
        <p className="text-gray-600 mb-6">Connect your LinkedIn account to get started.</p>
        <button 
          onClick={handleLogin}
          className="w-full px-4 py-2 text-white font-medium bg-blue-600 rounded-md hover:bg-blue-700 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
        >
          Login with LinkedIn
        </button>
      </div>
    </div>
  )
}