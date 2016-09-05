(function($){
    $.fn.formfield_stash = function(custom_options) {
        var options = {
            type:'dealer',
            dummy: 'dummy'
        }

        return this.each(function() {
            var _self = $(this);
            var prefix = '';
            var $options = _self.find("option");
            var fields = [];
            var fieldconfigs = {};
            var has_configs = false;
            if (_self.attr("data-original-field") != _self.attr("name")) {
                prefix = _self.attr("name").replace(_self.attr("data-original-field"), '');
            }

            _self.attr('data-formfield-stash', 'initialized');
            $.each($options, function(index, item) {
                // TODO: check for formsets/name prefixes in inlines
                var value = $(item).val();
                var config = _self.attr('data-formfield-stash-' + value)
                if (config) {
                    has_configs = true;
                    var temp_fields = config.split(",");
                    fieldconfigs[value] = temp_fields;
                    fields = fields.concat(temp_fields);
                } else {
                    fields.push(value);
                }
            });
            var $form = _self.closest("form");

            var on_change = function(e) {
                var current_value = _self.val();
                $.each(fields, function(index, item) {
                    var selector = "#id_" + prefix + item;
                    var $field = $form.find(selector);
                    var $wrap = $field.closest(".form-row");
                    if (item.indexOf("#") > -1) {
                        selector = item;
                        $wrap = $(selector);
                    }
                    if (!$wrap.size()) {
                        // multi widget fields workaround, for now!
                        $wrap = $form.find(selector + "_0").closest(".form-row");
                    }
                    if (has_configs) {
                        var current_config = fieldconfigs[current_value];
                        if ($.inArray(item, current_config) > -1) {
                            $wrap.show(0);
                        } else {
                            $wrap.hide(0);
                        }
                    } else {
                        if (item == current_value) {
                            $wrap.show(0);
                        } else {
                            $wrap.hide(0);
                        }
                    }
                })
            };

            _self.change(on_change);
            on_change();

            return this;
        });
    }
})(django.jQuery);


// init, including add row for inlines
django.jQuery(document).ready( function($) {

    $('.inline-group').each(function(index, inline) {
        if ($(inline).find("fieldset select[data-formfield-stash=true]").size()) {
            $(inline).find(".add-row").click(add_row_handler);
        };
    });

    function add_row_handler(event) {
        // depends on html structure, bad. but...
        var $inline = $(event.currentTarget).parent();
        var $to_enhance = $inline.find(".last-related:not(.empty-form ) select[data-formfield-stash=true]");
        $to_enhance.formfield_stash();
    }

    $('form select[data-formfield-stash=true]').not("[name*=__prefix__]").formfield_stash();
});