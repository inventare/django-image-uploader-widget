{
    'use strict';

    $ = window.django.jQuery;
    $(function(){
        function updateElementIndex(el, prefix, ndx) {
            const id_regex = new RegExp("(" + prefix + "-(\\d+|__prefix__))");
            const replacement = prefix + "-" + ndx;
            if ($(el).prop("for")) {
                $(el).prop("for", $(el).prop("for").replace(id_regex, replacement));
            }
            if (el.id) {
                id = el.id.replace(id_regex, replacement)
                el.id = id;
            }
            if (el.name) {
                el.name = el.name.replace(id_regex, replacement);
            }
        }

        function updateAllIndexes(root) {
            var items = root.find('.inline-related:not(.empty-form)');
            var prefix = root.data('prefix');
            var i;
            for (i = 0; i < items.length; i += 1) {
                updateElementIndex($(items).get(i), prefix, i);
                $(items.get(i)).find("*").each(function(){
                    updateElementIndex($(this).get(0), prefix, i);
                });
            }
            root.data('next', i);
            var totalForms = root.find('#id_' + prefix + '-TOTAL_FORMS');
            totalForms.val(i);
            var maxForms = root.find('#id_' + prefix + '-MAX_NUM_FORMS');
            if ((maxForms.val() === '') || (maxForms.val() - i) > 0) {
                root.find('.iuw-add-image-btn').addClass('visible-by-number');
            } else {
                root.find('.iuw-add-image-btn').removeClass('visible-by-number');
            }
        }

        function callFileClick(e) {
            var root = $(this).closest('.iuw-inline-root');
            var item = $(this).closest('.inline-related');
            if ($(e.target).hasClass('iuw-delete-icon')) {
                if (item.attr('data-raw')) {
                    item.addClass('deleted');
                    item.find('input[type=checkbox]').prop('checked', true);
                } else {
                    item.remove();
                }
                updateEmpty(root);
                return;
            }
            var file = item.find('input[type=file]');
            if (e.target == file[0]) {
                return;
            }
            file.trigger('click');
        }

        function fileInputChange(e) {
            var files = $(this).prop('files');
            if (files.length <= 0) {
                return;
            }
            var blob = URL.createObjectURL(files[0]);
            $(this).closest('.inline-related').find('img').attr('src', blob);
        }
        
        function appendItem(el, url) {
            var delete_icon = '';
            var item = $(el).closest('.inline-related');
            if (item.data('candelete')) {
                delete_icon = '<span class="iuw-delete-icon">X</span>'
            }
            $(el).append(
                '<img src="' + url + '" />' + delete_icon
            );
            item.off('click');
            item.on('click', callFileClick);
            var fileInput = item.find('input[type=file]');
            fileInput.off('change');
            fileInput.on('change', fileInputChange);
        }

        function updateEmpty(root) {
            var childs = root.find('.inline-related:not(.empty-form):not(.deleted)');
            if (childs.length > 0) {
                root.addClass('non-empty');
            } else {
                root.removeClass('non-empty');
            }
        }
        
        $('.iuw-inline-root .inline-related').each(function(){
            var hiddenInputs = $(this).find('input[type=hidden]');
            var rawImage = $(this).find('p.file-upload a');
            var fileInput = $(this).find('input[type=file]');
            var checkBoxInput = $(this).find('input[type=checkbox]');
            if (rawImage) {
                $(this).attr('data-raw', rawImage.attr('href'));
            }
            checkBoxInput.remove();
            hiddenInputs.remove();
            fileInput.remove();
            $(this).html('');
            $(this).append(hiddenInputs);
            $(this).append(fileInput);
            $(this).append(checkBoxInput);
            if ($(this).attr('data-raw')) {
                appendItem($(this), $(this).attr('data-raw'));
            }
        });
        $('.iuw-inline-root').each(function(){
            var data = $(this).closest('.inline-group').data();
            $(this).data('prefix', data.inlineFormset.options.prefix);
            updateEmpty($(this));
            updateAllIndexes($(this));
        });

        function handleAddImage(){
            var root = $(this).closest('.iuw-inline-root');
            if (root.find('input[type=file].temp_file').length == 0) {
                root.append('<input type="file" class="temp_file" accept="image/*" style="display: none;" />');
                root.find('input[type=file].temp_file').on('change', function(e){
                    var fileList = $(this).prop('files');
                    $(this).off('change');
                    $(this).remove();
                    var template = root.find('.inline-related.empty-form');
                    var row = template.clone(true)
                        .removeClass('empty-form')
                        .removeClass('last-related')
                        .attr('data-candelete', true)
                        .attr("id", root.data('prefix') + "-" + root.data('next'));
                    $(row).insertBefore($(template));
                    row.find('input[type=file]').prop('files', fileList);
                    var blob = URL.createObjectURL(fileList[0]);
                    appendItem(row, blob);
                    updateEmpty(root);
                    updateAllIndexes(root);
                });
            }
            root.find('input[type=file].temp_file').trigger('click');
        }

        $('.iuw-inline-root .iuw-add-image-btn').on('click', handleAddImage);
        $('.iuw-inline-root .iuw-empty').on('click', handleAddImage);
    });
}
