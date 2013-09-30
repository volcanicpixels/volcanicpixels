import $ from "jquery";
import NProgress from "nprogress";
import { showElement, hideElement, doError } from "modules/helpers";

$(document).ready(function(){

    var showError = false;
    var orderID = $('.order-id').val();

    $('.pending').show();

    /**
     * Checks the order status
     * @param  {Function} cb Callback to call if it is still pending
     * @return {[type]}      [description]
     */
    var checkStatus = function(cb) {
        cb = cb || function() {};
        $('.pending').addClass("loading");

        if (showError) {
            NProgress.start();
        }

        $.getJSON('order_status', {'order_id': orderID},  function(response){
            $('.pending').removeClass('loading');
            if (showError) {
                NProgress.done();
                showError = false;
            }
            if (doError(response)) {
                return;
            }

            if (response['data']['status'] === "pending" && showError === true) {
                showElement('.not-verified');
                cb();
            }

            if (response['data']['status'] === "active") {
                hideElement('.not-verified');
                hideElement('.pending');
                showElement('.configure');
            }

        });
    };


    var checkStatusRunner = function() {
        checkStatus(function() {
            setTimeout(checkStatusRunner, 1000 * 10);
        });
    };

    checkStatusRunner();

    var isRunning = false;

    var iveVerified = function() {
        if(isRunning) {
            return;
        }
        showError = true;
        isRunning = true;
        $('.ive-verified').addClass('loading').text("checking...").prop('disabled', true);
        checkStatus(function(){
            isRunning = false;
            $('.ive-verified').removeClass('loading').text("I've verified").prop('disabled', false);
        });
    };

    $('.ive-verified').click(iveVerified);

    var resendEmail = function() {
        $('.resend-email').prop('disabled', true).addClass('loading');
        NProgress.start();
        $.getJSON('resend_email', {'order_id': orderID},  function(response){
            $('.resend-email').prop('disabled', false).removeClass('loading');
            NProgress.done();
            if (doError(response, function(msg){
                $('.resend-error').text(msg);
                showElement('.resend-error');
                hidelement('.resend-success');
            })) {
                return;
            }

            hideElement('.resend-error');
            showElement('.resend-success');

        });
    };


    $('.resend-email').click(iveVerified);

});
