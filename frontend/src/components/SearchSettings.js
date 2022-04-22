import axios from "axios";
import React, { useState, useEffect } from "react";

import Box from "@mui/material/Box";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemText from "@mui/material/ListItemText";
import Divider from "@mui/material/Divider";
import Grid from "@mui/material/Grid";

import Button from "@mui/material/Button";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogTitle from "@mui/material/DialogTitle";
import useMediaQuery from "@mui/material/useMediaQuery";
import { useTheme } from "@mui/material/styles";
import FormControl from "@mui/material/FormControl";

import InputLabel from "@mui/material/InputLabel";
import MenuItem from "@mui/material/MenuItem";
import Select from "@mui/material/Select";

import {
  country_options,
  source_options,
  language_options,
  category_options,
} from "../utils";

const SearchSettings = () => {
  const access_token = localStorage.getItem("access_token");
  const config = {
    headers: {
      Authorization: `Bearer ${access_token}`,
    },
  };

  const [settings, setSettings] = useState({});

  useEffect(() => {
    async function fetchSettings() {
      const { data } = await axios.get(
        "http://localhost:8000/users/me/user-search-settings",
        config
      );
      setSettings(data);
    }
    fetchSettings();
  });

  const [open, setOpen] = React.useState(false);
  const theme = useTheme();
  const fullScreen = useMediaQuery(theme.breakpoints.down("md"));

  const [field_to_update, setField] = React.useState("");
  const [field_options, setOptions] = useState([]);

  const handleClickOpen = (event) => {
    setOpen(true);
    setField(event);
    switch (event) {
      case "country":
        setOptions(country_options);
        break;
      case "source":
        setOptions(source_options);
        break;
      case "language":
        setOptions(language_options);
        break;
      case "category":
        setOptions(category_options);
        break;
    }
  };

  const handleClickExit = () => {
    setOpen(false);
  };

  const handleClickSave = () => {
    setOpen(false);
    var key = field_to_update;
    var update_data = {};
    update_data[key] = chosen_option;
    axios({
      method: "patch",
      url: "http://localhost:8000/users/me/user-search-settings",
      data: update_data,
      headers: { Authorization: `Bearer ${access_token}` },
    });
  };

  const [chosen_option, setChoice] = React.useState("");
  const handleChange = (event) => {
    setChoice(event.target.value);
  };

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
            <ListItemButton
              id="country"
              onClick={(event) => handleClickOpen("country", event)}
            >
              <ListItemText primary={`Country`} />
              <ListItemText align="right" primary={`${settings.country}`} />
            </ListItemButton>
          </ListItem>

          <Divider />

          <ListItem disablePadding>
            <ListItemButton
              id="category"
              onClick={(event) => handleClickOpen("category", event)}
            >
              <ListItemText primary={`Category`} />
              <ListItemText align="right" primary={`${settings.category}`} />
            </ListItemButton>
          </ListItem>

          <Divider />

          <ListItem disablePadding>
            <ListItemButton
              id="source"
              onClick={(event) => handleClickOpen("source", event)}
            >
              <ListItemText primary={`Source`} />
              <ListItemText align="right" primary={`${settings.source}`} />
            </ListItemButton>
          </ListItem>

          <Divider />

          <ListItem disablePadding>
            <ListItemButton
              id="language"
              onClick={(event) => handleClickOpen("language", event)}
            >
              <ListItemText primary={`Language`} />
              <ListItemText align="right" primary={`${settings.language}`} />
            </ListItemButton>
          </ListItem>
        </List>
      </Box>

      <Dialog
        fullScreen={fullScreen}
        open={open}
        aria-labelledby="responsive-dialog-title"
      >
        <DialogTitle
          sx={{ width: "50%", minWidth: 300 }}
          id="responsive-dialog-title"
        >
          {`Update ${field_to_update}`}
        </DialogTitle>
        <FormControl fullWidth>
          <DialogContent>
            <List>
              <ListItem disablePadding>
                <ListItemButton>
                  <FormControl sx={{ width: "100%" }}>
                    <InputLabel id="demo-simple-select-label">
                      {field_to_update}
                    </InputLabel>
                    <Select
                      labelId="demo-simple-select-label"
                      id="demo-simple-select"
                      value={chosen_option}
                      label="label"
                      onChange={handleChange}
                    >
                      {field_options.map((option, index) => (
                        <MenuItem id="field_value" key={index} value={option}>
                          {option}
                        </MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                </ListItemButton>
              </ListItem>
            </List>
          </DialogContent>

          <DialogActions>
            <Button autoFocus onClick={handleClickExit}>
              Exit
            </Button>
            <Button onClick={handleClickSave} autoFocus>
              Save
            </Button>
          </DialogActions>
        </FormControl>
      </Dialog>
    </Grid>
  );
};

export default SearchSettings;
