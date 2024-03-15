import React, { useState } from 'react'

function MusicPlayer(props) {
    const [resMsg, setResMsg] = useState('')
    const timestamp = (props.song.timestamp_ms / props.song.duration_ms) * 100
    
    const controlSong = (e) => {
        const requestOptions = {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                'control': e.target.id
            })
        }
        fetch('/spotify/control/', requestOptions)
        .then((res) => {
            if(!res.ok) {
                setResMsg('Oops...Something Went Wrong :(')
            }
        })
    }
    const pauseSong = () => {
        const requestOptions = {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
        }
        fetch('/spotify/pause/', requestOptions)
        .then((res) => {
            if(!res.ok) setResMsg('Oops...Something went wrong :(')
            else setResMsg(res?.message)

        })
    }
    const playSong = () => {
        const requestOptions = {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
        }
        fetch('/spotify/play/', requestOptions)
        .then((res) => {
            if(!res.ok) setResMsg('Oops...Something went wrong :(')
            else setResMsg(res?.message)
        })
    }
    
    return props.song.title ? (
        <div>
            <div className='grid grid-cols-3 place-items-center w-full bg-gray-200 m-0'>
                <div className='col-span-1 bg-cover bg-center bg-contain'>
                    <img className='bg-cover w-full h-full' src={props.song?.images_urls?.med_img.url} alt='album cover' />
                </div>
                <div className='col-span-2'>
                    <h4 className='text-4xl m-2'>{props.song?.title}</h4>
                    <p className='text-lg font-medium text-gray-500'>{props.song?.artist}</p>
                    <div className='grid grid-cols-3 border'>
                        <button>
                            <span className="material-symbols-outlined text-5xl">skip_previous</span>
                        </button>
                        <button 
                            className='my-2'
                            // onClick={controlSong}
                        >
                            {props.song?.is_playing ? 
                                <span className="material-symbols-outlined text-3xl" id='pause' onClick={pauseSong}>pause_circle</span> :
                                <span className="material-symbols-outlined text-3xl" id='play' onClick={playSong}>play_circle</span>
                            }
                        </button>
                        <button>
                            <span className="material-symbols-outlined text-5xl">skip_next</span>
                        </button>
                    </div>
                </div>
            </div>
            <div className="timestamp">
                <progress max={props.song.duration_ms} value={props.song.timestamp_ms} className='w-full' />
            </div>
            <div>{resMsg}</div>
        </div>
    ) : (
        <div className='text-red-700 my-2 p-1 bg-red-100'>
            Sorry...Something went wrong :(
        </div>
    )
}

export default MusicPlayer