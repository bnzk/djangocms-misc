var ModelTranslation = (function( $ ) {
    'use strict';

    $('document').ready(init);

    var $buttons;
    var $menu;
    var fields = {};
    var now_lang = 'de';

    function init() {
        $menu = $('#page_form_lang_tabs.languagetabs_mixin');
        $buttons = $('input', $menu);
        prepare_form();
        $buttons.bind({ click: change_language });
    };

    function change_language(e) {
        e.preventDefault();
        var $button = $(this);
        var lang = $button.data('language');
        $buttons.removeClass('selected');
        $button.addClass('selected');
        fields[now_lang].addClass('pseudo-hidden');
        fields[lang].removeClass('pseudo-hidden');
        now_lang = lang;
    };

    function prepare_form() {
        var cms_path = getQueryVariable('cms_path');
        if (cms_path) {
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
        for( var i = 0; i < $buttons.length; i++ ) {
            var $button = $( $buttons[i] );
            var lang = $button.data('language');
            fields[lang] = $('.form-row[class$="_' + lang + '"]');
            if ( $button.hasClass('selected') ) {
                now_lang = lang;
            } else {
                // TODO delay until ckeditor is loaded
                fields[lang].addClass('pseudo-hidden');
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