import { useHistory } from "react-router-dom";

export default function UserCard({ user }) {
  const history = useHistory();
  const handleUserClick = () => {
    history.push(`/users/${user.id}`);
  };

  return (
    <div
      className="bg-white rounded-lg h-auto w-60 flex-shrink-0 p-4 pt-6 pb-4 inline-flex flex-col justify-center items-center shadow-md border-gray-300 border border-opacity-80 cursor-pointer group hover:transform hover:scale-105 transition duration-300 ease-in-out origin-bottom active:bg-gray-200"
      onClick={handleUserClick}
    >
      <div className="rounded-full h-20 w-20 bg-profile-img bg-contain shadow-xl" />
      <div className="text-center text-lg mt-6 font-semibold text-gray-900 text-opacity-90">
        {user.name}
      </div>
      <p className="text-sm mt-1 text-gray-700 font-light">
        {user.description}
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
