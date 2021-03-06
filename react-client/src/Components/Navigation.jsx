import { NavLink, useHistory } from "react-router-dom";
import { useAuth } from "../Contexts/authContext";
import axios from "axios";
import AlertModal from "./AlertModal";
import { useState } from "react";

export default function Navigation() {
  const { currentUser, setCurrentUser } = useAuth();
  const history = useHistory();

  // Show alert modal on logout
  const [showModal, setShowModal] = useState(false);

  const handleLogout = async () => {
    try {
      await axios.get("/api/logout");
      setShowModal(true);
    } catch (e) {
      console.log("logout failed: " + e);
    }
  };

  return (
    <>
      <AlertModal
        title="로그아웃 성공"
        isAlert={true}
        mainText="다음에 또 오세요! ☺"
        showModal={showModal}
        setShowModal={setShowModal}
        onModalClose={() => setCurrentUser(null)}
      />
      <div className="flex w-full h-20 bg-white justify-center items-center fixed z-20">
        <div className="inline-flex justify-end w-7/12 py-2 items-center mx-auto">
          <button className="font-bold text-xl leading-8 text-center h-8 w-20 mr-auto">
            <NavLink to="/">ElicerIn.</NavLink>
          </button>
          {currentUser && (
            <div className="inline-flex gap-x-2">
              <NavLink className="nav-item" to="/">
                네트워크
              </NavLink>
              <NavLink className="nav-item px-1" to={`/users/my-page`}>
                {`${currentUser.name}`}
              </NavLink>
              <button className="nav-item" onClick={handleLogout}>
                Logout
              </button>
            </div>
          )}
        </div>
      </div>
    </>
  );
}
