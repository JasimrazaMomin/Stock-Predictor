export default function About() {
    return (
      <div className="text-gray-900">
    <div className="container mx-auto p-6">
        <section className="text-center mb-12">
            <h2 className="text-2xl font-bold mb-4">Meet the Team</h2>
            <p className="text-gray-700 text-lg">We are a dedicated team working on creating a comprehensive stock watchlist application to help users manage their investments efficiently.</p>
        </section>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
           
            <div className="bg-white p-6 rounded-lg shadow-lg">
                <img src="https://media.licdn.com/dms/image/D4E03AQEDZuDyOzlhcQ/profile-displayphoto-shrink_200_200/0/1697733086863?e=2147483647&v=beta&t=j9j_anyGASOC5sFmnEpGyAGwaQcvvyE_AtalceaHMI8" alt="Team Member 1" className="mx-auto mb-4"/>
                <h3 className="text-xl font-semibold mb-2">Lojan Karunakaran</h3>
                <p className="text-gray-600 mb-4">Front-End Developer</p>
                <p className="text-gray-500 mb-4">Worked on the UI design and implementation of the watchlist feature. Ensured a responsive and user-friendly interface.</p>
                <a href="https://github.com/lojank" className="text-blue-500 hover:underline" target="_blank">GitHub</a> | 
                <a href="https://www.linkedin.com/in/lojan-karunakaran/" className="text-blue-500 hover:underline" target="_blank"> LinkedIn</a>
            </div>

         
            <div className="bg-white p-6 rounded-lg shadow-lg">
                <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcStdxx9r4bk2no0GVJ7h4VOidsqvxmekNB7yQ&s" alt="Team Member 2" className="profile-pic mx-auto mb-4"/>
                <h3 className="text-xl font-semibold mb-2">Jasimraza Momin</h3>
                <p className="text-gray-600 mb-4">Back-End Developer</p>
                <p className="text-gray-500 mb-4">Handled server-side logic and database integration. Ensured efficient data retrieval and storage.</p>
                <a href="https://github.com/JasimrazaMomin" className="text-blue-500 hover:underline" target="_blank">GitHub</a> | 
                <a href="https://www.linkedin.com/in/jasimraza-momin/" className="text-blue-500 hover:underline" target="_blank"> LinkedIn</a>
            </div>

            
            <div className="bg-white p-6 rounded-lg shadow-lg">
                <img src="path/to/profile3.jpg" alt="Team Member 3" className="profile-pic mx-auto mb-4"/>
                <h3 className="text-xl font-semibold mb-2">Roshan Gugi</h3>
                <p className="text-gray-600 mb-4">Back-End Developer</p>
                <p className="text-gray-500 mb-4">Handled server-side logic and database integration. Ensured efficient data retrieval and storage.</p>
                <a href="" className="text-blue-500 hover:underline" target="_blank">GitHub</a> | 
                <a href="" className="text-blue-500 hover:underline" target="_blank"> LinkedIn</a>
            </div>

       
            <div className="bg-white p-6 rounded-lg shadow-lg">
                <img src="path/to/profile4.jpg" alt="Team Member 4" className="profile-pic mx-auto mb-4"/>
                <h3 className="text-xl font-semibold mb-2">Asvith Kiruba</h3>
                <p className="text-gray-600 mb-4">Front-End Developer</p>
                <p className="text-gray-500 mb-4">Worked on the UI design and implementation of the watchlist feature. Ensured a responsive and user-friendly interface.</p>
                <a href="" className="text-blue-500 hover:underline" target="_blank">GitHub</a> | 
                <a href="" className="text-blue-500 hover:underline" target="_blank"> LinkedIn</a>
            </div>
        </div>
    </div>
</div>


    );
  }