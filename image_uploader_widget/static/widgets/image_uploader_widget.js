{
    'use strict';
    $ = window.django.jQuery;
    $(function(){
        $.fn.imageUploader = function() {
            const handler = {
                elements: $(this),
                callFileClick: function(e) {
                    var $root = $(this).closest('.iuw-root');
                    if ($(e.target).hasClass('iuw-delete-icon')) {
                        $root.removeAttr('data-raw');
                        $(this).closest('.iuw-image-preview').remove();
                        $root.find('input[type=checkbox]').prop('checked', true);
                        $root.find('input[type=file]').val(null);
                        $root.find('input[type=file]').trigger('change');
                        return;
                    }
                    $root.find('input[type=file]').trigger('click');
                },
                fileRemarker: function(e) {
                    var iuw = $(this).parent().data('iuw');
                    var raw = $(this).parent().attr('data-raw');
                    if (this.files.length == 0 && !raw) {
                        this.classList.remove('non-empty');
                        $(this).parent().find('input[type=checkbox]').prop('checked', true);
                    } else {
                        this.classList.add('non-empty');
                        $(this).parent().find('input[type=checkbox]').prop('checked', false);
                    }
                    $(this).parent().find('.iuw-image-preview').off('click').remove();
                    if (this.files.length > 0) {
                        url = URL.createObjectURL(this.files[0]);
                        iuw.appendItem($(this).parent(), url);
                    }
                    $(this).parent().find('.iuw-image-preview').on('click', iuw.callFileClick);
                },
                appendItem(el, url) {
                    var delete_icon = '';
                    if ($(el).data('candelete')) {
                        delete_icon = '<span class="iuw-delete-icon">X</span>'
                    }
                    var html = '<div class="iuw-image-preview">' +
                            '   <img src="' + url + '" />' +
                            delete_icon +
                            '</div>';
                    $(el).append(html);
                },
                init: function() {
                    var that = this;
                    this.elements.each(function(index, element){
                        $(element).data('iuw', that);
                        $(element).find('input[type=file]').each(function(){
                            $(this).on('change', that.fileRemarker);
                            $(this).trigger('change');
                        });
                        $(element).find('.iuw-empty').on('click', that.callFileClick);
                        if ($(element).attr('data-raw')) {
                            var raw_file = $(element).attr('data-raw');
                            that.appendItem(element, raw_file);
                            $(element).find('.iuw-image-preview').on('click', that.callFileClick);
                        }
                    });
                },
            };
            handler.init();
            return handler;
        };

        $(document).ready(function(){
            $('.iuw-root').imageUploader();
        })
    });
}