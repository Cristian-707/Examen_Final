from odoo import api, fields, models
from odoo.exceptions import ValidationError


class UnicahPrestamoEquipo(models.Model):
    _name = "unicah.prestamo.equipo"
    _description = "Préstamo de equipo UNICAH"

    name = fields.Char(string="Código / Motivo", required=True)
    solicitante_id = fields.Many2one("res.partner", string="Solicitante", required=True)
    equipo = fields.Selection([
        ("proyector", "Proyector Multimedia"),
        ("laptop", "Laptop Institucional"),
        ("camara", "Cámara Fotográfica / Video"),
        ("sonido", "Kit de Sonido y Micrófonos"),
    ], string="Equipo solicitado", required=True)
    fecha_prestamo = fields.Date(string="Fecha de entrega", required=True, default=fields.Date.context_today)
    fecha_devolucion = fields.Date(string="Fecha de devolución", required=True)
    dias_prestamo = fields.Integer(string="Días de préstamo", compute="_compute_dias_prestamo", store=True)
    estado = fields.Selection([
        ("borrador", "Solicitado"),
        ("prestado", "En préstamo"),
        ("devuelto", "Devuelto"),
    ], string="Estado", default="borrador", required=True)
    observaciones = fields.Text(string="Observaciones")

    @api.depends("fecha_prestamo", "fecha_devolucion")
    def _compute_dias_prestamo(self):
        for rec in self:
            if rec.fecha_prestamo and rec.fecha_devolucion and rec.fecha_devolucion >= rec.fecha_prestamo:
                rec.dias_prestamo = (rec.fecha_devolucion - rec.fecha_prestamo).days
            else:
                rec.dias_prestamo = 0

    @api.constrains("fecha_prestamo", "fecha_devolucion", "dias_prestamo")
    def _check_fechas_prestamo(self):
        for rec in self:
            if rec.fecha_devolucion < rec.fecha_prestamo:
                raise ValidationError("La fecha de devolución no puede ser anterior a la fecha de entrega.")
            if rec.dias_prestamo > 7:
                raise ValidationError("El préstamo de equipo no puede superar los 7 días.")

    def action_prestar(self):
        for rec in self:
            rec.estado = "prestado"

    def action_devolver(self):
        for rec in self:
            rec.estado = "devuelto"