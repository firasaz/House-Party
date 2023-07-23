import React, { useEffect, useState } from 'react'
import { useNavigate, useLocation, Link } from 'react-router-dom'
import Swal from 'sweetalert2'

function CreateRoom() {
  const [guestControl, setGuestControl] = useState(true)
  const [guestVotes, setGuestVotes] = useState(2)
  const [title, setTitle] = useState('Create A Room')
  
  const location = useLocation()
  const propsData = location.state
  useEffect(() => {
    if(propsData) {
      console.log(propsData)
      setGuestControl(propsData.control)
      setGuestVotes(propsData.votes)
      setTitle(propsData.isUpdate ? 'Update Room' : 'Create A Room')
      console.log(`propsData:${propsData.control}`)
    }
  }, [])

  const handleChange = (e) => {
    if(e.target.name === 'control') {
      e.target.id === 'play' ? setGuestControl(true) : setGuestControl(false)
    }
    else {
      setGuestVotes(e.target.value)
    }
  }

  const navigate = useNavigate();
  const handleCreate = () => {
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        guests_pause: guestControl,
        votes_to_skip: guestVotes
      }),
    }
    fetch('http://127.0.0.1:8000/api/create-room/', requestOptions)
    .then((res) => res.json())
    .then((data) => {
      navigate(`/room/${data.code}`)
    })
  }
  
  const handleUpdate = () => {
    const requestOptions = {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        guests_pause: guestControl,
        votes_to_skip: guestVotes
      }),
    }
    fetch('http://127.0.0.1:8000/api/update/', requestOptions)
    .then((res) => res.json())
    .then((data) => {
      Swal.fire({
        title: 'Update Room Alert',
        text: 'Room Updated Successfully',
        toast: true,
        timer: 3000,
        position: 'top-right',
        timerProgressBar: true,
      }).then(() => {
        navigate(`/room/${data.code}`)
      })
    })
  }

  return (
    <div className='mx-auto mt-2 p-5 w-96 text-xl text-center border-2 shadow-lg bg-zinc-50 rounded-lg'>
      <h1 className='font-semibold text-3xl'>{title}</h1>
      <p className='my-2'>Guest Control of Playback State</p>
      <div className="form">
        <input className='w-32' id='play' type="radio" name='control' onChange={handleChange} checked={guestControl} />
        <input className='w-32' id='notPlay' type="radio" name='control' onChange={handleChange} checked={!guestControl} />
        <label className='mx-4 p-1 rounded-md bg-gray-100' htmlFor='play'>Play/Pause</label>
        <label className='mx-4 p-1 rounded-md bg-gray-100' htmlFor='notPlay'>No Control</label>
        <div className='votes grid grid-cols-1'>
          <input className='border-b-2 mt-3 p-1 pl-2 w-64 m-auto text-center focus:outline-none focus:border-blue-200' 
          name='votes' type='number' min={1} max={10} value={guestVotes} required 
          onChange={handleChange} />
          <label className='text-sm text-gray-600 mt-1'>Votes Required To Skip Song</label>
          <button className='mt-3 p-2 text-white font-medium bg-blue-700 w-48 m-auto rounded-md hover:bg-blue-800' 
            onClick={propsData?.isUpdate ? handleUpdate : handleCreate} 
            type='submit'
          >
            {title}
          </button>
          <Link
            to='/'
            className={propsData?.isUpdate ? 'hidden' : 'mt-3 p-2 text-white font-medium bg-rose-600 w-24 m-auto rounded-md hover:bg-rose-700'}
          >
            Back
          </Link>
        </div>
      </div>
    </div>
  )
}

export default CreateRoom