import { createContext, useContext, useState, useEffect } from "react";

const AuthContext = createContext();

export function AuthProvider({ children }) {

  const [user, setUser] = useState(() => {
  return localStorage.getItem("user");
  });

  useEffect(() => {
  const storedUser = localStorage.getItem("user");
  if (storedUser) setUser(storedUser);
  }, []);

  const login = (username) => {

    localStorage.setItem(
      "user",
      username
    );

    setUser(username);
  };

  const logout = () => {

    localStorage.removeItem("user");

    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        login,
        logout
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () =>
  useContext(AuthContext);