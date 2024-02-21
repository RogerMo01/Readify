import { Dialog, Transition } from '@headlessui/react'
import { Fragment, useState } from 'react'
import { Book } from "../types/types";

interface Props {
  book: Book;
}

function Card({ book }: Props) {
  const [isOpen, setIsOpen] = useState(false)

  function closeModal() {
    setIsOpen(false)
  }

  function openModal() {
    setIsOpen(true)
  }

  return (
    <div>
        <div className="w-full h-full py-5 flex justify-center items-center" onClick={() => openModal()}>
          <div className="relative h-full flex justify-center rounded-xl hover:scale-105 duration-500 transform transition cursor-pointer border">
            <div className="w-52 pb-2 bg-white rounded-xl shadow-2xl z-10">
              <div className="relative">
                <img
                  src={book.imageURL_l}
                  className="w-full max-h-[320px] object-cover rounded-t-xl"
                  alt=""
                />
              </div>
              <div className="px-2 py-1">
                {/* Product Title */}
                <div className="md:text-xl text-xl font-bold ">
                  {book.bookTitle}
                </div>
                <hr className="mt-2 mr-4 ml-4" />
                <div className="">{book.bookAuthor}</div>
                <div className="flex py-2">
                  {/*  Year  */}
                  <div className="bg-gray-200 p-1 mr-2 rounded-full text-xs font-medium text-gray-900">
                    {book.yearOfPublication}
                  </div>
                  <div className="flex justify-between item-center">
                    <div className="flex items-center">
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        className="h-3 md:h-5 md:w-5 text-yellow-500"
                        viewBox="0 0 20 20"
                        fill="currentColor"
                      >
                        <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                      </svg>
                      {/* <!-- Rating total --> */}
                      <p className="text-gray-600 font-bold text-xs md:text-sm ml-1">
                        {book.avgRating}
                        {/* <!-- Count rating --> */}
                        <span className="text-gray-500 font-normal">
                          {" "}
                          ({book.countRating} ratings)
                        </span>
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Card Modal Info */}
        <Transition appear show={isOpen} as={Fragment}>
        <Dialog as="div" className="relative z-10" onClose={closeModal}>
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
                <Dialog.Panel className="w-full max-w-4xl transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all">
                  <Dialog.Title
                    as="h3"
                    className="text-xl font-medium leading-6 text-gray-900"
                  >
                    Book Info
                  </Dialog.Title>
                  <div className="mt-2 bg-gray-100 mx-5 rounded-xl">
                    <div className='flex flex-row'>
                        <img src={book.imageURL_l} className='h-80 border rounded-xl shadow-xl' />
                        <div className='ml-5'>
                            <div className='flex flex-col'>
                                <label className="text-xl font-bold">{book.bookTitle}</label>
                                <p className="text-md font-serif">ISBN: {book.isbn}</p>

                                <label className="text-lg font-bold mt-3">Author:</label>
                                <p className="text-lg font-serif">{book.bookAuthor}</p>

                                <label className="text-lg font-bold mt-3">Publisher:</label>
                                <p className="text-lg font-serif ">{book.publisher}</p>

                                <label className="text-lg font-bold mt-3">Year of publication:</label>
                                <p className="text-lg font-serif ">{book.yearOfPublication}</p>
                            </div>
                        </div>
                    </div>
                  </div>

                  <div className="mt-4">
                    <button
                      type="button"
                      className="inline-flex justify-center rounded-md border border-transparent bg-blue-200 px-4 py-2 text-sm font-medium text-blue-900 hover:bg-blue-200 focus:outline-none focus-visible:ring-2 "
                      onClick={closeModal}
                    >
                      Close
                    </button>
                  </div>
                </Dialog.Panel>
              </Transition.Child>
            </div>
          </div>
        </Dialog>
      </Transition>
    </div>
  );
}

export default Card;
