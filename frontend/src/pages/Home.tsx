import { useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { TEAMS } from "../data/teams";

export default function Home() {
  const navigate = useNavigate();
  const [homeId, setHomeId] = useState("");
  const [awayId, setAwayId] = useState("");

  const canPlay = homeId && awayId && homeId !== awayId;

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#050513] text-white p-6">
      <div className="w-full max-w-3xl text-center">
        <div className="flex items-center justify-center gap-3 mb-6">
          <img src="/pl-logo.png" className="h-12 w-12" />
          <h1 className="text-3xl font-extrabold">Premier League Match Simulator</h1>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          <select
            value={homeId}
            onChange={(e) => setHomeId(e.target.value)}
            className="w-full p-3 rounded-xl bg-white/10 border border-white/15"
          >
            <option value="">Home Team</option>
            {TEAMS.map((t) => (
              <option key={t.id} value={t.id}>{t.name}</option>
            ))}
          </select>

          <select
            value={awayId}
            onChange={(e) => setAwayId(e.target.value)}
            className="w-full p-3 rounded-xl bg-white/10 border border-white/15"
          >
            <option value="">Away Team</option>
            {TEAMS.map((t) => (
              <option key={t.id} value={t.id}>{t.name}</option>
            ))}
          </select>
        </div>

        <button
          disabled={!canPlay}
          onClick={() => navigate(`/match/${homeId}/${awayId}`)}
          className={`px-6 py-3 rounded-xl font-semibold transition
            ${canPlay ? "bg-white text-black hover:opacity-90" : "bg-white/20 text-white/50 cursor-not-allowed"}`}
        >
          Play / Simulate
        </button>

        {!canPlay && (
          <p className="mt-3 text-sm text-white/50">
            Select two different teams to start.
          </p>
        )}
      </div>
    </div>
  );
}
