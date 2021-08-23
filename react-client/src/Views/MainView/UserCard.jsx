import { useHistory } from "react-router-dom";

export default function UserCard({ user }) {
  const history = useHistory();
  const handleUserClick = () => {
    history.push(`/users/${user.id}`);
  };

  return (
    <div className="bg-green-200 h-48 w-40 flex-shrink-0 p-4 inline-flex flex-col">
      <div>{user.name}</div>
      <button
        className="bg-indigo-300 p-2 rounded-md mt-auto"
        onClick={handleUserClick}
      >
        정보 보기
      </button>
    </div>
  );
}
