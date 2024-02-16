import axios from "axios";
import { useEffect, useState } from "react";
import { Book } from "./types/types";
import Card from "./Card";

interface Props{
    title: string
}

function Collection({title}: Props) {
    const [bookList, setBookList] = useState<Book[]>([]);

    useEffect(() => {
        axios.get('http://localhost:8000/api/list')
          .then(response => {
            setBookList(response.data.data);
            console.log(`Received: ${response.data.data}`)
          })
          .catch(error => {
            console.log(error);
          });
      }, []);
      
    return(
        <div className="ml-6 mr-6">
            <h1 className="flex mt-12 md:mx-10 font-bold text-3xl text-gray-800 border-b"> 
                {title}
            </h1>
            <div
                className="flex overflow-x-scroll pb-10 hide-scroll-bar"
            >
                <div
                className="flex flex-nowrap"
                >
                    {bookList.map((book) => (
                        <div className="inline-block px-3">
                            <Card book={book}/>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}

export default Collection;