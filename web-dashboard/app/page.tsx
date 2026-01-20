"use client";
import { useEffect, useState } from "react";
import io from "socket.io-client";
import Gauge from "./components/Gauge";

// Connect to the Python Bridge
const socket = io("http://localhost:4000");

interface Alert {
  timestamp: string;
  message: string;
}

export default function Home() {
  const [rpm, setRpm] = useState(0);
  const [gear, setGear] = useState("N");
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [connectionStatus, setConnectionStatus] = useState("DISCONNECTED");

  useEffect(() => {
    // Check if already connected
    if (socket.connected) {
      setConnectionStatus("CONNECTED");
    }

    socket.on("connect", () => {
      setConnectionStatus("CONNECTED");
    });

    socket.on("disconnect", () => {
      setConnectionStatus("DISCONNECTED");
    });

    socket.on("telemetry", (data) => {
      setRpm(data.rpm);
      setGear(data.gear);
      setAlerts(data.alerts || []);
    });

    return () => {
      socket.off("connect");
      socket.off("disconnect");
      socket.off("telemetry");
      // socket.disconnect(); // Don't disconnect, let it persist
    };
  }, []);

  const latestAlert = alerts.length > 0 ? alerts[alerts.length - 1] : null;
  const isDanger = !!latestAlert;

  return (
    <main className={`flex min-h-screen flex-col items-center justify-center p-8 relative overflow-hidden transition-colors duration-100 ${isDanger ? 'bg-red-950/30' : 'bg-black'}`}>

      {/* SECURITY ALERT OVERLAY */}
      {isDanger && (
        <div className="absolute inset-0 pointer-events-none z-50 flex items-center justify-center animate-flash-red">
          <div className="bg-red-600/90 text-black font-black text-6xl px-12 py-6 transform -rotate-12 border-4 border-black shadow-[0_0_50px_rgba(255,0,0,0.8)] tracking-tighter uppercase">
            {latestAlert?.message || "SECURITY BREACH DETECTED"}
          </div>
        </div>
      )}

      {/* Header / Status Bar */}
      <div className={`absolute top-0 w-full p-4 flex justify-between items-center glass-panel rounded-none border-t-0 border-x-0 z-40 transition-colors ${isDanger ? 'border-red-500 bg-red-900/20' : ''}`}>
        <h1 className="text-xl font-bold tracking-widest text-white">
          DIGITAL TWIN <span className={isDanger ? "text-red-500" : "text-[#00f0ff]"}>INTERFACE</span>
        </h1>
        <div className="flex items-center gap-2">
          <div className={`w-2 h-2 rounded-full ${connectionStatus === 'CONNECTED' ? (isDanger ? 'bg-red-500 animate-ping' : 'bg-green-500 animate-pulse') : 'bg-red-500'}`}></div>
          <span className={`text-xs font-mono ${isDanger ? 'text-red-400 font-bold' : 'text-gray-400'}`}>
            {isDanger ? 'IDS ALERT ACTIVE' : connectionStatus}
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 w-full max-w-5xl mt-12 z-10">

        {/* Center: Main RPM Gauge */}
        <div className="col-span-1 lg:col-span-1 flex justify-center">
          <Gauge value={rpm} max={8000} label="Engine RPM" unit="RPM" color={isDanger ? "#ff0000" : undefined} />
        </div>

        {/* Right: Gear Indicator */}
        <div className={`col-span-1 flex flex-col items-center justify-center glass-panel p-8 min-h-[200px] transition-colors ${isDanger ? 'border-red-500 bg-red-950/50' : ''}`}>
          <span className="text-gray-500 text-sm uppercase tracking-widest mb-2">Transmission</span>
          <div className={`text-8xl font-black neon-text ${isDanger ? 'text-red-500' : 'text-white'}`}>
            {gear}
          </div>
          <div className="mt-4 flex gap-2">
            {['P', 'R', 'N', 'D'].map((g) => (
              <span key={g} className={`text-xs p-1 ${gear === g || (g === 'D' && ['1', '2', '3'].includes(gear)) ? (isDanger ? 'text-red-500 font-bold' : 'text-[#00f0ff] font-bold') : 'text-gray-700'}`}>
                {g}
              </span>
            ))}
          </div>
        </div>

        {/* Left: Info / Speed (Simulated) */}
        <div className="col-span-1 flex justify-center">
          {/* Simple simulation of speed logic: RPM * Gear * constant */}
          <Gauge value={(rpm / 8000) * 120} max={200} label="Vehicle Speed" unit="KM/H" color={isDanger ? "#ff0000" : "#ff0055"} />
        </div>

      </div>

      {/* Footer Log Placeholder */}
      <div className={`absolute bottom-8 w-full max-w-5xl p-4 glass-panel opacity-90 z-40 transition-colors ${isDanger ? 'border-red-500 bg-red-950/80 shadow-[0_0_20px_rgba(255,0,0,0.3)]' : 'opacity-50'}`}>
        <div className="text-xs text-gray-500 font-mono">SYSTEM LOGS:</div>
        <div className={`text-xs font-mono mt-1 ${isDanger ? 'text-red-500 font-bold animate-pulse' : 'text-[#00f0ff]'}`}>
          {isDanger
            ? `!! CRITICAL: ${latestAlert?.message} at ${new Date().toLocaleTimeString()} !!`
            : (connectionStatus === 'CONNECTED' ? '> SYSTEM ONLINE. TELEMETRY STREAM ACTIVE.' : '> SEARCHING FOR VEHICLE BUS...')
          }
        </div>
      </div>
    </main>
  );
}
