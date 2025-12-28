import { useMemo, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { ArrowUp, ArrowDown } from "lucide-react";
import { TEAMS } from "../data/teams";



type TeamSide = "HOME" | "AWAY";
type EventType = "GOAL" | "YELLOW" | "RED" | "SUB";

type PlayerRow = { number: number; name: string; rating?: number };

type MatchEvent =
  | {
      minute: number;
      type: "GOAL";
      side: TeamSide;
      scorer: string;
      assist?: string;
    }
  | {
      minute: number;
      type: "YELLOW" | "RED";
      side: TeamSide;
      player: string;
    }
  | {
      minute: number;
      type: "SUB";
      side: TeamSide;
      out: string;
      in: string;
    };

const pillBase =
  "px-3 py-1 rounded-full text-xs font-semibold border border-white/10 bg-white/5 hover:bg-white/10 transition";

export default function Match() {
  const [tab, setTab] = useState<"results" | "stats">("results");
  const [leftView, setLeftView] = useState<"lineup" | "bench">("lineup");
  const [rightView, setRightView] = useState<"lineup" | "bench">("lineup");

  const { homeId, awayId } = useParams();

const homeTeam = TEAMS.find((t) => t.id === homeId);
const awayTeam = TEAMS.find((t) => t.id === awayId);

if (!homeTeam || !awayTeam) {
  return (
    <div className="min-h-screen bg-[#050513] text-white p-6">
      <Link to="/" className="text-white/70 hover:text-white">← Back</Link>
      <p className="mt-6 text-white/70">Invalid teams selection.</p>
    </div>
  );
}


  // Mock data (later replace by API)
  const home = {
    name: homeTeam.name,
    score: 5,
    logo: homeTeam.logo,
    lineup: [
      { number: 24, name: "Onana", rating: 7.5 },
      { number: 2, name: "Foyth", rating: 6.9 },
      { number: 37, name: "Škriniar", rating: 7.0 },
      { number: 36, name: "Darmian", rating: 6.5 },
      { number: 32, name: "Dimarco", rating: 6.6 },
      { number: 23, name: "Barella", rating: 9.6 },
      { number: 20, name: "Çalhanoğlu", rating: 6.7 },
      { number: 7, name: "Mancini", rating: 6.7 },
      { number: 90, name: "Lukaku", rating: 10.0 },
      { number: 10, name: "Lautaro", rating: 7.4 },
      { number: 33, name: "Varela", rating: 6.6 },
    ] as PlayerRow[],
    bench: [
      { number: 12, name: "Handanović", rating: 6.4 },
      { number: 8, name: "Sensi", rating: 6.2 },
      { number: 14, name: "Asllani", rating: 6.1 },
      { number: 11, name: "Correa", rating: 6.0 },
      { number: 6, name: "De Vrij", rating: 6.3 },
      { number: 15, name: "Acerbi", rating: 6.2 },
      { number: 21, name: "Bellanova", rating: 6.1 },
    ] as PlayerRow[],
  };

  const away = {
    name: awayTeam.name,
    score: 1,
    logo: awayTeam.logo,
    lineup: [
      { number: 12, name: "Carnesecchi", rating: 4.4 },
      { number: 21, name: "Chiriches", rating: 5.8 },
      { number: 5, name: "Vásquez J.", rating: 4.0 },
      { number: 33, name: "Quagliata", rating: 6.2 },
      { number: 8, name: "Sydorchuk", rating: 4.2 },
      { number: 17, name: "Sernicola", rating: 5.8 },
      { number: 88, name: "Galdames", rating: 5.6 },
      { number: 28, name: "Meïté", rating: 4.5 },
      { number: 3, name: "Valeri", rating: 4.4 },
      { number: 77, name: "Okereke", rating: 5.6 },
      { number: 90, name: "Dessers", rating: 5.6 },
    ] as PlayerRow[],
    bench: [
      { number: 1, name: "Keeper 2", rating: 5.0 },
      { number: 19, name: "Midfielder 2", rating: 5.2 },
      { number: 22, name: "Forward 2", rating: 5.1 },
      { number: 41, name: "Defender 2", rating: 5.0 },
      { number: 66, name: "Winger 2", rating: 5.3 },
    ] as PlayerRow[],
  };

  const events: MatchEvent[] = [
    { minute: 47, type: "GOAL", side: "HOME", scorer: "Lukaku" },
    { minute: 56, type: "GOAL", side: "HOME", scorer: "Lukaku" },
    { minute: 63, type: "SUB", side: "AWAY", out: "Chiriches", in: "Aiwu" },
    { minute: 70, type: "GOAL", side: "HOME", scorer: "Lukaku" },
    { minute: 77, type: "SUB", side: "HOME", out: "Darmian", in: "Bastoni" },
    { minute: 77, type: "SUB", side: "AWAY", out: "Quagliata", in: "Ferrari" },
    { minute: 88, type: "YELLOW", side: "AWAY", player: "Galdames" },
  ];

  const stats = {
    possession: { home: 58, away: 42 },
    shots: { home: 16, away: 7 },
    shotsOnTarget: { home: 9, away: 2 },
    xg: { home: 2.4, away: 0.8 },
    fouls: { home: 10, away: 14 },
    corners: { home: 6, away: 3 },
    yellow: { home: 0, away: 1 },
    red: { home: 0, away: 0 },
  };

  const sortedEvents = useMemo(
    () => [...events].sort((a, b) => a.minute - b.minute),
    [events]
  );

  return (
    <div className="min-h-screen text-white relative overflow-hidden">
      {/* Background (dark + subtle glow) */}
      <div className="absolute inset-0 bg-[radial-gradient(900px_500px_at_50%_0%,rgba(99,102,241,0.25),transparent_60%),radial-gradient(700px_450px_at_20%_80%,rgba(16,185,129,0.18),transparent_60%),radial-gradient(700px_450px_at_80%_80%,rgba(249,115,22,0.12),transparent_60%)]" />
      <div className="absolute inset-0 bg-[#050513]" />

      <div className="relative max-w-6xl mx-auto p-6">
        {/* Top bar */}
        <div className="flex items-center justify-between mb-5">
          <Link to="/" className="text-white/70 hover:text-white">
            ← Back
          </Link>
          <div className="flex items-center gap-3">
            <img src="/pl-logo.png" alt="Premier League" className="h-12 w-12" />
          </div>
        </div>

        {/* Main panel */}
        <div className="rounded-3xl border border-white/10 bg-white/5 backdrop-blur-xl shadow-[0_0_60px_rgba(0,0,0,0.35)] overflow-hidden">
          {/* Score header */}
          <div className="px-6 py-5 border-b border-white/10">
            <div className="flex items-center justify-center gap-6">
              <div className="flex items-center gap-3">
                <img src={home.logo} className="h-10 w-10 rounded-full bg-white/10 border border-white/10" />
                <div className="font-semibold tracking-wide max-w-2xl">{home.name}</div>
              </div>

              <div className="flex justify-center items-center text-3xl md:text-4xl font-extrabold tracking-tight">
                <span>{home.score}</span>
                <span className="text-white/60 mx-3">-</span>
                <span>{away.score}</span>
              </div>

              <div className="flex items-center gap-3">
                <div className="font-semibold tracking-wide max-w-2xl">{away.name}</div>
                <img src={away.logo} className="h-10 w-10 rounded-full bg-white/10 border border-white/10" />
              </div>
            </div>
          </div>

          {/* Content grid */}
          <div className="grid grid-cols-1 lg:grid-cols-[1fr_1.2fr_1fr] gap-0">
            {/* Left: lineup */}
            <SidePanel
              titleLeft="LINEUP"
              titleRight="BENCH"
              active={leftView}
              onChange={setLeftView}
              accentClass="text-emerald-300"
              players={leftView === "lineup" ? home.lineup : home.bench}
              align="left"
            />

            {/* Center */}
            <div className="border-y lg:border-y-0 lg:border-x border-white/10">
              {/* Center tabs like FIFA bottom bar (but on top of center area) */}
              <div className="flex items-center justify-center gap-2 px-4 py-3 border-b border-white/10">
                <button
                  className={`${pillBase} ${
                    tab === "results"
                      ? "bg-white/15 border-white/20"
                      : "text-white/70"
                  }`}
                  onClick={() => setTab("results")}
                >
                  RESULTS
                </button>
                <button
                  className={`${pillBase} ${
                    tab === "stats"
                      ? "bg-white/15 border-white/20"
                      : "text-white/70"
                  }`}
                  onClick={() => setTab("stats")}
                >
                  STATS
                </button>
              </div>

              {/* Center content */}
              <div className="p-4 md:p-6">
                {tab === "results" ? (
                  <EventsTimeline events={sortedEvents} />
                ) : (
                  <StatsTable homeName={home.name} awayName={away.name} stats={stats} />
                )}
              </div>

              {/* Bottom bar like FIFA */}
              <div className="px-4 py-3 border-t border-white/10 flex items-center justify-center gap-4 text-xs text-white/50">
                <span className="uppercase tracking-wider flex justify-center items-center">
                  {tab === "results" ? "Viewing Results" : "Viewing Stats"}
                </span>
              </div>
            </div>

            {/* Right: lineup */}
            <SidePanel
              titleLeft="LINEUP"
              titleRight="BENCH"
              active={rightView}
              onChange={setRightView}
              accentClass="text-purple-300"
              players={rightView === "lineup" ? away.lineup : away.bench}
              align="right"
            />
          </div>
        </div>
      </div>
    </div>
  );
}

/* ---------- Components ---------- */

function SidePanel(props: {
  titleLeft: string;
  titleRight: string;
  active: "lineup" | "bench";
  onChange: (v: "lineup" | "bench") => void;
  accentClass: string;
  players: PlayerRow[];
  align: "left" | "right";
}) {
  const { titleLeft, titleRight, active, onChange, accentClass, players, align } =
    props;

  return (
    <div className="p-4 md:p-5">
      <div className={`flex items-center ${align === "left" ? "justify-start" : "justify-end"} gap-3 mb-3`}>
        <button
          className={`text-xs font-semibold tracking-wider ${
            active === "lineup" ? accentClass : "text-white/50"
          }`}
          onClick={() => onChange("lineup")}
        >
          {titleLeft}
        </button>
        <span className="text-white/20">|</span>
        <button
          className={`text-xs font-semibold tracking-wider ${
            active === "bench" ? accentClass : "text-white/50"
          }`}
          onClick={() => onChange("bench")}
        >
          {titleRight}
        </button>
      </div>

      <div className="space-y-2">
        {players.map((p) => (
          <div
            key={`${p.number}-${p.name}`}
            className={`flex items-center justify-between rounded-xl border border-white/10 bg-white/5 px-3 py-2 ${
              align === "left" ? "" : "flex-row-reverse"
            }`}
          >
            <div className={`flex items-center gap-3 ${align === "left" ? "" : "flex-row-reverse"}`}>
              <span className="text-xs text-white/50 w-6 text-right">{p.number}</span>
              <span className="text-sm">{p.name}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function EventsTimeline({ events }: { events: MatchEvent[] }) {
  return (
    <div className="relative">
      {/* center divider */}
      <div className="absolute left-1/2 top-0 bottom-0 w-px bg-white/10" />

      <div className="space-y-3">
        {events.map((e, idx) => {
          const isHome = e.side === "HOME";
          return (
            <div
              key={idx}
              className={`relative flex items-center ${
                isHome ? "justify-start" : "justify-end"
              }`}
            >
              <div
                className={`w-[calc(50%-16px)] rounded-2xl border border-white/10 bg-white/5 px-4 py-3 ${
                  isHome ? "mr-8" : "ml-8"
                }`}
              >
                <div className="flex items-center justify-between gap-3 text-xs text-white/60">
                  <span className="font-semibold text-white/80">{e.minute}'</span>
                  <span className="uppercase tracking-wider">
                    {labelForEvent(e)}
                  </span>
                </div>

                <div className="mt-1 text-sm">
                  {renderEventText(e)}
                </div>
              </div>

              {/* center dot */}
              <div className="absolute left-1/2 -translate-x-1/2 h-2.5 w-2.5 rounded-full bg-white/30 border border-white/20" />
            </div>
          );
        })}
      </div>
    </div>
  );
}

function labelForEvent(e: MatchEvent) {
  switch (e.type) {
    case "GOAL":
      return "Goal";
    case "YELLOW":
      return "Yellow";
    case "RED":
      return "Red";
    case "SUB":
      return "Substitution";
  }
}

function renderEventText(e: MatchEvent) {
  if (e.type === "GOAL") {
    return (
      <div>
        <span className="mr-2">⚽</span>
        <span className="font-semibold">{e.scorer}</span>
        {e.assist ? <span className="text-white/60"> (Ast: {e.assist})</span> : null}
      </div>
    );
  }
  if (e.type === "YELLOW") {
    return (
      <div>
        <span className="mr-2">🟨</span>
        <span className="font-semibold">{e.player}</span>
      </div>
    );
  }
  if (e.type === "RED") {
    return (
      <div>
        <span className="mr-2">🟥</span>
        <span className="font-semibold">{e.player}</span>
      </div>
    );
  }
  // SUB
  return (
    <div>
      <div className="flex items-center gap-2">
        <ArrowUp className="h-4 w-4 text-emerald-400" />
        <span className="font-semibold">{e.in}</span>
        </div>
        <div className="flex items-center gap-2 text-white/60">
        <ArrowDown className="h-4 w-4 text-red-400" />
        <span>{e.out}</span>
        </div>
    </div>
  );
}

function StatsTable({
  homeName,
  awayName,
  stats,
}: {
  homeName: string;
  awayName: string;
  stats: any;
}) {
  const rows: Array<{ label: string; h: string | number; a: string | number }> =
    [
      { label: "Possession (%)", h: stats.possession.home, a: stats.possession.away },
      { label: "Shots", h: stats.shots.home, a: stats.shots.away },
      { label: "Shots on Target", h: stats.shotsOnTarget.home, a: stats.shotsOnTarget.away },
      { label: "xG", h: stats.xg.home, a: stats.xg.away },
      { label: "Fouls", h: stats.fouls.home, a: stats.fouls.away },
      { label: "Corners", h: stats.corners.home, a: stats.corners.away },
      { label: "Yellow Cards", h: stats.yellow.home, a: stats.yellow.away },
      { label: "Red Cards", h: stats.red.home, a: stats.red.away },
    ];

  return (
    <div className="rounded-2xl border border-white/10 bg-white/5 overflow-hidden">
      <div className="grid grid-cols-3 px-4 py-3 border-b border-white/10 text-xs text-white/60">
        <div className="font-semibold text-white/80">{homeName}</div>
        <div className="text-center">STAT</div>
        <div className="font-semibold text-white/80 text-right">{awayName}</div>
      </div>

      <div className="divide-y divide-white/10">
        {rows.map((r) => (
          <div key={r.label} className="grid grid-cols-3 px-4 py-3 text-sm">
            <div className="text-white/80">{r.h}</div>
            <div className="text-center text-white/60">{r.label}</div>
            <div className="text-right text-white/80">{r.a}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
