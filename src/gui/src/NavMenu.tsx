import { Dispatch, SetStateAction } from "react";
import "./NavMenu.css"
import Library from "./Library";
import Config from "./Config";

interface Props{
  refreshValue: boolean,
  refresher: Dispatch<SetStateAction<boolean>>
}

function NavMenu({refreshValue, refresher}: Props) {
  

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
          <Library refreshValue={refreshValue} refresher={refresher}/> 
          
        </nav>
      </header>
    </>
  );
}

export default NavMenu;
