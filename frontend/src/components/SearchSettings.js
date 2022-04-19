import axios from "axios";
import React, { useState, useEffect } from "react";

import Box from "@mui/material/Box";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemText from "@mui/material/ListItemText";
import Divider from "@mui/material/Divider";
import Grid from "@mui/material/Grid";

const SearchSettings = () => {
  function handleClick(object) {
    console.log(object);
  }

  const access_token =
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huZG9lMSIsImV4cCI6MTY1MDM2MzI2OX0.DNcF-0_3R0yjMVH9oU_AQaH0jbw2D17efRUv7upczkc";

  const [settings, setSettings] = useState({});

  useEffect(() => {
    async function fetchSettings() {
      const config = {
        headers: {
          Authorization: `Bearer ${access_token}`,
        },
      };
      const { data } = await axios.get(
        "http://localhost:8000/users/me/user-search-settings",
        config
      );
      setSettings(data);
    }
    fetchSettings();
  }, []);

  return (
    <Grid
      container
      spacing={0}
      direction="column"
      alignItems="center"
      justifyContent="center"
      style={{ marginTop: "20%" }}
    >
      <Box sx={{ width: "50%", maxWidth: 360 }}>
        <List>
          <ListItem disablePadding>
            <ListItemButton onClick={handleClick}>
              <ListItemText primary={`Country`} />
              <ListItemText align="right" primary={`${settings.country}`} />
            </ListItemButton>
          </ListItem>

          <Divider />

          <ListItem disablePadding>
            <ListItemButton component="a" href="#simple-list">
              <ListItemText primary={`Category`} />
              <ListItemText align="right" primary={`${settings.category}`} />
            </ListItemButton>
          </ListItem>

          <Divider />

          <ListItem disablePadding>
            <ListItemButton component="a" href="#simple-list">
              <ListItemText primary={`Source`} />
              <ListItemText align="right" primary={`${settings.source}`} />
            </ListItemButton>
          </ListItem>

          <Divider />

          <ListItem disablePadding>
            <ListItemButton component="a" href="#simple-list">
              <ListItemText primary={`Language`} />
              <ListItemText align="right" primary={`${settings.language}`} />
            </ListItemButton>
          </ListItem>
        </List>
      </Box>
    </Grid>
  );
};

export default SearchSettings;
