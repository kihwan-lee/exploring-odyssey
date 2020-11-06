//==========================//
//      Modal Nav Menu      //
//==========================//

// Toggle Nav Menu
function showNav() {
  document.getElementsByClassName("homeNav")[0].classList.toggle("active");
}

// Ajax call to signal views.py for city page
// var url = $( '#selection-form' ).attr( 'action' );
// $("selection-button").click(function(e) {
//     e.preventDefault();
//     $.ajax({
//         type: "GET",
//         url: url,
//         data: { 
//             id: $('#locations').val();, 
//             },
//         success: function(result) {
//             alert('ok');
//         },
//         error: function(result) {
//             alert('error');
//         }
//     });
// });