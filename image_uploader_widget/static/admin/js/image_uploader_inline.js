{
    'use strict';
    $ = window.django.jQuery;
    $(function(){
        $.fn.inlineImageUploader = function() {
            const handler = {
                /**
                 * The initiated elements collection.
                 */
                elements: $(this),
                /**
                 * Item click event Handler.
                 * @param {Event} e The event object.
                 */
                callFileClick: function(e) {
                    var root = $(this).closest('.iuw-inline-root');
                    var data = root.data('iuw');
                    var item = $(this).closest('.inline-related');
                    if ($(e.target).hasClass('iuw-delete-icon')) {
                        if (item.attr('data-raw')) {
                            item.addClass('deleted');
                            item.find('input[type=checkbox]').prop('checked', true);
                        } else {
                            item.remove();
                        }
                        data.updateEmpty(root);
                        return;
                    }
                    var file = item.find('input[type=file]');
                    if (e.target == file[0]) {
                        return;
                    }
                    file.trigger('click');
                },
                /**
                 * Inner file input change event.
                 * @param {Event} e The event object.
                 */
                fileInputChange: function(e) {
                    var files = $(this).prop('files');
                    if (files.length <= 0) {
                        return;
                    }
                    var blob = URL.createObjectURL(files[0]);
                    $(this).closest('.inline-related').find('img').attr('src', blob);
                },
            };
            handler.init();
            return handler;
        };

    });
}
