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
                 * Update the indexes in a item.
                 * @param {HTMLElement} el The element to update indexes.
                 * @param {String} prefix The item prefix.
                 * @param {Number} ndx The item index.
                 */
                updateElementIndex: function(el, prefix, ndx) {
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
                },
                /**
                 * Update all item indexes in a root element.
                 * @param {HTMLElement} root The root html element.
                 */
                updateAllIndexes: function(root) {
                    var items = root.find('.inline-related:not(.empty-form)');
                    var prefix = root.data('prefix');
                    var i;
                    for (i = 0; i < items.length; i += 1) {
                        this.updateElementIndex($(items).get(i), prefix, i);
                        var that = this;
                        $(items.get(i)).find("*").each(function(){
                            that.updateElementIndex($(this).get(0), prefix, i);
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
                },
                /**
                 * Check if we have any item in the root and marker the root with a class.
                 * @param {HTMLElement} root The root element to check if we have any item.
                 */
                updateEmpty: function(root) {
                    var childs = $(root).find('.inline-related:not(.empty-form):not(.deleted)');
                    if (childs.length > 0) {
                        root.addClass('non-empty');
                    } else {
                        root.removeClass('non-empty');
                    }
                },
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
                /**
                 * Append a '.inline-related' markup to the '.inline-related'.
                 * @param {HTMLElement} el The element to append the '.inline-related' inner markup.
                 * @param {String} url The image url of the item.
                 */
                appendItem: function(el, url) {
                    var delete_icon = '';
                    var item = $(el).closest('.inline-related');
                    if (item.data('candelete')) {
                        delete_icon = '<span class="iuw-delete-icon">X</span>'
                    }
                    $(el).append(
                        '<img src="' + url + '" />' + delete_icon
                    );
                    item.off('click');
                    item.on('click', this.callFileClick);
                    var fileInput = item.find('input[type=file]');
                    fileInput.off('change');
                    fileInput.on('change', this.fileInputChange);
                },
                /**
                 * Adjust inline related element to this script standards.
                 * @param {HTMLElement} element The '.inline-related' element.
                 */
                adjustInlineRelated: function(element) {
                    var hiddenInputs = $(element).find('input[type=hidden]');
                    var rawImage = $(element).find('p.file-upload a');
                    var fileInput = $(element).find('input[type=file]');
                    var checkBoxInput = $(element).find('input[type=checkbox]');
                    if (rawImage) {
                        $(element).attr('data-raw', rawImage.attr('href'));
                    }
                    checkBoxInput.remove();
                    hiddenInputs.remove();
                    fileInput.remove();
                    $(element).html('');
                    $(element).append(hiddenInputs);
                    $(element).append(fileInput);
                    $(element).append(checkBoxInput);
                    if ($(element).attr('data-raw')) {
                        this.appendItem($(element), $(element).attr('data-raw'));
                    }
                },
                /**
                 * Add image event handler.
                 */
                handleAddImage: function(){
                    var root = $(this).closest('.iuw-inline-root');
                    var iuw = root.data('iuw');
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
                            iuw.appendItem(row, blob);
                            iuw.updateEmpty(root);
                            iuw.updateAllIndexes(root);
                        });
                    }
                    root.find('input[type=file].temp_file').trigger('click');
                },
                /**
                 * Initialize the image uploader inline.
                 */
                init: function() {
                    const that = this;
                    this.elements.each(function(index, element){
                        var data = $(element).closest('.inline-group').data();
                        $(element).data('prefix', data.inlineFormset.options.prefix);
                        that.updateEmpty($(element));
                        that.updateAllIndexes($(element));

                        $(element).find('.inline-related').each(function(index, related){
                            that.adjustInlineRelated(related);
                        });
                        $(element).find('.iuw-add-image-btn').on('click', that.handleAddImage);
                        $(element).find('.iuw-empty').on('click', that.handleAddImage);
                        $(element).data('iuw', that);
                    });
                }
            };
            handler.init();
            return handler;
        };

        $(document).ready(function(){
            $('.iuw-inline-root').inlineImageUploader();
        });
    });
}
