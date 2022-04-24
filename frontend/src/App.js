import Header from "./components/Header";
import { Container } from "@mui/material";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import React, { useState } from "react";

import NewsScreen from "./components/NewsScreen";
import SearchSettings from "./components/SearchSettings";
import SignIn from "./components/SignIn";
import SignUp from "./components/SignUp";
import { UserProvider } from "./userContext";
import UserProfile from "./components/UserProfile";

function getAccessToken() {
  return localStorage.getItem("access_token");
}

function getUserName() {
  return localStorage.getItem("user_name");
}

function App() {
  const [accessToken, setAccessToken] = useState(getAccessToken());
  const [userName, setUserName] = useState(getUserName());

  const values_for_provider = {
    accessToken,
    setAccessToken,
    userName,
    setUserName,
  };

  return (
    <Router>
      <UserProvider value={values_for_provider}>
        <Header isLoggedIn={accessToken} />
        <main>
          <Container>
            <Routes>
              <Route path="/news" element={<NewsScreen />} />
              <Route path="/profile" element={<UserProfile />} />
              <Route path="/settings" element={<SearchSettings />} />
              <Route path="/signin" element={<SignIn />} />
              <Route path="/signup" element={<SignUp />} />
            </Routes>
          </Container>
        </main>
      </UserProvider>
    </Router>
  );
}

export default App;
