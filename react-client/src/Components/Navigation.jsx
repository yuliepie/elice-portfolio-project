import { NavLink, useHistory } from "react-router-dom";
import { useAuth } from "../Contexts/authContext";
import axios from "axios";

export default function Navigation() {
  const { currentUser, setCurrentUser } = useAuth();
  const history = useHistory();

  const handleLogout = async () => {
    try {
      sessionStorage.setItem("user", "");
      await axios.get("/api/logout");
      alert("로그아웃 되었습니다.");

      setCurrentUser(null);
      history.push("/login");
    } catch (e) {
      console.log("logout failed: " + e);
    }
  };

  return (
    <div className="border-2 border-red-500 h-16 bg-gray-500 flex justify-end px-8 py-2 items-center fixed w-full">
      <div className="border-2 border-blue-500 h-8 w-20 mr-auto">logo</div>
      {currentUser && (
        <div className="inline-flex gap-x-4">
          <div className="w-20 border-yellow-100 border-2">
            <NavLink to="/">네트워크</NavLink>
          </div>
          <div className="w-20 border-yellow-100 border-2">
            <NavLink to={`/users/${currentUser.id}`}>마이페이지</NavLink>
          </div>
          <div className="w-20 border-yellow-100 border-2">
            <button onClick={handleLogout}>로그아웃</button>
          </div>
        </div>
      )}
    </div>
  );
}
