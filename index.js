$(document).ready(function(){

  $(".rotate_vote").click(function upVote(event){
    console.log('click');
      var event_id = event.target.id;
      var id_number = event_id.substring(event_id.indexOf("#")+1);
      var input_item = String('#'+'key-'+id_number);
      var input_key = $(input_item).val();
      console.log(id_number);
      var that = this;
      $.post("http://localhost:8080/", {"vote":1, "song_url_key":input_key} ,
        function(returnedData){
          if(returnedData === "Vote Success"){
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
        $.post("http://localhost:8080/", {"vote":-1, "song_url_key":input_key} ,
          function(returnedData){
            if(returnedData === "Vote Success"){
              var votes = $(that).closest('tr').find('td.votes_column');
              var count = parseInt(votes.html(),10)-1;
              votes.html(count);
            }
              console.log(returnedData);
          }).fail(function(e) {
            console.log(e);
        });
      });

});
