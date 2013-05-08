define(['zest', 'css!./logo'], function($z) {

  return $z.create([$z.Component], {

    options: {
      id: 'logo'
    },

    render: function(o) {
      return '<section><img src="/static/app/Logo/logo-icon.png" width="330" height="330" /></section>';
    },

  });

});