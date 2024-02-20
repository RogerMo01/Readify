import { UserBook } from "../types/types";
import { StarIcon } from '@heroicons/react/24/solid'

interface Props{
    book: UserBook
}
function BookView({book}:Props){

    return(
        <li className="mb-1 shadow-xl hover:">
            <div className="flex items-center space-x-4 rtl:space-x-reverse border rounded">
                <div className="flex-shrink-0">
                    <img className="w-16 h-20 rounded" src={book.cover} alt="Neil image"/>
                </div>
                <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900 truncate">
                    {book.title}
                    </p>
                    <p className="text-sm text-gray-500 truncate">
                    {book.author}
                    </p>
                    <div className="flex flex-row">
                        <StarIcon className='h-5 w-4 text-yellow-500 rounded-full' />
                        <p className="text-sm truncate">
                        {book.rating}.0
                        </p>
                    </div>
                </div>
            </div>
        </li>
    );
}

export default BookView;