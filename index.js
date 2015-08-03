$(document).ready(function(){
  ("#vote_arrow").click(function(){
    console.log('click');
    $.post("/", {"vote":1},
      function(returnedData){
          console.log('complete');
          console.log(returnedData);
      }).fail(function() {
        console.log('error');
    });
  });
});
