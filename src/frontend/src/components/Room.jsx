import React, { useEffect, useState } from 'react'
import { Link, useParams, useNavigate } from 'react-router-dom'
import axios from 'axios'

import MusicPlayer from './MusicPlayer'
import Swal from 'sweetalert2'

function Room({baseUrl}) {
    const [votes, setVotes] = useState()
    const [guestsControl, setGuestControl] = useState()
    const [isHost, setIsHost] = useState()
    const [spotifyAuthenticated, setSpotifyAuthenticated] = useState(false)
    const [song, setSong] = useState({})

    const { roomCode } = useParams()
    const roomData = {
        isUpdate: isHost,
        control: guestsControl,
        votes: votes,
    }
    const navigate = useNavigate()


    useEffect(() => {
        axios.get(`${baseUrl}/api/room/?code=${roomCode}`)
        .then((res) => {
            if(res.status === 200) {
                setVotes(res.data.votes_to_skip)
                setGuestControl(res.data.guests_pause)
                setIsHost(res.data.is_host)
                if(res.data.is_host) {
                    authenticateSpotify()
                }
            } else {
                navigate('/')
            }
        })
    }, [])

    const authenticateSpotify = () => {
        console.log('authspotify')
        fetch('http://127.0.0.1:8000/spotify/is-authenticated/')
        .then(res => res.json())
        .then((data) => {
            setSpotifyAuthenticated(data.status)
            console.log(`Spotify Authentication: ${data.status}`)
            if(!data.status) {
                console.log(`auth url!`)
                fetch('/spotify/get-auth-url/')
                .then(res => res.json())
                .then(data => window.location.replace(data.url))
            }
        })
    }

    useEffect(() => {
        // console.log(`Spotify Authentication Status Inside UseEffect: ${spotifyAuthenticated}`)
        let interval = setInterval(getCurrentSong, 1000)
        return () => clearInterval(interval)
        // getDummySongData()
    }, [spotifyAuthenticated])

    const getCurrentSong = () => {
        fetch('http://127.0.0.1:8000/spotify/current-song/')
        .then((res) => {
            if(!res.ok) {
                return {}
            }
            else {
                return res.json()
            }
        })
        .then((data) => {
            setSong(data)
        })
    }

    const getDummySongData = () => {
        setSong({
            "title": "Flowers",
            "artist": "Miley Cyrus",
            "duration_ms": 200454,
            "timestamp_ms": 100000,
            "images_urls": {
                "big_img": {
                    "height": 640,
                    "url": "https://i.scdn.co/image/ab67616d0000b273f429549123dbe8552764ba1d",
                    "width": 640
                },
                "med_img": {
                    "height": 300,
                    "url": "https://i.scdn.co/image/ab67616d00001e02f429549123dbe8552764ba1d",
                    "width": 300
                },
                "sm_img": {
                    "height": 64,
                    "url": "https://i.scdn.co/image/ab67616d00004851f429549123dbe8552764ba1d",
                    "width": 64
                }
            },
            "is_playing": false,
            "id": null
        })
    }

        
    const leaveRoom = () => {
        if(isHost) {
            fetch('/api/leave/')
            .then(() => {
                Swal.fire({
                    title: 'Unathenticate With Spotify?',
                    text: "Do you want to delete you authentication tokens from the database?",
                    type: 'warning',
                    showDenyButton: true,
                    confirmButtonText: 'Yes, delete my tokens',
                    denyButtonText: 'No, keep my tokens',
                    confirmButtonColor: '#39cc40',
                    denyButtonColor: '#c9342e',
                    timer: 10000,
                    timerProgressBar: true
                }).then((swalRes) => {
                    console.log(swalRes)
                    if(swalRes.isConfirmed) {
                        const requestOptions = {
                            method: 'DELETE',
                            headers: {'Content-Type': 'application/json'}
                        }
                        fetch('/spotify/delete-token/', requestOptions)
                    }
                    navigate('/')
                } )
            })
        }
        fetch('/api/leave/')
        .then(() => navigate('/'))
    }    
    return (
        <div className='mx-auto text-xl w-1/3 text-center m-2 grid grid-cols-1 border bg-zinc-100 rounded-lg border-zinc-300 drop-shadow-xl'>
            <h1 className='text-3xl text-green-600'><span className='font-semibold text-black'>Room Code:</span> {roomCode}</h1>
            <p className='mt-5'><span className='font-semibold'>Votes To Skip:</span> {votes}</p>
            <p className='mt-5'><span className='font-semibold'>Guests Can Pause:</span> {guestsControl?.toString()}</p>
            <p className='my-5'><span className='font-semibold'>Is This The Host:</span> {isHost?.toString()}</p>
            <MusicPlayer song={song} />
            <Link 
                to='/create-room'
                state={roomData}
                className={isHost ? 'p-2 bg-blue-700 text-white font-medium rounded-md hover:bg-blue-800 w-44 mx-auto' : 'hidden'}
            >
                Settings
            </Link>
            <button 
                className='p-2 bg-rose-600 text-white font-medium rounded-md hover:bg-rose-700 w-52 mx-auto my-4' 
                onClick={leaveRoom}
            >
                Leave Room
            </button>
        </div>
    )
}

export default Room