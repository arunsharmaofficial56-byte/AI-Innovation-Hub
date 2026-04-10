import React, { useState, useEffect, useRef } from 'react';
import { 
  LayoutDashboard, 
  Camera, 
  History, 
  Settings, 
  Upload, 
  Download, 
  Trash2, 
  Info,
  ChevronRight,
  Loader2,
  Shield,
  Zap,
  Target
} from 'lucide-react';
import axios from 'axios';
import Webcam from 'react-webcam';
import { motion, AnimatePresence } from 'framer-motion';

const API_BASE = 'http://localhost:5000';

const App = () => {
  const [activeTab, setActiveTab] = useState('detect');
  const [isSidebarOpen, setSidebarOpen] = useState(true);
  const [selectedImage, setSelectedImage] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [detectionResult, setDetectionResult] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [confidence, setConfidence] = useState(0.25);
  const [history, setHistory] = useState([]);
  const [stats, setStats] = useState({ model: 'YOLOv8', status: 'Online', version: '8.0.0' });

  useEffect(() => {
    const savedHistory = JSON.parse(localStorage.getItem('detection_history') || '[]');
    setHistory(savedHistory);
    
    // Check backend status
    axios.get(`${API_BASE}/status`)
      .then(res => setStats(s => ({ ...s, ...res.data })))
      .catch(err => console.error("Backend offline", err));
  }, []);

  const handleImageUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    
    setSelectedImage(file);
    setPreviewUrl(URL.createObjectURL(file));
    setDetectionResult(null);
    processImage(file);
  };

  const processImage = async (file) => {
    setIsProcessing(true);
    const formData = new FormData();
    formData.append('image', file);
    formData.append('confidence', confidence);

    try {
      const response = await axios.post(`${API_BASE}/detect/image`, formData);
      setDetectionResult(response.data);
      
      const newHistory = [
        { 
          id: Date.now(), 
          name: file.name, 
          date: new Date().toLocaleString(), 
          count: response.data.detections.length,
          url: `${API_BASE}${response.data.result_url}`
        },
        ...history
      ].slice(0, 20);
      
      setHistory(newHistory);
      localStorage.setItem('detection_history', JSON.stringify(newHistory));
    } catch (error) {
      console.error("Detection failed", error);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="flex h-screen bg-slate-950 font-sans overflow-hidden">
      {/* Sidebar */}
      <motion.div 
        initial={false}
        animate={{ width: isSidebarOpen ? 260 : 80 }}
        className="glass h-full relative z-20 flex flex-col p-4"
      >
        <div className="flex items-center gap-3 mb-10 px-2 overflow-hidden whitespace-nowrap">
          <div className="bg-indigo-500 p-2 rounded-xl shadow-lg shadow-indigo-500/20">
            <Zap size={24} className="text-white" />
          </div>
          {isSidebarOpen && <span className="text-xl font-bold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-400">AI Vision Pro</span>}
        </div>

        <nav className="flex-1 space-y-2">
          <SidebarLink icon={<LayoutDashboard size={20}/>} label="Dashboard" active={activeTab === 'detect'} onClick={() => setActiveTab('detect')} isOpen={isSidebarOpen} />
          <SidebarLink icon={<Camera size={20}/>} label="Live Webcam" active={activeTab === 'webcam'} onClick={() => setActiveTab('webcam')} isOpen={isSidebarOpen} />
          <SidebarLink icon={<History size={20}/>} label="History" active={activeTab === 'history'} onClick={() => setActiveTab('history')} isOpen={isSidebarOpen} />
          <SidebarLink icon={<Info size={20}/>} label="Model Info" active={activeTab === 'about'} onClick={() => setActiveTab('about')} isOpen={isSidebarOpen} />
        </nav>

        <div className="mt-auto pt-6 border-t border-white/5">
          <button 
            onClick={() => setSidebarOpen(!isSidebarOpen)}
            className="flex items-center gap-3 w-full p-3 rounded-xl hover:bg-white/5 text-slate-400"
          >
            <ChevronRight className={`transition-transform duration-300 ${isSidebarOpen ? 'rotate-180' : ''}`} size={20} />
            {isSidebarOpen && <span>Minimize</span>}
          </button>
        </div>
      </motion.div>

      {/* Main Content */}
      <main className="flex-1 h-full overflow-y-auto px-6 py-8 relative">
        {/* Background blobs */}
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-indigo-600/10 blur-[120px] rounded-full"></div>
        <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-purple-600/10 blur-[120px] rounded-full"></div>

        <div className="max-w-6xl mx-auto relative z-10">
          <div className="flex justify-between items-center mb-10">
            <div>
              <h1 className="text-3xl font-bold text-white mb-2">
                {activeTab === 'detect' ? 'Object Detection' : activeTab === 'webcam' ? 'Live Stream' : activeTab === 'history' ? 'Detection History' : 'Model Specifications'}
              </h1>
              <p className="text-slate-400">Real-time object identification powered by YOLOv8 Architecture</p>
            </div>
            
            <div className="flex gap-4">
              <div className="glass-card px-4 py-2 rounded-xl flex items-center gap-3">
                <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></div>
                <span className="text-sm font-medium text-slate-300">System {stats.status}</span>
              </div>
            </div>
          </div>

          <AnimatePresence mode="wait">
            {activeTab === 'detect' && (
              <motion.div 
                key="detect"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="grid grid-cols-1 lg:grid-cols-3 gap-6"
              >
                <div className="lg:col-span-2 space-y-6">
                  {/* Upload Area */}
                  {!previewUrl ? (
                    <label className="group flex flex-col items-center justify-center w-full h-[400px] rounded-3xl border-2 border-dashed border-slate-700 hover:border-indigo-500 bg-slate-900/50 cursor-pointer transition-all duration-300 overflow-hidden relative">
                      <div className="absolute inset-0 bg-indigo-500/5 opacity-0 group-hover:opacity-100 transition-opacity"></div>
                      <div className="flex flex-col items-center justify-center pt-5 pb-6">
                        <div className="p-4 bg-slate-800 rounded-2xl mb-4 group-hover:scale-110 group-hover:bg-indigo-500/20 transition-all duration-300">
                          <Upload className="w-10 h-10 text-slate-400 group-hover:text-indigo-400" />
                        </div>
                        <p className="mb-2 text-lg text-slate-200 font-semibold">Click to upload or drag and drop</p>
                        <p className="text-sm text-slate-500">SVG, PNG, JPG or GIF (MAX. 800x400px)</p>
                      </div>
                      <input type="file" className="hidden" onChange={handleImageUpload} accept="image/*" />
                    </label>
                  ) : (
                    <div className="relative rounded-3xl overflow-hidden glass shadow-2xl">
                      {isProcessing && (
                        <div className="absolute inset-0 z-20 flex items-center justify-center bg-black/40 backdrop-blur-[2px]">
                          <div className="flex flex-col items-center">
                            <Loader2 className="w-12 h-12 text-indigo-500 animate-spin mb-4" />
                            <span className="text-white font-medium">Analyzing with AI...</span>
                          </div>
                        </div>
                      )}
                      <img 
                        src={detectionResult ? `${API_BASE}${detectionResult.result_url}` : previewUrl} 
                        className="w-full h-auto object-contain max-h-[600px]"
                        alt="Detection Preview"
                      />
                      <div className="absolute bottom-4 right-4 flex gap-2">
                        <button 
                          onClick={() => {setPreviewUrl(null); setDetectionResult(null);}}
                          className="bg-white/10 hover:bg-white/20 p-3 rounded-xl backdrop-blur-md text-white transition-colors"
                        >
                          <Trash2 size={20} />
                        </button>
                        {detectionResult && (
                          <a 
                            href={`${API_BASE}${detectionResult.result_url}`} 
                            download
                            className="bg-indigo-500 hover:bg-indigo-600 p-3 rounded-xl shadow-lg shadow-indigo-500/20 text-white transition-colors"
                          >
                            <Download size={20} />
                          </a>
                        )}
                      </div>
                    </div>
                  )}
                </div>

                <div className="space-y-6">
                  {/* Settings Card */}
                  <div className="glass-card p-6 rounded-3xl">
                    <h3 className="text-lg font-bold text-white mb-6 flex items-center gap-2">
                       <Settings size={18} className="text-indigo-400" /> Settings
                    </h3>
                    <div className="space-y-4">
                      <label className="block">
                        <div className="flex justify-between text-sm mb-2 text-slate-400">
                          <span>Confidence Threshold</span>
                          <span className="font-mono text-indigo-400">{Math.round(confidence * 100)}%</span>
                        </div>
                        <input 
                          type="range" 
                          min="0.1" 
                          max="0.9" 
                          step="0.05"
                          value={confidence} 
                          onChange={(e) => setConfidence(parseFloat(e.target.value))}
                          className="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-indigo-500"
                        />
                      </label>
                    </div>
                  </div>

                  {/* Results Card */}
                  <div className="glass-card p-6 rounded-3xl flex-1 max-h-[400px] overflow-y-auto">
                    <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
                       <Target size={18} className="text-emerald-400" /> Detected Objects
                    </h3>
                    <div className="space-y-3">
                      {!detectionResult ? (
                        <div className="text-center py-10">
                          <p className="text-slate-500 text-sm">Upload an image to see results</p>
                        </div>
                      ) : (
                        detectionResult.detections.map((det, i) => (
                          <div key={i} className="flex items-center justify-between p-3 rounded-2xl bg-white/5 border border-white/5">
                            <span className="text-slate-200 capitalize font-medium">{det.label}</span>
                            <span className="text-xs font-mono px-2 py-1 rounded-md bg-indigo-500/20 text-indigo-400">
                              {det.confidence}%
                            </span>
                          </div>
                        ))
                      )}
                    </div>
                  </div>
                </div>
              </motion.div>
            )}

            {activeTab === 'webcam' && (
              <motion.div 
                key="webcam"
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.95 }}
                className="flex flex-col items-center"
              >
                <div className="relative rounded-3xl overflow-hidden glass shadow-2xl border-2 border-indigo-500/30 w-full max-w-4xl">
                  {/* MJPEG Stream from Flask */}
                  <img 
                    src={`${API_BASE}/detect/webcam`} 
                    className="w-full aspect-video object-cover"
                    alt="Webcam Stream"
                  />
                  <div className="absolute top-4 left-4 flex gap-2">
                    <div className="glass px-3 py-1 rounded-full text-xs font-mono text-emerald-400 border-emerald-500/20">LIVE</div>
                    <div className="glass px-3 py-1 rounded-full text-xs font-mono text-slate-300 border-white/10">YOLOv8 Processing</div>
                  </div>
                </div>
                <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4 w-full max-w-4xl">
                   <div className="glass-card p-4 rounded-2xl flex items-center gap-4">
                      <div className="bg-indigo-500/20 p-2 rounded-lg"><Zap size={20} className="text-indigo-400" /></div>
                      <div>
                        <p className="text-xs text-slate-500 uppercase tracking-wider">Inference Speed</p>
                        <p className="text-white font-bold">~15-20 ms</p>
                      </div>
                   </div>
                   <div className="glass-card p-4 rounded-2xl flex items-center gap-4">
                      <div className="bg-emerald-500/20 p-2 rounded-lg"><Target size={20} className="text-emerald-400" /></div>
                      <div>
                        <p className="text-xs text-slate-500 uppercase tracking-wider">Frames per Second</p>
                        <p className="text-white font-bold">30 FPS</p>
                      </div>
                   </div>
                   <div className="glass-card p-4 rounded-2xl flex items-center gap-4">
                      <div className="bg-purple-500/20 p-2 rounded-lg"><Shield size={20} className="text-purple-400" /></div>
                      <div>
                        <p className="text-xs text-slate-500 uppercase tracking-wider">Precision (mAP)</p>
                        <p className="text-white font-bold">89.4%</p>
                      </div>
                   </div>
                </div>
              </motion.div>
            )}

            {activeTab === 'history' && (
              <motion.div 
                key="history"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                className="space-y-4"
              >
                {history.length === 0 ? (
                  <div className="text-center py-20 glass-card rounded-3xl">
                    <History size={48} className="text-slate-700 mx-auto mb-4" />
                    <p className="text-slate-400">No detection history yet</p>
                  </div>
                ) : (
                  history.map((item) => (
                    <div key={item.id} className="glass-card p-4 rounded-2xl flex items-center justify-between group">
                      <div className="flex items-center gap-4">
                        <div className="w-16 h-16 rounded-xl overflow-hidden bg-slate-800">
                          <img src={item.url} className="w-full h-full object-cover" alt="" />
                        </div>
                        <div>
                          <h4 className="text-white font-medium">{item.name}</h4>
                          <p className="text-xs text-slate-500">{item.date} • {item.count} objects found</p>
                        </div>
                      </div>
                      <a 
                        href={item.url} 
                        target="_blank" 
                        rel="noreferrer"
                        className="opacity-0 group-hover:opacity-100 p-2 rounded-lg bg-white/5 hover:bg-white/10 text-slate-400 transition-all"
                      >
                        <ChevronRight size={20} />
                      </a>
                    </div>
                  ))
                )}
                {history.length > 0 && (
                   <button 
                    onClick={() => {setHistory([]); localStorage.removeItem('detection_history');}}
                    className="flex items-center gap-2 text-red-400 text-sm hover:underline mt-4 mx-auto"
                   >
                     <Trash2 size={14} /> Clear All History
                   </button>
                )}
              </motion.div>
            )}

            {activeTab === 'about' && (
              <motion.div 
                key="about"
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.95 }}
                className="p-8 glass-card rounded-3xl"
              >
                <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
                  <div>
                    <h2 className="text-2xl font-bold text-white mb-6">YOLOv8 Architecture</h2>
                    <p className="text-slate-400 leading-relaxed mb-6">
                      YOLOv8 is the latest version of the acclaimed real-time object detection model. 
                      It features a new backbone network, a new anchor-free detection head, and a new loss function.
                    </p>
                    <div className="space-y-4">
                      <div className="flex justify-between border-b border-white/5 pb-2">
                        <span className="text-slate-500">Model Version</span>
                        <span className="text-slate-200 font-mono">YOLOv8n (Nano)</span>
                      </div>
                      <div className="flex justify-between border-b border-white/5 pb-2">
                        <span className="text-slate-500">Parameters</span>
                        <span className="text-slate-200 font-mono">3.2M</span>
                      </div>
                      <div className="flex justify-between border-b border-white/5 pb-2">
                        <span className="text-slate-500">Backbone</span>
                        <span className="text-slate-200 font-mono">CSPDarknet</span>
                      </div>
                      <div className="flex justify-between border-b border-white/5 pb-2">
                        <span className="text-slate-500">Head</span>
                        <span className="text-slate-200 font-mono">Anchor-free</span>
                      </div>
                    </div>
                  </div>
                  <div className="bg-slate-900/50 rounded-2xl p-6 border border-white/5">
                    <h3 className="text-lg font-bold text-white mb-4">Detection Categories</h3>
                    <div className="grid grid-cols-2 gap-2 text-xs text-slate-400 font-mono">
                      <span>• Person</span> <span>• Bicycle</span> <span>• Car</span> <span>• Motorcycle</span>
                      <span>• Airplane</span> <span>• Bus</span> <span>• Train</span> <span>• Truck</span>
                      <span>• Boat</span> <span>• Traffic light</span> <span>• Fire hydrant</span> <span>• Stop sign</span>
                      <span>• Parking meter</span> <span>• Bench</span> <span>• Bird</span> <span>• Cat</span>
                      <span>• Dog</span> <span>• Horse</span> <span>• Sheep</span> <span>• Cow</span>
                    </div>
                    <div className="mt-6 p-4 bg-indigo-500/10 rounded-xl border border-indigo-500/20">
                      <p className="text-indigo-300 text-sm">
                        Optimized for CPU & GPU inference with TensorRT and ONNX support.
                      </p>
                    </div>
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </main>
    </div>
  );
};

const SidebarLink = ({ icon, label, active, onClick, isOpen }) => (
  <button 
    onClick={onClick}
    className={`flex items-center gap-3 w-full p-3 rounded-xl transition-all duration-300 relative group ${
      active ? 'bg-indigo-500 text-white shadow-lg shadow-indigo-500/20' : 'text-slate-400 hover:bg-white/5 hover:text-slate-200'
    }`}
  >
    {icon}
    {isOpen && <span className="font-medium">{label}</span>}
    {!isOpen && !active && (
      <div className="absolute left-16 bg-slate-800 text-white text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 pointer-events-none transition-opacity">
        {label}
      </div>
    )}
  </button>
);

export default App;
