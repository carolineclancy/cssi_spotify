$(document).ready(function(){
  $.post('superman', { field1: "hello", field2 : "hello2"}, 
    function(returnedData){
         console.log(returnedData);
});
});
