import React, { useState, useEffect } from 'react';
import { 
  Settings, 
  Activity, 
  Terminal, 
  MapPin, 
  Navigation, 
  Radio, 
  Gauge,
  Compass,
  Zap,
  Info,
  Layers,
  AlertCircle,
  Cpu,
  Monitor
} from 'lucide-react';
import { io } from 'socket.io-client';
import { motion, AnimatePresence } from 'framer-motion';
import axios from 'axios';

// Dashboard Configuration
const DASHBOARD_PORT = 4567;
const SOCKET_URL = `http://localhost:${DASHBOARD_PORT}`;

const App = () => {
  const [telemetry, setTelemetry] = useState({
    speed: 0,
    steering_angle: 0,
    throttle: 0,
    image: null,
    mode: 'Manual'
  });
  const [logs, setLogs] = useState(["[System] Initializing Simulation Bridge..."]);
  const [activeTab, setActiveTab] = useState('drive');
  const [isSimulationStarting, setIsSimulationStarting] = useState(false);

  useEffect(() => {
    // 1. Establish Socket Connection
    const socket = io(SOCKET_URL);

    socket.on('connect', () => {
      setLogs(prev => [...prev.slice(-10), "[System] Connected to Simulator Bridge."]);
    });

    socket.on('dashboard_update', (data) => {
      setTelemetry(data);
      // Logic for log updates (e.g. on turns)
      if (Math.abs(data.steering_angle) > 0.05) {
        setLogs(prev => [...prev.slice(-10), `[Drive] Turn Detected: ${data.steering_angle.toFixed(2)}`]);
      }
    });

    return () => socket.disconnect();
  }, []);

  const handleStartSimulation = async () => {
    if (isSimulationStarting) return;
    setIsSimulationStarting(true);
    setLogs(prev => [...prev, "[System] Requesting Simulator Launch..."]);
    try {
      const response = await axios.post(`${SOCKET_URL}/api/start`);
      if (response.data.status === 'started') {
        setLogs(prev => [...prev, "[System] Simulator process spawned successfully."]);
      } else {
        setLogs(prev => [...prev, `[System] Bridge Response: ${response.data.status}`]);
      }
    } catch (err) {
      setLogs(prev => [...prev.slice(-10), `[Error] Connection Failed: ${err.message}`]);
    } finally {
      setIsSimulationStarting(false);
    }
  };

  return (
    <div className="flex h-screen bg-[#05070a] text-slate-200 font-sans overflow-hidden">
      {/* Sidebar Overlay Blobs */}
      <div className="absolute top-0 -left-20 w-64 h-64 bg-indigo-600/10 blur-[120px]"></div>

      {/* Sidebar */}
      <aside className="w-20 lg:w-64 border-r border-white/5 flex flex-col p-6 z-20 backdrop-blur-3xl">
        <div className="flex items-center gap-3 mb-12">
          <div className="p-2 bg-indigo-500 rounded-xl shadow-lg shadow-indigo-500/30">
            <Zap className="w-6 h-6 text-white" />
          </div>
          <span className="text-xl font-bold tracking-tight hidden lg:block">AI-CAR 06</span>
        </div>

        <nav className="flex-1 space-y-4">
          <NavItem icon={<Navigation />} label="Live Drive" active={activeTab === 'drive'} onClick={() => setActiveTab('drive')} />
          <NavItem icon={<Monitor />} label="Lane Analysis" active={activeTab === 'analysis'} onClick={() => setActiveTab('analysis')} />
          <NavItem icon={<Cpu />} label="Model Stats" active={activeTab === 'model'} onClick={() => setActiveTab('model')} />
          <NavItem icon={<Settings />} label="Settings" active={activeTab === 'settings'} onClick={() => setActiveTab('settings')} />
        </nav>

        <div className="mt-auto space-y-4">
          <div className="glass-card p-4 rounded-2xl border border-white/5 bg-white/[0.02]">
            <p className="text-[10px] uppercase font-bold text-slate-500 tracking-widest mb-1">Status</p>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></div>
              <p className="text-sm font-medium">Bridge Online</p>
            </div>
          </div>
        </div>
      </aside>

      {/* Main Dashboard */}
      <main className="flex-1 flex flex-col p-8 overflow-y-auto relative z-10">
        <header className="flex justify-between items-center mb-10">
          <div>
            <h1 className="text-3xl font-bold tracking-tight mb-1">Self-Driving Dashboard</h1>
            <p className="text-slate-400 text-sm">Autonomous Vehicle Telemetry Interface — Hardware Acceleration Active</p>
          </div>
          <div className="flex gap-4">
            <button 
              onClick={handleStartSimulation}
              disabled={isSimulationStarting}
              className={`px-6 py-2 rounded-xl text-white font-medium transition-all shadow-lg ${
                isSimulationStarting 
                ? 'bg-slate-700 cursor-not-allowed' 
                : 'bg-indigo-500 hover:bg-indigo-600 shadow-indigo-500/20 active:scale-95'
              }`}
            >
              {isSimulationStarting ? 'Initialising...' : 'Start Simulation'}
            </button>
          </div>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Visualizer (Live Feed) */}
          <section className="lg:col-span-2 space-y-8">
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="relative aspect-video rounded-[32px] overflow-hidden border border-white/10 shadow-2xl group"
            >
              {/* Scanline Effect */}
              <div className="absolute inset-0 pointer-events-none z-20 bg-[radial-gradient(ellipse_at_center,transparent_0%,rgba(0,0,0,0.4)_100%)]"></div>
              <div className="absolute top-0 left-0 w-full h-[2px] bg-indigo-400/20 z-20 animate-scan"></div>
              
              {/* Live Image from Simulator */}
              {telemetry.image ? (
                <img src={`data:image/jpeg;base64,${telemetry.image}`} className="w-full h-full object-cover" alt="View" />
              ) : (
                <div className="w-full h-full bg-slate-900 flex items-center justify-center flex-col gap-4">
                  <div className="p-6 rounded-full bg-slate-800 border border-white/5">
                    <Radio className="w-12 h-12 text-slate-500 animate-pulse" />
                  </div>
                  <p className="text-slate-500 font-medium">Waiting for Simulator Signal...</p>
                </div>
              )}

              {/* HUD Overlays */}
              <div className="absolute top-6 left-6 flex gap-3 z-30">
                <Badge label="1080P" icon={<Layers className="w-3 h-3" />} />
                <Badge label="NVIDIA" icon={<Cpu className="w-3 h-3" />} color="emerald" />
              </div>

              <div className="absolute bottom-10 left-10 flex flex-col gap-1 z-30">
                <p className="text-[10px] uppercase font-bold text-slate-300 tracking-[0.2em] drop-shadow-md">Current Drive Mode</p>
                <p className="text-4xl font-black text-indigo-400 tracking-tight drop-shadow-lg">{telemetry.mode.toUpperCase()}</p>
              </div>
            </motion.div>

            {/* Bottom Metrics */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
              <MetricCard label="Speed" value={telemetry.speed.toFixed(1)} unit="km/h" icon={<Gauge />} />
              <MetricCard label="Steering" value={telemetry.steering_angle.toFixed(2)} unit="rad" icon={<Compass />} />
              <MetricCard label="Throttle" value={Math.round(telemetry.throttle * 100)} unit="%" icon={<Zap />} />
              <MetricCard label="Latency" value="14" unit="ms" icon={<Activity />} />
            </div>
          </section>

          {/* Right Section: Telemetry & Logs */}
          <section className="space-y-8 flex flex-col">
            <div className="glass-card flex-1 min-h-[400px] p-8 rounded-[32px] border border-white/10 bg-white/[0.01] flex flex-col">
              <div className="flex items-center justify-between mb-8">
                <h3 className="font-bold flex items-center gap-2"><Terminal className="w-4 h-4 text-indigo-400" /> System Logs</h3>
                <span className="text-[10px] font-mono text-slate-500">v1.0-ALPHA</span>
              </div>
              <div className="flex-1 space-y-4 font-mono text-xs text-slate-400 overflow-y-auto">
                {logs.map((log, i) => (
                  <motion.div key={i} initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }}>
                    <span className="text-indigo-500 mr-2">➜</span> {log}
                  </motion.div>
                ))}
              </div>
            </div>

            {/* Safety Alerts */}
            <div className="glass-card p-6 rounded-[32px] border border-white/10 bg-indigo-500/5">
              <div className="flex items-center gap-4">
                <div className="p-3 bg-indigo-500/20 rounded-2xl">
                  <AlertCircle className="w-6 h-6 text-indigo-400" />
                </div>
                <div>
                  <h4 className="font-bold text-sm">Lane Assist Active</h4>
                  <p className="text-xs text-slate-500">Autonomous Steering Model Integrated.</p>
                </div>
              </div>
            </div>
          </section>
        </div>
      </main>
    </div>
  );
};

