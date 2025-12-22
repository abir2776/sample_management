from rest_framework.throttling import SimpleRateThrottle


class SingleAPIViewThrottle(SimpleRateThrottle):
    scope = "single_api"

    def get_cache_key(self, request, view):
        ip = self.get_ident(request)
        return f"single_api_{ip}"
