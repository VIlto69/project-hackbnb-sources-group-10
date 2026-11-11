import os
import re
import stripe

# [D3] Format attendu d'un identifiant de session Checkout Stripe
CHECKOUT_SESSION_ID_FORMAT = re.compile(r'^cs_(test|live)_[A-Za-z0-9]{10,200}$')


def _api_key():
    # [D6] La clé vient uniquement de l'environnement (jamais du code versionné)
    key = os.getenv('STRIPE_API_KEY')
    if not key:
        raise RuntimeError("STRIPE_API_KEY is not set")
    return key


def create_checkout(reference, name, unit_price, quantity, confirmation_secret):
    """
        Create Stripe checkout
        Documentation: https://docs.stripe.com/checkout/quickstart?client=react&lang=python
    """

    stripe.api_key = _api_key()
    origin_host = os.getenv('APP_ORIGIN_HOST')
    return stripe.checkout.Session.create(
        mode='payment',
        success_url=f"{origin_host}/booking/{reference}?checkout_confirmation_secret={confirmation_secret}",
        cancel_url=origin_host,
        # [D4] On attache la référence à la session pour pouvoir la vérifier ensuite
        client_reference_id=reference,
        line_items=[
            {
                'quantity': quantity,
                'price_data': {
                    'currency': 'EUR',
                    'unit_amount': round(unit_price * 100),
                    'product_data': {
                        'name': name,
                    },
                },
            },
        ],
    )


def _check_session_id(checkout_session_id: str):
    # [D3] Validation stricte avant tout appel à Stripe
    if not isinstance(checkout_session_id, str) or not CHECKOUT_SESSION_ID_FORMAT.fullmatch(checkout_session_id):
        raise ValueError("Invalid checkout session ID")


def get_checkout_lines(checkout_session_id):
    """
        [D3] Plus de construction d'URL à la main : on passe par la librairie officielle,
        qui encode l'identifiant, et l'identifiant vient de la base de données.
    """
    _check_session_id(checkout_session_id)
    stripe.api_key = _api_key()
    lines = stripe.checkout.Session.list_line_items(checkout_session_id)
    return [
        {
            "description": line.description,
            "amount_total": line.amount_total,
            "currency": line.currency,
        }
        for line in lines.data
    ]


def is_checkout_paid(checkout_session_id, expected_reference):
    """
        [D4] Vérifie directement auprès de Stripe que la session est bien payée
        et qu'elle correspond à la réservation.
    """
    _check_session_id(checkout_session_id)
    stripe.api_key = _api_key()
    session = stripe.checkout.Session.retrieve(checkout_session_id)
    return session.payment_status == "paid" and session.client_reference_id == expected_reference
