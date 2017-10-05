$(document).ready(function () {
    $('.article-subscribe').on('click', function (e) {
        e.preventDefault();
        let url = '/subscribe/' + $(this).attr('id');
        let article_url = $(location).attr('pathname');
        let article_subscribe_button = $('.article-subscribe');
        $.ajax({
            type: 'GET',
            url: url,
            dataType: 'json',
            success: function (response) {
                article_subscribe_button.html(response.message);
                if (response.message == 'отписаться') {
                    let new_subscription = $('<li></li>');
                    let sub_link = $('<a href="/article/' + response.article + '">' + response.article_title + ' (0)</a>');
                    new_subscription.prepend(sub_link);
                    $('.dropdown-menu').append(new_subscription);
                }
                else{
                    $('.dropdown-menu').find('a[href$="/article/' + response.article + '"]').parent().remove();
                }
            }
        })
    });
});
