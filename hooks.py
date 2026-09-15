"""Rename leftover XML-IDs from aa_gantt_project_test (and a brief aa_gantt merge)."""

# Same xml id *names* as the old companion, so ir.model.data can be retargeted.
_PROJECT_XMLID_NAMES = (
    "view_project_task_aa_gantt",
    "view_task_form2_aa_gantt_dates",
    "action_view_task_aa_gantt_inject",
    "action_view_task_menu_aa_gantt_inject",
    "action_view_my_task_aa_gantt_inject",
    "act_project_project_2_project_task_all_aa_gantt_inject",
    "project_task_action_sub_task_aa_gantt_inject",
    "action_view_task_from_milestone_aa_gantt_inject",
    "project_milestone_action_view_tasks_aa_gantt_inject",
    "project_task_action_from_partner_aa_gantt_inject",
    "field_project_task__planned_date_begin",
    "field_project_task__aa_gantt_progress",
)


def _move_xmlids(cr, old_module, names=None):
    """Reassign ir.model.data rows to aa_gantt_project_task without dropping records."""
    if names:
        cr.execute(
            """
            UPDATE ir_model_data AS old
               SET module = 'aa_gantt_project_task'
             WHERE old.module = %s
               AND old.name IN %s
               AND NOT EXISTS (
                   SELECT 1 FROM ir_model_data AS neu
                    WHERE neu.module = 'aa_gantt_project_task'
                      AND neu.name = old.name
               )
            """,
            [old_module, tuple(names)],
        )
        cr.execute(
            """
            DELETE FROM ir_model_data
             WHERE module = %s
               AND name IN %s
            """,
            [old_module, tuple(names)],
        )
        return

    cr.execute(
        """
        UPDATE ir_model_data AS old
           SET module = 'aa_gantt_project_task'
         WHERE old.module = %s
           AND NOT EXISTS (
               SELECT 1 FROM ir_model_data AS neu
                WHERE neu.module = 'aa_gantt_project_task'
                  AND neu.name = old.name
           )
        """,
        [old_module],
    )
    cr.execute("DELETE FROM ir_model_data WHERE module = %s", [old_module])


def pre_init_hook(env):
    """Keep planned_date_begin / views when renaming the companion module.

    Do not uninstall aa_gantt_project_test from Apps — that would drop the
    date column. This hook reassigns XML-IDs and marks the old module
    uninstalled in SQL.
    """
    cr = env.cr
    _move_xmlids(cr, "aa_gantt_project_test")
    _move_xmlids(cr, "aa_gantt", _PROJECT_XMLID_NAMES)
    # ir.model.fields.modules is computed in Odoo 18 — not a stored column.
    cr.execute(
        """
        DELETE FROM ir_module_module_dependency
         WHERE name = 'aa_gantt_project_test'
            OR module_id IN (
                SELECT id FROM ir_module_module WHERE name = 'aa_gantt_project_test'
            )
        """
    )
    cr.execute(
        """
        UPDATE ir_module_module
           SET state = 'uninstalled'
         WHERE name = 'aa_gantt_project_test'
           AND state IN ('installed', 'to upgrade', 'to remove')
        """
    )
