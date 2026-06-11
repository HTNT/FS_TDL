export default function Home() {
  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Welcome to Full-Stack App
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          React + TypeScript + FastAPI
        </p>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-2xl font-semibold mb-2">Frontend</h2>
            <ul className="text-left text-gray-600">
              <li>✓ React 18</li>
              <li>✓ TypeScript</li>
              <li>✓ React Router</li>
              <li>✓ TanStack Query</li>
              <li>✓ React Hook Form</li>
              <li>✓ Tailwind CSS</li>
              <li>✓ Zustand</li>
            </ul>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-2xl font-semibold mb-2">Backend</h2>
            <ul className="text-left text-gray-600">
              <li>✓ FastAPI</li>
              <li>✓ SQLAlchemy</li>
              <li>✓ PostgreSQL</li>
              <li>✓ Redis</li>
              <li>✓ JWT Auth</li>
              <li>✓ Pytest</li>
            </ul>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-2xl font-semibold mb-2">DevOps</h2>
            <ul className="text-left text-gray-600">
              <li>✓ Docker</li>
              <li>✓ Docker Compose</li>
              <li>✓ Uvicorn</li>
              <li>✓ Vite</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}
