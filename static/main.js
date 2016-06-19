$(window).load(function() {
	//$("#loading").delay(2000).fadeOut(500);
	$("#loading-center").click(function() {
	  	event.preventDefault();
	})
	$("#1").fadeIn("slow");

	setTimeout(function(){ 
		$("#1").fadeOut("slow");
		$("#2").fadeIn("slow");
	}, 7000);
	setTimeout(function(){ 
		$("#2").fadeOut("slow");
		$("#3").fadeIn("slow");
	}, 13000);
	setTimeout(function(){ 
		$("#3").fadeOut("slow");
		$("#4").fadeIn("slow");
	}, 20000);

	setTimeout(function(){ 
	    window.location = "http://localhost:8023/results";

	}, 25000);
})


$("#login-button").click(function(event){  
    //var that = this;
    // event.preventDefault();
    /*if (pressed = false) {
	event.preventDefault();
	pressed = true;
    }*/
    $('form').fadeOut(400);
    $('.wrapper').addClass('form-success');
    window.location = "http://localhost:8023/results";
    /*setTimeout(function() {
	document.getElementById("#login-button").click();
	console.log("success");
    }, 4000);
    pressed = false;*/
});

