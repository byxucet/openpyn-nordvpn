# -*- coding: utf-8 -*-
import os
import re
from itertools import islice

# CONFIGURATION PLACEHOLDERS
# spaces are intentionally let by the end of the word
SERVER_ADDRESS = 'remote '
CIPHER = 'cipher '
AUTH_DIGEST = 'auth '
TLS_CONTROL_CHANNEL_SECURITY = 'key-direction '
PROTOCOL = 'proto '
TLS_RENEGOTIATION_TIME = 'reneg-sec '
CONNECTION_RETRY = 'resolv-retry '
LOG_VERBOSITY = 'verb '

# TEMPLATE PLACEHOLDERS
T_SERVER_ADDRESS = 'addr'
 # = 'adns'
T_CIPHER = 'cipher'
 # = 'comp'
T_CUSTOM_CONFIGURATION = 'custom2'
T_DESCRIPTION = 'desc'
T_AUTH_DIGEST = 'digest'
T_TLS_CONTROL_CHANNEL_SECURITY = 'hmac'
T_PASSWORD = 'password'
T_PORT = 'port'
T_PROTOCOL = 'proto'
T_TLS_RENEGOTIATION_TIME = 'reneg'
T_CONNECTION_RETRY = 'retry'
 # = 'rgw'
 # = 'unit' ##
 # = 'userauth'
T_USERNAME = 'username'
 # = 'useronly'
 # = 'vpn_upload_unit' ###


