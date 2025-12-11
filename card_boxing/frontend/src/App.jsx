import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Login from "./pages/Login";
import UserHome from "./pages/UserHome";
import MyRobots from "./pages/MyRobots";
import Register from './pages/Register';
// import CreateRobot from "./pages/CreateRobot";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/home" element={<UserHome />} />
      <Route path="/robots" element={<MyRobots />} />
      <Route path="/register" element={<Register />} />
      {/* <Route path="/createrobot" element={<CreateRobot />} /> */}
    </Routes>
  );
}
