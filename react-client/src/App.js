import "./App.css";
import { AuthProvider } from "./Contexts/authContext";
import Routes from "./Routes/Routes";

function App() {
  // TODO: don't get/save user from session storage (might be out of sync with server)
  // TODO: Send a request to server to get current logged in user's details
  const user = sessionStorage.getItem("user");
  return (
    <AuthProvider user={user}>
      <Routes />
    </AuthProvider>
  );
}

export default App;
