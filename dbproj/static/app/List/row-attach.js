define(['zest', 'jquery'], function($z) {

  return $z.create([$z.Constructor, $z.InstanceEvents], {

    construct: function(el, o) {
      this.$el = $(el);
      this.$input = $(el).find('input');
    },

    prototype: {
      
      getValue: function() {
        return this.$input.val();
      },

      fadeOut: function() {
        var self = this;
        this.$el.fadeOut('slow', function() {
          self.dispose();
        });
      },
      
      dispose: function() {
        this.$el.unbind();        
      }

    }

  });

});