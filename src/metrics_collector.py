import datetime
from typing import Tuple

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from fastapi.exceptions import HTTPException
from prometheus_client import Gauge

from .logger import *


class MetricsCollector:
    """
    A class for collecting Certbot certificate metrics and exposing them via Prometheus.
    """

    def __init__(self, config_dir: str) -> None:
        """
        Initializes the MetricsCollector object.

        :param config_dir: The directory where Certbot stores its configuration files.
        """
        self.config_dir = ""
        self.set_config_dir(config_dir)
        self.cert_expiration = Gauge('certbot_certificate_expiration',
                                     'Days to expiration date of Certbot certificate',
                                     ['certificate_name'])
        self.cert_expiration_date = Gauge('certbot_certificate_expiration_date',
                                          'Exact date and time of expiration of Certbot certificate',
                                          ['certificate_name'])

    def set_config_dir(self, config_dir: str) -> None:
        """
        Sets the directory where Certbot stores its configuration files.

        :param config_dir: The directory where Certbot stores its configuration files.
        """
        if not os.path.isdir(config_dir):
            logger.error(f'{config_dir} is not a directory or does not exist')
            raise HTTPException(status_code=500, detail=f'{config_dir} is not a directory or does not exist')

        self.config_dir = config_dir

    def get_certificates(self) -> Tuple:
        """
        Gets a list of Certbot certificates.

        :return: A list of tuples containing the certificate and its path.
        """
        for cert_name in os.listdir(self.config_dir):
            cert_path = os.path.join(self.config_dir, cert_name, "cert.pem")
            if not os.path.isfile(cert_path):
                continue

            with open(cert_path, "rb") as f:
                cert_pem = f.read()

            try:
                cert = x509.load_pem_x509_certificate(cert_pem, default_backend())
                yield cert
            except Exception as e:
                logger.exception(f'Failed to parse certificate {cert_path}: {e}')
                raise HTTPException(status_code=500, detail=f'Failed to parse certificate {cert_path}: {e}')

    @staticmethod
    def get_expiration_date(cert: x509.Certificate) -> datetime.datetime:
        """
        Gets the expiration date of a Certbot certificate.

        :param cert: The certificate to get the expiration date for.
        :return: The expiration date of the certificate.
        """
        not_after = cert.not_valid_after
        return not_after.replace(tzinfo=datetime.timezone.utc)

    def collect_metrics(self) -> None:
        """
        Collects Certbot certificate metrics and updates Prometheus Gauges with the collected values.

        :return: None
        """
        certificates = list(self.get_certificates())
        if not certificates:
            logger.info(f'No certificates found')
            return

        now = datetime.datetime.now(datetime.timezone.utc)
        for cert in certificates:
            exp_date = self.get_expiration_date(cert)
            days_left = (exp_date - now).days
            cert_subject = cert.subject.rfc4514_string().replace("CN=", "")

            try:
                self.cert_expiration.labels(cert_subject).set(days_left)
                self.cert_expiration_date.labels(cert_subject).set(int(exp_date.timestamp()))
            except Exception as e:
                logger.exception(f'Failed to set gauge of {cert_subject}: {e}')
                raise HTTPException(status_code=500, detail=f'Failed to set gauge of {cert_subject}: {e}')
