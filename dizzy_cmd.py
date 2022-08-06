#!/usr/bin/env python3
#       dizzy_cmd.py
#       Copyright 2017 Daniel Mende <mail@c0decafe.de>

from argparse import ArgumentParser
from os.path import basename
from sys import version_info, exit, argv
from dizzy import config    #Needs to be load before anything using external dependencies
from dizzy.job import Job
from dizzy import profile
from dizzy.log import print_dizzy, REDUCE

if version_info.major < 3:
    print("This script is intended for use with python >= 3!")
    exit(1)

def main(do_profile=False):
    print_dizzy("%s version %s running on %s" % (basename(argv[0]), config.CONFIG["GLOBALS"]["VERSION"], config.CONFIG["GLOBALS"]["PLATFORM"]), REDUCE)

    parser = ArgumentParser()
    parser.add_argument(dest='file', metavar='jobfile', nargs='?', default="")
    parser.add_argument("-s", help="Start at the given step", type=int, dest="start_at", default=0)
    parser.add_argument("-d", help="Output status every SEC seconds", type=float, dest="status_delay", metavar="SEC",
                        default=60)
    parser.add_argument("-l", help="List all loaded modules and their contents.", dest="print_config", action='store_true')
    parser.add_argument("-o", help="Overwrite a config option", type=str, dest="options", action="append", default=[])
    args = parser.parse_args()

    if do_profile:
        profile.profile_on()

    if args.print_config:
        config.print_config()
        exit(0)

    options = {}
    for i in args.options:
        if not "=" in i:
            parser.error("Argument to -o needs to be in form 'option.name=value'.")
        splited = i.split("=")
        opt_name = splited[0]
        value = splited[1]
        if not "." in opt_name:
            parser.error("Argument to -o needs to be in form 'option.name=value'.")
        splited = opt_name.split(".")
        opt = splited[0]
        name = splited[1]
        if not opt in options:
            options[opt] = { name : value }
        else:
            options[opt][name] = value

    if args.file == "":
        parser.error("Argument 'jobfile' is required.")

    j = Job(args.file, args.start_at, options)
    j.start()
    try:
        while j.is_alive():
            j.join(args.status_delay)
            if j.is_alive():
                j.print_status()
    except KeyboardInterrupt:
        if j.is_alive():
            j.print_status()
        exit(1)

    if do_profile:
        profile.profile_off()
        import pprint
        pprint.pprint(profile.get_profile_stats())

if __name__ == '__main__':
    main(False)
