jQuery(document).ready(function ($) {

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