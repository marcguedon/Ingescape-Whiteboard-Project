#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  Puissance4_View version 1.0
#  Created by Ingenuity i/o on 2024/11/07
#
# "no description"
#

import signal
import getopt
import time
from pathlib import Path
import traceback
import sys

from Puissance4_View import *

port = 5670
agent_name = "Puissance4_View"
device = None
verbose = False
is_interrupted = False

short_flag = "hvip:d:n:"
long_flag = ["help", "verbose", "interactive_loop", "port=", "device=", "name="]

ingescape_path = Path("~/Documents/Ingescape").expanduser()


def print_usage():
    print("Usage example: ", agent_name, " --verbose --port 5670 --device device_name")
    print("\nthese parameters have default value (indicated here above):")
    print("--verbose : enable verbose mode in the application (default is disabled)")
    print("--port port_number : port used for autodiscovery between agents (default: 31520)")
    print("--device device_name : name of the network device to be used (useful if several devices available)")
    print("--name agent_name : published name for this agent (default: ", agent_name, ")")
    print("--interactive_loop : enables interactive loop to pass commands in CLI (default: false)")


def print_usage_help():
    print("Available commands in the terminal:")
    print("	/quit : quits the agent")
    print("	/help : displays this message")

def return_io_value_type_as_str(value_type):
    if value_type == igs.INTEGER_T:
        return "Integer"
    elif value_type == igs.DOUBLE_T:
        return "Double"
    elif value_type == igs.BOOL_T:
        return "Bool"
    elif value_type == igs.STRING_T:
        return "String"
    elif value_type == igs.IMPULSION_T:
        return "Impulsion"
    elif value_type == igs.DATA_T:
        return "Data"
    else:
        return "Unknown"

def return_event_type_as_str(event_type):
    if event_type == igs.PEER_ENTERED:
        return "PEER_ENTERED"
    elif event_type == igs.PEER_EXITED:
        return "PEER_EXITED"
    elif event_type == igs.AGENT_ENTERED:
        return "AGENT_ENTERED"
    elif event_type == igs.AGENT_UPDATED_DEFINITION:
        return "AGENT_UPDATED_DEFINITION"
    elif event_type == igs.AGENT_KNOWS_US:
        return "AGENT_KNOWS_US"
    elif event_type == igs.AGENT_EXITED:
        return "AGENT_EXITED"
    elif event_type == igs.AGENT_UPDATED_MAPPING:
        return "AGENT_UPDATED_MAPPING"
    elif event_type == igs.AGENT_WON_ELECTION:
        return "AGENT_WON_ELECTION"
    elif event_type == igs.AGENT_LOST_ELECTION:
        return "AGENT_LOST_ELECTION"
    else:
        return "UNKNOWN"

def signal_handler(signal_received, frame):
    global is_interrupted
    print("\n", signal.strsignal(signal_received), sep="")
    is_interrupted = True


def on_agent_event_callback(event, uuid, name, event_data, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Puissance4_View)
        # add code here if needed
    except:
        print(traceback.format_exc())


def on_freeze_callback(is_frozen, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Puissance4_View)
        # add code here if needed
    except:
        print(traceback.format_exc())

# services
def Actionresult_callback(sender_agent_name, sender_agent_uuid, service_name, tuple_args, token, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Puissance4_View)
        agent_object.Actionresult(sender_agent_name, sender_agent_uuid, token)
    except:
        print(traceback.format_exc())


def Elementcreated_callback(sender_agent_name, sender_agent_uuid, service_name, tuple_args, token, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Puissance4_View)
        Elementid = tuple_args[0]
        agent_object.Elementcreated(sender_agent_name, sender_agent_uuid, Elementid, token)
    except:
        print(traceback.format_exc())


def Show_Choosing_Player_callback(sender_agent_name, sender_agent_uuid, service_name, tuple_args, token, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Puissance4_View)
        Player = tuple_args[0]
        agent_object.Show_Choosing_Player(sender_agent_name, sender_agent_uuid, Player)
    except:
        print(traceback.format_exc())


def Choose_Token_Color_callback(sender_agent_name, sender_agent_uuid, service_name, tuple_args, token, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Puissance4_View)
        Color = tuple_args[0]
        agent_object.Choose_Token_Color(sender_agent_name, sender_agent_uuid, Color)
    except:
        print(traceback.format_exc())


def Preview_Token_callback(sender_agent_name, sender_agent_uuid, service_name, tuple_args, token, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Puissance4_View)
        Column_Number = tuple_args[0]
        Color = tuple_args[1]
        agent_object.Preview_Token(sender_agent_name, sender_agent_uuid, Column_Number, Color)
    except:
        print(traceback.format_exc())


def Place_Token_callback(sender_agent_name, sender_agent_uuid, service_name, tuple_args, token, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Puissance4_View)
        Player = tuple_args[0]
        Line_Number = tuple_args[1]
        Column_Number = tuple_args[2]
        agent_object.Place_Token(sender_agent_name, sender_agent_uuid, Player, Line_Number, Column_Number)
    except:
        print(traceback.format_exc())


def Show_Playing_Player_callback(sender_agent_name, sender_agent_uuid, service_name, tuple_args, token, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Puissance4_View)
        Player = tuple_args[0]
        agent_object.Show_Playing_Player(sender_agent_name, sender_agent_uuid, Player)
    except:
        print(traceback.format_exc())


