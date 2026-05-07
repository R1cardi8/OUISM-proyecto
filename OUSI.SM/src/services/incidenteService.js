import axios from 'axios'

const api = axios.create({
  baseURL: 'http://127.0.0.1:3000/api',
  timeout: 8000,
})

export default {
  // Incidentes
  getIncidentes()        { return api.get('/incidentes')         },
  createIncidente(data)  { return api.post('/incidentes', data)  },
  deleteIncidente(id)    { return api.delete(`/incidentes/${id}`) },

  // Usuarios
  registro(data)         { return api.post('/registro', data)    },
  login(data)            { return api.post('/login', data)       },
}