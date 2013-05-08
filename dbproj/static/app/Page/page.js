define(['zest', 'jquery', '~/app/Logo/logo', '~/app/List/list-login', '~/app/Button/button', 'md5', 'css!./page.css'], function($z, $, Logo, ListLogin, Button, md5) {

  return $z.create([$z.Component], {

    options: {
      title: 'Default site title',
      id: 'frame'
    },

    LogoRegion: Logo,
    ListRegion: ListLogin,
    ButtonsRegion: 
      [{
        options: {
          className: 'right login-btn',
          text: 'Log in'
        },
        render: Button
      },
      {
        options: {
          text: 'Register'
        },
        render: Button
      }],

    render: function(o) {
      var page  = '<section>{`LogoRegion`}';  
          page += '<section id="main" class="loading narrow"><header id="header"></header>';
          page += '{`ListRegion`}';
          page += '<footer id="footer">{`ButtonsRegion`}</footer></section>';
          page += '<footer id="info"><p>Log in or register to begin.</p><p>CSC2001F Assignment 7</p></footer></section>';
          
      return page;
    },

    attach: './page-attach'

  });

});