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

  // Load user library
  useEffect(() => {
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
      });

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [refreshValue]);

  useEffect(() => {
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [refreshValue]);

  return (
    <>
      <Collection title="Made for you" books={mainBooksList} />
      {favAuthorBooksList.length > 0 && <Collection title={`More from ${favAuthor}`} books={favAuthorBooksList} />}
    </>
  );
}

export default CollectionGroup;
