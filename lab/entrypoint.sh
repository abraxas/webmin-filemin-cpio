#!/usr/bin/env bash
set -euo pipefail

JAIL=/lab/jail
LIMITED_USER=fileuser
LIMITED_PASS=filepass
USERS_FILE=/etc/webmin/miniserv.users
ACL_FILE=/etc/webmin/webmin.acl
MODULE_ACL=/etc/webmin/filemin/${LIMITED_USER}.acl
DEFAULT_ACL=/usr/share/webmin/filemin/defaultacl
TARGET=/tmp/WEBMIN-H10-CPIO-WRITE

export DEBIAN_FRONTEND=noninteractive

need_tools=0
command -v rpm2cpio >/dev/null 2>&1 || need_tools=1
command -v cpio >/dev/null 2>&1 || need_tools=1
perl -MFile::MimeInfo -e 1 >/dev/null 2>&1 || need_tools=1
if [[ "${need_tools}" == 1 ]]; then
  apt-get update
  if ! apt-get install -y --no-install-recommends cpio libfile-mimeinfo-perl rpm; then
    apt-get install -y --no-install-recommends cpio libfile-mimeinfo-perl rpm2cpio
  fi
fi
command -v rpm2cpio >/dev/null
command -v cpio >/dev/null
perl -MFile::MimeInfo -e 1

mkdir -p "${JAIL}"
chmod 755 "${JAIL}"
rm -f "${TARGET}" "${JAIL}/h10.rpm"
rm -rf "${JAIL}/h10"

hash="$(perl -e 'print crypt($ARGV[0], q($6$).$ARGV[1])' "${LIMITED_PASS}" "webminh10")"
if ! grep -q "^${LIMITED_USER}:" "${USERS_FILE}"; then
  printf '%s:%s:0\n' "${LIMITED_USER}" "${hash}" >>"${USERS_FILE}"
fi
chmod 600 "${USERS_FILE}"
perl -e 'crypt($ARGV[0], $ARGV[1]) eq $ARGV[1] or die "crypt-mismatch"' \
  "${LIMITED_PASS}" "${hash}"

if ! grep -q "^${LIMITED_USER}:" "${ACL_FILE}"; then
  echo "${LIMITED_USER}: filemin" >>"${ACL_FILE}"
fi
chmod 600 "${ACL_FILE}"

mkdir -p /etc/webmin/filemin
{
  grep -v -E '^(allowed_paths|work_as_root)=' "${DEFAULT_ACL}" || true
  echo "allowed_paths=${JAIL}"
  echo "work_as_root=1"
} >"${MODULE_ACL}"
chmod 600 "${MODULE_ACL}"

exec /usr/bin/perl /usr/share/webmin/miniserv.pl --nofork /etc/webmin/miniserv.conf
