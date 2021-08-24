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
    <div className="w-full h-12 bg-white fixed">
      <div className="flex justify-end w-4/6 py-2 items-center mx-auto">
        <button className="font-bold text-lg leading-8 text-center h-8 w-20 mr-auto">
          <NavLink to="/">ElicerIn.</NavLink>
        </button>
        {currentUser && (
          <div className="inline-flex gap-x-2">
            <button className="nav-item">
              <NavLink to="/">네트워크</NavLink>
            </button>
            <button className="nav-item">
              <NavLink to={`/users/my-page`}>마이페이지</NavLink>
            </button>
            <button className="nav-item" onClick={handleLogout}>
              Logout
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
