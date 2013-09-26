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

export { showElement, hideElement };
