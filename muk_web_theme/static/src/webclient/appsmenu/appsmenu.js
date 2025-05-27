/** @odoo-module **/

import { useEffect } from "@odoo/owl";
import { url } from "@web/core/utils/urls";
import { useBus, useService } from "@web/core/utils/hooks";

import { Dropdown } from "@web/core/dropdown/dropdown";

export class AppsMenu extends Dropdown {
	static template = 'muk_web_theme.AppsMenu';
	static props = {
		...Dropdown.props
	};

	switch() {
		let toggled = true
		if(this.state.open == false) {
			toggled = false
		} else {
			toggled = !this.state.open
		}
        return this.changeStateAndNotify({
            open: toggled,
			groupIsOpen: toggled && this.props.autoOpen,
        });
    }
	
	
	setup() {
		super.setup();
		

		useEffect(
			(open) => {
				if (open) {
					const openMainPalette = (ev) => {
						if (
							!this.commandServiceOpen &&
							ev.key.length === 1 &&
							!ev.ctrlKey &&
							!ev.altKey
						) {
							this.commandService.openMainPalette(
								{ searchValue: `/${ev.key}` },
								() => { this.commandPaletteOpen = false; }
							);
							this.commandPaletteOpen = true;
						}
					}
					window.addEventListener("keydown", openMainPalette);
					return () => {
						window.removeEventListener("keydown", openMainPalette);
						this.commandPaletteOpen = false;
					}
				}
			},
			() => [this.state.open]
		);
		useBus(this.env.bus, "ACTION_MANAGER:UI-UPDATED", this.switch);
	}
}
