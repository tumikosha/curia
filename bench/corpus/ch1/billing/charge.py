"""Списание по заказу."""

from gateway.client import charge as gateway_charge


def charge_order(order_id: int, amount: int) -> dict:
    if amount < 0:
        raise ValueError("negative amount")
    return gateway_charge(order_id, amount)