// UI Components
const NavItem = ({ icon, label, active, onClick }) => (
  <button 
    onClick={onClick}
    className={`w-full flex items-center gap-4 p-4 rounded-2xl transition-all group ${
      active ? 'bg-indigo-500 text-white shadow-xl shadow-indigo-500/20' : 'hover:bg-white/5 text-slate-400 hover:text-white'
    }`}
  >
    <span className={active ? 'text-white' : 'group-hover:text-white transition-colors'}>{icon}</span>
    <span className="font-semibold text-sm hidden lg:block">{label}</span>
  </button>
);

const Badge = ({ label, icon, color = 'indigo' }) => (
  <div className={`px-3 py-1.5 rounded-full glass border border-white/10 flex items-center gap-2 text-[10px] font-bold tracking-wider`}>
    <span className={`text-${color}-400`}>{icon}</span>
    {label}
  </div>
);

const MetricCard = ({ label, value, unit, icon }) => (
  <div className="glass-card p-6 rounded-3xl border border-white/10 bg-white/[0.01] hover:bg-white/[0.03] transition-all">
    <div className="p-2 mb-4 text-slate-500">{icon}</div>
    <div className="flex items-baseline gap-1">
      <span className="text-2xl font-black text-white leading-none">{value}</span>
      <span className="text-[10px] uppercase font-bold text-slate-500 tracking-widest">{unit}</span>
    </div>
    <p className="text-xs text-slate-500 mt-2 font-medium">{label}</p>
  </div>
);

export default App;
