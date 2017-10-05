function errorCatcher(response, bc=undefined){
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
        error_message.append($('<div>' + response[e] + '</div>'));
    }
    if (bc){
        error_message.css({'background-color': '#00af14', 'border-color': '#00af14'});
    }
    error_messages.append(error_message);
    setTimeout(function () {$('#' + id).fadeOut(1500, function () {
        $('#' + id).remove();});
    }, 5000);
}
