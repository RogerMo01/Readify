import { Book } from "../types/types";

interface Props{
    book: Book
}

function Card({book}: Props){
    
    return(
        <div className="w-full h-full py-5 flex justify-center items-center">
            <div className="relative h-full flex justify-center rounded-xl hover:scale-105 duration-500 transform transition cursor-pointer border">
                
                <div className="w-52 pb-2 bg-white rounded-xl shadow-2xl z-10">

                    <div className="relative">

                        <img src={book.imageURL_l} className="w-full h-72 object-cover rounded-t-xl" alt=""/>
                        
                        {/* Tag */}
                        {/* {book.awards.length > 2 && <div className="bottom-0 right-0 mb-2 mr-2 px-2 rounded-lg absolute bg-green-500 text-gray-100 text-xs font-medium">Award winning</div>} */}
                    </div>

                    <div className="px-2 py-1">

                        {/* Product Title */}
                        <div className="md:text-xl text-xl font-bold ">{book.bookTitle}</div>
                        <hr className="mt-2 mr-4 ml-4" />
                        <div className="">{book.bookAuthor}</div>

                        <div className="flex py-2">

                            {/*  Distance  */}
                            <div className="bg-gray-200 p-1 mr-2 rounded-full text-xs font-medium text-gray-900">
                                {book.yearOfPublication}
                            </div>

                            <div className="flex justify-between item-center">
                                    <div className="flex items-center">

                                        <svg xmlns="http://www.w3.org/2000/svg" className="h-3 md:h-5 md:w-5 text-yellow-500" viewBox="0 0 20 20"
                                            fill="currentColor">
                                            <path
                                                d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                                        </svg>

                                        {/* <!-- Rating total --> */}
                                        <p className="text-gray-600 font-bold text-xs md:text-sm ml-1">
                                            {book.avgRating}
                                            {/* <!-- Jumlah review --> */}
                                            <span className="text-gray-500 font-normal"> ({book.countRating} ratings)</span>
                                        </p>
                                    </div>
                            </div>
                        </div>
                        
                        {/* <!-- Alamat --> */}
                        {/* <p className="pb-1 md:pb-2 text-xs md:text-sm text-gray-500">Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua</p> */}
                        {/* <!-- Tombol pesan --> */}
                        {/* <a className="inset-x-0 bottom-0 flex justify-center bg-blue-500 hover:bg-white text-sm md:text-base border hover:border-2 hover:border-blue-500 rounded-xl w-14 md:w-16 p-1 text-gray-100 hover:text-blue-900" href="#">Order</a> */}
                    
                    </div>
                </div>
            </div> 
        </div>
    );
}

export default Card;