import { useState } from 'react'

type ChatResponse = {
  assistant_message: string
  extracted_requirements: Record<string, unknown>
  ready_to_generate: boolean
}

type GenerateResponse = {
  project_id: string
  verification: {
    passed: boolean
    checks: Array<{name: string; passed: boolean}>
  }
  files: string[]
}

const api = 'http://localhost:8000/api'

export function App() {
  const [session, setSession] = useState<string | null>(null)
  const [message, setMessage] = useState('')
  const [chat, setChat] = useState<string[]>([])
  const [requirements, setRequirements] = useState<Record<string, unknown>>({})
  const [generated, setGenerated] = useState<GenerateResponse | null>(null)

  const ensureSession = async () => {
    if (session) return session
    const res = await fetch(`${api}/session`, { method: 'POST' })
    const data = await res.json()
    setSession(data.session_id)
    return data.session_id as string
  }

  const send = async () => {
    const sid = await ensureSession()
    const res = await fetch(`${api}/chat/${sid}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message }),
    })
    const data: ChatResponse = await res.json()
    setChat((prev) => [...prev, `You: ${message}`, `Assistant: ${data.assistant_message}`])
    setRequirements(data.extracted_requirements)
    setMessage('')
  }

  const generate = async () => {
    if (!session) return
    const res = await fetch(`${api}/generate/${session}`, { method: 'POST' })
    const data: GenerateResponse = await res.json()
    setGenerated(data)
  }

  return (
    <div className="layout">
      <section>
        <h1>Intent-to-Executable Platform</h1>
        <textarea value={message} onChange={(e) => setMessage(e.target.value)} placeholder="Describe your app..." />
        <div className="actions">
          <button onClick={send}>Send</button>
          <button onClick={generate} disabled={!session}>Generate Project</button>
        </div>
        <div className="chat">{chat.map((line, i) => <p key={i}>{line}</p>)}</div>
      </section>
      <section>
        <h2>Extracted Requirements</h2>
        <pre>{JSON.stringify(requirements, null, 2)}</pre>
        <h2>Project Preview</h2>
        {generated ? (
          <>
            <p>Project ID: {generated.project_id}</p>
            <p>Status: {generated.verification.passed ? 'Passed' : 'Failed'}</p>
            <ul>{generated.files.map((f) => <li key={f}>{f}</li>)}</ul>
            <a href={`http://localhost:8000/api/projects/${generated.project_id}/download`}>Download ZIP</a>
          </>
        ) : <p>No project generated yet.</p>}
      </section>
    </div>
  )
}
