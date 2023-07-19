import { BrowserRouter as Router, Routes, Route} from 'react-router-dom';
import HomePage from './components/HomePage';
import CreateRoom from './components/CreateRoom';
import Room from './components/Room';
import RoomJoinPage from './components/RoomJoinPage';

function App() {

  return (
    <>
      <Router>
        <Routes>
          <Route path='/' element={ <HomePage /> } />
          <Route path='/create-room' element={ <CreateRoom /> } />
          <Route path='/room/:roomCode' element={ <Room />} />
          <Route path='/join' element={ <RoomJoinPage /> } />
        </Routes>
      </Router>
    </>
  )
}

export default App
