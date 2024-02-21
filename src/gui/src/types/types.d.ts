
export interface Book{
    isbn: string,
    bookTitle: string,
    bookAuthor: string,
    yearOfPublication: string,
    publisher: string,
    imageURL_s: string,
    imageURL_m: string,
    imageURL_l: string,
    avgRating: string,
    countRating: string
}

export interface UserBook{
    rating: string,
    title: string,
    author: string,
    cover: string
}