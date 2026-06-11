import axios from '@/lib/axios'

export interface LoginCredentials {
  username: string
  password: string
}

export interface RegisterData {
  email: string
  username: string
  password: string
}

export interface AuthResponse {
  access_token: string
  token_type: string
}

export const authApi = {
  login: async (credentials: LoginCredentials) => {
    const formData = new FormData()
    formData.append('username', credentials.username)
    formData.append('password', credentials.password)
    
    const { data } = await axios.post<AuthResponse>('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    })
    return data
  },

  register: async (userData: RegisterData) => {
    const { data } = await axios.post('/auth/register', userData)
    return data
  },
}
