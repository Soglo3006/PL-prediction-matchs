import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { TEAMS } from "../data/teams";
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";


export default function Home() {
  const navigate = useNavigate();
  const [homeId, setHomeId] = useState("");
  const [awayId, setAwayId] = useState("");

  const canPlay = homeId && awayId && homeId !== awayId;

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#050513] text-white p-6">
      <div className="w-full max-w-3xl text-center">
        <div className="flex flex-col items-center justify-center gap-3 mb-6">
          <img src="/pl-logo.png" className="h-30 w-30" />
          <h1 className="text-3xl font-extrabold">Premier League Match Simulator</h1>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          <Select value={homeId} onValueChange={setHomeId}>
            <SelectTrigger className="w-full h-15 p-3 rounded-xl bg-white/10 border border-white/15 cursor-pointer">
              <SelectValue placeholder="Home Team" className="text-center"/>
            </SelectTrigger>
            <SelectContent className="max-h-64 overflow-y-auto">
              <SelectGroup>
                <SelectLabel>Home Team</SelectLabel>
                {TEAMS.map((t) => (
                  <SelectItem className="cursor-pointer" key={t.id} value={t.id}>{t.name}</SelectItem>
                ))}
              </SelectGroup>
            </SelectContent>
          </Select>

          <Select value={awayId} onValueChange={setAwayId}>
            <SelectTrigger className="w-full h-15 p-3 rounded-xl bg-white/10 border border-white/15 cursor-pointer">
              <SelectValue placeholder="Away Team" />
            </SelectTrigger>
            <SelectContent className="max-h-64 overflow-y-auto">
              <SelectGroup>
                <SelectLabel>Away Team</SelectLabel>
                {TEAMS.map((t) => (
                  <SelectItem className="cursor-pointer" key={t.id} value={t.id}>{t.name}</SelectItem>
                ))}
              </SelectGroup>
            </SelectContent>
          </Select>
        </div>

        <button
          disabled={!canPlay}
          onClick={() => navigate(`/match/${homeId}/${awayId}`)}
          className={`px-6 py-3 rounded-xl font-semibold transition
            ${canPlay ? "bg-white text-black hover:opacity-90 cursor-pointer" : "bg-white/20 text-white/50 cursor-not-allowed"}`}
        >
          Play
        </button>
      </div>
    </div>
  );
}
