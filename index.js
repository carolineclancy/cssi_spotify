$(document).ready(function(){

  $(".rotate_vote").click(function upVote(event){
    console.log('click');
      var event_id = event.target.id;
      var id_number = event_id.substring(event_id.indexOf("#")+1);
      var input_item = String('#'+'key-'+id_number);
      var input_key = $(input_item).val();
      console.log(id_number);
      var that = this;
      $.post("/", {"vote":1, "song_url_key":input_key} ,
        function(returnedData){
          if(returnedData === "Vote Failed"){
            alert("You need to be logged in to vote!");
            return;
          }else if(returnedData === "Double Vote Failed"){
            alert("You can't double vote!")
          }else{
            var votes = $(that).closest('tr').find('td.votes_column');
            var count = parseInt(votes.html(),10)+1;
            votes.html(count);
          }
        }).fail(function(e) {
          console.log(e);
      });


});

    $(".down_vote_arrow").click(function(event){
      console.log('click');
        var event_id = event.target.id;
        var id_number = event_id.substring(event_id.indexOf("#")+1);
        var input_item = String('#'+'key-'+id_number);
        var input_key = $(input_item).val();
        var that = this;
        console.log(id_number);
        $.post("/", {"vote":-1, "song_url_key":input_key} ,
          function(returnedData){
            if(returnedData === "Vote Failed"){
              alert("You need to be logged in to vote!");
              return;
            }else if(returnedData === "Double Vote Failed"){
              alert("You can't double vote!");
            }else{
              var votes = $(that).closest('tr').find('td.votes_column');
              console.log('voted');
              var count = parseInt(votes.html(),10)-1;
              votes.html(count);
            }
          }).fail(function(e) {
            console.log(e);
        });
      });

});
