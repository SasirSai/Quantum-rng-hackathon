import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { Monitor, Users } from "lucide-react";

const ProjectorPage = () => {
  const [currentCode] = useState("QNT2024XY");
  const [timeLeft, setTimeLeft] = useState(45); // 45 seconds countdown

  useEffect(() => {
    const timer = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev <= 1) {
          // Reset to 45 when it reaches 0
          return 45;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="min-h-screen relative overflow-hidden bg-quantum-dark">
      {/* Enhanced quantum particles for projector */}
      <div className="quantum-particles">
        {[...Array(30)].map((_, i) => (
          <div
            key={i}
            className="quantum-particle"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 3}s`,
              animationDuration: `${2 + Math.random() * 1}s`,
              width: `${3 + Math.random() * 2}px`,
              height: `${3 + Math.random() * 2}px`,
            }}
          />
        ))}
      </div>

      <div className="relative z-10 h-screen flex flex-col">
        {/* Header */}
        <header className="p-8 text-center border-b border-border/30">
          <div className="flex items-center justify-center gap-3 mb-2">
            <Monitor className="h-8 w-8 text-accent" />
            <h1 className="text-3xl md:text-4xl font-bold text-foreground">
              Quantum Attendance
            </h1>
          </div>
          <p className="text-xl text-accent font-semibold">CS101 - Computer Science Fundamentals</p>
          <Link
            to="/"
            className="inline-block mt-2 text-muted-foreground hover:text-foreground transition-colors text-sm"
          >
            ← Back to Student Portal
          </Link>
        </header>

        {/* Main Display Area */}
        <main className="flex-1 flex flex-col items-center justify-center p-8">
          {/* Code Display */}
          <div className="text-center mb-16">
            <h2 className="text-2xl md:text-3xl font-semibold text-muted-foreground mb-8">
              Attendance Code
            </h2>
            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-r from-quantum-purple/20 to-quantum-cyan/20 rounded-2xl blur-xl"></div>
              <div className="relative bg-card/20 backdrop-blur-sm border border-border/30 rounded-2xl p-12 shadow-glow">
                <div className="font-mono text-8xl md:text-9xl lg:text-[12rem] font-black text-transparent bg-gradient-to-r from-quantum-purple to-quantum-cyan bg-clip-text tracking-wider">
                  {currentCode}
                </div>
              </div>
            </div>
          </div>

          {/* Timer Display */}
          <div className="text-center">
            <h3 className="text-xl md:text-2xl font-semibold text-muted-foreground mb-4">
              Code Refresh Timer
            </h3>
            <div className="relative">
              <div className="absolute inset-0 bg-accent/10 rounded-xl blur-lg"></div>
              <div className="relative bg-card/30 backdrop-blur-sm border border-accent/30 rounded-xl px-8 py-4">
                <div className={`font-mono text-4xl md:text-5xl font-bold transition-colors duration-300 ${
                  timeLeft <= 10 ? 'text-destructive animate-pulse' : 'text-accent'
                }`}>
                  {formatTime(timeLeft)}
                </div>
              </div>
            </div>
          </div>

          {/* Session Info */}
          <div className="absolute bottom-8 right-8 bg-card/20 backdrop-blur-sm border border-border/30 rounded-lg p-4">
            <div className="flex items-center gap-2 text-muted-foreground">
              <Users className="h-5 w-5" />
              <span className="text-sm">Session Active</span>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
};

export default ProjectorPage;