define("modules/credit-card/index",
  ["modules/helpers","jquery","stripe","exports"],
  function(__dependency1__, $, Stripe, __exports__) {
    "use strict";
    var showElement = __dependency1__.showElement;
    var hideElement = __dependency1__.hideElement;

    Stripe.setPublishableKey('pk_test_NgVxcRzPcljLftdwhuJAMMpX');

    var formatCardNumber = function(e) {
    };

    var cardExpiry = function() {
        var expiry = $(this).val().replace(' ', '');

        if (expiry.indexOf('/') === -1) {
            return;
        }

        expiry = expiry.split('/');

        if (expiry.length !== 2) {
            return;
        }

        console.log(expiry);

        $('.cc-expiry-month').val(expiry[0]);
        $('.cc-expiry-year').val(expiry[1]);

    };

    var setupCard = function() {
        $(this).find('.cc-expiry').on('keyup', cardExpiry);
    };

    /**
     * Binds events to all .credit-card elements
     */
    var setup = function() {
        $('.credit-card').each(setupCard);
    };

    var parseError = function(error) {
        if (error.param === "number") {
            $('.credit-card .cc-number').addClass('error');
        }

        if (error.param === "cvc") {
            $('.credit-card .cc-cvc').addClass('error');
        }

        if (error.param === "exp_month") {
            $('.credit-card .cc-expiry-month').addClass('error');
        }

        if (error.param === "exp_year") {
            $('.credit-card .cc-expiry-year').addClass('error');
        }

        if($('.payment-error').length === 0) {
            alert(error.message);
        } else {
            $(".payment-error").text(error.message);
            showElement('.payment-errors');
        }
    };

    var tokenize = function(cb, errback) {
        cb = cb || function(){};
        errback = errback || function(){};
        var form = $('.credit-card').parents('form');
        Stripe.createToken(form[0], function(status, response) {
            $('.credit-card input').removeClass('error');
            if (response.error) {
                parseError(response.error);
                errback(response.error);
            } else {
                hideElement('.payment-errors');
                var token = response['id'];
                $('.stripe-token').val(token);
                cb();
            }
        });
    };


    __exports__.setup = setup;
    __exports__.tokenize = tokenize;
  });