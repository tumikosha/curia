"""Фоновая задача: построить отчёт и выложить на SFTP партнёра."""

import logging
from datetime import date, timedelta

import paramiko
from celery import Celery

from app.settings import settings
from reports.export import build_xlsx

log = logging.getLogger("returns_report")
celery = Celery("reports", broker=settings.BROKER_URL)


@celery.task(bind=True, max_retries=3, default_retry_delay=600)
def deliver_returns_report(self, day_iso: str | None = None) -> str:
    day = date.fromisoformat(day_iso) if day_iso else date.today() - timedelta(days=1)
    payload = build_xlsx(day)
    name = f"returns_{day.isoformat()}.xlsx"
    try:
        _upload(name, payload)
    except (paramiko.SSHException, OSError) as exc:
        log.warning("sftp upload failed, retry %s: %s", self.request.retries, exc)
        try:
            raise self.retry(exc=exc)
        except self.MaxRetriesExceededError:
            _alert(f"returns report for {day} not delivered after 3 retries: {exc}")
            raise
    log.info("delivered %s (%d bytes)", name, len(payload))
    return name


def _upload(name: str, payload: bytes) -> None:
    transport = paramiko.Transport((settings.ACME_SFTP_HOST, 22))
    transport.connect(username=settings.ACME_SFTP_USER, pkey=settings.acme_sftp_key())
    try:
        sftp = paramiko.SFTPClient.from_transport(transport)
        with sftp.open(f"/incoming/{name}", "wb") as fh:
            fh.write(payload)
    finally:
        transport.close()


def _alert(text: str) -> None:
    from app.slack import post
    post(channel="#ops-alerts", text=text)
