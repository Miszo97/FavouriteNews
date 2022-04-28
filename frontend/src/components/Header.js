import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Toolbar from "@mui/material/Toolbar";

import Container from "@mui/material/Container";
import Button from "@mui/material/Button";
import Link from "@mui/material/Link";
import React, { useContext } from "react";
import { UserContext } from ".././userContext";

export function logout(setAccessToken, setUserName) {
  setAccessToken(null);
  setUserName(null);
  localStorage.removeItem("access_token");
  localStorage.removeItem("user_name");
}

const LoginControl = () => {
  const setAccessToken = useContext(UserContext).setAccessToken;
  const setUserName = useContext(UserContext).setUserName;
  const accessToken = useContext(UserContext).accessToken;
  const userName = useContext(UserContext).userName;

  if (accessToken) {
    return (
      <Box
        sx={{
          flexGrow: 0,
          backgroundColor: "inherit",
          display: { xs: "none", md: "flex" },
        }}
      >
        <Button sx={{ my: 2, color: "white", display: "block" }}>
          {userName}
        </Button>

        <Button
          sx={{ my: 2, color: "white", display: "block" }}
          onClick={() => {
            logout(setAccessToken, setUserName);
          }}
        >
          Logout
        </Button>
      </Box>
    );
  }

  return (
    <Box
      sx={{
        flexGrow: 0,
        backgroundColor: "inherit",
        display: { xs: "none", md: "flex" },
      }}
    >
      <Link href="/signin">
        <Button sx={{ my: 2, color: "white", display: "block" }}>Login</Button>
      </Link>
      <Link href="/signup">
        <Button sx={{ my: 2, color: "white", display: "block" }}>
          Sign Up
        </Button>
      </Link>
    </Box>
  );
};

const SearchSettings = () => {
  const accessToken = useContext(UserContext).accessToken;

  if (accessToken) {
    return (
      <Link href="/settings">
        <Button sx={{ my: 1, color: "white", display: "block" }}>
          Search Settings
        </Button>
      </Link>
    );
  }
};

const Header = () => {
  return (
    <AppBar position="static" sx={{ backgroundColor: "#313C56" }}>
      <Container maxWidth="xxl">
        <Toolbar disableGutters>
          <Box
            sx={{
              flexGrow: 1,
              backgroundColor: "inherit",
              display: { xs: "none", md: "flex" },
            }}
          >
            <Link href="/news">
              <Button sx={{ my: 1, color: "white", display: "block" }}>
                News
              </Button>
            </Link>
            <SearchSettings />
          </Box>
          <Link href="/profile" style={{ textDecoration: "none" }}>
            <LoginControl />
          </Link>
        </Toolbar>
      </Container>
    </AppBar>
  );
};
export default Header;
