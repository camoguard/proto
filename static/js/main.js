jQuery(document).ready(function ($) {

  $('#navbar-search').typeahead({
    source: function(typeahead, query) {
      var _this = this;
      return $.ajax({
        url: "/search/autocomplete/?q=" + query,
        success: function(data) {
          return typeahead.process(data);
        }
      });
    },
    onselect: function(obj) {
      return $.ajax({
        url: "/api/v1/" + obj['model_name'] + "/" + obj['pk'],
        success: function(data) {
          window.location.href = data['absolute_url'];
        }
      });
    },
    property: "title"
  });



  $('a.comment-reply').on('click', function (e) {
    e.preventDefault();

    var link = $(this);

    $.ajaxQueue({
      'url': link.attr('href'),
      'dataType': 'html',
      'success': function (html) {
        $('#comment-list form').remove();
        link.after(html);
      },
      'error': function  () {
        alert('Unable to retrieve comment form.');
      }
    });
  });

});
