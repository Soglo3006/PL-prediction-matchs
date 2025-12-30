import { useMemo, useState, useEffect, useRef, type JSX  } from "react";
import { Link, useParams, useNavigate } from "react-router-dom";
import { ArrowUp, ArrowDown, RefreshCw, Users,RectangleVertical } from "lucide-react";
import { GiSoccerBall, GiRunningShoe  } from "react-icons/gi";
import { TEAMS } from "../data/teams";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Button } from "@/components/ui/button";

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

type TeamSide = "HOME" | "AWAY";

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
  const [loading, setLoading] = useState(true);
  const [matchData, setMatchData] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const hasSimulated = useRef(false);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [newHomeId, setNewHomeId] = useState("");
  const [newAwayId, setNewAwayId] = useState("");
  const navigate = useNavigate();

  const { homeId, awayId } = useParams();

  const homeTeam = TEAMS.find((t) => t.id === homeId);
  const awayTeam = TEAMS.find((t) => t.id === awayId);

  const simulateMatch = async (home: string, away: string) => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_URL}/predict_match`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ home_team: home, away_team: away })
      });

      const data = await response.json();
      
      if (data.error) {
        setError(data.error);
      } else {
        setMatchData(data);
      }
    } catch (err) {
      console.error('Erreur réseau:', err);
      setError('Erreur de connexion au serveur');
    } finally {
      setLoading(false);
    }
  };

  const handleReplay = () => {
    if (!homeTeam || !awayTeam) return;
    hasSimulated.current = false;
    simulateMatch(homeTeam.name, awayTeam.name);
  };

  const handleChangeTeams = () => {
    if (!newHomeId || !newAwayId || newHomeId === newAwayId) return;
    setIsDialogOpen(false);
    navigate(`/match/${newHomeId}/${newAwayId}`);
    hasSimulated.current = false;
    
    const newHome = TEAMS.find(t => t.id === newHomeId);
    const newAway = TEAMS.find(t => t.id === newAwayId);
    if (newHome && newAway) {
      simulateMatch(newHome.name, newAway.name);
    }
  };

  useEffect(() => {
  if (!homeTeam || !awayTeam) return;
  if (hasSimulated.current) return;
  hasSimulated.current = true;
  simulateMatch(homeTeam.name, awayTeam.name);
}, [homeTeam, awayTeam]);

  const events: MatchEvent[] = useMemo(() => {
    if (!matchData) return [];
    
    const allEvents: MatchEvent[] = [];

    // Ajouter les buts
    if (matchData?.buteurs?.home_team) {
      matchData.buteurs.home_team.forEach(([scorer, minute]: [string, number]) => {
        const assist = matchData.passeur.home_team.find(([_, m]: [string, number]) => m === minute)?.[0];
        allEvents.push({
          minute,
          type: "GOAL",
          side: "HOME",
          scorer,
          assist
        });
      });
    }

    if (matchData?.buteurs?.away_team) {
      matchData.buteurs.away_team.forEach(([scorer, minute]: [string, number]) => {
        const assist = matchData.passeur.away_team.find(([_, m]: [string, number]) => m === minute)?.[0];
        allEvents.push({
          minute,
          type: "GOAL",
          side: "AWAY",
          scorer,
          assist
        });
      });
    }

    // Ajouter les cartons jaunes
    if (matchData?.yellow_cards?.home_team) {
      matchData.yellow_cards.home_team.forEach(([player, minute]: [string, number]) => {
        allEvents.push({ minute, type: "YELLOW", side: "HOME", player });
      });
    }

    if (matchData?.yellow_cards?.away_team) {
      matchData.yellow_cards.away_team.forEach(([player, minute]: [string, number]) => {
        allEvents.push({ minute, type: "YELLOW", side: "AWAY", player });
      });
    }

    // Ajouter les cartons rouges
    if (matchData?.red_cards?.home_team) {
      matchData.red_cards.home_team.forEach(([player, minute]: [string, number]) => {
        allEvents.push({ minute, type: "RED", side: "HOME", player });
      });
    }

    if (matchData?.red_cards?.away_team) {
      matchData.red_cards.away_team.forEach(([player, minute]: [string, number]) => {
        allEvents.push({ minute, type: "RED", side: "AWAY", player });
      });
    }

    // Ajouter les substitutions
    if (matchData?.joueurs_remplaces?.home_team && matchData?.joueurs_rentres?.home_team) {
      matchData.joueurs_remplaces.home_team.forEach(([out, minute]: [string, number], idx: number) => {
        const inPlayer = matchData.joueurs_rentres.home_team[idx]?.[0];
        if (inPlayer) {
          allEvents.push({ minute, type: "SUB", side: "HOME", out, in: inPlayer });
        }
      });
    }

    if (matchData?.joueurs_remplaces?.away_team && matchData?.joueurs_rentres?.away_team) {
      matchData.joueurs_remplaces.away_team.forEach(([out, minute]: [string, number], idx: number) => {
        const inPlayer = matchData.joueurs_rentres.away_team[idx]?.[0];
        if (inPlayer) {
          allEvents.push({ minute, type: "SUB", side: "AWAY", out, in: inPlayer });
        }
      });
    }

    return allEvents.sort((a, b) => a.minute - b.minute);
  }, [matchData]);

  const stats = useMemo(() => {
    return {
      possession: { 
        home: matchData?.possesion?.home_team , 
        away: matchData?.possesion?.away_team
      },
      shots: { 
        home: matchData?.tirs?.home_team, 
        away: matchData?.tirs?.away_team
      },
      shotsOnTarget: { 
        home: matchData?.tirs_cadres?.home_team, 
        away: matchData?.tirs_cadres?.away_team 
      },
      fouls: { 
        home: matchData?.fouls?.home_team, 
        away: matchData?.fouls?.away_team
      },
      corners: { 
        home: matchData?.corners?.home_team, 
        away: matchData?.corners?.away_team
      },
      yellow: { 
        home: matchData?.yellow_cards?.home_team?.length, 
        away: matchData?.yellow_cards?.away_team?.length 
      },
      red: { 
        home: matchData?.red_cards?.home_team?.length, 
        away: matchData?.red_cards?.away_team?.length 
      },
    };
  }, [matchData]);

  if (loading) {
    return (
      <div className="min-h-screen bg-[#050513] text-white p-6 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white mx-auto mb-4"></div>
          <p>Simulation du match en cours...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-[#050513] text-white p-6">
        <Link to="/" className="text-white/70 hover:text-white">← Back</Link>
        <div className="mt-6 text-center">
          <p className="text-red-400">{error}</p>
          <button 
            onClick={() => window.location.reload()} 
            className="mt-4 px-4 py-2 bg-white/10 rounded-lg hover:bg-white/20"
          >
            Réessayer
          </button>
        </div>
      </div>
    );
  }

  const home = {
    name: homeTeam.name,
    score: matchData?.score?.home_team,
    logo: homeTeam.logo,
  };

  const away = {
    name: awayTeam.name,
    score: matchData?.score?.away_team,
    logo: awayTeam.logo,
  };

  return (
    <div className="min-h-screen text-white relative overflow-hidden">
      <div className="absolute inset-0 bg-[radial-gradient(900px_500px_at_50%_0%,rgba(99,102,241,0.25),transparent_60%),radial-gradient(700px_450px_at_20%_80%,rgba(16,185,129,0.18),transparent_60%),radial-gradient(700px_450px_at_80%_80%,rgba(249,115,22,0.12),transparent_60%)]" />
      <div className="absolute inset-0 bg-[#050513]" />

      <div className="relative max-w-6xl mx-auto p-6">
        <div className="flex items-center justify-between mb-5">
        <div className="flex gap-3">
          <Button
            variant="outline"
            onClick={handleReplay}
            className="bg-white/5 border-white/10  text-white cursor-pointer"
          >
            <RefreshCw className="h-4 w-4 mr-2" />
            Rejouer
          </Button>

          <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
            <DialogTrigger asChild>
              <Button
                variant="outline"
                className="bg-white/5 border-white/10 text-white cursor-pointer"
              >
                Changer les équipes
              </Button>
            </DialogTrigger>
            <DialogContent className="bg-[#0a0a1b] border-white/10 text-white">
              <DialogHeader>
                <DialogTitle>Choisir de nouvelles équipes</DialogTitle>
                <DialogDescription className="text-white/60">
                  Sélectionnez deux équipes différentes
                </DialogDescription>
              </DialogHeader>
              <div className="space-y-4 mt-4">
                <div>
                  <label className="text-sm text-white/70 mb-2 block">Domicile</label>
                  <Select value={newHomeId} onValueChange={setNewHomeId}>
                    <SelectTrigger className="bg-white/5 border-white/10 text-white cursor-pointer">
                      <SelectValue placeholder="Choisir" />
                    </SelectTrigger>
                    <SelectContent className="bg-[#0a0a1b] border-white/10 text-white max-h-64 overflow-y-auto ">
                      {TEAMS.map((team) => (
                        <SelectItem className="cursor-pointer" key={team.id} value={team.id}>
                          {team.name}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div>
                  <label className="text-sm text-white/70 mb-2 block">Extérieur</label>
                  <Select value={newAwayId} onValueChange={setNewAwayId}>
                    <SelectTrigger className="bg-white/5 border-white/10 text-white cursor-pointer">
                      <SelectValue placeholder="Choisir" />
                    </SelectTrigger>
                    <SelectContent className="bg-[#0a0a1b] border-white/10 text-white max-h-64 overflow-y-auto">
                      {TEAMS.map((team) => (
                        <SelectItem className="cursor-pointer" key={team.id} value={team.id}>
                          {team.name}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <Button
                  onClick={handleChangeTeams}
                  disabled={!newHomeId || !newAwayId || newHomeId === newAwayId}
                  className="w-full bg-white text-black hover:bg-white/90 cursor-pointer"
                >
                  Play
                </Button>
              </div>
            </DialogContent>
          </Dialog>
        </div>

        <div className="flex items-center gap-3">
          <img src="/pl-logo.png" alt="PL" className="h-20 w-20" />
        </div>
      </div>

        <div className="rounded-3xl border border-white/10 bg-white/5 backdrop-blur-xl shadow-[0_0_60px_rgba(0,0,0,0.35)] overflow-hidden">
          <div className="px-6 py-5 border-b border-white/10">
            <div className="flex items-center justify-center gap-6">
              <div className="flex items-center gap-3">
                <img src={home.logo} className="h-full w-25 border-white/10" />
                <div className="font-semibold tracking-wide">{home.name}</div>
              </div>

              <div className="flex justify-center items-center text-3xl md:text-4xl font-extrabold tracking-tight">
                <span>{home.score}</span>
                <span className="text-white/60 mx-3">-</span>
                <span>{away.score}</span>
              </div>

              <div className="flex items-center gap-3">
                <div className="font-semibold tracking-wide max-w-2xs">{away.name}</div>
                <img src={away.logo} className="h-full w-25 border-white/10" />
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-[1fr_2fr_1fr] gap-0">
            <SidePanel
              title="LINEUP"
              players={matchData?.lineups?.home_team?.starting_11 || []}
              bench={matchData?.lineups?.home_team?.bench || []}
              align="left"
              accentClass="text-emerald-300"
              events={events}
              side="HOME"
            />
            <div className="border-y lg:border-y-0 lg:border-x border-white/10">
              <div className="flex items-center justify-center gap-2 px-4 py-3 border-b border-white/10">
                <button
                  className={`${pillBase} ${
                    tab === "results"
                      ? "bg-white/15 border-white/20"
                      : "text-white/70 cursor-pointer"
                  }`}
                  onClick={() => setTab("results")}
                >
                  RESULTS
                </button>
                <button
                  className={`${pillBase} ${
                    tab === "stats"
                      ? "bg-white/15 border-white/20"
                      : "text-white/70 cursor-pointer"
                  }`}
                  onClick={() => setTab("stats")}
                >
                  STATS
                </button>
              </div>

              <div className="p-4 md:p-6">
                {tab === "results" ? (
                  <EventsTimeline events={events} />
                ) : (
                  <StatsTable homeName={home.name} awayName={away.name} stats={stats} />
                )}
              </div>

              <div className="px-4 py-3 border-t border-white/10 flex items-center justify-center gap-4 text-xs text-white/50">
                <span className="uppercase tracking-wider">
                  {tab === "results" ? "Viewing Results" : "Viewing Stats"}
                </span>
              </div>
            </div>
            <SidePanel
              title="LINEUP"
              players={matchData?.lineups?.away_team?.starting_11 || []}
              bench={matchData?.lineups?.away_team?.bench || []}
              align="right"
              accentClass="text-purple-300"
              events={events}
              side="AWAY"
            />
          </div>
        </div>
      </div>
    </div>
  );
}

function EventsTimeline({ events }: { events: MatchEvent[] }) {
  if (events.length === 0) {
    return (
      <div className="text-center text-white/50 py-8">
        Aucun événement dans ce match
      </div>
    );
  }

  return (
    <div className="relative">
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
      <div className="flex gap-2">
        <span className="mr-2"><GiSoccerBall className="w-4 h-4 text-white drop-shadow-lg" /></span>
        <span className="font-semibold">{e.scorer}</span>
        {e.assist ? <span className="text-white/60"> (Ast: {e.assist})</span> : null}
      </div>
    );
  }
  if (e.type === "YELLOW") {
    return (
      <div className="flex">
        <span className="mr-2"><RectangleVertical className="w-4 h-6 text-yellow-400 fill-yellow-400" /></span>
        <span className="font-semibold">{e.player}</span>
      </div>
    );
  }
  if (e.type === "RED") {
    return (
      <div>
        <span className="mr-2"><RectangleVertical className="w-4 h-6 text-red-400 fill-red-400" /></span>
        <span className="font-semibold">{e.player}</span>
      </div>
    );
  }
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
  const rows: Array<{ label: string; h: string | number; a: string | number }> = [
    { label: "Possession (%)", h: stats.possession.home, a: stats.possession.away },
    { label: "Shots", h: stats.shots.home, a: stats.shots.away },
    { label: "Shots on Target", h: stats.shotsOnTarget.home, a: stats.shotsOnTarget.away },
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

function SidePanel({
  title,
  players,
  bench,
  align,
  accentClass,
  events,
  side,
}: {
  title: string;
  players: Array<{ Player: string; Pos: string }>;
  bench: Array<{ Player: string; Pos: string }>;
  align: "left" | "right";
  accentClass: string;
  events: MatchEvent[];
  side: TeamSide;
}) {
  const [view, setView] = useState<"lineup" | "bench">("lineup");

  // Ordre des positions
  const positionOrder: Record<string, number> = {
    'GK': 1,
    'DF': 2,
    'MF': 3,
    'FW': 4
  };

  // Fonction pour extraire la première position
  const getFirstPosition = (pos: string): string => {
    if (pos.includes(',')) {
      return pos.split(',')[0];
    }
    return pos;
  };

  // Trier les joueurs par position
  const sortedPlayers = [...players].sort((a, b) => {
    const posA = getFirstPosition(a.Pos);
    const posB = getFirstPosition(b.Pos);
    return (positionOrder[posA] || 99) - (positionOrder[posB] || 99);
  });

  const sortedBench = [...bench].sort((a, b) => {
    const posA = getFirstPosition(a.Pos);
    const posB = getFirstPosition(b.Pos);
    return (positionOrder[posA] || 99) - (positionOrder[posB] || 99);
  });

  const displayPlayers = view === "lineup" ? sortedPlayers : sortedBench;

  // Fonction pour obtenir les symboles d'un joueur
  const getPlayerSymbols = (playerName: string): JSX.Element[] => {
    const symbols: JSX.Element[] = [];
    
    // Compter les buts
    const goals = events.filter(
    e => e.type === "GOAL" && e.side === side && e.scorer === playerName
  ).length;
  for (let i = 0; i < goals; i++) {
    symbols.push(
      <GiSoccerBall 
        key={`goal-${i}`}
        className="h-4 w-4 text-white drop-shadow-lg"
      />
    );
  }

    // Vérifier les passes décisives
    const assists = events.filter(
      e => e.type === "GOAL" && e.side === side && e.assist === playerName
    ).length;
    for (let i = 0; i < assists; i++) {
      symbols.push(
        <GiRunningShoe 
          key={`assist-${i}`}
          className="h-5 w-5 text-white/70 drop-shadow-lg"
        />
      );
    }

    // Vérifier les cartons jaunes
    const yellows = events.filter(
      e => e.type === "YELLOW" && e.side === side && e.player === playerName
    ).length;
    for (let i = 0; i < yellows; i++) {
      symbols.push(<RectangleVertical className="w-4 h-6 text-yellow-400 fill-yellow-400" />);
    }

    // Vérifier les cartons rouges
    const reds = events.filter(
      e => e.type === "RED" && e.side === side && e.player === playerName
    ).length;
    for (let i = 0; i < reds; i++) {
      symbols.push(<RectangleVertical className="w-4 h-6 text-red-400 fill-red-400" />);
    }

    return symbols;
  };

  return (
    <div className="p-4 md:p-5">
      <div className={`flex items-center ${align === "left" ? "justify-start" : "justify-end"} gap-3 mb-3`}>
        <button
          className={`text-xs font-semibold tracking-wider ${
            view === "lineup" ? accentClass : "text-white/50"
          }`}
          onClick={() => setView("lineup")}
        >
          LINEUP
        </button>
        <span className="text-white/20">|</span>
        <button
          className={`text-xs font-semibold tracking-wider ${
            view === "bench" ? accentClass : "text-white/50"
          }`}
          onClick={() => setView("bench")}
        >
          BENCH
        </button>
      </div>

      <div className="space-y-2">
        {displayPlayers.map((p, idx) => {
          const symbols = getPlayerSymbols(p.Player);
          
          return (
            <div
              key={`${p.Player}-${idx}`}
              className={`flex items-center justify-between rounded-xl border border-white/10 bg-white/5 px-3 py-2 ${
                align === "left" ? "" : "flex-row-reverse"
              }`}
            >
              <div className={`flex items-center gap-3 ${align === "left" ? "" : "flex-row-reverse"}`}>
                <span className="text-xs text-white/50 w-8">{getFirstPosition(p.Pos)}</span>
                {align === "left" ? (
                  <div className="flex items-center gap-2">
                  <span className="text-sm">{p.Player}</span>
                  {symbols.length > 0 && (
                    <div className="flex gap-1">
                      {symbols.map((symbol, i) => (
                        <span key={i} className="text-xs">{symbol}</span>
                      ))}
                    </div>
                  )}
                </div>
                ) : (
                  <div className="flex items-center gap-2 flex-row-reverse">
                  <span className="text-sm">{p.Player}</span>
                  {symbols.length > 0 && (
                    <div className="flex gap-1">
                      {symbols.map((symbol, i) => (
                        <span key={i} className="text-xs">{symbol}</span>
                      ))}
                    </div>
                  )}
                </div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}