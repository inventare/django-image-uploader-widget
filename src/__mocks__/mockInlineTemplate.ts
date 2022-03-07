import { ImageUploaderInlineFormSet } from '../Inline/Utils';

interface getMockInlineTemplateOptions {
    formset?: ImageUploaderInlineFormSet;
    images?: string[];
    canDelete?: boolean;
    maxCount?: number | string;
}

export const getMockInlineTemplate = ({
    formset = {
        name: 'my-editor',
        options: {
            prefix: 'my-prefix',
            addText: 'add',
            deleteText: 'delete',
        },
    },
    images = [],
    canDelete = true,
    maxCount = 1000,
}: getMockInlineTemplateOptions) => `
<div
    class="iuw-inline-admin-formset inline-group"
    id="${formset.options.prefix}-group"
    data-inline-type="image-uploader"
    data-inline-formset='${JSON.stringify(formset)}'
>
    <label>Images:</label>

    <div class="iuw-inline-root">
        <div>
            <input type="hidden" name="${formset.options.prefix}-TOTAL_FORMS" value="0" id="id_${formset.options.prefix}-TOTAL_FORMS" />
            <input type="hidden" name="${formset.options.prefix}-INITIAL_FORMS" value="0" id="id_${formset.options.prefix}-INITIAL_FORMS" />
            <input type="hidden" name="${formset.options.prefix}-MIN_NUM_FORMS" value="0" id="id_${formset.options.prefix}-MIN_NUM_FORMS" />
            <input type="hidden" name="${formset.options.prefix}-MAX_NUM_FORMS" value="${maxCount}" id="id_${formset.options.prefix}-MAX_NUM_FORMS" />
            ${images.map((image, index) => `
                <div
                    class="inline-related has_original" id="${formset.options.prefix}-${index}"
                    ${canDelete ? ' data-candelete="true" ' : ''}
                >
                    <fieldset class="module aligned ">
                        <div class="form-row field-image">
                            <div>
                                <label class="required" for="id_${formset.options.prefix}-${index}-image">Image:</label>
                                <p class="file-upload">
                                    Currently: <a href="${image}">${image}</a><br>Change:
                                    <input type="file" name="${formset.options.prefix}-${index}-image" accept="image/*" id="id_${formset.options.prefix}-${index}-image" />
                                </p>
                            </div>
                        </div>
                    </fieldset>
                    ${canDelete ? `<input type="checkbox" name="${formset.options.prefix}-${index}-DELETE" id="id_${formset.options.prefix}-${index}-DELETE" />` : ''}
                    <input type="hidden" name="${formset.options.prefix}-${index}-id" value="1" id="id_${formset.options.prefix}-${index}-id" />
                    <input type="hidden" name="${formset.options.prefix}-${index}-example" value="1" id="id_${formset.options.prefix}-${index}-example"/>
                </div>
            `).join('')}
            <div
                class="inline-related empty-form last-related" id="${formset.options.prefix}-empty"
                ${canDelete ? ' data-candelete="true" ' : ''}
            >
                <fieldset class="module aligned ">
                    <div class="form-row field-image">
                        <div>
                            <label class="required" for="id_${formset.options.prefix}-__prefix__-image">Image:</label>
                            <input type="file" name="${formset.options.prefix}-__prefix__-image" accept="image/*" id="id_${formset.options.prefix}-__prefix__-image" />
                        </div>
                    </div>
                </fieldset>
                <input type="hidden" name="${formset.options.prefix}-__prefix__-id" id="id_${formset.options.prefix}-__prefix__-id" />
                <input type="hidden" name="${formset.options.prefix}-__prefix__-example" value="1" id="id_${formset.options.prefix}-__prefix__-example" />
            </div>
            
            <div class="iuw-add-image-btn">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" width="100%" height="100%"><path xmlns="http://www.w3.org/2000/svg" d="M21 15v3h3v2h-3v3h-2v-3h-3v-2h3v-3h2zm.008-12c.548 0 .992.445.992.993V13h-2V5H4v13.999L14 9l3 3v2.829l-3-3L6.827 19H14v2H2.992A.993.993 0 0 1 2 20.007V3.993A1 1 0 0 1 2.992 3h18.016zM8 7a2 2 0 1 1 0 4 2 2 0 0 1 0-4z"></path></svg>
                <span>{% translate 'Add image' %}</span>
            </div>
            <div class="iuw-empty">
                <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi bi-cloud-upload" viewBox="0 0 16 16" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" width="100%" height="100%"><path xmlns="http://www.w3.org/2000/svg" fill-rule="evenodd" d="M4.406 1.342A5.53 5.53 0 0 1 8 0c2.69 0 4.923 2 5.166 4.579C14.758 4.804 16 6.137 16 7.773 16 9.569 14.502 11 12.687 11H10a.5.5 0 0 1 0-1h2.688C13.979 10 15 8.988 15 7.773c0-1.216-1.02-2.228-2.313-2.228h-.5v-.5C12.188 2.825 10.328 1 8 1a4.53 4.53 0 0 0-2.941 1.1c-.757.652-1.153 1.438-1.153 2.055v.448l-.445.049C2.064 4.805 1 5.952 1 7.318 1 8.785 2.23 10 3.781 10H6a.5.5 0 0 1 0 1H3.781C1.708 11 0 9.366 0 7.318c0-1.763 1.266-3.223 2.942-3.593.143-.863.698-1.723 1.464-2.383z"></path><path xmlns="http://www.w3.org/2000/svg" fill-rule="evenodd" d="M7.646 4.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1-.708.708L8.5 5.707V14.5a.5.5 0 0 1-1 0V5.707L5.354 7.854a.5.5 0 1 1-.708-.708l3-3z"></path></svg>
                <span>{% translate 'Drop your images here or click to select...' %}</span>
            </div>
            <div class="iuw-drop-label">
                <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi bi-cloud-upload" viewBox="0 0 16 16" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" width="100%" height="100%"><path xmlns="http://www.w3.org/2000/svg" fill-rule="evenodd" d="M4.406 1.342A5.53 5.53 0 0 1 8 0c2.69 0 4.923 2 5.166 4.579C14.758 4.804 16 6.137 16 7.773 16 9.569 14.502 11 12.687 11H10a.5.5 0 0 1 0-1h2.688C13.979 10 15 8.988 15 7.773c0-1.216-1.02-2.228-2.313-2.228h-.5v-.5C12.188 2.825 10.328 1 8 1a4.53 4.53 0 0 0-2.941 1.1c-.757.652-1.153 1.438-1.153 2.055v.448l-.445.049C2.064 4.805 1 5.952 1 7.318 1 8.785 2.23 10 3.781 10H6a.5.5 0 0 1 0 1H3.781C1.708 11 0 9.366 0 7.318c0-1.763 1.266-3.223 2.942-3.593.143-.863.698-1.723 1.464-2.383z"></path><path xmlns="http://www.w3.org/2000/svg" fill-rule="evenodd" d="M7.646 4.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1-.708.708L8.5 5.707V14.5a.5.5 0 0 1-1 0V5.707L5.354 7.854a.5.5 0 1 1-.708-.708l3-3z"></path></svg>
                <span>{% translate 'Drop your images here...' %}</span>
            </div>
        </div>
    </div>
</div>`;

