function NavMenu() {
  return (
    <header className="bg-white mt-0">
      <nav
        className="flex  items-center justify-between bg-gray-400 p-6 lg:px-8"
        aria-label="Global"
      >
        <div className="flex lg:flex-1">
          <a href="#" className="-m-1.5 p-1.5">
            <span className="sr-only">Your Company</span>
            <img
              className="h-8 w-auto"
              src="https://tailwindui.com/img/logos/mark.svg?color=indigo&shade=600"
              alt=""
            />
          </a>
        </div>
      </nav>
    </header>
  );
}

export default NavMenu;
