var Cashmere;

function CashmereApp($) {
  this.Operation = {
    'delete': function(pk) {
      $.ajax({
        url: '/api/operations/' + pk + '/',
        type: 'DELETE',
        success: function () {
          $('#operation_' + pk).remove();
        }
      });
    }
  };
}

(function ($) {  
  $(document).ready(function() {
    Cashmere = new CashmereApp($);
  });
}(jQuery));
