jQuery(function($) {
	var SITE_ROOT = $("#siteroot").val();
	$("#submitter").click(function () {

		// Check the text areas
		var noval = 0;
		$("form textarea").each(function() {
			if(this.value == "") noval++;
		});
		if (noval > 0) return alert("Please answer all questions. Thanks!");
				
		// Check the multiple choices
		var radios = {};
		$("form input:radio").each(function() {	radios[this.name] = true; });
		for(i in radios) {
			if (! $(":radio[name="+i+"]:checked").length) 
    			return alert("Please answer all questions. Thanks!");
		}	

		var postdata = new Array();
		 //REVIEW ID
		postdata = $("#respform").serializeArray();
		postdata.push($("#review-id").serializeArray()[0]);
		// Send it off!
		
		$.post(SITE_ROOT+"/review/respprep/", postdata,
	    	function(data) {
	    		$("#surveycontent").remove();
	    		$("#ajaxmsg").html(data);    		
	    });			

	});

})