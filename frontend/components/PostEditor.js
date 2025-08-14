import React, {useState} from 'react'
import axios from 'axios'

export default function PostEditor(){
  const [topic, setTopic] = useState('')
  const [draft, setDraft] = useState('')
  const [loading, setLoading] = useState(false)
  const [publishing, setPublishing] = useState(false)

  async function generatePost(){
    if (!topic) return;
    setLoading(true)
    try{
      const res = await axios.post('http://localhost:8000/api/generate-post', { topic, tone: 'professional' })
      setDraft(res.data.draft)
    }catch(err){
      alert('Error generating post: ' + (err.response?.data?.detail || err.message))
    }finally{
      setLoading(false)
    }
  }

  async function publishPost(){
    if (!draft) return;
    setPublishing(true)
    try{
      // Call the new publish-post endpoint
      const res = await axios.post('http://localhost:8000/api/publish-post', { topic, tone: 'professional' })
      alert('Post published successfully! Check your LinkedIn profile.')
      console.log(res.data);
      setDraft(''); // Clear the draft after successful publish
      setTopic(''); // Clear the topic as well
    }catch(err){
      alert('Error publishing post: ' + (err.response?.data?.detail || err.message))
    }finally{
      setPublishing(false)
    }
  }

  return (
    <div>
      <h3 className="text-xl font-semibold text-gray-700 mb-4">Generate & Publish LinkedIn Post</h3>
      <div className="flex flex-col sm:flex-row gap-4 mb-6">
        <input 
          value={topic}
          onChange={e=>setTopic(e.target.value)}
          placeholder="Enter a topic, e.g. 'AI for healthcare'"
          className="flex-grow px-4 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 focus:outline-none"
          disabled={loading || publishing}
        />
        <button 
          onClick={generatePost}
          disabled={!topic || loading || publishing}
          className={`px-6 py-2 text-white font-medium rounded-md transition-colors ${
            !topic || loading || publishing ? 'bg-gray-400 cursor-not-allowed' : 'bg-green-600 hover:bg-green-700'
          }`}
        >
          {loading ? 'Generating...' : 'Generate Draft'}
        </button>
      </div>

      <div className="bg-gray-50 border border-gray-200 rounded-md p-4 mb-4">
        <textarea 
          value={draft}
          onChange={e=>setDraft(e.target.value)}
          rows={10}
          placeholder="Your generated post will appear here..."
          className="w-full h-full p-2 bg-transparent border-none focus:outline-none resize-none text-gray-700"
          readOnly // Make the draft textarea read-only after generation
        />
      </div>

      <button
        onClick={publishPost}
        disabled={!draft || publishing}
        className={`w-full px-6 py-2 text-white font-medium rounded-md transition-colors ${
          !draft || publishing ? 'bg-blue-300 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700'
        }`}
      >
        {publishing ? 'Publishing...' : 'Publish to LinkedIn'}
      </button>

    </div>
  )
} 