// pages/index.js

export default function Home() {
  return (
    <div className="h-[85vh] flex flex-col">
      <main className="container mx-auto py-10">
        <div className="text-center">
        <h2 className="text-4xl font-bold text-gray-900 mb-4">
          Track the <span className='border-b-green-400 border-b-2'>Sentiment</span> of the <span className='border-b-green-400 border-b-2'>Market</span>
        </h2>

          <p className="text-gray-500 text-lg">Stay ahead with real-time updates on the S&P 500. Monitor trends, analyze performance, and make informed investment decisions effortlessly.</p>
        </div>
        <div className="mt-12">
          <img className='grayscale-50 h-[50vh] w-[100vw] object-cover' src='https://assets.entrepreneur.com/content/3x2/2000/1673985418-ENT-StockTradingBundle.jpeg'/>
        </div>
      </main>
    </div>
  );
}


{/* <button style={{ padding: '10px 20px', fontSize: '16px', cursor: 'pointer' }}>
              Go to Stock Display
            </button> */}