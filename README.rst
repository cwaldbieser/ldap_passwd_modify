###########################
 LDAP Password Modify Tool
###########################

Used to test the LDAP password change extended control. Can BIND as a
user and attempt to change that user's password. Can BIND as an admin
user and attempt to change a different user's password. Can test a BIND
against an arbitrary user.

**********
 Examples
**********

Test a password:

.. code:: shell

   $ ./.venv/bin/python3 ./passwd_modify.py --host ldap.example.org -P 389 --start-tls -t uid=johnsmith,ou=people,dc=example,dc=org
   Current Password:
   [D 250811 11:38:10 passwd_modify:32] BIND DN >>uid=johnsmith,ou=people,dc=example,dc=org<<
   [D 250811 11:38:10 passwd_modify:33] BIND password >>secret-password<<
   [D 250811 11:38:11 passwd_modify:94] LDAP Client: TLS established.
   [D 250811 11:38:11 passwd_modify:95] Attempting to BIND to LDAP ...
   [D 250811 11:38:11 passwd_modify:98] LDAP Client: Successful BIND as 'uid=johnsmith,ou=people,dc=example,dc=org'.
   BIND for DN 'uid=johnsmith,ou=people,dc=example,dc=org' was successful.

BIND as an admin entry and modify the password or a user entry:

.. code:: shell

   $ ./.venv/bin/python3 ./passwd_modify.py --host ldap.example.org -P 389 --start-tls \
   > -b cn=root,dc=example,dc=org -p ~/openldap/root.passwd uid=johnsmith,ou=people,dc=example,dc=org
   Current Password:
   New Password:
   [D 250811 11:44:19 passwd_modify:35] BIND DN >>cn=root,dc=example,dc=org<<
   [D 250811 11:44:19 passwd_modify:36] BIND password >><<
   [D 250811 11:44:20 passwd_modify:97] LDAP Client: TLS established.
   [D 250811 11:44:20 passwd_modify:98] Attempting to BIND to LDAP ...
   [D 250811 11:44:20 passwd_modify:101] LDAP Client: Successful BIND as 'cn=root,dc=example,dc=org'.
   Result for password change: True
   LDAP result: {'result': 0, 'description': 'success', 'dn': '', 'message': '', 'referrals': None, 'responseName': None, 'responseValue': None, 'type': 'extendedResp', 'new_password': True}
   new password: >>new-password<<

Change password as a user entry. Requires knowing current password for
user entry:

.. code:: shell

   $ ./.venv/bin/python3 ./passwd_modify.py --host ldap.example.org -P 389 --start-tls uid=johnsmith,ou=people,dc=example,dc=org
   Current Password:
   New Password:
   [D 250811 11:48:30 passwd_modify:35] BIND DN >>uid=johnsmith,ou=people,dc=example,dc=org<<
   [D 250811 11:48:30 passwd_modify:36] BIND password >>secret-password<<
   [D 250811 11:48:31 passwd_modify:97] LDAP Client: TLS established.
   [D 250811 11:48:31 passwd_modify:98] Attempting to BIND to LDAP ...
   [D 250811 11:48:31 passwd_modify:101] LDAP Client: Successful BIND as 'uid=johnsmith,ou=people,dc=example,dc=org'.
   Result for password change: True
   LDAP result: {'result': 0, 'description': 'success', 'dn': '', 'message': '', 'referrals': None, 'responseName': None, 'responseValue': None, 'type': 'extendedResp', 'new_password': True}
   new password: >>new-password<<
