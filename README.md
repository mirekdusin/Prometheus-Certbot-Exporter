Prometheus Certbot Exporter
===========================

[![CodeFactor](https://www.codefactor.io/repository/github/mirekdusin/prometheus-certbot-exporter/badge/main)](https://www.codefactor.io/repository/github/mirekdusin/prometheus-certbot-exporter/overview/main)

[![Dependencies](https://img.shields.io/badge/dependencies-cryptography-blue)](https://pypi.org/project/cryptography/)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Prometheus Certbot Exporter is a simple Python metrics exporter that collects metrics from Certbot SSL/TLS certificates. The exporter uses the cryptography library to parse certificates and calculate the days until expiration.

* * * * *

Metrics
-------

The Prometheus Certbot Exporter exposes the following metrics for each SSL/TLS certificate:

-   `certbot_certificate_expiration`: Days until certificate expiration.
-   `certbot_certificate_expiration_date`: Exact date and time of expiration of Certbot certificate.

Each metric is labeled with the `certificate_name`.

Installation
------------

To install Prometheus Certbot Exporter you need to perform the following steps:

      git clone https://github.com/mirekdusin/prometheus-certbot-exporter.git /opt/certbot-exporter

### Requirements

      cryptography

## Configuration

The Prometheus Certbot Exporter can be configured using a YAML file. The default configuration file is located at `/opt/certbot-exporter/src/config.yml`.
You can customize the configuration by creating your own YAML file and passing the path to the file when you start the exporter using -c or --config argument.

The following parameters can be set in the configuration file:

-   `ip`: the IP address or hostname that the exporter should bind to (default: "localhost")
-   `port`: the port number that the exporter should listen on (default: 9099)
-   `tls_cert`: the path to the TLS/SSL certificate file for the exporter (optional)
-   `tls_key`: the path to the TLS/SSL private key file for the exporter (optional)
-   `config_dir`: the path to the Certbot certificates firectory (default: "/etc/letsencrypt/live")


## Usage

You can run Prometheus Certbot Exporter by executing the `main.py` file:

       sudo python3 main.py [-c </path/to/config.yml>]


## Running as a Systemd Service

You can run Prometheus Certbot Exporter as systemd service. Example:

      [Unit]
      Description=Prometheus Certbot Exporter
      After=network.target

      [Service]
      User=root
      Group=root
      Type=simple
      WorkingDirectory=/opt/certbot-exporter/
      ExecStart=python3 /opt/certbot-exporter/main.py
      Restart=always

      [Install]
      WantedBy=multi-user.target

For security reasons, it's a good idea to configure your firewall so that only the Prometheus server can access the exporter metrics. You can do this by adding a rule to your firewall that only allows incoming traffic on port 9099 from the IP address of your Prometheus server. This will prevent others from accessing the exporter metrics.

## License

This application is released under the MIT License.

## Contributing

If you have any suggestions, bug reports, or feature requests, please create an issue or submit a pull request.
