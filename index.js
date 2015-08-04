$(document).ready(function(){
  $(".vote_arrow").click(function(){
    console.log('click');
    // $("#song_key").submit(function (event){
    //   event.preventDefault();
    // });

    $.post("http://localhost:8080/", {"vote":1},
      function(returnedData){
          console.log('complete');
          console.log(returnedData);
      }).fail(function(e) {
        console.log(e);
    });
  });
});
