let comments_list = {};

String.prototype.format = function() {
    let formatted = this;
    for (let i = 0; i < arguments.length; i++) {
        let regexp = new RegExp('\\{'+i+'\\}', 'gi');
        formatted = formatted.replace(regexp, arguments[i]);
    }
    return formatted;
};


function checkRedirect(){
    try {
        if (localStorage.getItem('message_id') != 'undefined' && localStorage.getItem('message_id') != null) {
            let message_id = localStorage.getItem('message_id');
            let redirect_comment = $('#comments-list').find('#' + message_id);
            scrollToComment(redirect_comment);
            window.localStorage.clear();
        }
    }
    catch (e){

    }
}


function normalizeTextArea(ta){
    ta.find('textarea').css('height', '124px');
    ta[0].reset();
}


function scrollToComment(comment){
    return $('body, html').animate({ scrollTop: $(comment).offset().top}, 500);
}


function errorCatcher(response){
    let id = 0;
    let error_messages = $('#error-messages');

    if (error_messages.children().length === 0){
        id = 1;
    }
    else{
        id = error_messages.children().last().attr('id') + 1;
    }

    let error_message = $('<div class="panel panel-default error-message" id="' + id + '"></div>');
    for (let e in response){
        error_message.append(response[e]);
    }
    error_messages.append(error_message);
    setTimeout(function () {$('#' + id).fadeOut(1500, function () {
        $('#' + id).remove();});
    }, 5000);
}


function popover_builder(username, avatar, blacklist){
    let text = '';
    if (blacklist){
        text = 'удалить из черного списка';
    }

    else{
        text = 'добавить в черный список';
    }


    let image = '<img src="' + avatar + '" class="media-object img-circle-comment">';
    let left_wing = '<a href="#"', right_wing =  '>' + image + '</a>';
    let data_toggle = ' data-toggle="popover"';
    let data_placement = ' data-placement="top"';
    let data_trigger  = ' data-trigger="focus"';
    let data_content = "<div><a class='send-message-popover'>написать сообщение</a></div>" +
                       "<div><a href='/" + username + "/user_info/'>информация о пользователе</a></div>" +
                       "<div><a class='blacklist-user-popover' href='/block_user/" + username + "/'>" + text + "</a></div>";
    let data_content_ready = ' data-content="{0}"'.format(data_content);
    return left_wing + data_toggle + data_placement + data_trigger + data_content_ready + right_wing;

}


function blacklistUser(comment){
    let ignore_button = $('<div class="ignore-block">показать</div>');
    let ignore_border = $('<div class="ignore-border"></div>');
    ignore_button.insertAfter(comment.find('.comment-message-info:first'));
    comment.find('.comment-message-footer').hide();
    comment.find('.comment-message-text').hide();
    comment.append(ignore_border);
    $('.popover').attr('data-content', '123');
    comment.find('.blacklist-user-popover').html('удалить из черного списка');
    return comment
}


function removeFromBlacklist(comment){
    comment.find('.ignore-block').remove().find('.ignore-block-hide').remove();
    comment.find('.ignore-border').remove();
    comment.find('.comment-message-footer').show();
    comment.find('.comment-message-text').show();
    comment.find('.blacklist-user-popover').html('добавить в черный список');
    return comment;
}


