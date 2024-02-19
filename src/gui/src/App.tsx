import { useState } from 'react'
import './App.css'
import Collection from './components/Collection'
import NavMenu from './components/NavMenu'

function App() {
  const [refresh, setRefresh] = useState(false);

  return (
    <>
      <NavMenu refreshValue={refresh} refresher={setRefresh}/>
      <Collection refreshValue={refresh} title='Suggested for you'/>
    </>
  )
}

export default App
