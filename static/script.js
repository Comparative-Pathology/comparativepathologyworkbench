
$(document).ready(function(){
		$("textarea").attr({"rows": "10",
							"cols": "50"
		});
});

$(document).ready(function(){
	
	$("#matrix_info").on("hide.bs.collapse", function(){
		$(".toggle-info").html('<i class="fa fa-info"></i>');
	});
	
	$("#matrix_info").on("show.bs.collapse", function(){
		$(".toggle-info").html('<i class="fa fa-window-minimize"></i>');
	});

});

$( document ).ready( function () {
	$(".toggle-sidebar").click(function () {
		$("#sidebar").toggleClass("visible invisible");
		$("#indicator-2").toggleClass("fa-window-minimize fa-file-image");
		
		return false;
	});
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

function confirmation(question) {

	var defer = $.Deferred();
	
	$('<div></div>')
    	.html(question)
	    .dialog({
    	    autoOpen: true,
        	modal: true,
	        title: 'Confirmation',
    	    buttons: {
        	    "SWAP": function () {
            	    defer.resolve("swap");
                	$(this).dialog("close");
            	},
	            "OVERWRITE": function () {
    	            defer.resolve("overwrite");
        	        $(this).dialog("close");
	            },
	            "OVERWRITE and LEAVE": function () {
    	            defer.resolve("overwrite_leave");
        	        $(this).dialog("close");
	            }
    	    },
        	close: function () {
	            //$(this).remove();
    	        $(this).dialog('destroy').remove();
    	        window.location.reload();
        	}
	    });
	
	return defer.promise();
	
	};

function onclick(source, target){
	
	var question = "Do you want to SWAP Cells or OVERWRITE the Target Cell?";

	confirmation(question).then(function (answer) {
    
    	//console.log(answer);
	
    	if (answer == "swap"){
        	
        	//alert("Swapping Cell " + target + " with Cell " + source);
        	
			//console.log(source);
	    	//console.log(target);
	
		    $.ajax({
        		url: '{% url 'matrices:swap_cells' %}',
		        data: {
        		  'source': source,
		          'target': target,
        		  csrfmiddlewaretoken: '{{ csrf_token }}'
		        },
		        dataType: 'json',
		        type: 'post',
        		success: function (data) {
        			if (data.failure) {
        				alert("Cell Swap Failed! Source: " + data.source + "  Target: " + data.target);
        			}
					window.location.reload();
        		}
        	});
		}

    	if (answer == "overwrite"){
        
        	//alert("Overwriting Cell " + target + " with Cell " + source);

			//console.log(source);
	    	//console.log(target);
	
		    $.ajax({
        		url: '{% url 'matrices:overwrite_cell' %}',
		        data: {
        		  'source': source,
		          'target': target,
        		  csrfmiddlewaretoken: '{{ csrf_token }}'
		        },
		        dataType: 'json',
		        type: 'post',
        		success: function (data) {
        			if (data.failure) {
        				alert("Cell Overwrite Failed! Source: " + data.source + "  Target: " + data.target);
        			}
        			window.location.reload();
        		}
        	});
    	}
    	
    	if (answer == "overwrite_leave"){
        
        	//alert("Overwriting Cell " + target + " and Leave Cell " + source);

			//console.log(source);
	    	//console.log(target);
	
		    $.ajax({
        		url: '{% url 'matrices:overwrite_cell_leave' %}',
		        data: {
        		  'source': source,
		          'target': target,
        		  csrfmiddlewaretoken: '{{ csrf_token }}'
		        },
		        dataType: 'json',
		        type: 'post',
        		success: function (data) {
        			if (data.failure) {
        				alert("Cell Overwrite and Leave Failed! Source: " + data.source + "  Target: " + data.target);
        			}
        			window.location.reload();
        		}
        	});
    	}
    	
		//window.location.reload();

	});
}


function allowDrop(ev){
	ev.preventDefault();
}

function drag(ev){
	ev.dataTransfer.setData("Text",ev.target.id);
}

function drop(ev){


	ev.preventDefault();

    var src = document.getElementById(ev.dataTransfer.getData("Text"));
	var srcParent = src.parentNode;

	var source_array = src.id.split("_",2);
	var source = source_array[1];
    
    var tgt = ev.currentTarget.firstElementChild;
	var target_array = tgt.id.split("_",2);
	var target = target_array[1];

	ev.currentTarget.replaceChild(src, tgt);
    srcParent.appendChild(tgt);

	onclick(source, target);
    

}


function allowColDrop(ev){
	ev.preventDefault();
}

function dragCol(ev){
	ev.dataTransfer.setData("Text",ev.target.id);
}

function dropCol(ev){

	ev.preventDefault();
    var src = document.getElementById(ev.dataTransfer.getData("Text"));
    var srcParent = src.parentNode;

	var source_array = src.id.split("_",2);
	var source = source_array[1];
    
    var tgt = ev.currentTarget.firstElementChild;
	var target_array = tgt.id.split("_",2);
	var target = target_array[1];

    ev.currentTarget.replaceChild(src, tgt);
    srcParent.appendChild(tgt);

    $.ajax({
        url: '{% url 'matrices:swap_columns' %}',
        data: {
          'source': source,
          'target': target,
          csrfmiddlewaretoken: '{{ csrf_token }}'
        },
        dataType: 'json',
        type: 'post',
        success: function (data) {
          if (data.failure) {
            alert("Column Swap Failed! Source: " + data.source + "  Target: " + data.target);
          }
		  window.location.reload();
        }
      });

}

function allowRowDrop(ev){
	ev.preventDefault();
}

function dragRow(ev){
	ev.dataTransfer.setData("Text",ev.target.id);
}

function dropRow(ev){

	ev.preventDefault();
    var src = document.getElementById(ev.dataTransfer.getData("Text"));
    var srcParent = src.parentNode;

	var source_array = src.id.split("_",2);
	var source = source_array[1];

    var tgt = ev.currentTarget.firstElementChild;
	var target_array = tgt.id.split("_",2);
	var target = target_array[1];

    ev.currentTarget.replaceChild(src, tgt);
    srcParent.appendChild(tgt);

    $.ajax({
        url: '{% url 'matrices:swap_rows' %}',
        data: {
          'source': source,
          'target': target,
          csrfmiddlewaretoken: '{{ csrf_token }}'
        },
        dataType: 'json',
        type: 'post',
        success: function (data) {
          if (data.failure) {
            alert("Row Swap Failed! Source: " + data.source + "  Target: " + data.target);
          }
		  window.location.reload();
        }
      });

}

