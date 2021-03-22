odoo.define("department_matrix.dep_matrix", function (require) {
  "use strict";
  var basic_fields = require("web.basic_fields");
  var registry = require("web.field_registry");

  var CounterCharWidget = basic_fields.FieldChar.extend({
    events: _.extend({}, basic_fields.FieldChar.prototype.events, {
      keyup: "_onKeypress",
    }),

    _onKeypress: function (e, n) {
      $(this.$el[1]).text(this.display_number_of_value(e.target));
    },

    display_number_of_value: function (target) {
      return (
        (target.value.length || "_") + "/" + (this.field.counter_size || this.field.size || "_")
      );
    },

    counter_render: function (is_render_edit = false) {
      var $span = $('<span class="counter_widget_span"></>');
      if (is_render_edit) {
        $span.addClass("counter_wiget_list_edit_span");
      }
      $span.text(this.display_number_of_value(this));
      $span.attr("title", "Number of characters/ Max length");
      this.$el.addClass("counter_wiget_list_input");
      this.$el = this.$el.add($span);
    },

    _renderReadonly: function () {
      var def = this._super.apply(this, arguments);
      this.counter_render();
      return def;
    },

    _renderEdit: function () {
      var def = this._super.apply(this, arguments);
      if (this.field.counter_size && this.field.counter_size > 0) {
        this.$el.attr('maxlength', this.field.counter_size);
    }
      this.counter_render(true);
      return def;
    },
  });

  registry.add("counter_char", CounterCharWidget); 
});
