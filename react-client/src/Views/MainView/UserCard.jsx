import { useHistory } from "react-router-dom";

export default function UserCard({ user }) {
  const history = useHistory();
  const handleUserClick = () => {
    history.push(`/users/${user.id}`);
    console.log(user);
  };

  return (
    <div
      className="bg-white rounded-lg h-auto w-60 flex-shrink-0 p-4 pt-6 pb-4 inline-flex flex-col justify-center items-center shadow-md border-gray-300 border border-opacity-80 cursor-pointer group hover:transform hover:scale-105 transition duration-300 ease-in-out origin-bottom active:bg-gray-200"
      onClick={handleUserClick}
    >
      <img
        className="rounded-full h-24 w-24 shadow-xl"
        src={
          user.imagePath
            ? `${process.env.REACT_APP_SERVER_DOMAIN}/${user.imagePath}`
            : "https://i0.wp.com/prikachi.com/wp-content/uploads/2020/07/DPP1.jpg"
        }
      />
      <div className="text-center text-lg mt-5 font-semibold text-gray-900 text-opacity-90">
        {user.name}
      </div>
      <div></div>
      <p
        className={`w-full text-center whitespace-nowrap truncate text-sm mt-1 font-light ${
          !user.description ? "text-transparent" : "text-gray-700"
        }`}
      >
        {user.description ? user.description : "placeholder text"}
      </p>
      <div className="px-2 h-0.5 w-full m-4 border-gray-400 border-b border-opacity-50  "></div>
      <button
        className="py-2 px-4 rounded-full mt-auto mb-2 text-sm main-btn"
        onClick={handleUserClick}
      >
        정보 보기
      </button>
    </div>
  );
}
