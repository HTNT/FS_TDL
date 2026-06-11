import axios from '@/lib/axios'

export interface User {
  id: number
  email: string
  username: string
  is_active: boolean
  is_superuser: boolean
  created_at: string
}

export const usersApi = {
  getUsers: async () => {
    const { data } = await axios.get<User[]>('/users/')
    return data
  },

  getUser: async (userId: number) => {
    const { data } = await axios.get<User>(`/users/${userId}`)
    return data
  },
}
