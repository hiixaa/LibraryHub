
import { BrowserRouter, Routes, Route } from 'react-router-dom'

import './App.css'

import Navbar from './components/Navbar'
import Home from './pages/Home'
import BookDetails from './pages/BookDetails'
import MyLoans from './pages/MyLoans'
import Basket from './pages/Basket'
import NotFound from './pages/NotFound'

import { MemberProvider } from './context/MemberContext'
import { BasketProvider } from './context/BasketContext'

function App() {
  return (
    <MemberProvider>
      <BasketProvider>
        <BrowserRouter>
          <Navbar />

          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/books/:isbn" element={<BookDetails />} />
            <Route path="/me" element={<MyLoans />} />
            <Route path="/basket" element={<Basket />} />
            <Route path="/admin/add" element={<Home />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </BrowserRouter>
      </BasketProvider>
    </MemberProvider>
  )
}

export default App

