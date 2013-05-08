define(['zest', 'css!./row'], function($z) {

  return $z.create([$z.Component], {

    options: {
      inputType: 'input',
      text: 'Default label',
    },

    render: function(o) {
      var tpl  = ['<li>',
                  '<div class="view">',
                  '<input class="toggle" type="checkbox" checked>',
                  '<label>' + o.text + '</label>',
                  '</div>',
                  '<input class="edit" value="' + o.text + '">',
                  '</li>'];

      return tpl.join(' ');
    },

    pipe: true,
    
    attach: './row-attach'

  });

});