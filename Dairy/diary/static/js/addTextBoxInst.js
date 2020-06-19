$(document).ready(function() {


      $(".add-more-Inst").click(function(){ 
          var html = $(".copy").html();
          $(".after-add-more-Inst").before(html);
      });


      $("body").on("click",".remove",function(){ 
          $(this).parents(".control-group").remove();
      });


    });