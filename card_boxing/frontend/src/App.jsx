import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Login from "./pages/Login";
import UserHome from "./pages/UserHome";
import MyRobots from "./pages/MyRobots";
import CreateRobot from "./pages/CreateRobot";


export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/home" element={<UserHome />} />
      <Route path="/robots" element={<MyRobots />} />
      <Route path="/create-robot" element={<CreateRobot />} />
    </Routes>
  );
}
