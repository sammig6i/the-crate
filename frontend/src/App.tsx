import { ChakraProvider, CSSReset } from '@chakra-ui/react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import AlbumGrid from './components/AlbumGrid'
import AlbumDetail from './components/AlbumDetail'
import AdminDashboard from './components/AdminDashboard'
import Layout from './components/Layout'

const queryClient = new QueryClient()

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ChakraProvider>
        <CSSReset />
        <Router>
          <Layout>
            <Routes>
              <Route path="/" element={<AlbumGrid />} />
              <Route path="/albums/:id" element={<AlbumDetail />} />
              <Route path="/admin" element={<AdminDashboard />} />
            </Routes>
          </Layout>
        </Router>
      </ChakraProvider>
    </QueryClientProvider>
  )
}

export default App 