import { Navigate } from "react-router-dom";

const Protected = ({ children }) => {
  const access_token = localStorage.getItem("access_token");

  if (!access_token) {
    return <Navigate to="/signin" replace />;
  }
  return children;
};
export default Protected;
