'use client'

import PlayerCard from '@/components/PlayerCard'
import { Suspense, useEffect, useState } from 'react'

interface Player {
  player_id: number
  name: string
  position: string
  jersey_number: string | number
}

function LoadingSpinner() {
  return (
    <div className='min-h-screen flex items-center justify-center'>
      <div className='w-8 h-8 border-4 border-black border-t-transparent rounded-full animate-spin'></div>
    </div>
  )
}

function ErrorDisplay({ error }: { error: string }) {
  return (
    <div className='min-h-screen flex items-center justify-center'>
      <div className='text-red-600 text-xl max-w-md text-center'>
        <p className='font-bold mb-4'>Error Loading Player Data</p>
        <p>{error}</p>
        <p className='text-sm mt-4 text-gray-600'>
          Please make sure the backend server is running at
          http://127.0.0.1:5000
        </p>
      </div>
    </div>
  )
}

function PlayerGrid({ players }: { players: Player[] }) {
  return (
    <div className='grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 p-6'>
      {players.map((player, index) => (
        <PlayerCard
          key={index}
          name={player.name}
          position={player.position}
          jerseyNumber={player.jersey_number}
        />
      ))}
    </div>
  )
}

export default function Home() {
  const [players, setPlayers] = useState<Player[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchPlayers = async () => {
      try {
        console.log('Fetching players...')
        const response = await fetch('http://127.0.0.1:5000/api/roster', {
          method: 'GET',
          headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json'
          }
        })

        console.log('Response status:', response.status)

        if (!response.ok) {
          const errorText = await response.text()
          console.error('Error response:', errorText)
          throw new Error(
            `Failed to fetch players: ${response.status} ${errorText}`
          )
        }

        const data = await response.json()
        console.log('Received data:', data)
        console.log('First player data:', data[0])
        console.log('First player jersey number:', data[0]?.jersey_number)
        console.log(
          'All jersey numbers:',
          data.map((p: Player) => ({ name: p.name, jersey: p.jersey_number }))
        )

        if (!Array.isArray(data)) {
          throw new Error('Invalid data format received from API')
        }

        setPlayers(data)
      } catch (err) {
        console.error('Fetch error:', err)
        setError(
          err instanceof Error
            ? err.message
            : 'An error occurred while fetching player data'
        )
      } finally {
        setLoading(false)
      }
    }

    fetchPlayers()
  }, [])

  if (error) {
    return <ErrorDisplay error={error} />
  }

  return (
    <main className='min-h-screen bg-gray-100 py-8'>
      <div className='container mx-auto px-4'>
        <h1 className='text-4xl font-bold text-center mb-8 text-red-600'>
          Boston Red Sox Roster
        </h1>
        <Suspense fallback={<LoadingSpinner />}>
          {loading ? <LoadingSpinner /> : <PlayerGrid players={players} />}
        </Suspense>
      </div>
    </main>
  )
}
