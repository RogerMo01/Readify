import { Dialog, Transition } from '@headlessui/react'
import { Fragment, SetStateAction, useState } from 'react'
import { PlusCircleIcon } from '@heroicons/react/24/solid'
import { StarIcon } from '@heroicons/react/24/solid'
import axios from 'axios'
import { Book } from '../types/types'

interface Props{
    book: Book,
    refreshValue: boolean,
    refresh: React.Dispatch<SetStateAction<boolean>>
}

export default function RateModal({book, refreshValue, refresh}: Props) {
    const [isOpen, setIsOpen] = useState(false)
    const totalStarts = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    const [rate, setRate] = useState(6)

  function closeModal() {
    setIsOpen(false)
  }

  function openModal() {
    setIsOpen(true)
  }

  async function handleAddBook(event: React.MouseEvent): Promise<void> {
        console.log(event)

        try {
            const request = {
                'isbn': book.isbn,
                'bookTitle': book.bookTitle,
                'bookAuthor': book.bookAuthor,
                'imageURL_s': book.imageURL_s,
                'rating': rate.toString()
            }

            const response = await axios.post('http://localhost:8000/api/add-book/', request);
            console.log('Server answer:', response.data);
            refresh(!refreshValue)

        } catch (error) {
            console.error('Error: POST:', error);
        }
        closeModal()
    }




    function handleRate(i: number): void {
        setRate(i)
    }

  return (
    <>
      <PlusCircleIcon className="h-6 w-10 text-blue-600 mr-10 hover:cursor-pointer rounded-full hover:text-blue-500" onClick={openModal} />

      <Transition appear show={isOpen} as={Fragment}>
        <Dialog as="div" className="relative z-10" onClose={closeModal} static>
          <Transition.Child
            as={Fragment}
            enter="ease-out duration-300"
            enterFrom="opacity-0"
            enterTo="opacity-100"
            leave="ease-in duration-200"
            leaveFrom="opacity-100"
            leaveTo="opacity-0"
          >
            <div className="fixed inset-0 bg-black/25" />
          </Transition.Child>

          <div className="fixed inset-0 overflow-y-auto">
            <div className="flex min-h-full items-center justify-center p-4 text-center">
              <Transition.Child
                as={Fragment}
                enter="ease-out duration-300"
                enterFrom="opacity-0 scale-95"
                enterTo="opacity-100 scale-100"
                leave="ease-in duration-200"
                leaveFrom="opacity-100 scale-100"
                leaveTo="opacity-0 scale-95"
              >
                <Dialog.Panel className="w-full max-w-md transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all">
                  <Dialog.Title
                    as="h3"
                    className="text-lg font-medium leading-6 text-gray-900"
                  >
                    Rate the book
                  </Dialog.Title>
                  <div className="mt-2">
                    <div className='flex flex-row'>
                        {totalStarts.map((i) => (
                            <StarIcon className={`h-10 w-10 ${i <= rate ? 'text-yellow-500' : 'text-gray-300'} hover:cursor-pointer rounded-full`} onClick={() => handleRate(i)}/>
                        ))}
                    </div>
                  </div>

                  <div className="mt-4">
                    <button
                      type="button"
                      className="inline-flex justify-center rounded-md border border-transparent bg-blue-100 px-4 py-2 text-sm font-medium text-blue-900 hover:bg-blue-300 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
                      onClick={handleAddBook}
                    >
                      Rate
                    </button>
                  </div>
                </Dialog.Panel>
              </Transition.Child>
            </div>
          </div>
        </Dialog>
      </Transition>
    </>
  )
}
