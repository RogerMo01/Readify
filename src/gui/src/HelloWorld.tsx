import { useState, useEffect } from 'react';
import axios from 'axios';

function HelloWorld() {
  const [message, setMessage] = useState('');

  useEffect(() => {
    axios.get('http://localhost:8000/api/hello-world')
      .then(response => {
        setMessage(response.data.message);
        console.log(`Received: ${response.data.message}`)
      })
      .catch(error => {
        console.log(error);
      });
  }, []);

  return (
    <div>
      <h1>Hello, World!</h1>
      {(message) ? <p>{message}</p> : "No connection established"}
    </div>
  );
}

export default HelloWorld;