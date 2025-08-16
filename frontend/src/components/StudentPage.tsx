import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { CheckCircle, XCircle, User, Hash } from "lucide-react";
import { Link } from "react-router-dom";

const StudentPage = () => {
  const [rollNumber, setRollNumber] = useState("");
  const [status, setStatus] = useState<"idle" | "success" | "error">("idle");
  const [isLoading, setIsLoading] = useState(false);

  // Mock current code for display
  const currentCode = "QNT2024XY";

  const handleMarkAttendance = async () => {
    if (!rollNumber.trim()) return;
    
    setIsLoading(true);
    
    // Simulate API call
    setTimeout(() => {
      setStatus(Math.random() > 0.3 ? "success" : "error");
      setIsLoading(false);
    }, 1500);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      handleMarkAttendance();
    }
  };

  return (
    <div className="min-h-screen relative overflow-hidden">
      {/* Quantum particles background */}
      <div className="quantum-particles">
        {[...Array(50)].map((_, i) => (
          <div
            key={i}
            className="quantum-particle"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 3}s`,
              animationDuration: `${3 + Math.random() * 2}s`,
            }}
          />
        ))}
      </div>

      <div className="relative z-10 container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-6xl font-bold bg-gradient-to-r from-quantum-purple to-quantum-cyan bg-clip-text text-transparent mb-4">
            Quantum Attendance
          </h1>
          <p className="text-xl text-muted-foreground">Student Portal</p>
          <Link
            to="/projector"
            className="inline-block mt-4 text-accent hover:text-accent/80 transition-colors"
          >
            Switch to Projector View →
          </Link>
        </div>

        <div className="max-w-2xl mx-auto space-y-8">
          {/* Main Attendance Card */}
          <Card className="backdrop-blur-sm bg-card/80 border-border/50 shadow-quantum">
            <CardHeader className="text-center">
              <CardTitle className="flex items-center justify-center gap-2 text-2xl">
                <User className="h-6 w-6 text-primary" />
                Mark Your Attendance
              </CardTitle>
              <CardDescription>
                Enter your roll number to mark attendance for today's session
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-2">
                <Input
                  type="text"
                  placeholder="Enter your roll number"
                  value={rollNumber}
                  onChange={(e) => setRollNumber(e.target.value)}
                  onKeyPress={handleKeyPress}
                  className="text-lg h-12 bg-background/50 border-border/50 focus:border-primary"
                  disabled={isLoading}
                />
              </div>

              <Button
                onClick={handleMarkAttendance}
                disabled={!rollNumber.trim() || isLoading}
                className="w-full h-12 text-lg font-semibold bg-gradient-to-r from-quantum-purple to-quantum-cyan hover:from-quantum-purple/80 hover:to-quantum-cyan/80 transition-all duration-300 animate-glow"
              >
                {isLoading ? "Marking Attendance..." : "Mark Attendance"}
              </Button>

              {/* Status Display */}
              {status !== "idle" && (
                <div className={`flex items-center justify-center gap-2 p-4 rounded-lg ${
                  status === "success" 
                    ? "bg-success/20 text-success border border-success/30" 
                    : "bg-destructive/20 text-destructive border border-destructive/30"
                }`}>
                  {status === "success" ? (
                    <>
                      <CheckCircle className="h-6 w-6" />
                      <span className="font-semibold">Attendance marked successfully!</span>
                    </>
                  ) : (
                    <>
                      <XCircle className="h-6 w-6" />
                      <span className="font-semibold">Failed to mark attendance. Please try again.</span>
                    </>
                  )}
                </div>
              )}
            </CardContent>
          </Card>

          {/* Current Code Display */}
          <Card className="backdrop-blur-sm bg-card/60 border-border/30">
            <CardHeader className="text-center pb-4">
              <CardTitle className="flex items-center justify-center gap-2 text-lg">
                <Hash className="h-5 w-5 text-accent" />
                Current Session Code
              </CardTitle>
            </CardHeader>
            <CardContent className="text-center">
              <div className="font-mono text-3xl font-bold text-accent tracking-wider">
                {currentCode}
              </div>
              <p className="text-sm text-muted-foreground mt-2">
                This code is displayed on the projector
              </p>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default StudentPage;