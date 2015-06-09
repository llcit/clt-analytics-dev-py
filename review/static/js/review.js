jQuery(function($) {
	var SITE_ROOT = $("#siteroot").val();
	$(".guide-btn").click(function (e) {
		var $disp = $(this).closest("div").next().find("div.guide-display");
		$disp.slideToggle(300,"linear");
		
	});
	
	$(".comment-btn").click(function (e) {
		var $disp = $(e.target).parent('div').next().find(".comment-display");
		$disp.slideToggle(300,"linear");  
	});



	$(".showDialog").click(function (e) {
		$('#dialog').modal('toggle');  
	});

    $('.choices').click(function(){
    	$(this).siblings('div').removeClass('selected');
    	$(this).addClass('selected');
    	//defining the results
    	$choice = $(this).find("input:hidden");
		var review = $("#review-id").serializeArray()[0];
		var questionid = $(this).siblings("input").serializeArray()[0];			
		var postdata = new Array();
        //cancel the original selection
    	if($(this).hasClass('chosen')){
			postdata.push(review);
			postdata.push(questionid);
			$(this).removeClass('chosen');
			$(this).removeClass('selected');		
			$.post(SITE_ROOT+"/review/respclear/", postdata, function(data) { 
				if(data.iscomp) 
					$("#qstatus").css("display", "block")
				else 
					$("#qstatus").css("display", "none")
				$("#questioncounter").html(data.counter);
			});
    	}else{// it is a new selection
			postdata = $choice.serializeArray();
			postdata.push(review);
			postdata.push(questionid);
			$(this).siblings('div').removeClass('chosen');
			$(this).addClass('chosen');
			$.post($("#siteroot").val()+"/review/resp/", postdata, function(data) {
				if(data.iscomp) 
					$("#qstatus").css("display", "block")
				else 
					$("#qstatus").css("display", "none")
				$("#questioncounter").html(data.counter);
			});
    	}
    })


	$(".small-button").click(function (e) {
		var $disp = $(e.target).parent().parent().parent().parent();
		$disp.slideToggle( 500, function() {
			if($disp.css("display") == "none") {
				$comm = $disp.find(".edit-surface");
				var postdata = $comm.serializeArray();
				var review = $("#review-id").serializeArray()[0];
				var section = $comm.closest(".review-section").find("input").serializeArray()[0];
				postdata.push(review);
				postdata.push(section);
				$.post(	SITE_ROOT+"/review/comm/", postdata, function(data) { 
					// $("#ajaxmsg").html(data);
					$disp.parent().parent().prev().find("span").css("visibility","hidden");
    	            //console.log("some thing has been saved");
				});
			}
		});		
	});

	$(document).ready(function(n) {
		

        $(".review-section").find("textarea").each(function(){
        	$(this).change(function(){
    	    $(this).parent().parent().parent().parent().parent().parent().prev().find("span").css("visibility","visible");
    	    //console.log("some thing has been changed");
    	    if ($(this).prop('value') == $(this).prop('defaultValue')){
    	    $(this).parent().parent().parent().parent().parent().parent().prev().find("span").css("visibility","hidden");
    	    //console.log("some thing has been unchanged");
    	    }
        	});
        	});

	});
	
	

})