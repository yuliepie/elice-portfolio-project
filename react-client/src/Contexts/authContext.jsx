import { createContext, useContext, useState } from "react";

const AuthContext = createContext(null);

// Context Provider for wrapping children
// Gets user if there is any, set that user as state,
// And makes that state accessible from children
export const AuthProvider = ({ user, children }) => {
  // user = { email, id, name }
  const [currentUser, setCurrentUser] = useState(user);

  return (
    <AuthContext.Provider value={{ currentUser, setCurrentUser }}>
      {children}
    </AuthContext.Provider>
  );
};

// Hook that can be used by children
export const useAuth = () => useContext(AuthContext);
