
$(document).ready(function(){
		$("textarea").attr({"rows": "10",
							"cols": "50"
		});
});


$(document).ready(function(){
	
	$("#matrix_info").on("hide.bs.collapse", function(){
		$(".toggle-info").html('<i class="fa fa-info fa-lg"></i>');
	});
	
	$("#matrix_info").on("show.bs.collapse", function(){
		$(".toggle-info").html('<i class="fa fa-window-minimize fa-lg"></i>');
	});

});


$( document ).ready( function () {
	$(".toggle-sidebar").click(function () {

		var flag = sessionStorage.getItem("sidebartoggle");
			
		//console.log("click BEFORE sessionStorage.sidebartoggle = ", flag)
	
		if (flag == "true") {
	
			//console.log("click Flag TRUE");

			sessionStorage.setItem("sidebartoggle", "false");
	
			$("#matrix_sidebar").removeClass("visible");
			$("#matrix_sidebar").addClass("invisible");
			$("#indicator-2").removeClass("fa-window-minimize");
			$("#indicator-2").addClass("fa-cart-arrow-down");
		}
		else {
	
			//console.log("click Flag FALSE");
		
			sessionStorage.setItem("sidebartoggle", "true");
	
			$("#matrix_sidebar").removeClass("invisible");
			$("#matrix_sidebar").addClass("visible");
			$("#indicator-2").removeClass("fa-cart-arrow-down");
			$("#indicator-2").addClass("fa-window-minimize");
		}

		return false;
	});
}); 

$( document ).ready( function () {

    window.onload = function (e) {

		//console.log("window.onload");

		if(sessionStorage) {
		
			var flag = sessionStorage.getItem("sidebartoggle");
			
			//console.log("onload sessionStorage.sidebartoggle = ", flag)

			if (flag == ""){
			
			    sessionStorage.setItem("sidebartoggle", "false");

				$("#matrix_sidebar").removeClass("visible");
				$("#matrix_sidebar").addClass("invisible");
				$("#indicator-2").removeClass("fa-window-minimize");
				$("#indicator-2").addClass("fa-cart-arrow-down");
			}
			else {
			
				if (flag == "true") {
	
					//console.log("Load Flag TRUE")

					$("#matrix_sidebar").removeClass("invisible");
					$("#matrix_sidebar").addClass("visible");
					$("#indicator-2").removeClass("fa-cart-arrow-down");
					$("#indicator-2").addClass("fa-window-minimize");
				}
				else {
	
					//console.log("Load Flag FALSE")
		
					$("#matrix_sidebar").removeClass("visible");
					$("#matrix_sidebar").addClass("invisible");
					$("#indicator-2").removeClass("fa-window-minimize");
					$("#indicator-2").addClass("fa-cart-arrow-down");
				}
			}
		}
    };
}); 


$( document ).ready( function () {
    $( '.dropdown-menu a.dropdown-toggle' ).on( 'click', function ( e ) {
        var $el = $( this );
        $el.toggleClass('active-dropdown');
        var $parent = $( this ).offsetParent( ".dropdown-menu" );
        if ( !$( this ).next().hasClass( 'show' ) ) {
            $( this ).parents( '.dropdown-menu' ).first().find( '.show' ).removeClass( "show" );
        }
        var $subMenu = $( this ).next( ".dropdown-menu" );
        $subMenu.toggleClass( 'show' );
        
        $( this ).parent( "li" ).toggleClass( 'show' );

        $( this ).parents( 'li.nav-item.dropdown.show' ).on( 'hidden.bs.dropdown', function ( e ) {
            $( '.dropdown-menu .show' ).removeClass( "show" );
            $el.removeClass('active-dropdown');
        } );
        
         if ( !$parent.parent().hasClass( 'navbar-nav' ) ) {
            $el.next().css( { "top": $el[0].offsetTop, "left": $parent.outerWidth() - 4 } );
        }

        return false;
    } );
} );	
