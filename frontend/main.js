function markAttendance() {
    const roll = document.getElementById("rollInput").value;
    const status = document.getElementById("status");
  
    if (roll.trim() === "") {
      status.textContent = "❌ Please enter a roll number";
      status.style.color = "red";
    } else {
      status.textContent = "✅ Attendance Recorded (dummy)";
      status.style.color = "green";
    }
  }
  
  function startCountdown() {
    let timeLeft = 60;
    const timerEl = document.getElementById("timer");
  
    const interval = setInterval(() => {
      timeLeft--;
      timerEl.textContent = timeLeft;
  
      if (timeLeft <= 0) {
        timeLeft = 60; // reset for demo
        document.getElementById("projectorCode").textContent = "NEWCODE9"; // dummy refresh
      }
    }, 1000);
  }
  