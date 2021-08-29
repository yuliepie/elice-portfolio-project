import "./App.css";
import { AuthProvider } from "./Contexts/authContext";
import Routes from "./Routes/Routes";
import axios from "axios";
import { useEffect, useState } from "react";

function App() {
  const [currentUser, setCurrentUser] = useState(null); // Check current user with server
  useEffect(() => {
    axios
      .get("/api/whoami")
      .then((resp) => {
        if (resp) {
          setCurrentUser(resp.data);
          console.log("Current user: ", currentUser);
        }
      })
      .catch((e) => {
        if (e.response.status === 401) {
          console.log("No logged in user.");
        } else {
          throw e;
        }
      });
  }, []);

  return (
    <AuthProvider currentUser={currentUser} setCurrentUser={setCurrentUser}>
      <Routes />
    </AuthProvider>
  );
}

export default App;
