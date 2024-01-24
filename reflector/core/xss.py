from .vuln import Vuln


class XSS(Vuln):
    def generate_payloads(self):
        ctx = {
            '<script>alert()</script>': '<script>alert()</script>'
        }

        return ctx