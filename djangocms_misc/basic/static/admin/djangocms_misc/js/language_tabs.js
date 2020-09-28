var ModelTranslation = (function( $ ) {
    'use strict';

    $('document').ready(init);

    var $buttons;
    var $menu;
    var translated_items = {};
    var now_lang = 'de';
    var $doc = $(document);

    function init() {
        $menu = $('#page_form_lang_tabs.languagetabs_mixin');
        $buttons = $('input', $menu);
        guess_language();
        get_translated_items();
        $buttons.bind({ click: change_language });
        // official django custom event!
        $doc.on('formset:added', get_translated_items);
    };

    function add_class($items, css_class) {
        // if we dont do this, we cannot target like [class$=_lang], thus using [class*=_de], target main_description_en, when selecting de ...
        for(var i=0; i<$items.length; i++ ) {
            var $item = $($items[i]);
            $item.attr('class', css_class + ' ' + $item.attr('class'));
        }
    };

    function change_language(e) {
        e.preventDefault();
        var $button = $(this);
        var lang = $button.data('language');
        $buttons.removeClass('selected');
        $button.addClass('selected');
        add_class(translated_items[now_lang], 'pseudo-hidden');
        translated_items[lang].removeClass('pseudo-hidden');
        now_lang = lang;
    };

    function guess_language() {
        var cms_path = getQueryVariable('cms_path');
        if (cms_path) {
            // get pre selected language from cms path!
            // assume its /lang_code/whatever-slug/xy/
            var cms_path = decodeURIComponent(cms_path);
            var pieces = cms_path.split('/');
            if (pieces.length > 2) {
                var new_lang = pieces[1];
                var $new_selected = $buttons.filter("[data-language='" + new_lang + "']");
                if ($new_selected.length) {
                    $buttons.removeClass('selected');
                    $new_selected.addClass('selected');
                }
            }
        }
    };

    function get_translated_items() {
        for( var i = 0; i < $buttons.length; i++ ) {
            var $button = $( $buttons[i] );
            var lang = $button.data('language');
            if (translated_items[lang]) {
                translated_items[lang].removeClass('pseudo-hidden');
            }
            translated_items[lang] = $(
                // '.form-row[class*="_' + lang + '"][class*="field-"], td[class*="_' + lang + '"][class*="field-"], th:contains([' + lang + '])'
                '.form-row[class$="_' + lang + '"], td[class$="_' + lang + '"], th:contains([' + lang + '])'
            );
            if ($button.hasClass('selected') ) {
                now_lang = lang;
            } else {
                // TODO delay until ckeditor is loaded
                add_class(translated_items[lang], 'pseudo-hidden ');
            }
        }
    };

    // hate this! but this is a good solution, from
    // https://css-tricks.com/snippets/javascript/get-url-variables/
    function getQueryVariable(variable)
    {
           var query = window.location.search.substring(1);
           var vars = query.split("&");
           for (var i=0;i<vars.length;i++) {
                   var pair = vars[i].split("=");
                   if(pair[0] == variable){return pair[1];}
           }
           return(false);
    }

})( django.jQuery );