import axios from "axios";
import { useEffect, useState } from "react";

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
import FormControl from "@mui/material/FormControl";
import { useTheme } from "@mui/material/styles";
import TextField from "@mui/material/TextField";
import Alert from "@mui/material/Alert";

const UserProfile = () => {
  const access_token = localStorage.getItem("access_token");
  const config = {
    headers: {
      Authorization: `Bearer ${access_token}`,
    },
  };

  const [field_value, setFieldValue] = useState("");
  const handleChange = (event) => {
    setFieldValue(event.target.value);
  };

  const [open, setOpen] = useState(false);
  const [field_to_update, setField] = useState(null);
  const [refresh_nr, setRefresh] = useState(0);
  const handleClickSave = () => {
    async function updateUser() {
      let key = field_to_update;
      let update_data = {};
      update_data[key] = field_value;

      axios.patch("http://localhost:8000/users/me", update_data, config);

      if (field_to_update == "username") {
        localStorage.removeItem("access_token");
        localStorage.removeItem("user_name");
      }
      setOpen(false);
      setRefresh(refresh_nr + 1);
    }
    updateUser();
  };

  const handleClickOpen = (event) => {
    setOpen(true);
    setField(event);
  };
  const handleClickExit = () => {
    setOpen(false);
  };

  const [user, setUser] = useState({});
  useEffect(() => {
    async function get_current_user() {
      const current_user = await axios.get(
        "http://localhost:8000/users/me",
        config
      );
      setUser(current_user.data);
    }

    get_current_user();
  }, [refresh_nr]);

  const theme = useTheme();
  const fullScreen = useMediaQuery(theme.breakpoints.down("md"));
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
              onClick={(event) => handleClickOpen("username", event)}
            >
              <ListItemText primary={`username`} />
              <ListItemText align="right" primary={`${user.username}`} />
            </ListItemButton>
          </ListItem>
          <Divider />

          <ListItem disablePadding>
            <ListItemButton
              onClick={(event) => handleClickOpen("email", event)}
            >
              <ListItemText primary={`email`} />
              <ListItemText align="right" primary={`${user.email}`} />
            </ListItemButton>
          </ListItem>
          <Divider />
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
                <TextField
                  fullWidth
                  label={`New ${field_to_update}`}
                  autoFocus
                  onChange={handleChange}
                />
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

export default UserProfile;
