// Set the date we're counting down to
var countDownDate = new Date().getTime() + 5000;

// Update the count down every 1 second
var x = setInterval(function() {

    // Get todays date and time
    var now = new Date().getTime();

    // Find the distance between now and the count down date
    var distance = countDownDate - now;

    // Time calculations for days, hours, minutes and seconds
    var days = Math.floor(distance / (1000 * 60 * 60 * 24));
    var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    var seconds = Math.floor((distance % (1000 * 60)) / 1000);

    // Display the result in the element with id="demo"
    document.getElementById("target_time_banner").innerHTML = days + "d " + hours + "h " +
        minutes + "m " + seconds + "s ";

    // If the count down is finished, write some text 
    if (distance < 0) {
        clearInterval(x);
        document.getElementById("target_time_banner").innerHTML = "Done";
//        console.log(this.dataset)
        odoo.define('examination.my_js', function(require) {
             'use strict';
             var ajax = require('web.ajax');
             console.log("Here")
             $.ajax({
             type: "POST",
             url:'/survey/submit/shimaa-1',
             data: {'page_id': 1, 'task': 'addcode', 'format': 'json'},
             dataType: 'json',
             success: function (response) {
             console.log(response);
             }
             });
});
//             ajax.jsonRpc("/survey/submit/shimaa-1", 'call').then(function(result) {
//                 console.log("inner console");
//                 console.log(result);
//             });
//         })
//        $.ajax({
//            type: "POST",
//            url: "/survey/submit/shimaa-1",
//            data: { param: {
//                "page_id":this.recordData
//            } }
//        }).done(function(o) {
//            // do something
//        });
    }
}, 1000);