def Show_Winner_callback(sender_agent_name, sender_agent_uuid, service_name, tuple_args, token, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Puissance4_View)
        Player = tuple_args[0]
        Point1_row = tuple_args[1]
        Point1_col = tuple_args[2]
        Point2_row = tuple_args[3]
        Point2_col = tuple_args[4]
        agent_object.Show_Winner(sender_agent_name, sender_agent_uuid, Player, ((Point1_row, Point1_col), (Point2_row, Point2_col)))
    except:
        print(traceback.format_exc())


def Init_Color_Choice_callback(sender_agent_name, sender_agent_uuid, service_name, tuple_args, token, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Puissance4_View)
        agent_object.Init_Color_Choice(sender_agent_name, sender_agent_uuid)
    except:
        print(traceback.format_exc())


def Init_Game_callback(sender_agent_name, sender_agent_uuid, service_name, tuple_args, token, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Puissance4_View)
        agent_object.Init_Game(sender_agent_name, sender_agent_uuid)
    except:
        print(traceback.format_exc())


if __name__ == "__main__":

    # catch SIGINT handler before starting agent
    signal.signal(signal.SIGINT, signal_handler)
    interactive_loop = False

    try:
        opts, args = getopt.getopt(sys.argv[1:], short_flag, long_flag)
    except getopt.GetoptError as err:
        igs.error(err)
        sys.exit(2)
    for o, a in opts:
        if o == "-h" or o == "--help":
            print_usage()
            exit(0)
        elif o == "-v" or o == "--verbose":
            verbose = True
        elif o == "-i" or o == "--interactive_loop":
            interactive_loop = True
        elif o == "-p" or o == "--port":
            port = int(a)
        elif o == "-d" or o == "--device":
            device = a
        elif o == "-n" or o == "--name":
            agent_name = a
        else:
            assert False, "unhandled option"

    igs.agent_set_name(agent_name)
    igs.definition_set_version("1.0")
    igs.log_set_console(verbose)
    igs.log_set_file(True, None)
    igs.log_set_stream(verbose)
    igs.set_command_line(sys.executable + " " + " ".join(sys.argv))

    igs.debug(f"Ingescape version: {igs.version()} (protocol v{igs.protocol()})")

    if device is None:
        # we have no device to start with: try to find one
        list_devices = igs.net_devices_list()
        list_addresses = igs.net_addresses_list()
        if len(list_devices) == 1:
            device = list_devices[0]
            igs.info("using %s as default network device (this is the only one available)" % str(device))
        elif len(list_devices) == 2 and (list_addresses[0] == "127.0.0.1" or list_addresses[1] == "127.0.0.1"):
            if list_addresses[0] == "127.0.0.1":
                device = list_devices[1]
            else:
                device = list_devices[0]
            print("using %s as de fault network device (this is the only one available that is not the loopback)" % str(device))
        else:
            if len(list_devices) == 0:
                igs.error("No network device found: aborting.")
            else:
                igs.error("No network device passed as command line parameter and several are available.")
                print("Please use one of these network devices:")
                for device in list_devices:
                    print("	", device)
                print_usage()
            exit(1)

    agent = Puissance4_View()

    igs.observe_agent_events(on_agent_event_callback, agent)
    igs.observe_freeze(on_freeze_callback, agent)

    igs.output_create("game_title", igs.STRING_T, None)

    igs.service_init("actionResult", Actionresult_callback, agent)
    igs.service_arg_add("actionResult", "succeeded", igs.BOOL_T)
    igs.service_init("elementCreated", Elementcreated_callback, agent)
    igs.service_arg_add("elementCreated", "elementId", igs.INTEGER_T)
    igs.service_init("show_choosing_player", Show_Choosing_Player_callback, agent)
    igs.service_arg_add("show_choosing_player", "player", igs.INTEGER_T)
    igs.service_init("choose_token_color", Choose_Token_Color_callback, agent)
    igs.service_arg_add("choose_token_color", "color", igs.STRING_T)
    igs.service_init("preview_token", Preview_Token_callback, agent)
    igs.service_arg_add("preview_token", "column_number", igs.INTEGER_T)
    igs.service_arg_add("preview_token", "color", igs.STRING_T)
    igs.service_init("place_token", Place_Token_callback, agent)
    igs.service_arg_add("place_token", "player", igs.INTEGER_T)
    igs.service_arg_add("place_token", "line_number", igs.INTEGER_T)
    igs.service_arg_add("place_token", "column_number", igs.INTEGER_T)
    igs.service_init("show_playing_player", Show_Playing_Player_callback, agent)
    igs.service_arg_add("show_playing_player", "player", igs.INTEGER_T)
    igs.service_init("show_winner", Show_Winner_callback, agent)
    igs.service_arg_add("show_winner", "player", igs.INTEGER_T)
    igs.service_arg_add("show_winner", "point1_row", igs.INTEGER_T)
    igs.service_arg_add("show_winner", "point1_col", igs.INTEGER_T)
    igs.service_arg_add("show_winner", "point2_row", igs.INTEGER_T)
    igs.service_arg_add("show_winner", "point2_col", igs.INTEGER_T)
    igs.service_init("init_color_choice", Init_Color_Choice_callback, agent)
    igs.service_init("init_game", Init_Game_callback, agent)

    igs.start_with_device(device, port)
    # catch SIGINT handler after starting agent
    signal.signal(signal.SIGINT, signal_handler)

    if interactive_loop:
        print_usage_help()
        while True:
            command = input()
            if command == "/quit":
                break
            elif command == "/help":
                print_usage_help()
    else:
        while (not is_interrupted) and igs.is_started():
            time.sleep(2)
            agent.Game_TitleO = "Connect 4"

    if igs.is_started():
        igs.stop()
