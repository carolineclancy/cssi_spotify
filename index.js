$(document).ready(function(){
  $(".vote_arrow").click(function(event){
    console.log('click');
      // var input_key = null;
      // var i=0;
      // $('.key_list').each(function(){
      //     i++;
      //     var newID='key'+i;
      //     $(this).attr('id',newID);
      //     input_key = $(this).val();
      // });
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
    });

  $(".down_vote_arrow").click(function(){
    console.log('click');
    // $("#song_key").submit(function (event){
    //   event.preventDefault();
    // });
    input_key=$("#key1").val();
    $.post("http://localhost:8080/", {"vote":-1, "song_url_key":input_key} ,
      function(returnedData){
          console.log('complete');
          console.log(returnedData);
      }).fail(function(e) {
        console.log(e);
    });
  });
});
