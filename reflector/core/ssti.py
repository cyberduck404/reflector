from .vuln import Vuln


class SSTI(Vuln):
    def generate_payloads(self):
        ctx = {
            '{{7331*1337}}': '9801547',

        }

        return ctx