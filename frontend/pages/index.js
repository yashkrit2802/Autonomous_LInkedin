// pages/index.js
import React from 'react'
import Link from 'next/link'
import PostEditor from '../components/PostEditor'

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-4xl mx-auto bg-white rounded-lg shadow-xl p-8">
        <header className="flex justify-between items-center mb-6 border-b pb-4">
          <h1 className="text-3xl font-bold text-gray-800">Influence OS — Dashboard</h1>
          {/* This is a temporary login link. This will be updated once authentication is fully integrated. */}
          <Link href="/login" className="px-4 py-2 text-white bg-blue-600 rounded-md hover:bg-blue-700 transition-colors">
            Login with LinkedIn
          </Link>
        </header>

        <PostEditor />
      </div>
    </div>
  )
}