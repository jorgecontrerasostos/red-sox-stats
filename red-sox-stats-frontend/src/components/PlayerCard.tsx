interface PlayerCardProps {
  name: string
  position: string
  jerseyNumber: string | number | null
}

export default function PlayerCard({
  name,
  position,
  jerseyNumber
}: PlayerCardProps) {
  return (
    <div className='bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-300 p-6'>
      <div className='flex flex-col items-center text-center'>
        <h3 className='text-xl font-bold text-gray-800 mb-2'>{name}</h3>
        <div className='flex gap-4 items-center'>
          <span className='text-gray-600'>{position}</span>
          {jerseyNumber && (
            <span className='text-red-600 font-bold'>#{jerseyNumber}</span>
          )}
        </div>
      </div>
    </div>
  )
}
