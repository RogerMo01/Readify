import { Dispatch, SetStateAction, useState } from "react";
import "./NavMenu.css"
import UserModal from "./UserModal";
import Config from "./Config";

interface Props{
  refreshValue: boolean,
  refresher: Dispatch<SetStateAction<boolean>>
}

function NavMenu({refreshValue, refresher}: Props) {
  const [showModal, setShowModal] = useState(false)

  const toggle = () => {setShowModal(!showModal)}

  function handleClick(event: React.MouseEvent): void {
    console.log(event)
    toggle();
  }

  return (
    <>
      <header className="bg-white mt-0 shadow-2xl">
        <nav
          className="flex items-center justify-center menu-brand p-3 lg:px-8"
          aria-label="Global"
        >
          <div className="flex lg:flex-1 justify-center">
            <a href="#" className="-m-1.5 p-1.5 mr-auto">
              <span className="sr-only">Readify</span>
              <img
                className="h-20 w-auto"
                src="brand.png"
                alt="Readify"
              />
            </a>
          </div>
          <Config refreshValue={refreshValue} refresher={refresher} />
          <button className="bg-blue-500 hover:bg-blue-400 text-white font-bold py-2 px-4 border-b-4 border-blue-700 hover:border-blue-500 rounded ml-auto" onClick={handleClick}>
            My Library
          </button>
        </nav>
      </header>
      {showModal && <UserModal open={showModal} setOpen={setShowModal} refreshValue={refreshValue} refresher={refresher}/> }
    </>
  );
}

export default NavMenu;
