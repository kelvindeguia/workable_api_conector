/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListController } from "@web/views/list/list_controller";
import { useService } from "@web/core/utils/hooks";

class WorkableListController extends ListController {
    setup() {
        super.setup();
        this.orm = useService("orm");
        this.notification = useService("notification");
    }

    async onSyncFromWorkable() {
        try {
            const result = await this.orm.call(
                "workable.job",
                "action_sync_from_workable",
                [[]]
            );

            if (result?.params) {
                this.notification.add(
                    result.params.message,
                    {
                        title: result.params.title,
                        type: result.params.type || "success",
                    }
                );
            } else {
                this.notification.add(
                    "Sync completed!",
                    { type: "success" }
                );
            }

            await this.model.root.load();

        } catch (error) {
            this.notification.add(
                "Sync failed: " + (error.message || "Unknown error"),
                {
                    type: "danger",
                    title: "Workable Sync Error",
                }
            );
        }
    }
}

WorkableListController.template = "workable_job.WorkableListView";

const workableListView = {
    ...listView,
    Controller: WorkableListController,
};

registry.category("views").add("workable_list_jobs", workableListView);