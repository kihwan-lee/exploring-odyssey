//==========================//
//      Modal Nav Menu      //
//==========================//

// Toggle Nav Menu
function showNav() {
  document.getElementsByClassName("homeNav")[0].classList.toggle("active");
}

// Cities Search Bar Functionality
// $(document).ready(function() {
//   $("#search-button").click(function() {
//     const location_id = $('#location_id').val();
//     window.location = "/locations/" + location_id
//   })
// })

function citiesSearch() {
  document.querySelector('.city-search-form').addEventListener('submit', (e) => {
    e.preventDefault();
    window.location= document.getElementById('location_id').value;
  });
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