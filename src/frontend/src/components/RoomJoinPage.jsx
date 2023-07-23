import {React, useState} from 'react'
import { Link, useNavigate } from 'react-router-dom'

function RoomJoinPage() {
    const [input, setInput] = useState()
    const [error, setError] = useState()
    
    const handleChange = (e) => {
        setInput(e.target.value)
        setError()
    }
    const navigate = useNavigate()
    const handleSubmit = () => {
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type':'application/json' },
            body: JSON.stringify({
                'code': input,
            })
        }
        fetch('http://127.0.0.1:8000/api/join/', requestOptions).then((res) => {
            if(res.ok) navigate(`/room/${input}`)
            else {
                setError('Room not found. Code Incorrect')
            }
        })
    }
  return (
    <div className=
    'grid grid-cols-1 w-96 p-5 text-xl text-center mx-auto mt-2 border-2 shadow-lg bg-zinc-50 rounded-lg'>
        <h1 className='text-3xl font-semibold'>Join A Room</h1>
        <input placeholder='Enter a Room Code'
        className='w-56 p-2 mt-4 mx-auto text-center border-2 rounded-md focus:outline-none focus:border-blue-800'
        onChange={handleChange} />
        <p className={error ? 'text-red-500 text-sm' : 'hidden'}>{error}</p>
        <button className='bg-blue-700 text-white w-40 mx-auto font-medium p-2 mt-4 rounded-md hover:bg-blue-800 focus:outline-none focus:border-blue-950'
        onClick={handleSubmit}>
            Enter Room
        </button>
        <Link 
            to = '/'
            className='bg-rose-600 text-white w-32 mx-auto font-medium p-2 mt-4 rounded-md hover:bg-rose-700 focus:outline-none focus:border-blue-950'
        >
            Back
        </Link>
    </div>
  )
}

export default RoomJoinPage