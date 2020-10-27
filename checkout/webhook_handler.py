from django.http import HttpResponse


class Stripe_WebHook_Handler:
    """ Handle stripe webhooks """

    def __init__(self, request):
        self.request = request

    def handle_payment_intent_succeeded(self, event):
        """ Handle Stripes payment intent succeeded webhook """
        intent = event.data.object
        print(intent)
        return HttpResponse(content=f'Webhook recieved: {event["type"]}',
                            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """ Handle Stripes payment intent payment failed webhook """
        return HttpResponse(content=f'Webhook recieved: {event["type"]}',
                            status=200)

    def handle_webhook(self, event):
        """ Handle Stripes unknown webhook """
        return HttpResponse(content=f'Unknown Webhook recieved: \
                            {event["type"]}', status=200)
