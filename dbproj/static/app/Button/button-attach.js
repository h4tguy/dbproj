define(['zest', 'jquery'], function($z) {

  return $z.create([$z.Constructor, $z.InstanceEvents], {

    _events: ['click'],

    construct: function(el, o) {
      this.$button = $(el);
      this.$button.click(this.click);
    },

    prototype: {
      
      click: function() {},

      dispose: function() {
        this.$button.unbind();
      }

    }

  });

});