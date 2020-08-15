#!/usr/bin/env python3

# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "LICENSE.txt" file accompanying this file.
# This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, express or implied. See the License for the
# specific language governing permissions and # limitations under the License.
import re
import subprocess as sub
import webbrowser
import time
import sys
import getopt
import getpass
import argparse
import platform


DCV_CONNECT_SCRIPT = "/usr/libexec/dcvcddconnect.sh"
VERSION = "0.0.3"


class DCVConnectionError(Exception):
    """Error raised with DCV connection fails."""

    pass


def _check_command_output(cmd):
    return sub.check_output(cmd, shell=True, universal_newlines=True, stderr=sub.STDOUT).strip()


def error(message, fail_on_error=True):
    """Print an error message and Raise SystemExit exception to the stderr if fail_on_error is true."""
    if fail_on_error:
        sys.exit("ERROR: {0}".format(message))
    else:
        print("ERROR: {0}".format(message))


def warn(message):
    """Print a warning message."""
    print("WARNING: {0}".format(message))


def check_version(server_version):
    """Compare the script version with the provided version, if it's lower print a warning."""
    server_version_list = server_version.split(".")
    current_version_list = VERSION.split(".")
    server = (server_version_list[0], server_version_list[1], server_version_list[2])
    current = (current_version_list[0], current_version_list[1], current_version_list[2])
    if server > current:
        warn("You are running an out of date version of this script. Local version: {0}, server version: {1}\nPlease download again the client.\n"
             .format(VERSION, server_version))


def retry(func, func_args, attempts=1, wait=0):
    """
    Call function and re-execute it if it raises an Exception.
    :param func: the function to execute.
    :param func_args: the positional arguments of the function.
    :param attempts: the maximum number of attempts. Default: 1.
    :param wait: delay between attempts. Default: 0.
    :returns: the result of the function.
    """
    while attempts:
        try:
            return func(*func_args)
        except Exception as e:
            attempts -= 1
            if not attempts:
                raise e

            print("{0}, retrying in {1} seconds..".format(e, wait))
            time.sleep(wait)


def _parse_args():
    """Parse command line arguments."""
    current_user = getpass.getuser()

    parser = argparse.ArgumentParser(
        description="Connects to a remote DCV Cloud Developer Desktop",
        usage="dcv-cdd.py <command> <instance> [-u/--user] [-w/--web]\n" +
              "                                       [-n/--native] [-p/--path]\n" +
              "       Try 'dcv-cdd.py --help' for more details")

    # Command argumet (mandatory)
    parser.add_argument("command", type=str,
                        choices=["connect", "create-session", "close-session"],
                        help="Command to be executed remotely.")
    parser.add_argument("instance", type=str,
                        help="The instance address where you want to connect")

    # Optional group - mutual exclusive choice about client
    group_client = parser.add_mutually_exclusive_group()
    group_native = group_client.add_mutually_exclusive_group()
    group_native.add_argument("-n", "--native", action="store_true",
                              help="Use the native client. Search the dcvviewer in path or in the standar path")
    group_native.add_argument("-p", "--path", type=str,
                              metavar="dcvviewer_path",
                              help="Use the native client. Pass the path of client executable dcvviewer")
    group_client.add_argument("-w", "--web", action="store_true",
                              help="Use the web client (calls the default browser)")

    # Other optional arguments
    parser.add_argument("-u", "--user", type=str,
                        default=current_user,
                        help="The username for the connection (default: {0})".format(current_user))

    # Version
    parser.add_argument("--version", action="version",
                        version="{prog}s {version}".format(prog="%(prog)", version=VERSION))

    args, unknown = parser.parse_known_args()
    if args.path:
        args.native = True

    if unknown:
        if unknown[0] == '--':
            args.native_params = unknown[1:]
        else:
            args.native_params = unknown
    else:
        args.native_params = ['']

    return args


def _use_web_client(cmd, instance):
    """
    Starts the connection with the web client and default browser.
    :param cmd: ssh command line
    :param instance: instance address
    """
    try:
        url = retry(_retrieve_dcv_session_url, func_args=[cmd, instance], attempts=4)
        url_message = "Please use the following one-time URL in your browser within 30 seconds:\n{0}".format(url)
    except DCVConnectionError as e:
        error(
             "Something went wrong during DCV connection.\n{0}".format(e)
        )

    try:
        if not webbrowser.open_new(url):
            raise webbrowser.Error("Unable to open the Web browser.")
    except webbrowser.Error as e:
        print("{0}\n{1}".format(e, url_message))


def _get_native_default_path():
    try:
        # Check if dcvviewer is in the path
        path = "dcvviewer"
        cmd = path + " --version"
        sub.check_output(cmd, shell=True, stderr=sub.STDOUT)
    except sub.CalledProcessError:
        # Check if it is in a standard location
        local_sys = platform.system()

        if local_sys == "Windows":
            path = "\"C:\\Program Files (x86)\\NICE\\DCV\\Client\\bin\\dcvviewer.exe\""
        elif local_sys == "Linux":
            path = "/usr/bin/dcvviewer"
        elif local_sys == "Darwin":
            # Mac OsX
            path = "/Applications/DCV\\ Viewer.app/Contents/MacOS/dcvviewer"
        else:
            path = None

        if path:
            try:
                cmd = path + " --version"
                sub.check_output(cmd, shell=True, stderr=sub.STDOUT)
            except sub.CalledProcessError:
                path = None

    return path


