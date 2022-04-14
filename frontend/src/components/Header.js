import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';

import Container from '@mui/material/Container';
import Button from '@mui/material/Button';
import Tooltip from '@mui/material/Tooltip';
import Link from '@mui/material/Link';

const Header = () => {
  return (
    <AppBar position="static" sx={{backgroundColor: '#313C56'}}>
      <Container maxWidth="xxl">
        <Toolbar disableGutters>
          <Box sx={{ flexGrow: 1, backgroundColor: "inherit", display: { xs: 'none', md: 'flex' } }}>

            <Link href="/news">
                <Button
                sx={{ my: 1, color: 'white', display: 'block' }}
                >
                News
                </Button>
            </Link>
            <Link href="/settings">
                <Button
                sx={{ my: 1, color: 'white', display: 'block' }}
                >
                Search Settings
                </Button>
            </Link>
          </Box>
          <Box sx={{ flexGrow: 0 }}>
            <Tooltip title="Open settings">
                <Button sx={{ my: 2, color: 'white', display: 'block' }}> Login</Button>
            </Tooltip>
          </Box>
        </Toolbar>
      </Container>
    </AppBar>
  );
};
export default Header;
