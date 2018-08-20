$(document).ready(function () {

  var colors = ['#fff5e0', '#f9ffbe', '#e1ffce', '#d7e8e6', '#fbe8ff']
  var i = 0;
  $(".item").each(function() {
      $(this).css("background-color", colors[i++]); // increment here
      if(i == 5) i = 0; // reset the counter here
  });

  console.log("Running Fundación Educate & Colors...")


});
