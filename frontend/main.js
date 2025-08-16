function markAttendance() {
    let roll = document.getElementById("roll").value;
    document.getElementById("result").innerText = "Submitting roll " + roll + "...";
  }
  
  // Placeholder: will later fetch /current API
  function fetchCurrent() {
    document.getElementById("code").innerText = "DUMMY1234"; 
    document.getElementById("countdown").innerText = "60s";
  }
  