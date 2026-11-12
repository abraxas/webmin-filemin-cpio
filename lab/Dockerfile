FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive \
    LANG=C \
    WEBMIN_CONFIG=/etc/webmin \
    WEBMIN_VAR=/var/webmin \
    PERLLIB=/usr/share/webmin

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        cpio \
        hostname \
        libfile-mimeinfo-perl \
        libio-pty-perl \
        libnet-ssleay-perl \
        openssl \
        perl \
        rpm \
        shared-mime-info \
        unzip \
    && ln -sf /usr/bin/perl /usr/local/bin/perl \
    && rm -rf /var/lib/apt/lists/*

COPY . /usr/share/webmin
WORKDIR /usr/share/webmin

RUN set -eux; \
    export config_dir=/etc/webmin \
        var_dir=/var/webmin \
        perl=/usr/bin/perl \
        autoos=3 \
        os_type=debian-linux \
        os_version=12 \
        real_os_type="Debian Linux" \
        real_os_version=12 \
        port=10000 \
        login=root \
        password=labroot \
        ssl=0 \
        atboot=0 \
        nostart=1 \
        noportcheck=1; \
    /bin/sh ./setup.sh; \
    test "$(cat /etc/webmin/version)" = "2.670"; \
    grep -q '^ssl=0' /etc/webmin/miniserv.conf; \
    sed -i \
        -e 's/^ipv6=.*/ipv6=0/' \
        -e 's/^ssl_enforce=.*/ssl_enforce=0/' \
        -e 's/^syslog=.*/syslog=0/' \
        /etc/webmin/miniserv.conf; \
    grep -q '^ssl_enforce=0' /etc/webmin/miniserv.conf \
        || echo 'ssl_enforce=0' >> /etc/webmin/miniserv.conf; \
    grep -q '^no_pam=' /etc/webmin/miniserv.conf \
        || echo 'no_pam=1' >> /etc/webmin/miniserv.conf; \
    grep -q '^nofork=' /etc/webmin/miniserv.conf \
        || echo 'nofork=1' >> /etc/webmin/miniserv.conf; \
    mkdir -p /var/mail /var/spool/mail /lab/jail

LABEL version="2.670" \
      git_commit="3a2b2b8671c0669c129f5275b3dd1853106ae02b" \
      webmin.version="2.670" \
      webmin.commit="3a2b2b8671c0669c129f5275b3dd1853106ae02b" \
      webmin.tag="2.670" \
      lab="WEBMIN-H10-FILEMIN-CPIO"

EXPOSE 10000
CMD ["/usr/bin/perl", "/usr/share/webmin/miniserv.pl", "--nofork", "/etc/webmin/miniserv.conf"]