function comment_builder(response, key){
    if (response.editable == true){
        comments_list[key] = response.comment_text;
        return $('#'+ key + '.comment-message').find('.comment-message-text').html(response.comment_text);
    }
    let message = $('<div class="comment-message" id=' + key +'></div>');
    let message_avatar = $('<div class="message-avatar" id=' + response.rating_model_pk + '>' +
        popover_builder(response.username, response.avatar, response.blacklisted) + '</div>');
    let message_info = $('<div class="comment-message-info"><span class="comment-number">' + response.comment_name + '</span>'
        + ' ' + '<span class="comment-author-username" data-id="' + response.username + '">' + response.username + '</span>'
        + ' ' + '<span class="comment-created">' + response.datetime + '</span></div>');
    let message_text = $('<div class="comment-message-text">' + response.comment_text + '</div>');
    let message_footer = $('<div class="comment-message-footer"><span class="comment-answer">ответить</span>&#160&#160' +
        '<span class="like-painter ' + response.check_color + '">' + '<span class="like-buttons-comment">' +
        '<span class="glyphicon glyphicon-thumbs-up like" data-grade="like"><a href="/comment/rate/' + key + '/like/"></a></span> ' +
        '<span class="total-likes">' + response.likes + '</span>' + ' ' +
        '<span class="glyphicon glyphicon-thumbs-down like" data-grade="dislike"><a href="/comment/rate/' + key + '/dislike/"></a></span> ' +
        '<span class="total-dislikes">' + response.dislikes + '</span></span></p></div>');
    if (response.target_name){
        message_text.prepend($("<span class='target-name'>" + response.target_name + ", " + "</span>"));
    }
    if (response.login_user == response.username || response.current_session == response.session){
        message_footer.prepend($('<span class="comment-edit" id="' + key + '">редактировать</span>'))
    }
    let new_comment = message.append(message_avatar).append(message_info).append(message_text).append(message_footer);
    new_comment.find('[data-toggle="popover"]').popover({html:true});

    if (response.blacklisted){
        new_comment = blacklistUser(new_comment);
    }

    comments_list[key] = {'comment_text': response.comment_text,
                          'likes': response.likes,
                          'dislikes': response.dislikes,
                          'check_color': response.check_color};

    if (response.parent){
        let child = $('<div class="child"></div>');
        child.append(new_comment);

        $(response.parent).append(child);
    }
    else{
        $('#comments-list').append(new_comment);
    }

    return new_comment;
}


function updateComment(response, key){
    let comment = $('#' + key);
    comment.find('.comment-message-text:first').text(response.comment_text);
    comment.find('.total-likes:first').text(response.likes);
    comment.find('.total-dislikes:first').text(response.dislikes);
    comment.find('.like-painter:first').attr('class', 'like-painter ' + response.check_color);
    comments_list[key] = {'comment_text': response.comment_text,
                          'likes': response.likes,
                          'dislikes': response.dislikes,
                          'check_color': response.check_color};
    return comment
}


function commentsCountRefresher(){
    $('.comments-count').html($('#comments-list').find('.comment-message').length)
}


function loadComments() {
    $.ajax({
        type: 'POST',
        url: '/load_comments/' + $(location).attr('pathname').split('/')[2] + '/',
        data: {'data': JSON.stringify(comments_list)},
        dataType: 'json',
        headers: {"X-CSRFToken": $.cookie("csrftoken")},
        success: function (response) {
            for (key in response) {
                if ('update' in response[key]) {
                    updateComment(response[key], key);

                }
                else {
                    comment_builder(response[key], key);
                }
            }
            commentsCountRefresher();

        }
    }).success(function () {
        setTimeout(function () {
            loadComments()
        }, 5000)
    });
}

function formSubmit(form, pk){
    let url = '';
    if (pk != undefined){
        url = '/edit_comment/' + pk + '/';
    }
    else{
        url = $(location).attr('pathname');
    }
    $.ajax({type: 'POST',
                url: url,
                data: form.serialize(),
                dataType: 'json',
                success: function (response) {
                    if ('errors' in response){
                        errorCatcher(response.errors);
                    }
                    else{
                        if (pk == undefined){
                            form.trigger('reset');
                            commentsCountRefresher();
                            if (form.find('.parent').val() != ''){
                                form.hide();
                            }
                            key = Object.keys(response)[0];
                            scrollToComment(comment_builder(response[key], key));
                        }
                        else{
                            let new_text = form.find('textarea').val();
                            form.parent().parent().find('.comment-message-text:first').text(new_text);
                            form.hide();
                            comments_list[form.closest('.comment-message').attr('id')]['comment_text'] = new_text;
                        }
                        $('.comment-edit-hide').attr('class', 'comment-edit');
                        $('.comment-answer-hide').attr('class', 'comment-answer');
                        commentsCountRefresher();
                    }
                },
                error: function (xhr, errmsg, err) {
                    alert(xhr.status + ": " + xhr.responseText);
                }

        });
}

