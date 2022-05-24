interface StartGameProps {
    questions: {
        id: number;
        content: string;
    }[]
    teams: {
        id: number;
        name: string;
        score: number;
    }[]
    onClick: () => void
}


const StartGame = ({ questions, teams, onClick }: StartGameProps) => {
    const stats = [
        { name: 'Questions', stat: questions.length },
        { name: 'Teams', stat: teams.length },
    ]
    return <div className='grid place-items-center h-full'>
        <div>
            <img className='mx-auto' src="https://imgur.com/bw1McHh.png" alt="logo" />

            <dl className="mt-5 w-full grid grid-cols-1 gap-5 sm:grid-cols-2">
                {stats.map((item) => (
                    <div key={item.name} className="px-4 py-5 bg-white shadow rounded-lg overflow-hidden sm:p-6">
                        <dt className="text-sm font-medium text-gray-500 truncate">{item.name}</dt>
                        <dd className="mt-1 text-3xl font-semibold text-gray-900">{item.stat}</dd>
                    </div>
                ))}
            </dl>

            <div className="shadow mt-5 sm:rounded-md sm:overflow-hidden px-4 py-5 bg-white sm:p-6">
                <h1 className="text-2xl font-bold">Start game?</h1>
                <p className="mt-4">
                    This will be the <span className='font-bold'>HARDEST</span> trivia game you&apos;ve ever played. Are you ready?
                </p>
                <button
                    type="button"
                    className="mt-4 w-full justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-indigo-600 text-base font-medium text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:w-auto sm:text-sm"
                    onClick={onClick}
                >
                    ok
                </button>
            </div>
        </div>
    </div>
}

export default StartGame