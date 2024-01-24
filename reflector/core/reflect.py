from .vuln import Vuln


class Reflect(Vuln):
    def generate_payloads(self):
        ctx = {
            'fvckh4ck3ron3': 'fvckh4ck3ron3'
        }

        return ctx