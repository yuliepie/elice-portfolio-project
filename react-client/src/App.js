import { BrowserRouter, Route, Switch } from "react-router-dom";
import LoginPage from "./Views/LoginView/LoginPage";
import "./App.css";
import SignUpPage from "./Views/SignUpView/SignUpPage";
import UserDetailPage from "./Views/UserDetailView/UserDetailPage";
import UserListPage from "./Views/UserListView/UserListPage";

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
        <Route path="/myPage">
          <UserDetailPage />
        </Route>
        <Route path="/">
          <UserListPage />
        </Route>
      </Switch>
    </BrowserRouter>
  );
}

export default App;
