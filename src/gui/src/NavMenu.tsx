import "./NavMenu.css"

function NavMenu() {
  return (
    <header className="bg-white mt-0 shadow-2xl">
      <nav
        className="flex items-center justify-center menu-brand p-3 lg:px-8"
        aria-label="Global"
      >
        <div className="flex lg:flex-1 justify-center">
          <a href="#" className="-m-1.5 p-1.5">
            <span className="sr-only">Readify</span>
            <img
              className="h-20 w-auto"
              src="logo.png"
              alt="Readify"
            />
          </a>
        </div>
      </nav>
    </header>
  );
}

export default NavMenu;
