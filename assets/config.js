var require = {
    baseUrl: '/assets',
    paths: {
        stripe: 'https://js.stripe.com/v2/?1',
        jquery: 'components/jquery/jquery',
        requirejs: 'components/requirejs/require',
        nprogress: 'components/nprogress/nprogress'
    },
    shim: {
        stripe: {
            exports: 'Stripe'
        },
        nprogress: {
            exports: 'NProgress'
        }
    }
};
