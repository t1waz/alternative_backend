from .services import OrderService
from common.common import SimpleValidator
from django.core.exceptions import ValidationError


def validate_is_already_sended(**kwargs):
    if OrderService().is_board_already_sended(board=kwargs.get('board')):
        raise ValidationError("Already sended")


def validate_is_not_already_sended(**kwargs):
    if not OrderService().is_board_already_sended(board=kwargs.get('board')):
        raise ValidationError("Already sended")


def validate_order(**kwargs):
    if not OrderService().get_order_quantity(board=kwargs.get('board'),
                                             order_id=kwargs.get('order')):
        raise ValidationError("Invalid order")


def validate_order_quantity(**kwargs):
    if not OrderService().valid_order_quantity(board=kwargs.get('board'),
                                               order_id=kwargs.get('order')):
        raise ValidationError("Order full")


def validate_delete_order_quantity(**kwargs):
    if not OrderService().get_order_quantity(board=kwargs.get('board'),
                                             order_id=kwargs.get('order')):
        raise ValidationError("Wrong order")


def validate_board_models(**kwargs):
    pass    # TODO


def validate_board_models_quantity(**kwargs):
    pass    # TODO


class SendedBoardValidation(SimpleValidator):
    validators = (validate_is_already_sended,
                  validate_order,
                  validate_order_quantity)


class DeleteSendedValidation(SimpleValidator):
    validators = (validate_is_not_already_sended,
                  validate_delete_order_quantity)


class OrderValidation(SimpleValidator):
    validators = (validate_board_models,
                  validate_board_models_quantity)