def _use_native_client_path(cmd, instance, path, client_params=['']):
    """
    Starts the connection with the native client in the
    default location. It can exit (on error) or not.
    :param cmd: ssh command line
    :param instance: instance address
    :param path: the path where the dcvviewer file is
    """
    try:
        params = retry(_retrieve_dcv_native_params,
                       func_args=[cmd, instance],
                       attempts=4).split()
    except DCVConnectionError as e:
        error(
             "Something went wrong during DCV connection.\n" +
             "Error: {0}".format(e)
        )

    try:
        cmd = "{0} {1} {2}".format(path, ' '.join(client_params), ' '.join(params))
        sub.check_call(cmd, shell=True, stderr=sub.STDOUT)
    except sub.CalledProcessError as e:
        error("Issue in executing the {0} client.\n".format(path) +
              "Error: {0}".format(e.output))


def dcv_connect(args):
    """
    Execute cloud developer desktop dcv connect command.
    :param args: options for the command
    """

    # Prepare ssh command to execute in the master instance
    cmd = 'ssh {USER}@{INSTANCE} "{REMOTE_COMMAND} {DCV_COMMAND}"'.format(
        USER=args.user,
        INSTANCE=args.instance,
        REMOTE_COMMAND=DCV_CONNECT_SCRIPT,
        DCV_COMMAND=args.command
    )

    if args.command == "connect":
        if args.web and not args.native:
            # The use of only the web client was selected
            _use_web_client(cmd, args.instance)
        elif not args.web and args.native:
            # The use of only the native client was selected
            if args.path:
                _use_native_client_path(cmd, args.instance, args.path, args.native_params)
            else:
                path = _get_native_default_path()
                if path:
                    _use_native_client_path(cmd, args.instance, path, args.native_params)
                else:
                    error("No native client found.\n" +
                          "Try specifing a path with -p option or using the web client.")
        else:
            # Try to connect using the native client, and then the web client
            path = _get_native_default_path()
            if path:
                _use_native_client_path(cmd, args.instance, path, args.native_params)
            else:
                print("No DCV native client found. Using the web client.")
                _use_web_client(cmd, args.instance)
    else:
        retry(_execute_dcv_session_command, func_args=[cmd], attempts=4)


def _retrieve_dcv_from_ssh(ssh_cmd, instance, native):
    """
    Connect by ssh to the master instance, prepare DCV session
    and return the DCV session URL or native parameters.
    """
    try:
        output = _check_command_output(ssh_cmd)
        # At first ssh connection, the ssh command alerts it is adding the host to the known hosts list
        if re.search("Permanently added .* to the list of known hosts.", output):
            output = _check_command_output(ssh_cmd)

        dcv_parameters = re.search(
            r"DcvServerPort=([\d]+) DcvSessionId=([\w]+) DcvSessionToken=([\w-]+) DcvClientScriptVersion=([\d]+[.][\d]+[.][\d]+)", output
        )
        if dcv_parameters:
            dcv_server_port = dcv_parameters.group(1)
            dcv_session_id = dcv_parameters.group(2)
            dcv_session_token = dcv_parameters.group(3)
            server_script_version = dcv_parameters.group(4)
        else:
            error(
                "Something went wrong during DCV connection. Please manually execute the command:\n{0}\n".format(ssh_cmd)
            )

    except sub.CalledProcessError as e:
        if "{0}: No such file or directory".format(DCV_CONNECT_SCRIPT) in e.output:
            error(
                "Check if the DCV server is installed on your Cloud Developer Desktop"
            )
        else:
            raise DCVConnectionError(e.output)

    check_version(server_script_version)

    if native:
        return "{IP}:{PORT}#{SESSION_ID} --auth-token={TOKEN}".format(
            IP=instance,
            PORT=dcv_server_port,
            SESSION_ID=dcv_session_id,
            TOKEN=dcv_session_token
        )

    # else web
    return "https://{IP}:{PORT}?authToken={TOKEN}#{SESSION_ID}".format(
        IP=instance,
        PORT=dcv_server_port,
        TOKEN=dcv_session_token,
        SESSION_ID=dcv_session_id
    )


def _retrieve_dcv_native_params(ssh_cmd, instance):
    """
    Connect by ssh to the master instance, prepare DCV session and
    return the DCV native parameters.
    """
    return _retrieve_dcv_from_ssh(ssh_cmd, instance, True)


def _retrieve_dcv_session_url(ssh_cmd, instance):
    """
    Connect by ssh to the master instance, prepare DCV session
    and return the DCV session URL.
    """
    return _retrieve_dcv_from_ssh(ssh_cmd, instance, False)


def _execute_dcv_session_command(ssh_cmd):
    """
    Connect by ssh to the master instance, and executes the related command.
    """
    try:
        output = _check_command_output(ssh_cmd)
        # At first ssh connection, the ssh command alerts it is adding the host to the known hosts list
        if re.search("Permanently added .* to the list of known hosts.", output):
            output = _check_command_output(ssh_cmd)

        dcv_parameters = re.search(
            r"DcvClientScriptVersion=([\d]+[.][\d]+[.][\d]+)", output
        )
        if dcv_parameters:
            server_script_version = dcv_parameters.group(1)
        else:
            error(
                "Something went wrong during DCV connection. Please manually execute the command:\n{0}\n".format(ssh_cmd)
            )

        check_version(server_script_version)

        print(output.split("\n")[1])

    except sub.CalledProcessError as e:
        if "{0}: No such file or directory".format(DCV_CONNECT_SCRIPT) in e.output:
            error(
                "Check if the DCV server is installed on your Cloud Developer Desktop"
            )
        else:
            raise DCVConnectionError(e.output)


if __name__ == "__main__":
    args = _parse_args()
    dcv_connect(args)

# ex:ts=4:et:
