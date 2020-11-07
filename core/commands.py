from enum import Enum


class Commands(Enum):
    CMD = "CMD"
    SEND_PDF_FILE = "SEND_PDF_FILE"
    SEND_FILE = "SEND_FILE"

    SETUP_CLIENT = "SETUP_CLIENT"
    DECODE_TYPE = "DECODE_TYPE"

    START_DECRYPT = "START_DECRYPT"
    STOP_DECRYPT = "STOP_DECRYPT"

    COUNT_OF_CLIENTS = "COUNT_OF_CLIENTS"
    CURRENT_CLIENT = "CURRENT_CLIENT"

    DICTIONARY = "DICTIONARY"
    DICTIONARY_PATH = "DICTIONARY_PATH"

    BRUTE_FORCE = "BRUTE_FORCE"
    BRUTE_FORCE_REGEX = "BRUTE_FORCE_REGEX"
    BRUTE_FORCE_MIN = "BRUTE_FORCE_MIN"
    BRUTE_FORCE_MAX = "BRUTE_FORCE_MAX"

    FOUND_PASSWORD = "FOUND_PASSWORD"
    NOT_FOUND_PASSWORD = "NOT_FOUND_PASSWORD"

    @staticmethod
    def create_command(*args):
        cmd = Commands.CMD.value + ":"
        for command in args:
            if isinstance(command, tuple):
                for x in command:
                    cmd += Commands._append_cmd(x)
            else:
                cmd += Commands._append_cmd(command)

        return cmd.strip(':')

    @staticmethod
    def _append_cmd(val):
        try:
            ret = val.value
        except AttributeError:
            ret = str(val)
        ret += ":"
        return ret


    @staticmethod
    def get_value(received_command: str, cmd):
        if not received_command:
            return None

        received_command = received_command.split(":")

        for num, part in enumerate(received_command):
            if cmd.value in part:
                try:
                    return received_command[num + 1]
                except IndexError:
                    return part

        return None


if __name__ == '__main__':
    cmd = Commands.create_command(Commands.SETUP_CLIENT,
                                  Commands.COUNT_OF_CLIENTS, 10,
                                  Commands.CURRENT_CLIENT, 2,
                                  Commands.DECODE_TYPE, Commands.DICTIONARY)
    #cmd = Commands.create_command(Commands.SEND_PDF_FILE)
    print(Commands.get_value(cmd, Commands.DECODE_TYPE))

