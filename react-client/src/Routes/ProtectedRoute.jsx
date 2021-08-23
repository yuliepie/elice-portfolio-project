import { Redirect } from "react-router-dom";
import { useAuth } from "../Contexts/authContext";
import { Route } from "react-router-dom";

export default function ProtectedRoute({ children, ...rest }) {
  // Call auth context hook to determine if user logged in
  const { currentUser } = useAuth();

  // If logged in, render component
  // If not, redirect to login page (with current location info)
  return (
    <Route
      {...rest}
      render={({ location }) =>
        currentUser ? (
          children
        ) : (
          <Redirect to={{ pathname: "/login", state: { from: location } }} />
        )
      }
    />
  );
}
