/** @odoo-module **/

import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";
import { CharField, charField } from '@web/views/fields/char/char_field';
import { useService } from "@web/core/utils/hooks";

export class ClipBoardField extends CharField{
    static props = {
        ...CharField.props
    }
    static template = "bad_tejas_apani.ClipBoardField";
    setup() {
        super.setup();
        this.notification = useService('notification');
    }
    copyIntoClipboard(ev){
        const value = this.props.record.data[this.props.name]
        navigator.clipboard.writeText(value);
        this.notification.add(_t("Text copied"), {
                    type: "info",
                    sticky: false,
                });

    }

}


export const clipBoardField = {
    component : ClipBoardField,
    displayName : _t("ClipBoard Field"),
    supportedTypes : ["char"]

}

registry.category("fields").add("clipboard_field",clipBoardField);