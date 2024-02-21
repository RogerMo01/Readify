import { useEffect, useState } from "react";
import Collection from "./Collection";
import axios from "axios";
import { Book } from "../types/types";

interface Props {
  refreshValue: boolean;
}

function CollectionGroup({ refreshValue }: Props) {
  const [mainBooksList, setMainBooksList] = useState<Book[]>([]);
  const [favAuthorBooksList, setFavAuthorBooksList] = useState<Book[]>([]);
  const [favAuthor, setFavAuthor] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  // Load user library
  useEffect(() => {
    setIsLoading(true);
    
    axios
      .get("http://localhost:8000/api/main-recommendation")
      .then((response) => {
        setMainBooksList(response.data.data);
      })
      .catch((error) => {
        console.log(error);
      });

    axios
      .get("http://localhost:8000/api/author-recommendation")
      .then((response) => {
        setFavAuthor(response.data.author);
        setFavAuthorBooksList(response.data.list);
      })
      .catch((error) => {
        console.log(error);
      })
      .finally(() => {
        // Ocultar el spinner cuando las solicitudes han terminado
        setIsLoading(false);
      });

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [refreshValue]);


  return (
    <>
      {isLoading && (
        <div className="flex items-center justify-center mt-64">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-blue-500"></div>
        </div>
      )}
      {!isLoading &&
        <>
          <Collection title="Made for you" books={mainBooksList} />
          {favAuthorBooksList.length > 0 && <Collection title={`More from ${favAuthor}`} books={favAuthorBooksList} />}
        </>
      }
    </>
  );
}

export default CollectionGroup;
