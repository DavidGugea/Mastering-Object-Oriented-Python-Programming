from AuditedClass import AuditedClass


class Table(AuditedClass):
    def bet(self, bet: str, amount: int) -> None:
        self.logger.info(f"Betting {amount} on {bet}")
        self.audit.info(f"Bet:{bet!r}, Amount:{amount!r}")
