from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    prestamo_equipo_ids = fields.One2many(
        "unicah.prestamo.equipo",
        "solicitante_id",
        string="Préstamos de equipo",
    )
    total_prestamos_equipo = fields.Integer(
        string="Total préstamos",
        compute="_compute_total_prestamos_equipo",
    )

    @api.depends("prestamo_equipo_ids")
    def _compute_total_prestamos_equipo(self):
        for partner in self:
            partner.total_prestamos_equipo = len(partner.prestamo_equipo_ids)