interface GetMockManagementFormsOptions {
    prefix?: string;
    maxCount?: number | string;
    total?: boolean;
    initial?: boolean;
    min?: boolean;
    max?: boolean;
}

export const getMockManagementForms = ({
    prefix = 'test',
    maxCount = 1000,
    total = true,
    initial = true,
    min = true,
    max = true,
}: GetMockManagementFormsOptions) => `
    ${total ? `<input type="hidden" name="${prefix}-TOTAL_FORMS" value="0" id="id_${prefix}-TOTAL_FORMS" />` : ''}
    ${initial ? `<input type="hidden" name="${prefix}-INITIAL_FORMS" value="0" id="id_${prefix}-INITIAL_FORMS" />` : ''}
    ${min ? `<input type="hidden" name="${prefix}-MIN_NUM_FORMS" value="0" id="id_${prefix}-MIN_NUM_FORMS" />` : ''}
    ${max ? `<input type="hidden" name="${prefix}-MAX_NUM_FORMS" value="${maxCount}" id="id_${prefix}-MAX_NUM_FORMS" />` : ''}
`;

export interface GetMockImageItemOptions {
    canDelete?: boolean;
    prefix?: string;
    index?: number;
    image: string | null;
}

export const getMockImageItem = ({
    prefix = 'test',
    index = 0,
    canDelete = true,
    image,
}: GetMockImageItemOptions) => `
<div
    class="${image ? 'inline-related has_original' : 'inline-related empty-form last-related'}" id="${prefix}-${index}"
    ${canDelete ? ' data-candelete="true" ' : ''}
>
    ${image ? `<fieldset class="module aligned ">
        <div class="form-row field-image">
            <div>
                <label class="required" for="id_${prefix}-${index}-image">Image:</label>
                <p class="file-upload">
                    Currently: <a href="${image}">${image}</a><br>Change:
                    <input type="file" name="${prefix}-${index}-image" accept="image/*" id="id_${prefix}-${index}-image" />
                </p>
            </div>
        </div>
    </fieldset>` : `<fieldset class="module aligned ">
        <div class="form-row field-image">
            <div>
                <label class="required" for="id_${prefix}-__prefix__-image">Image:</label>
                <input type="file" name="${prefix}-__prefix__-image" accept="image/*" id="id_${prefix}-__prefix__-image" />
            </div>
        </div>
    </fieldset>`}
    ${canDelete ? `<input type="checkbox" name="${prefix}-${index}-DELETE" id="id_${prefix}-${index}-DELETE" />` : ''}
    <input type="hidden" name="${prefix}-${index}-id" value="1" id="id_${prefix}-${index}-id" />
    <input type="hidden" name="${prefix}-${index}-example" value="1" id="id_${prefix}-${index}-example"/>
</div>
`;
