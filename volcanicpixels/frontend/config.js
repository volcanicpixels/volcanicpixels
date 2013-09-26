var require = {
    baseUrl: '/assets',
    paths: {
        'stripe': 'https://js.stripe.com/v2/?1'
    },
    shim: {
        'stripe': {
          exports: 'Stripe'
        },
        'nprogress': {
          exports: 'NProgress'
        }
    }
};
