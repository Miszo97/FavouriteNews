import Alert from "@mui/material/Alert";
import Box from "@mui/material/Box";

export const FeedbackUpdateField = (props) => {
  const response = props.response;
  const field = props.field;

  if (response == null) return;

  switch (response.status) {
    case 200:
      return (
        <Box marginBottom={2}>
          <Alert severity="success">{field} has been updated</Alert>
        </Box>
      );
    default:
      return (
        <Box marginBottom={2}>
          <Alert severity="error">{response.data.error}</Alert>
        </Box>
      );
  }
};
