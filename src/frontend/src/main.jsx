import React from 'react'
import ReactDOM from 'react-dom/client'
import './index.css'

import { BrowserRouter as Router, Routes, Route} from 'react-router-dom';
import HomePage from './components/HomePage';
import CreateRoom from './components/CreateRoom';
import Room from './components/Room';
import RoomJoinPage from './components/RoomJoinPage';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <Router>
        <Routes>
          <Route path='/' element={ <HomePage /> } />
          <Route path='/create-room' element={ <CreateRoom /> } />
          <Route path='/room/:roomCode' element={ <Room />} />
          <Route path='/join' element={ <RoomJoinPage /> } />
        </Routes>
      </Router>
  </React.StrictMode>,
)
