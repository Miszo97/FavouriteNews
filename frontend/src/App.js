import Header from "./components/Header";
import { Container } from "@mui/material";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

import NewsScreen from "./components/NewsScreen";
import SearchSettings from "./components/SearchSettings";
import SignIn from "./components/SignIn";
import SignUp from "./components/SignUp";

function App() {
  return (
    <Router>
      <Header />

      <main>
        <Container>
          <Routes>
            <Route path="/news" element={<NewsScreen />} />
            <Route path="/settings" element={<SearchSettings />} />
            <Route path="/signin" element={<SignIn />} />
            <Route path="/signup" element={<SignUp />} />
          </Routes>
        </Container>
      </main>
    </Router>
  );
}

export default App;
