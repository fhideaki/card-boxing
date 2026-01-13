import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import Cards from "./pages/Cards";
import Parts from "./pages/Parts";
import MyRobots from "./pages/MyRobots";

// import MyRobots from "./pages/MyRobots";
// import Login from "./pages/Login";

function App() {
  return (
    <Router>
      {/* A Navbar fica fora das Routes para aparecer em todas as páginas */}
      <Navbar />
      
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/cards" element={<Cards />} />
        <Route path="/parts" element={<Parts />} />
        <Route path="/robots" element={<MyRobots />} />
        {/* <Route path="/robots" element={<MyRobots />} />
        <Route path="/login" element={<Login />} /> */}
      </Routes>
    </Router>
  );
}

export default App;