class Converter(object):
    _username = None        #: NordVPN username
    _password = None        #: NordVPN password
    _description = None     #: NordVPN description
    _port = None            #: NordVPN port
    _protocol = None        #: NordVPN protocol

    _name = None            #: NordVPN name
    _source_folder = None   #: OpenVPN configuration folder
    _certs_folder = None    #: OpenVPN Certificates configuration folder
    _ca = None              #: NordVPN certificate
    _static = None          #: NordVPN static key

    def __init__(self, debug_mode=False):
        self.debug_mode = debug_mode
        self._extracted_data = {}

    def set_name(self, name):
        """Name for the VPN connection"""
        if not name:
            raise Exception("You have to specify an name.")

        self._name = name

    def set_source_folder(self, source_input):
        """Sets the source configuration folder for the openvpn config files"""
        if not source_input or not os.path.isdir(source_input):
            raise Exception("You have to specify a valid path for the source configuration folder.")

        self._source_folder = source_input

    def set_certs_folder(self, certs_output):
        """Sets the certificates destination folder"""
        if not certs_output or not os.path.isdir(certs_output):
            raise Exception("You have to specify a valid path for the certificates destination folder.")

        self._certs_folder = certs_output

    def set_description(self, description):
        """Description for the VPN connection"""
        if not description:
            raise Exception("You have to specify an description.")

        self._description = description

    def set_password(self, password):
        """Password for the VPN connection"""
        if not password:
            raise Exception("You have to specify an password.")

        self._password = password

    def set_port(self, port):
        """Port for the VPN connection"""
        if not port:
            raise Exception("You have to specify an port.")

        self._port = port

    def set_protocol(self, protocol):
        """Protocol for the VPN connection"""
        if not protocol:
            raise Exception("You have to specify an protocol.")

        self._protocol = protocol

    def set_username(self, username):
        """Username for the VPN connection"""
        if not username:
            raise Exception("You have to specify an username.")

        self._username = username

    def extract_information(self, input_file):
        """Extracts the needed information from the source configuration files"""
        self.pprint("Starting to extract information for {}".format(input_file))

        # input_file_full = os.path.join(self._source_folder, input_file)
        # with open(input_file_full, 'r') as f:
        #     lines = f.readlines()
        #     f.close()
        #
        # data = ""
        # for line in lines:
        #     if not line.startswith("#"):
        #         data = data + line;
        #         self._extract_server_address(line)
        #         self._extract_cipher(line)
        #         self._extract_auth_digest(line)
        #         self._extract_tls_control_channel_security(line)
        #         self._extract_tls_renegotiation_time(line)
        #         self._extract_connection_retry(line)
        #         print(line, end="")

        input_file_full = os.path.join(self._source_folder, input_file)
        with open(input_file_full, 'r') as lines:
            data = ""
            for line in islice(lines, 10):
                pass

            for line in islice(lines, 40):
                if line.startswith("#"):
                    continue;
                #print(line, end="")
                if line.startswith("<ca>"):
                    data = data + line;
                    break
                elif self._extract_server_address(line):
                    pass
                elif self._extract_cipher(line):
                    pass
                elif self._extract_auth_digest(line):
                    pass
                elif self._extract_tls_renegotiation_time(line):
                    pass
                elif self._extract_connection_retry(line):
                    pass

            for line in lines:
                if line.startswith("#"):
                    continue;
                if line.startswith(TLS_CONTROL_CHANNEL_SECURITY):
                    self._extract_tls_control_channel_security(line)
                    continue;
                #print(line, end="")
                data = data + line;
            lines.close()

        #print(data, end="")

        self._extract_vpn_description()
        self._extract_vpn_password()
        self._extract_vpn_port()
        self._extract_vpn_protocol()
        self._extract_vpn_username()

        #self._extract_name(input_file)
        self._extract_certificates(data)

        self.pprint(self._ca)
        self.pprint(self._static)
        self.pprint(self._extracted_data)

        return self._extracted_data

    def _extract_server_address(self, line):
        """Specific extractor for Server Address"""
        if SERVER_ADDRESS in line:
            _, value, _ = line.split()
            self._extracted_data[T_SERVER_ADDRESS] = value
            return True
        return False

    def _extract_cipher(self, line):
        """Specific extractor for Legacy/Fallback Cipher"""
        if CIPHER in line:
            _, value = line.split()
            self._extracted_data[T_CIPHER] = value
            return True
        return False

    def _extract_auth_digest(self, line):
        """Specific extractor for Auth digest"""
        if AUTH_DIGEST in line:
            _, value = line.split()
            self._extracted_data[T_AUTH_DIGEST] = value
            return True
        return False


    def _extract_tls_control_channel_security(self, line):
        """Specific extractor for TLS Control Channel Security"""
        if TLS_CONTROL_CHANNEL_SECURITY in line:
            _, value = line.split()
            self._extracted_data[T_TLS_CONTROL_CHANNEL_SECURITY] = value
            return True
        return False

    def _extract_tls_renegotiation_time(self, line):
        """Specific extractor for TLS Renegotiation Time"""
        if TLS_RENEGOTIATION_TIME in line:
            _, value = line.split()
            self._extracted_data[T_TLS_RENEGOTIATION_TIME] = value
            return True
        return False

    def _extract_connection_retry(self, line):
        """Specific extractor for Connection Retry"""
        if CONNECTION_RETRY in line:
            _, value = line.split()
            if value == "infinite":
                self._extracted_data[T_CONNECTION_RETRY] = "-1"
            else:
                self._extracted_data[T_CONNECTION_RETRY] = value
            return True
        return False


    def _extract_vpn_description(self):
        """Description for the VPN connection"""
        self._extracted_data[T_DESCRIPTION] = self._description

    def _extract_vpn_password(self):
        """Password for the VPN connection"""
        self._extracted_data[T_PASSWORD] = self._password

    def _extract_vpn_port(self):
        """Port for the VPN connection"""
        self._extracted_data[T_PORT] = self._port

    def _extract_vpn_protocol(self):
        """Protocol for the VPN connection"""
        self._extracted_data[T_PROTOCOL] = self._protocol

    def _extract_vpn_username(self):
        """Username for the VPN connection"""
        self._extracted_data[T_USERNAME] = self._username


    def _extract_name(self, input_file):
        """Specific extractor for VPN configuration name"""
        vpn_name = input_file.__str__()
        vpn_name = vpn_name.replace('nordvpn.com.', '').replace('.ovpn', '')

        self._name = vpn_name

    def _extract_certificates(self, input_file):
        # prepare regex
        regex_ca = re.compile("<ca>.(.*).</ca>", re.IGNORECASE|re.DOTALL)
        regex_tls = re.compile("<tls-auth>.(.*).</tls-auth>", re.IGNORECASE|re.DOTALL)

        # extract keys
        match_string = regex_ca.search(input_file)
        if match_string is not None:
            self._ca = match_string.group(1)

        match_string = regex_tls.search(input_file)
        if match_string is not None:
            self._static = match_string.group(1)

    def _write_certificates(self):
        # write keys
        if self._ca is not None:
            cert_name = "vpn_crt_client" + "1" + "_ca"
            cert_file = open(os.path.join(self._certs_folder, cert_name), 'w')
            cert_file.write(self._ca)
            cert_file.close()

        if self._static is not None:
            cert_name = "vpn_crt_client" + "1" + "_static"
            cert_file = open(os.path.join(self._certs_folder, cert_name), 'w')
            cert_file.write(self._static)
            cert_file.close()

    def pprint(self, msg, appmsg=False):
        """
        Generic function to conditionally print messages
        application messages are always printed out
        debug messages are printed out based on the value of debugMode flag
        """
        if appmsg:
            print(msg)
            return

        if self.debug_mode:
            print(msg)
