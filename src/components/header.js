import Logo from './logo';
// import Search from '../../public/search.png'
import Link from "next/link"

export default function Header() {
  return (
    <header className="bg-white py-2 h-[15vh]">
        <div className="mx-auto flex justify-between items-center gap-4">
            <div className='flex justify-center items-center pl-10'>
                    <h1 className="text-lg font-bold"><a href='http://localhost:3000/'>500 Fetcher</a></h1>
                    <Logo />
            </div>
       
            <div className="flex-grow flex items-center justify-center">
            <div class="relative w-full">
  <input
    placeholder="Search any stock from the S&P500"
    type="text"
    class="w-full p-3 rounded-md border border-gray-300 focus:ring-blue-500 focus:ring-1 focus:outline-none"
  />
  <span class="absolute inset-y-0 right-4 flex items-center justify-center">
    <svg
      xmlns="http://www.w3.org/2000/svg"
      class="h-5 w-5 text-gray-500"
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-width="2"
        d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
      />
    </svg>
  </span>
</div>
        </div>

            <nav className="flex gap-6 pr-10">
                <Link href="/" className="text-gray-500 hover:text-gray-700">Home</Link>
                <Link href="/watchlist" className="text-gray-500 hover:text-gray-700">Watchlist</Link>
                <Link href="/about" className="text-gray-500 hover:text-gray-700">About</Link>
                <a href="https://github.com/JasimrazaMomin/Stock-Predictor" className="text-gray-500 hover:text-gray-700" target='_blank'>GitHub</a>
            </nav>
        </div>
    </header> 

  );
}
