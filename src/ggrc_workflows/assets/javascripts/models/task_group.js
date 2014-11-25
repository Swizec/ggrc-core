/*!
    Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: dan@reciprocitylabs.com
    Maintained By: dan@reciprocitylabs.com
*/


(function (can) {

  can.Model.Cacheable("CMS.Models.TaskGroup", {
    root_object: "task_group",
    root_collection: "task_groups",
    category: "workflow",
    findAll: "GET /api/task_groups",
    findOne: "GET /api/task_groups/{id}",
    create: "POST /api/task_groups",
    update: "PUT /api/task_groups/{id}",
    destroy: "DELETE /api/task_groups/{id}",

    mixins: ["contactable"],

    attributes: {
      contact : "CMS.Models.Person.stub",
      workflow: "CMS.Models.Workflow.stub",
      task_group_tasks: "CMS.Models.TaskGroupTask.stubs",
      tasks: "CMS.Models.Task.stubs",
      task_group_objects: "CMS.Models.TaskGroupObject.stubs",
      objects: "CMS.Models.get_stubs",
      modified_by: "CMS.Models.Person.stub",
      context: "CMS.Models.Context.stub",
      end_date: "date",
    },

    tree_view_options: {
      sort_property: 'sort_index',
      //show_view: GGRC.mustache_path + "/task_groups/tree.mustache",
      footer_view: GGRC.mustache_path + "/task_groups/tree_footer.mustache"
    },

    init: function () {
      var that = this;
      this._super && this._super.apply(this, arguments);
      this.validateNonBlank("title");
      this.validate(["_transient.contact", "contact"], function (newVal, prop) {
        var contact_exists = this.contact ? true : false;
        var reified_contact = contact_exists ? this.contact.reify() : false;
        var contact_has_email_address = reified_contact ? reified_contact.email : false;

        // This check will not work until the bug introduced with commit 8a5f600c65b7b45fd34bf8a7631961a6d5a19638
        // is resolved.
        if (!contact_has_email_address) {
          return "No valid contact selected for assignee";
        }
      });

      // Refresh workflow people:
      this.bind("created", function (ev, instance) {
        if (instance instanceof that) {
          instance.refresh_all_force('workflow', 'context')
        }
      });
      this.bind("updated", function (ev, instance) {
        if (instance instanceof that) {
          instance.refresh_all_force('workflow', 'context')
        }
      });
    }
  }, {});


  can.Model.Cacheable("CMS.Models.TaskGroupTask", {
    root_object: "task_group_task",
    root_collection: "task_group_tasks",
    findAll: "GET /api/task_group_tasks",
    create: "POST /api/task_group_tasks",
    update: "PUT /api/task_group_tasks/{id}",
    destroy: "DELETE /api/task_group_tasks/{id}",

    mixins : ["contactable"],
    attributes: {
      context: "CMS.Models.Context.stub",
      contact: "CMS.Models.Person.stub",
      modified_by: "CMS.Models.Person.stub",
      task_group: "CMS.Models.TaskGroup.stub",
    },

    init: function () {
      var that = this;
      this._super && this._super.apply(this, arguments);
      this.validateNonBlank("title");
      this.validate([
        "start_date",
        "end_date",
        "relative_end_month",
        "relative_end_day",
        "relative_start_month",
        "relative_start_day"
      ], function (newVal, prop){
        var that = this,
         workflow = GGRC.page_instance(),
         dates_are_valid = true;

        // Handle cases of a workflow with start and end dates
        if (workflow.frequency === 'one_time') {
            dates_are_valid =
                 that.start_date && 0 < that.start_date.length
              && that.end_date && 0 < that.end_date.length;
        }

        if (!dates_are_valid) {
          return "Start and/or end date is invalid";
        }
      });

      this.bind("created", function (ev, instance) {
        if (instance instanceof that) {
          if (instance.task_group.reify().selfLink) {
            instance.task_group.reify().refresh();
            instance._refresh_workflow_people();
          }
        }
      });

      this.bind("updated", function (ev, instance) {
        if (instance instanceof that) {
          instance._refresh_workflow_people();
        }
      });
    }
  }, {
    init : function () {
      this._super && this._super.apply(this, arguments);
      this.bind("task_group", function (ev, newVal) {
        var that = this;
        if (!newVal)
          return;

        newVal = newVal.reify();

        new RefreshQueue().enqueue(newVal).trigger().then(function () {
          var tgt,
              tgts = newVal.task_group_tasks.slice(0);

          do {
            tgt = tgts.splice(tgts.length - 1, 1)[0];
            tgt = tgt && tgt.reify();
          } while (tgt === that);

          if (!tgt)
            return new $.Deferred().reject("no existing task group task");
          else
            return new RefreshQueue().enqueue(tgt).trigger();
        }).then(function (tgts) {
          var tgt = tgts[0];

          can.each(
            ["relative_start_day",
             "relative_start_month",
             "relative_end_day",
             "relative_end_month",
             "start_date",
             "end_date"],
            function (prop) {
              if (tgt[prop] && !that[prop]) {
                that.attr(prop, tgt.attr(prop) instanceof Date ? new Date(tgt[prop]) : tgt[prop]);
              }
            }
          );
        });
      });
    },

    _refresh_workflow_people: function () {
      //  TaskGroupTask assignment may add mappings and role assignments in
      //  the backend, so ensure these changes are reflected.
      var task_group, workflow;
      task_group = this.task_group.reify();
      if (task_group.selfLink) {
        workflow = task_group.workflow.reify();
        return workflow.refresh().then(function (workflow) {
          return workflow.context.reify().refresh();
        });
      }
    },

    response_options_csv: can.compute(function (val) {
      if (val != null) {
        this.attr("response_options", $.map(val.split(","), $.proxy("".trim.call, "".trim)));
      } else {
        return (this.attr("response_options") || []).join(", ");
      }
    })
  });


})(window.can);
