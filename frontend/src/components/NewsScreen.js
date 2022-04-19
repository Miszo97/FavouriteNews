import axios from "axios";
import { useState, useEffect } from "react";
import Card from "@mui/material/Card";
import CardActions from "@mui/material/CardActions";
import CardContent from "@mui/material/CardContent";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import Grid from "@mui/material/Grid";

const NewsScreen = () => {
  const access_token =
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huZG9lMSIsImV4cCI6MTY1MDM2MzI2OX0.DNcF-0_3R0yjMVH9oU_AQaH0jbw2D17efRUv7upczkc";

  const config = {
    headers: {
      Authorization: `Bearer ${access_token}`,
    },
  };

  const [news, setNews] = useState([]);

  useEffect(() => {
    async function fetchNews() {
      const { data } = await axios.get(
        "http://localhost:8000/users/me/followed-articles",
        config
      );
      setNews(data);
    }

    fetchNews();
  }, []);

  function handleClick(url) {}
  return (
    <Grid
      direction="column"
      alignItems="center"
      justifyContent="center"
      style={{ marginTop: "5%", marginBottom: "10%" }}
    >
      {news.map((article, index) => (
        <Card
          style={{ marginTop: "2%" }}
          sx={{ minWidth: 275 }}
          key={article.id}
        >
          <CardContent>
            <Typography variant="h5" component="div">
              {article.title}
            </Typography>
            <Typography sx={{ mb: 1.5 }} color="text.secondary">
              {article.author} {article.source}
            </Typography>
            <Typography variant="body2">{article.description}</Typography>
          </CardContent>
          <CardActions>
            <a href={article.url}>
              <Button onClick={handleClick} size="small">
                Read More
              </Button>
            </a>
          </CardActions>
        </Card>
      ))}
    </Grid>
  );
};
export default NewsScreen;
