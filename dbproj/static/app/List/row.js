define(['zest', 'css!./row'], function($z) {

  return $z.create([$z.Component], {

    options: {
      inputType: 'input',
      label: 'Default label',
    },

    render: function(o) {
      var tpl  = ['<li>',
                  '<div class="view">',
                  '<input class="toggle" type="checkbox" checked>',
                  '<label>' + o.label + '</label>',
                  '</div>',
                  '<input class="edit" value="' + o.label + '">',
                  '</li>'];

      return tpl.join(' ');
    },

    pipe: true,
    
    attach: './row-attach'

  });

});