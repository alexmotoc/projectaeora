$(document).ready(function(){
      $('.parallax').parallax();
      
      var options = [{
        selector: '#staggered-test',
        offset: 300,
        callback: function(el) {
          Materialize.showStaggeredList($(el));
        }
      }];

      Materialize.scrollFire(options);
});
