#! /usr/bin/env python

import argparse
import getpass
from contextlib import contextmanager

import ldap3
from ldap3 import HASHED_SALTED_SHA512
from logzero import logger


class LDAPBindError(Exception):
    """
    LDAP BIND Error
    """


def main(args):
    """
    Change LDAP password.
    """
    ldap_host = args.host
    ldap_port = args.port
    target_dn = args.dn
    start_tls = args.start_tls
    bind_dn = target_dn
    if args.bind_dn:
        bind_dn = args.bind_dn
    curr_passwd = getpass.getpass("Current Password: ").strip()
    new_passwd = getpass.getpass("New Password: ").strip()
    bind_passwd = curr_passwd
    logger.debug(f"BIND DN >>{bind_dn}<<")
    logger.debug(f"BIND password >>{bind_passwd}<<")
    if args.passwd_file is not None:
        bind_passwd = args.passwd_file.read().strip()
    with connect_to_ldap(
        ldap_host, bind_dn, bind_passwd, start_tls=start_tls, ldap_port=ldap_port
    ) as ldap:
        if args.test_bind:
            print(f"BIND for DN '{bind_dn}' was successful.")
            return
        kwds = {}
        if args.algorithm == "sha512":
            kwds["hash_algorithm"] = HASHED_SALTED_SHA512
        result = ldap.extend.standard.modify_password(
            user=target_dn,
            new_password=new_passwd,
            **kwds,
        )
    print(f"Result for password change: {result}")
    print(f"LDAP result: {ldap.result}")
    print(f"new password: >>{new_passwd}<<")


@contextmanager
def connect_to_ldap(
    ldap_host, ldap_bind_dn, ldap_bind_passwd, start_tls=False, ldap_port=1389
):
    """
    Context manager provides a LDAP connection.

    :returns: LDAP connection, ready to use.
    """
    conn = connect_to_ldap_impl__(
        ldap_host, ldap_bind_dn, ldap_bind_passwd, start_tls, ldap_port
    )
    try:
        yield conn
    finally:
        try:
            conn.unbind()
        finally:
            pass


def connect_to_ldap_impl__(
    ldap_host, ldap_bind_dn, ldap_bind_passwd, start_tls, ldap_port
):
    """
    Connect and BIND to LDAP.
    The connection and BIND configuration is taken from environment variables.

    :returns: An LDAP connection ready to use.
    """
    server = ldap3.Server(ldap_host, port=ldap_port, get_info=ldap3.SCHEMA)
    conn = ldap3.Connection(
        server,
        user=ldap_bind_dn,
        password=ldap_bind_passwd,
        check_names=False,
    )
    if start_tls:
        conn.start_tls()
        logger.debug("LDAP Client: TLS established.")
    logger.debug("Attempting to BIND to LDAP ...")
    if not conn.bind():
        raise LDAPBindError(f"Error BINDing to LDAP directory: {conn.result}")
    logger.debug(f"LDAP Client: Successful BIND as '{ldap_bind_dn}'.")
    return conn


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Change LDAP password")
    parser.add_argument("--host", default="localhost", action="store", help="LDAP host")
    parser.add_argument(
        "-P", "--port", default=1389, type=int, action="store", help="LDAP port"
    )
    parser.add_argument(
        "--start-tls", action="store_true", help="Use StartTLS over LDAP before BIND."
    )
    parser.add_argument("dn", action="store", help="The DN of the entry to update.")
    parser.add_argument(
        "-b", "--bind-dn", action="store", help="The DN of the entry to BIND as."
    )
    parser.add_argument(
        "-p",
        "--passwd-file",
        action="store",
        type=argparse.FileType("r"),
        help="File containing the BIND password.",
    )
    parser.add_argument(
        "-t",
        "--test-bind",
        action="store_true",
        help="Test BIND only-- don't change password.",
    )
    parser.add_argument(
        "-a",
        "--algorithm",
        default="cleartext",
        choices=["cleartext", "sha512"],
        help="Hashing algorithm to use.",
    )
    cli_args = parser.parse_args()
    main(cli_args)
