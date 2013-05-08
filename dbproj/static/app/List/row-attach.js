define(['zest', 'jquery'], function($z) {

  return $z.create([$z.Constructor, $z.InstanceEvents], {

    construct: function(el, o) {
      this.$input = $(el).find('input');
    },

    prototype: {
      
      getValue: function() {
        return this.$input.val();
      },
      
      dispose: function() {
        this.$input.unbind();
      }

    }

  });

});