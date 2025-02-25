"""Sets up command line interface."""
import logging
from argparse import ArgumentParser
from vilma import VERSION
from vilma.make_ld_schema import main as make_ld_schema
from vilma.make_ld_schema import args as make_ld_schema_args
from vilma.vi_options import main as fit
from vilma.vi_options import args as fit_args

COMMANDS = {
    'make_ld_schema': {'cmd': make_ld_schema, 'parser': make_ld_schema_args},
    'fit': {'cmd': fit, 'parser': fit_args}
}


def main():
    """
    Takes command line input and calls appropriate vilma command.

    The available commands are:
        make_ld_schema: Build a block diagonal LD matrix and store it in the
            format needed by vilma.
        fit: Fit a model to GWAS summary statistics and use that model to build
            polygenic scores.

    Calling vilma <command> --help will show the available options for each
    subcommand.
    """
    parser = ArgumentParser(
        description="""
                    vilma v%s uses variational inference to estimate variant
                    effect sizes from GWAS summary data while simultaneously
                    learning the overall distribution of effects.
                    """ % VERSION,
        usage='vilma <command> <options>'
    )
    subparsers = parser.add_subparsers(title='Commands', dest='command')
    for cmd in COMMANDS:
        cmd_parser = COMMANDS[cmd]['parser'](subparsers)
        cmd_parser.add_argument(
            '--logfile', required=False, type=str, default='',
            help='File to store information about the vilma run. To print to '
                 'stdout use "-". Defaults to no logging.'
        )
    args = parser.parse_args()
    try:
        func = COMMANDS[args.command]['cmd']
    except KeyError:
        parser.print_help()
        exit()
    if args.logfile == '-':
        logging.basicConfig(level=0)
    elif args.logfile:
        logging.basicConfig(filename=args.logfile, level=0)
    func(args)


if __name__ == '__main__':
    main()
