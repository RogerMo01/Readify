import React, { Dispatch, Fragment, SetStateAction, useEffect, useRef, useState } from 'react'
import { Dialog, Transition } from '@headlessui/react'
import { BookOpenIcon } from '@heroicons/react/24/outline'
import axios from 'axios'
import { Book } from '../types/types'
import BookView from './BookView'
import SearchItem from './SearchItem'

interface Props{
  refreshValue: boolean,
  refresher: Dispatch<SetStateAction<boolean>>
}

export default function Library({refreshValue, refresher}: Props) {
  const [bookList, setBookList] = useState<Book[]>([]);
  const [query, setQuery] = useState('');
  const [startSearch, setStartSearch] = useState(false);
  const [userBooks, setUserBooks] = useState([]);
  // const [userBooksInfo, setUserBooksInfo] = useState<Book[]>([]);
  const cancelButtonRef = useRef(null)
  
  const [refresh, setRefresh] = useState(false);

  const [showModal, setShowModal] = useState(false)

  const toggle = () => {setShowModal(!showModal)}

  function handleClick(event: React.MouseEvent): void {
    console.log(event)
    toggle();
  }

  // Ask for search query
  useEffect(() => {
    console.log("Trim = " + query.trim());

    if (query.trim() !== '') {
      axios.get('http://localhost:8000/api/filter-books')
        .then(response => {
          setBookList(response.data.data);
          console.log(`Received: ${response.data.data}`)
        })
        .catch(error => {
          console.log(error);
        });
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [startSearch, refresh])


  // Load user library
  useEffect(() => {
    axios.get('http://localhost:8000/api/user-books')
      .then(response => {
        setUserBooks(response.data.data);
        console.log(`Received: ${response.data.data}`)
      })
      .catch(error => {
        console.log(error);
      });
    
    refresher(!refreshValue)
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [refresh])


  // Load user book info
  // useEffect(() => {
  //   const fetchData = async () => {
  //     try {
  //       // Array para almacenar las promesas de las consultas
  //       const promises = userBooks.map(async (book) => {
  //         const response = await axios.get<Book>(`tu_url_de_consulta/${book[0]}`);
  //         const current = userBooksInfo;
  //         current.push(response.data);  

  //         setUserBooksInfo(current)
  //       });

  //       // Ejecutar todas las consultas de forma simultánea
  //       await Promise.all(promises);
  //     } catch (error) {
  //       console.error('Error al realizar las consultas:', error);
  //     }
  //   };

  //   // Llama a la función fetchData cuando cambie userBooks
  //   fetchData();
  // // eslint-disable-next-line react-hooks/exhaustive-deps
  // }, [userBooks]);


  // Filter search result
  useEffect(() => {
    const filteredList = bookList.filter(b => !userBooks.some(userBook => userBook[0] === b.isbn))
    setBookList(filteredList)
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [userBooks])
  


  function handleSearch(event: React.MouseEvent): void {
    console.log(event)
    setStartSearch(!startSearch)
  }

  function handleChange(event: React.ChangeEvent<HTMLInputElement>): void {
    const value = event.target.value;
    setQuery(value)
  }

  return (
    <>
      <button className="bg-blue-500 hover:bg-blue-400 text-white font-bold py-2 px-4 border-b-4 border-blue-700 hover:border-blue-500 rounded ml-auto" onClick={handleClick}>
        My Library
      </button>

      <Transition.Root show={showModal} as={Fragment}>
        <Dialog as="div" className="relative z-10" initialFocus={cancelButtonRef} onClose={setShowModal}>
          <Transition.Child
            as={Fragment}
            enter="ease-out duration-300"
            enterFrom="opacity-0"
            enterTo="opacity-100"
            leave="ease-in duration-200"
            leaveFrom="opacity-100"
            leaveTo="opacity-0"
          >
            <div className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" />
          </Transition.Child>

          <div className="fixed inset-0 z-10 w-screen overflow-y-auto">
            <div className="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
              <Transition.Child
                as={Fragment}
                enter="ease-out duration-300"
                enterFrom="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
                enterTo="opacity-100 translate-y-0 sm:scale-100"
                leave="ease-in duration-200"
                leaveFrom="opacity-100 translate-y-0 sm:scale-100"
                leaveTo="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
              >
                <Dialog.Panel className="relative transform overflow-hidden rounded-lg bg-white text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-6xl">
                  <div className="bg-white px-4 pb-4 pt-5 sm:p-6 sm:pb-4">
                    <div className="sm:items-start">

                      <div className="mx-auto flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-full bg-gray-100 sm:mx-0 sm:h-10 sm:w-10">
                        <BookOpenIcon className="h-6 w-6 text-blue-600" aria-hidden="true" />
                      </div>
                      <div className="mt-3 text-center sm:ml-4 sm:mt-0 sm:text-left">
                        <Dialog.Title as="h3" className="text-base font-semibold leading-6 text-gray-900">
                          My Library
                        </Dialog.Title>

                        <div className="mt-2">

                          <div className="md:max-w-2xl mx-auto">   
                            <label className="mb-2 text-sm font-medium text-gray-900 sr-only dark:text-white">Search</label>
                            <div className="relative">
                                <div className="absolute inset-y-0 start-0 flex items-center ps-3 pointer-events-none">
                                    <svg className="w-4 h-4 text-gray-500 dark:text-gray-400" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 20">
                                        <path stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z"/>
                                    </svg>
                                </div>
                                <input className="block w-full p-4 ps-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-100 focus:ring-blue-500 focus:border-blue-500" placeholder="Search Book" required onChange={handleChange} />
                                <button className="text-white absolute end-2.5 bottom-2.5 bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-4 py-2 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800" onClick={handleSearch}>Search</button>
                            </div>
                          </div>
                          
                          <div className='mt-2'>
                            {bookList.map((book) => (
                              <ul className="mx-20 divide-y divide-gray-200">
                                <SearchItem book={book} refreshValue={refresh} refresh={setRefresh} />
                              </ul>
                            ))}
                          </div>
                        </div>
                        
                        <hr className='mt-10 mb-10 border-solid'/>

                        <div>
                          <label className='text-lg font-bold'>My Books:</label>
                          {userBooks.map((br) => (
                            <ul className="mx-5 divide-y divide-gray-200">
                              <BookView book={{title: br[1]['title'], author: br[1]['author'], cover : br[1]['cover'], rating: br[1]['rating']}} />
                            </ul>
                          ))}
                        </div>
                      </div>
                    </div>
                  </div>

                  <div className="bg-gray-50 px-4 py-3 sm:flex sm:flex-row-reverse sm:px-6">
                    <button
                      type="button"
                      className="inline-flex w-full justify-center rounded-md bg-gray-500 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-gray-600 sm:ml-3 sm:w-auto"
                      onClick={() => setShowModal(false)}
                    >
                      Close
                    </button>
                  </div>

                </Dialog.Panel>
              </Transition.Child>
            </div>
          </div>
        </Dialog>
      </Transition.Root>
    </>
  )
}
