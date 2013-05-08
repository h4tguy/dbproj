define(['zest', 'jquery', 'css!./button'], function($z, $) {

  return $z.create([$z.Component], {

    options: {
      text: 'Default'
    },

    render: function(o) {
      return '<button>' + o.text + '</button>';
    },

    attach: './button-attach'
    
  });

});