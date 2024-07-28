from weasyprint import HTML

from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

def generate_and_send_order_pdf(order_context, order_id, user_email, customer_first_name, customer_last_name):
    try:
        html_string = render_to_string("payment/order_pdf.html", order_context)
        html = HTML(string=html_string)
        pdf = html.write_pdf()

        if pdf is None:
            print("No PDF to send")
            return None

        subject = f"Order Confirmation - Order #{order_id}"
        body_html = render_to_string(
            "payment/order_confirmation_email.html",
            {"customer": f"{customer_first_name} {customer_last_name}"}
        )

        email = EmailMessage(
            subject,
            body_html,
            settings.EMAIL_HOST_USER,
            [user_email]
        )
        email.content_subtype = "html"
        pdf_filename = f"order_{order_id}.pdf"
        email.attach(pdf_filename, pdf, 'application/pdf')
        email.send()

    except Exception as e:
        print(f"Error: {e}")
        return None
'''
from weasyprint import HTML
from celery import shared_task

import logging

from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

from accounts.models import CartItems, Order


logger = logging.getLogger(__name__)


@shared_task
def generate_order_pdf(order_context):
    try:
        order = Order.objects.get(id=order_context["order_id"])
        cart_items = CartItems.objects.filter(id__in=order_context["cart_items_ids"])
        order_context["order"] = order
        order_context["cart_items"] = cart_items
        html_string = render_to_string("payment/order_pdf.html", order_context)
        html = HTML(string=html_string)
        pdf = html.write_pdf()

        return pdf
    except Exception as e:
        logger.error(f"Error generating PDF {e}", exc_info=True)
        return None


@shared_task
def send_order_pdf_email(
    order_id, user_email, customer_first_name, customer_last_name, order_pdf
):
    if order_pdf is None:
        print("PDF not found")
        return None

    try:
        subject = f"Order Confirmation - Order #{order_id}"
        body = render_to_string(
            "payment/order_confirmation_email.txt",
            {"customer": f"{customer_first_name} {customer_last_name}"},
        )
        email = EmailMessage(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [user_email],
        )
        email.attach(f"order_{order_id}.pdf", order_pdf, "application/pdf")
        email.send()
    except Exception as e:
        logger.error(f"Error sending email {e}", exc_info=True)
        return None

        
@shared_task
def generate_and_send_order_pdf(
    order_context, user_email, customer_first_name, customer_last_name
):
    try:
        logger.error("Task started: generate_and_send_order_pdf")

        order = Order.objects.get(id=order_context.pop("order_id"))
        cart_items = CartItems.objects.filter(
            id__in=order_context.pop("cart_items_ids")
        )
        order_context["order"] = order
        order_context["cart_items"] = cart_items

        logger.error(f"Fetched order and cart items for order #{order.id}")

        html_string = render_to_string("payment/order_pdf.html", order_context)
        html = HTML(string=html_string)
        pdf = html.write_pdf()

        if pdf:
            logger.error(f"Generated PDF for order #{order.id}")

            subject = f"Order Confirmation - Order #{order.id}"
            body_html = render_to_string(
                "payment/order_confirmation_email.html",
                {"customer": f"{customer_first_name} {customer_last_name}"},
            )

            email = EmailMessage(
                subject, body_html, settings.EMAIL_HOST_USER, [user_email]
            )
            email.content_subtype = "html"

            pdf_filename = f"order_{order.id}.pdf"
            email.attach(pdf_filename, pdf, "application/pdf")

            email.send()
            logger.error(f"Email sent to {user_email} with order PDF")
        else:
            logger.error(f"Failed to generate PDF for order #{order.id}")
    except Exception as e:
        logger.error(f"Error in generating and sending order PDF: {e}", exc_info=True)

        
'''