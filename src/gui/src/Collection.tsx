import axios from "axios";
import { useEffect, useState } from "react";
import { Book } from "./types/types";
import Card from "./Card";

function Collection() {
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
            <h1 className="flex py-5 md:px-10 px-5 md:mx-20 mx-5 font-bold text-4xl text-gray-800"> Books </h1>
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