var ending_time = new Date().getTime() + 10000;
var x = setInterval(function) {
    var current = new Date().getTime();
    var interval = ending_time - current;

}

//var seconds = 5400; #Total duration of the exam 90min
//
//function secondPassed() {
//
//var minutes = Math.round((seconds - 30)/60);
//
//var remainingSeconds = seconds % 60;
//
//if (remainingSeconds < 10) {
//
//remainingSeconds = "0" + remainingSeconds;
//
//}
//
//document.getElementById('countdown').innerHTML = "Total Duration"+" " + minutes + ":" + remainingSeconds;
//
//if (seconds == 0) {
//
//clearInterval(countdownTimer);
//
//document.getElementById('countdown').innerHTML = "Times Up Leave the Exam hall";
//
//window.location="http://localhost:8069/page/exam/result";
//
//} else {
//
//seconds--;
//
//}
//
//}
//
//var countdownTimer = setInterval('secondPassed()', 1000);