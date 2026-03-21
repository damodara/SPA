import stripe
from django.conf import settings


def get_stripe_api_key() -> str:
    api_key = getattr(settings, "STRIPE_SECRET_KEY", None)
    if not api_key:
        raise RuntimeError(
            "STRIPE_SECRET_KEY не задан в настройках. "
            "Добавьте его в .env и config.settings."
        )
    return api_key


def create_stripe_product(name: str) -> str:
    """
    Создание продукта в Stripe.

    Возвращает id созданного продукта.
    """
    stripe.api_key = get_stripe_api_key()

    product = stripe.Product.create(name=name)
    return product["id"]


def create_stripe_price(product_id: str, amount_rub: int, currency: str = "rub") -> str:
    """
    Создание цены в Stripe.

    amount_rub — сумма в рублях, Stripe ожидает сумму в копейках.
    Возвращает id созданной цены.
    """
    stripe.api_key = get_stripe_api_key()

    unit_amount = amount_rub * 100
    price = stripe.Price.create(
        product=product_id,
        unit_amount=unit_amount,
        currency=currency,
    )
    return price["id"]


def create_stripe_checkout_session(
    price_id: str, success_url: str, cancel_url: str
) -> dict:
    """
    Создание checkout-сессии Stripe для получения ссылки на оплату.

    Возвращает словарь с полями:
        - id: id сессии
        - url: ссылка на оплату
    """
    stripe.api_key = get_stripe_api_key()

    session = stripe.checkout.Session.create(
        success_url=success_url,
        cancel_url=cancel_url,
        mode="payment",
        line_items=[
            {
                "price": price_id,
                "quantity": 1,
            }
        ],
    )
    return {"id": session["id"], "url": session["url"]}
