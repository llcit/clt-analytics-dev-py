jQuery(function($) {
	var SITE_ROOT = $("#siteroot").val();
	$(".guide-btn").click(function (e) {
		var $disp = $(this).parent().next().find(".guide");
		$disp.fadeToggle("slow");	
	});

	$(".small-button").click(function (e) {
		var $disp = $(e.target).parent();
		$disp.fadeToggle(450);		
	});
	
	$('.sortText').hide();
	$( ".sort-button" ).click(function() {
	  $( this ).find('.sortIcon').toggleClass( "icon-flipped");
	  $('.sortText').toggle("fast");
	});
    
    $( '.toShort' ).hide();
	$( ".reviewerShort" ).click(function() {
	  $( this ).toggleClass( "glyphicon-minus");
      $( this ).toggleClass( "glyphicon-plus");
      // $( '.toShort' ).toggleClass('celldisplay');
      $( '.toShort' ).toggle('fast');
	});

	
	$(document).ready(function(n) {

		$("[data-toggle=tooltip]").tooltip();
		$("[data-toggle=popover]").popover();

    	$('.commentToggle').click(function(){
      		var comment_panel = $(this).parents("div.section-header").find('.comments');
    		comment_panel.slideToggle( "fast", function() {});
		});
	});

})