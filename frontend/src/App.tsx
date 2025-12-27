import { Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Match from "./pages/Match";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/match/:homeId/:awayId" element={<Match />} />
    </Routes>
  );
}
