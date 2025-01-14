''' Middleware for our views'''


class CaptureUserDetailsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        
        # --- get executed before the responses is been executed
        # Capture IP address
        ip = self.get_client_ip(request)
        if not hasattr(request, 'client_ip'):
            request.client_ip = ip

        # Ensure session key exists
        if not hasattr(request, 'session_key'):
            request.session_key = request.session.session_key
            if not request.session_key:  # If session does not exist, create it
                request.session.create()

        # Proceed with request processing
        response = self.get_response(request)

        # --- get executed after the responses is been executed

        return response

    def get_client_ip(self, request):
        """Extract the client's IP address from the request headers."""
        x_forwarded_for = request.META.get(
            'HTTP_X_FORWARDED_FOR')  # For proxied requests
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]  # Use the first IP in the list
        else:
            # Default IP address from request
            ip = request.META.get('REMOTE_ADDR')
        return ip
