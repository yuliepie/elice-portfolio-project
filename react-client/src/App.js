import { BrowserRouter, Route, Switch } from "react-router-dom";
import LoginPage from "./Views/LoginView/LoginPage";
import "./App.css";
import SignUpPage from "./Views/SignUpView/SignUpPage";
import UserDetailPage from "./Views/UserDetailView/UserDetailPage";

function App() {
  return (
    <BrowserRouter>
      <Switch>
        <Route path="/login">
          <LoginPage />
        </Route>
        <Route path="/signup">
          <SignUpPage />
        </Route>
        <Route path="/c">
          <UserDetailPage />
        </Route>
      </Switch>
    </BrowserRouter>
  );
}

export default App;
