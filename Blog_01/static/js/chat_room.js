$(document).ready(function () {
    let scroll_border = 0;
    let total_objects = 0;
    let first_load = true;
    let messages_list = {};
    current_room_id = $(location).attr('pathname').split('/')[2];
    let message_send_url = '/send_chat_message/' + current_room_id + '/';

    function messageBuilder(data, pk, user){
        let message = $('<li class="message-chat-message" id="' + pk + '"></li>');
        let message_info = $('<div class="message-chat-message-info"></div>');
        let message_created = $('<span class="message-chat-message-created">' + data.created + '</span>');
        let message_username = $('<span class="message-chat-message-username">' + data.username + '</span>');
        let message_text = $('<div class="message-chat-message-text">' + data.message_text + '</div>');
        let message_image = $('<img class="img-circle chat-user" src="' + data.user_image + '">');
        message.append(message_info.append(message_image).append(message_username)
               .append(message_created)).append(message_text);
        if (data.check == false){
            if (user != data.username){
                message_info.append($('<div class="read-dot"></div>'));
                data.check = true;
            }
            else{
                message_info.append($('<div class="unread-dot"></div>'));
            }
        }
        else{
            message_info.append($('<div class="read-dot"></div>'));
        }
        messages_list[pk] = data;
        return message;
    }

    function scrollBottom(){
        return $('.message-chat-list-wrap').scrollTop(1E10);
    }

    function messageUpdate(key) {
        $('#' + key).find('.unread-dot').attr('class', 'read-dot');
    }

    function messageAppender(message_list, user){
        for (let key in message_list){
            if (message_list[key].update == true){
                    message_list[key].update = false;
                    messageUpdate(key);
            }
            else{
                $('.message-chat-list').append(messageBuilder(message_list[key], key, user));
                let chat_window = $('.message-chat-list-wrap');
                if(chat_window[0].scrollHeight <= chat_window.scrollTop() + chat_window.outerHeight() + 200){
                    scrollBottom();
                }
            }
        }
    }

    function messagePrepender(message_list, user){
        let reversed_list = [];
        for (let key in message_list){
            reversed_list.unshift(key);
        }
        reversed_list.forEach(function (key) {
            $('.message-chat-list').prepend(messageBuilder(message_list[key], key, user));
        })
    }

    function messageListBuilder(response, scroll) {
        if (response.total_objects != undefined){
            total_objects = response.total_objects;
        }
        let message_list = response.messages_list;
        let user = response.user;
        if (scroll == true){
            return messagePrepender(message_list, user)
        }
        return messageAppender(message_list, user);
    }

    function loadMessages(scroll=false, border=0){
        let url = $(location).attr('pathname');
        $.ajax({
            type: 'POST',
            url: url,
            dataType: 'json',
            data: {'data': JSON.stringify(messages_list), 'border': JSON.stringify(border)},
            headers: { "X-CSRFToken": $.cookie("csrftoken") },
            success: function (response) {
                return messageListBuilder(response, scroll);
            },
            complete: function () {
                if (first_load == true){
                    first_load = false;
                    scrollBottom();
                }
                if(scroll == false){
                    setTimeout(function() {loadMessages()}, 2000)
                }
            }
        })
    }

    (loadMessages());

    $(document).on('click', '.chat-user', function () {
        $(location).attr('href', '/' + $(this).parent().find(".message-chat-message-username").text() + '/user_info/');
    });

    $('.message-chat-list-wrap').on('scroll', function (e) {
        if (Object.keys(messages_list).length < total_objects && $(this).scrollTop() == 0){
            scroll_border += 50;
            let old_position = $('.message-chat-list:first-child').offset().top;
            $(this).animate({scrollTop: old_position}, 0);
            return loadMessages(true, scroll_border);
        }
    });

    $('.message-submit').click(function (e) {
        e.preventDefault();
        let form = $('.message-chat-form');
        $.ajax({
            type: 'POST',
            dataType: 'json',
            data: form.serialize(),
            url: $(location).attr('pathname'),
            success: function (response) {
                if ('errors' in response){
                    form.find('textarea').focus();
                    return errorCatcher(response.errors);
                }
                else{
                    messageListBuilder(response);
                    form.trigger('reset');
                    form.find('textarea').focus();
                    return scrollBottom();
                }
            }
        })
    });

    $('.message-submit-chat').click(function (e) {
        e.preventDefault();
        let form = $('.message-chat-form');
        $.ajax({
            type: 'POST',
            dataType: 'json',
            data: form.serialize(),
            url: message_send_url,
            success: function (response) {
                if ('errors' in response){
                    form.find('textarea').focus();
                    return errorCatcher(response.errors);
                }
                else{
                    messageListBuilder(response);
                    form.trigger('reset');
                    form.find('textarea').focus();
                    return scrollBottom();
                }
            }
        })
    });
});
