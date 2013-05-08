define(['zest', './row-input', 'css!./list'], function($z, RowInput) {

  return $z.create([$z.Component], {

    options: {
      id: 'main-list',

      ListRows: [{
        options: {
          className: 'studentno-input',
          placeholder: 'Student Number'
        },
        render: RowInput
      }, {
        options: {
          className: 'password-input',
          placeholder: 'Password',
          inputType: 'password'
        },
        render: RowInput
      }],

    },

    render: function(o) {
      return '<ul>{`ListRows`}</ul>';
    },

  });

});