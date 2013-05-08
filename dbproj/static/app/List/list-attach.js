define(['zest', 'jquery'], function($z) {

  return $z.create([$z.Constructor, $z.InstanceEvents], {

    _events: [],

    construct: function(el, o) {     
      this.$list = $(el);
    },

    prototype: {

      clearList: function(o) {
        var self = this;
        return this.$list.fadeOut('slow', function() {
          self.dispose();
        });
      },

      dispose: function() {
        this.$list.unbind();
      }

    }

  });

});