$(document).ready(function (e) {
    setTimeout(loadComments(), 10000);
    $(document).ajaxComplete(function () {
        checkRedirect();
    });


    $("[data-toggle=popover]").popover({html: true, container: 'body'});

    $(document).on('click', '#commentpagediv-id', function (e) {
        e.preventDefault();
        return expandComments(url, '#comment-pagination-id', '#comment-load-id');
    });

    $(document).on('click', '[data-toggle="popover"]', function (e) {
        e.preventDefault();
    });

    $(document).on('click', '.answer-submit', function (e) {
        e.preventDefault();
        let form = $(this).parent();
        let id = $(this).attr('id');
        return formSubmit(form, id);
    });

    $(document).on('click', '.comment-answer', function (e) {
        e.preventDefault();
        let answer_form = $('#answer-form');
        answer_form.show();
        normalizeTextArea(answer_form);
        answer_form.find('.parent').val($(this).closest('.comment-message').attr('id'));
        answer_form.appendTo($(this).parent());
        $('.comment-answer-hide').attr('class', 'comment-answer').show();
        $(this).attr('class', 'comment-answer-hide');
        $('.input-placeholder').show();
        $('.answer-submit').removeAttr('id');
        $('.comment-edit-hide').attr('class', 'comment-edit');
        answer_form.find('textarea').focus();
    });

    $(document).on('click', '.input-placeholder', function () {
        $('.answer-submit').removeAttr('id');
        let answer_form = $('#answer-form');
        answer_form.show();
        answer_form.find('.parent').val('');
        $(this).hide();
        normalizeTextArea(answer_form);
        answer_form.insertAfter('.input-placeholder');
        answer_form.find('textarea').focus();
    });

    $(document).on('click', '.comment-edit-hide', function (e) {
        e.preventDefault();
        $(this).attr('class', 'comment-edit');
        $(this).parent().find('#answer-form').hide();
    });

    $(document).on('click', '.comment-answer-hide', function (e) {
        e.preventDefault();
        $(this).attr('class', 'comment-answer');
        $(this).closest('.comment-edit-hide').attr('class', 'comment-edit');
        $(this).parent().find('#answer-form').hide();
    });

    $(document).on('click', '.parent-name', function (e) {
        e.preventDefault();
        let name = $(this).html();
        let target_comment = $('.article-comments').find('.comment-number[id="' + name + '"]');
        target_comment.parent().parent();
        $('html, body').animate({scrollTop: target_comment.offset().top}, 300);
    });

    $(document).on('click', '.comment-edit', function (e) {
        $('.comment-answer-hide').attr('class', 'comment-answer');
        $('.comment-edit-hide').attr('class', 'comment-edit');

        $(this).attr('class', 'comment-edit-hide');
        $('.input-placeholder').show();
        let text = $(this).parent().parent().find('.comment-message-text:first').text();
        let answer_form = $('#answer-form').appendTo($(this).parent());
        normalizeTextArea(answer_form);
        answer_form.val(text).show();
        answer_form.find('textarea').val(text);
        answer_form.val($(this).closest('.comment-message-text').text());
        $('.answer-submit').attr('id', $(this).attr('id'));
        answer_form.find('textarea').focus();
    });

    autosize($('textarea'));

    $(document).on('click', '.ignore-block', function (e) {
        e.preventDefault();
        $(this).next().show();
        $(this).attr('class', 'ignore-block-hide').html('скрыть');
    });

    $(document).on('click', '.ignore-block-hide', function (e) {
        e.preventDefault();
        $(this).next().hide();
        $(this).attr('class', 'ignore-block').html('показать');
    });

    $(document).on('click', '.target-name', function (e) {
        e.preventDefault();
        let name = $(this).html().split(',')[0];
        let target_comment = $('.comment-number:contains("' + name + '")').closest('.comment-message');
        return scrollToComment(target_comment);
    });

});
