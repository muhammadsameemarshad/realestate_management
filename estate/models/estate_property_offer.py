from odoo import api, models, fields, exceptions
from datetime import datetime, timedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    validity = fields.Integer(default=7)
    name = fields.Char(string='Name', required=True)
    price = fields.Float(string="Price", required=True)
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")],
        string="Status",
        required=True,
    )
    partner_id = fields.Many2one(
        "res.partner", string="Partner", required=True, ondelete="restrict"
    )
    property_id = fields.Many2one(
        "estate.property",
        string="Property",
        required=True,
        ondelete="cascade",
        domain="[('state', 'in', ('new', 'offer_received'))]",
    )
    date_deadline = fields.Date(string='Date Deadline')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ], default='draft', string='Offer State')




@api.depends("create_date", "validity")
def _compute_date_deadline(self):
    for offer in self:
        if offer.create_date:
            offer.date_deadline = offer.create_date + timedelta(days=offer.validity)


def _inverse_date_deadline(self):
    for offer in self:
        if offer.create_date and offer.date_deadline:
            offer.validity = (offer.date_deadline - offer.create_date).days
@api.model
def _check_state_transition(self, current_state, target_state):
        valid_transitions = {
            'draft': ['accepted', 'refused'],
            'accepted': [],
            'refused': [],
        }
        return target_state in valid_transitions.get(current_state, [])


def action_accept_offer(self):
        for record in self:
            if record.state != 'draft':
                raise exceptions.UserError("Offer cannot be accepted in its current state.")
            property_id = record.property_id
            if property_id.state != 'draft':
                raise exceptions.UserError("Property is not in a valid state to accept an offer.")
            property_id.buyer_id = record.buyer_id
            property_id.selling_price = record.price
            record.state = 'accepted'




    # @api.model
    # def _check_state_transition(self, current_state, target_state):
    #     valid_transitions = {
    #         'draft': ['canceled', 'sold'],
    #         'canceled': [],
    #         'sold': [],
    #     }
    #     return target_state in valid_transitions.get(current_state, [])

# @api.one
def action_cancel_property(self):
        for record in self:
            if record.state != 'draft':
                raise exceptions.UserError("Property cannot be canceled in its current state.")
            property_id = record.property_id
            if property_id.state != 'new':
                raise exceptions.UserError("Property is not in a valid state to cancel.")
            property_id.state = 'canceled'
            record.state = 'refused'


# @api.one
def action_mark_as_sold(self):
    for record in self:
        if record.state != 'draft':
            raise exceptions.UserError("Property cannot be marked as sold in its current state.")
        property_id = record.property_id
        if property_id.state != 'offer_received':
            raise exceptions.UserError("Property is not in a valid state to mark as sold.")
        property_id.state = 'sold'
        property_id.buyer_id = record.partner_id.id
        property_id.selling_price = record.price
        record.state = 'accepted'

# @api.one
def action_refuse_offer(self):
        for record in self:
            if record.state != 'draft':
                raise exceptions.UserError("Offer cannot be refused in its current state.")
            record.state = 'refused'
