from odoo import api, fields, models


class ProjectTask(models.Model):
    """Enterprise-aligned planning fields for aa_gantt on Community.

    Odoo Enterprise Project Gantt uses ``planned_date_begin`` as the bar
    start and ``date_deadline`` as the bar end. Community only ships
    ``date_assign`` (set when assignees change — not a true start) and
    ``date_deadline``. This inherit adds the missing begin field and a
    progress percentage suitable for the Gantt bar fill.
    """

    _inherit = "project.task"

    planned_date_begin = fields.Datetime(
        string="Planned Start",
        tracking=True,
        copy=False,
        index=True,
        help="Planned start used by the AA Gantt view "
             "(same role as Enterprise planned_date_begin).",
    )
    aa_gantt_progress = fields.Float(
        string="Gantt Progress",
        compute="_compute_aa_gantt_progress",
        store=False,
        help="0–100 progress shown on the AA Gantt bar. "
             "Closed tasks = 100; otherwise derived from sub-task completion.",
    )

    @api.depends("subtask_completion_percentage", "is_closed")
    def _compute_aa_gantt_progress(self):
        for task in self:
            if task.is_closed:
                task.aa_gantt_progress = 100.0
            else:
                task.aa_gantt_progress = round(
                    (task.subtask_completion_percentage or 0.0) * 100.0, 2
                )

    @api.onchange("planned_date_begin", "date_deadline")
    def _onchange_aa_gantt_planned_dates(self):
        """Keep begin <= deadline when both are set (Enterprise-like sanity)."""
        if (
            self.planned_date_begin
            and self.date_deadline
            and self.planned_date_begin > self.date_deadline
        ):
            self.date_deadline = self.planned_date_begin
