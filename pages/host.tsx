import { NextPageContext } from 'next'
import authorizeRequest from '@middlewares/authorizeRequest'
import io from 'socket.io-client'
import { useEffect, useState } from 'react'
import { CheckCircleIcon, ExclamationCircleIcon } from '@heroicons/react/solid'

let socket

interface CorrectAnswerEvent {
    question: string
    answer: string
}

const Host = () => {
    const [connected, setConnected] = useState(false)
    const [payload, setPayload] = useState<CorrectAnswerEvent>()

    const socketInitializer = async () => {
        await fetch('/api/verifySocketIsRunning')
        socket = io()

        socket.on('connect', () => {
            setConnected(true)
        })

        socket.on('disconnect', () => {
            setConnected(false)
        })

        socket.on('correct-answer-event', (payload: CorrectAnswerEvent) => {
            setPayload(payload)
        })
    }

    useEffect(() => {
        socketInitializer()
    }, [])

    return <div className='p-4'>
        {!connected &&
            <div className="rounded-md bg-red-50 p-4">
                <div className="flex">
                    <div className="flex-shrink-0">
                        <ExclamationCircleIcon className="h-5 w-5 text-red-400" aria-hidden="true" />
                    </div>
                    <div className="ml-3">
                        <p className="text-sm font-medium text-red-800">Disconnected from server</p>
                    </div>
                </div>
            </div>
        }

        {connected &&
            <div className="rounded-md bg-green-50 p-4">
                <div className="flex">
                    <div className="flex-shrink-0">
                        <CheckCircleIcon className="h-5 w-5 text-green-400" aria-hidden="true" />
                    </div>
                    <div className="ml-3">
                        <p className="text-sm font-medium text-green-800">Connected to server</p>
                    </div>
                </div>
            </div>
        }

        <div className='p-4'>
            <p><span className='font-bold'>Question: </span>{ payload ? payload.question : 'waiting' }</p>
            <p><span className='font-bold'>Answer: </span>{ payload ? payload.answer : 'waiting' }</p>
        </div>
    </div>
}

export const getServerSideProps = authorizeRequest(async (ctx: NextPageContext) => {
    return { props: {}}
  })


export default Host