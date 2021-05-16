odoo.define('department_matrix.dep_matrix', function (require) {
    "use strict";
        // var _t = core._t;
        var basic_fields = require('web.basic_fields');
        var registry = require('web.field_registry');
        
        // widget implementation
        var CounterCharWidget = basic_fields.FieldChar.extend({
            events: _.extend({}, basic_fields.FieldChar.prototype.events, {
                'keyup': '_onKeypress',
            }),

            _onKeypress: function(e,n) {
                $(this.$el[1]).text(this.display_number_of_value(e.target))
            },

            display_number_of_value : function(target){
                return (target.value.length || '_' ) + '/' +  (this.field.size || '_')
            },

            // _render: function() {
            //     // console.log('***_renderEdit***', 'this.field', this.field)
            //     var def = this._super.apply(this, arguments);
            //     var $span = $('<span name="enforced_tz" class="fa fa-info-circle o_tz_warning ndt_span"  style="color:#dc3545;margin-left:2px"></>');
            //     $span.text(this.display_number_of_value(this))
            //     $span.attr('title', 'Number of characters/ Max length');
            //     this.$el.addClass('ndt_input')
            //     this.$el = this.$el.add($span)
            //     return def;
            // },

            _renderReadonly: function () {
                var def = this._super.apply(this, arguments);
                var $span = $('<span name="enforced_tz" class="fa fa-info-circle o_tz_warning "  style="color:#dc3545;margin-left:2px"></>');
                $span.text(this.display_number_of_value(this))
                $span.attr('title', 'Number of characters/ Max length');
                this.$el.addClass('ndt_input')
                this.$el = this.$el.add($span)
                return def;
               
            },

            _renderEdit: function() {

                var def = this._super.apply(this, arguments);
                var $span = $('<span name="enforced_tz" class="fa fa-info-circle o_tz_warning ndt_span"  style="color:#dc3545;margin-left:2px"></>');
                $span.text(this.display_number_of_value(this))
                $span.attr('title', 'Number of characters/ Max length');
                this.$el.addClass('ndt_input')
                this.$el = this.$el.add($span)
                return def;


               
            },



        });
        
        registry.add('counter_char', CounterCharWidget); // add our "bold" widget to the widget registry

})
