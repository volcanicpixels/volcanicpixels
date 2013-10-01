define("ssl/complete",
  ["modules/helpers","jquery","nprogress"],
  function(__dependency1__, $, NProgress) {
    "use strict";
    var showElement = __dependency1__.showElement;
    var hideElement = __dependency1__.hideElement;
    var doError = __dependency1__.doError;

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
            $('.ive-verified').addClass('loading').text("checking...").prop('disabled', true);

            if (showError) {
                NProgress.start();
            }

            $.getJSON('order_status', {'order_id': orderID},  function(response){
                $('.ive-verified').removeClass('loading').text("I've verified").prop('disabled', false);
                if (showError) {
                    NProgress.done();
                }
                if (doError(response)) {
                    showError = false;
                    return;
                }

                if (response['data']['status'] === "pending") {
                    if (showError) {
                        showElement('.not-verified');
                    }
                    cb();
                }

                if (response['data']['status'] === "active") {
                    hideElement('.not-verified');
                    hideElement('.pending');
                    showElement('.configure');
                }
            
                showError = false;

            });
        };


        var checkStatusRunner;
        var runCount = 0;

        checkStatusRunner = function() {
            checkStatus(function() {
                runCount++;
                var timer = 1000 * 10;
                if (runCount > 6) {
                    timer = timer * 2;
                }
                if (runCount > 10) {
                    timer = timer * 2;
                }
                if (runCount < 30) {
                    setTimeout(checkStatusRunner, timer);
                }
            
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
            checkStatus(function(){
                isRunning = false;
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
                    hideElement('.resend-success');
                })) {
                    return;
                }

                hideElement('.resend-error');
                showElement('.resend-success');

            });
        };


        $('.resend-email').click(resendEmail);

    });

  });
