import { useState } from 'react'
import './App.css'
import NavMenu from './components/NavMenu'
import CollectionGroup from './components/CollectionGroup';

function App() {
  const [refresh, setRefresh] = useState(false);

  return (
    <>
      <NavMenu refreshValue={refresh} refresher={setRefresh}/>
      <CollectionGroup refreshValue={refresh}/>
    </>
  )
}

export default App
