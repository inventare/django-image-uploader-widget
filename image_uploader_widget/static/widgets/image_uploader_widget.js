{
    'use strict';

    $ = window.django.jQuery;
    $(function(){
        function callFileClick(e) {
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
        }

        function appendItem(el, url) {
            var delete_icon = '';
            if ($(el).data('candelete')) {
                delete_icon = '<span class="iuw-delete-icon">X</span>'
            }
            $(el).append(
                '<div class="iuw-image-preview">' +
                '   <img src="' + url + '" />' +
                delete_icon +
                '</div>'
            );
        }

        function fileRemarker() {
            if (this.files.length == 0) {
                this.classList.remove('non-empty');
                $(this).parent().find('input[type=checkbox]').prop('checked', true);
            } else {
                this.classList.add('non-empty');
                $(this).parent().find('input[type=checkbox]').prop('checked', false);
            }
            $(this).parent().find('.iuw-image-preview').off('click').remove();
            if (this.files.length > 0) {
                url = URL.createObjectURL(this.files[0]);
                appendItem($(this).parent(), url);
            }
            $(this).parent().find('.iuw-image-preview').on('click', callFileClick);
        }

        $('.iuw-root input[type=file]').each(function(){
            $(this).on('change', fileRemarker);
            $(this).trigger('change');
        });
        $('.iuw-root .iuw-empty').on('click', callFileClick);
        $('.iuw-root[data-raw]').each(function(){
            var raw_file = $(this).attr('data-raw');
            appendItem(this, raw_file);
            $(this).find('.iuw-image-preview').on('click', callFileClick);
        });
    });
}