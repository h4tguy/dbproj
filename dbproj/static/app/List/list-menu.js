define(['zest', './row', 'css!./list'], function($z, Row) {

  return $z.create([$z.Component], {

    options: {
      id: 'main-list',
      text: 'hello'
    },
    ListRegion: function() {
      return {
        options: {
          text: 'good bye'
        },
        render: Row
      }
    },

    render: function(o) {
      return '<div>{`ListRegion`}</div>'
    },

  });

});