
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
    rating: "0.0",
    title: "Flesh Tones: A Novel",
    author: "M. J. Rose"
    cover: "http://images.amazon.com/images/P/034545104X.01.THUMBZZZ.jpg"
}