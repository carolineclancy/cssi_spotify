$(document).ready(function(){

  $(".rotate_vote").click(function upVote(event){
    console.log('click');
      var event_id = event.target.id;
      var id_number = event_id.substring(event_id.indexOf("#")+1);
      var input_item = String('#'+'key-'+id_number);
      var input_key = $(input_item).val();
      console.log(id_number);
      $.post("http://localhost:8080/", {"vote":1, "song_url_key":input_key} ,
        function(returnedData){
            console.log('complete');
            console.log(returnedData);
        }).fail(function(e) {
          console.log(e);
      });
      var votes = $(this).closest('tr').find('td.votes_column');
      var count = parseInt(votes.html(),10)+1;
      votes.html(count);
    });


    $(".down_vote_arrow").click(function(event){
      console.log('click');
        var event_id = event.target.id;
        var id_number = event_id.substring(event_id.indexOf("#")+1);
        var input_item = String('#'+'key-'+id_number);
        var input_key = $(input_item).val();
        console.log(id_number);
        $.post("http://localhost:8080/", {"vote":-1, "song_url_key":input_key} ,
          function(returnedData){
              console.log('complete');
              console.log(returnedData);
          }).fail(function(e) {
            console.log(e);
        });
        var votes = $(this).closest('tr').find('td.votes_column');
        var count = parseInt(votes.html(),10)-1;
        votes.html(count);
      });
});
