import { useHistory } from "react-router-dom";

export default function UserCard({ user }) {
  const history = useHistory();
  const handleUserClick = () => {
    history.push(`/users/${user.id}`);
  };

  return (
    <div className="bg-white rounded-lg h-auto w-48 flex-shrink-0 p-4 pt-6 inline-flex flex-col justify-center items-center shadow-md border-gray-300 border border-opacity-80">
      <div className="rounded-full h-20 w-20 bg-profile-img bg-contain shadow-xl" />
      <div className="text-center text-lg mt-4 font-semibold text-gray-900 text-opacity-90">
        {user.name}
      </div>
      <p className="text-xs mt-1 font-medium text-gray-500">
        {user.description}
      </p>
      <div className="px-2 h-0.5 w-full m-3 border-gray-400 border-b border-opacity-50"></div>
      <button
        className="py-2 px-4 rounded-full mt-auto text-sm main-btn"
        onClick={handleUserClick}
      >
        정보 보기
      </button>
    </div>
  );
}
