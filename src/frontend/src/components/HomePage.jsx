import React, { useEffect, useState } from 'react'
import { Link, Navigate, useLocation } from 'react-router-dom'

function HomePage() {
  const [roomCode, setRoomCode] = useState(null)
  const location = useLocation()
  if(location.state?.left) {
    setRoomCode(null)
  }

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/in-room/')
    .then(res => res.json())
    .then(data => setRoomCode(data.room_code))
  }, [])
  
  return roomCode ? ( 
    <Navigate to={`/room/${roomCode}`} /> 
    ) : (
      <div className='text-xl w-96 mx-auto text-center h-48 mt-2 dark:text-white dark:bg-slate-800 bg-zinc-50 border rounded-lg border-zinc-300 drop-shadow-md'>
        <h1 className='font-semibold my-2'>House Party</h1>
        <div className="flex gap-6 justify-center mt-5">
          <Link
            className='p-1 bg-sky-300 rounded-sm hover:bg-sky-400 focus:outline-sky-500'
            to='/join'
          >
            Join Room
          </Link>
          <Link
            className='p-1 bg-rose-300 rounded-sm hover:bg-rose-400 focus:outline-rose-500'
            to='/create-room'
          >
            Create Room
          </Link>
        </div>
      </div>
    )
}

export default HomePage