import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import Home from './pages/Home'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-100">
        <nav className="bg-white shadow-lg">
          <div className="max-w-7xl mx-auto px-4">
            <div className="flex justify-between items-center h-16">
              <div className="flex space-x-4">
                <Link to="/" className="text-gray-800 hover:text-blue-600 px-3 py-2">
                  Home
                </Link>
                <Link to="/dashboard" className="text-gray-800 hover:text-blue-600 px-3 py-2">
                  Dashboard
                </Link>
              </div>
              <div className="flex space-x-4">
                <Link to="/login" className="text-gray-800 hover:text-blue-600 px-3 py-2">
                  Login
                </Link>
                <Link to="/register" className="text-gray-800 hover:text-blue-600 px-3 py-2">
                  Register
                </Link>
              </div>
            </div>
          </div>
        </nav>

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/dashboard" element={<Dashboard />} />
        </Routes>
      </div>
    </BrowserRouter>
  )
}

export default App
