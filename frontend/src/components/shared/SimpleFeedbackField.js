import Box from "@mui/material/Box";
import Alert from "@mui/material/Alert";

const SimpleFeedbackField = (props) => {
  const response = props.response;
  let box = "";
  if (response === "success") {
    box = (
      <Box marginBottom={2}>
        <Alert severity="success">Successfully updated!</Alert>
      </Box>
    );
  } else if (response === "failure") {
    box = (
      <Box marginBottom={2}>
        <Alert severity="error">Something went wrong</Alert>
      </Box>
    );
  }
  return box;
};

export default SimpleFeedbackField;
