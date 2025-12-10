import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import UserHome from "./pages/UserHome";
import MyRobots from "./pages/MyRobots";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/home" element={<UserHome />} />
        <Route path="/robots" element={<MyRobots />} />
      </Routes>
    </BrowserRouter>
  );
}
