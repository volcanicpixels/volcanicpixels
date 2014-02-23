import $ from "jquery";

var showElement = function(selector) {
    if ($(selector).hasClass('dismissed')) {
        return;
    }
    if ($(selector).hasClass('hide')) {
        $(selector).hide().removeClass('hide').slideDown(100);
    }
};

var hideElement = function(selector) {
    if (!$(selector).hasClass('hide')) {
        $(selector).slideUp(100,function(){
            $(this).addClass('hide');
        });
    }
};

var doError = function(response, cb) {
    cb = cb || alert;
    if(!response.status || response.status !==  "SUCCESS") {
        var msg = response.msg || 'Unknown error occured';
        cb(msg);
        return true;
    }
    return false;
};

export { showElement, hideElement, doError };
