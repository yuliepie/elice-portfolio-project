import ProtectedRoute from "./ProtectedRoute";
import { BrowserRouter, Redirect, Route, Switch } from "react-router-dom";
import LoginPage from "../Views/LoginView/LoginPage";
import SignUpPage from "../Views/SignUpView/SignUpPage";
import UserDetailPage from "../Views/UserDetailView/UserDetailPage";
import MainPage from "../Views/MainView/MainPage";
import { useAuth } from "../Contexts/authContext";

export default function Routes() {
  const { currentUser } = useAuth();
  console.log("current user routes", currentUser);

  return (
    <BrowserRouter>
      <Switch>
        {/* Not protected */}
        <Route path="/login">
          {currentUser ? <Redirect to="/" /> : <LoginPage />}
        </Route>
        <Route path="/signup">
          {currentUser ? <Redirect to="/" /> : <SignUpPage />}
        </Route>
        {/* Protected - needs to be logged in */}
        <ProtectedRoute exact path="/users/my-page">
          <UserDetailPage myPage={true} />
        </ProtectedRoute>
        {currentUser && (
          <ProtectedRoute exact path={`/users/${currentUser.id}`}>
            <Redirect to="/users/my-page" />
          </ProtectedRoute>
        )}
        <ProtectedRoute exact path="/users/:id">
          <UserDetailPage />
        </ProtectedRoute>
        <ProtectedRoute exact path="/">
          <MainPage />
        </ProtectedRoute>
      </Switch>
    </BrowserRouter>
  );
}
