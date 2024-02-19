import { Book } from "../types/types";
import { SetStateAction } from "react";
import RateModal from "./RateModal";

interface Props{
    book: Book,
    refreshValue: boolean,
    refresh: React.Dispatch<SetStateAction<boolean>>
}
function SearchItem({book, refreshValue, refresh}:Props){

    return(
        <li className="mb-1 shadow-xl hover:">
            <div className="flex items-center space-x-4 rtl:space-x-reverse border rounded">
                <div className="flex-shrink-0">
                    <img className="w-16 h-20 rounded" src={book.imageURL_s} alt="Neil image"/>
                </div>
                <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900 truncate">
                        {book.bookTitle}
                    </p>
                    <div className="flex flex-row">
                        <p className="text-sm text-gray-500 truncate">
                            {book.bookAuthor}
                        </p>
                        <p className="ml-auto">
                            {book.avgRating}
                        </p>
                        <svg xmlns="http://www.w3.org/2000/svg" className="w-5 text-yellow-500" viewBox="0 0 20 20"
                            fill="currentColor">
                            <path
                                d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                        </svg>
                        <p className="text-sm text-gray-400">
                            ({book.countRating} reviews)
                        </p>
                        <RateModal book={book} refresh={refresh} refreshValue={refreshValue}/>
                        {/* <PlusCircleIcon className="h-6 w-10 text-blue-600 mr-10 hover:cursor-pointer rounded-full hover:text-blue-500" onClick={handleAddBook} /> */}
                    </div>
                    <p className="text-sm text-gray-500">
                        {book.yearOfPublication}
                    </p>
                </div>
            </div>
        </li>
    );
}

export default SearchItem;