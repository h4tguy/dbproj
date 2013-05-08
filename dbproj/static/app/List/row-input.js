define(['zest', './row', 'css!./row'], function($z, Row) {

  return $z.create([Row], {

    _extend: {
      options: 'REPLACE',
      render: 'REPLACE'
    },

    options: {
      placeholder: 'Default placeholder'
    },

    render: function(o) {
      var tpl  = '<li>';
          tpl +=   '<div class="view">';
          tpl +=     '<input class="plain"' + ((o.inputType == 'password') ? 'type="password"' : '') + ' placeholder="' + o.placeholder + '">';
          tpl +=   '</div>';
          tpl += '</li>';

      return tpl;
    },

  });
  
});