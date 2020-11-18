# -*- coding: utf-8 -*-
import click
import os
import sys

plugin_folder = os.path.join(os.path.dirname(__file__), 'commands')
os.environ['LANG'] = 'C.UTF-8'
os.environ['LC_ALL'] = 'C.UTF-8'


if sys.version_info[0] == 3 and sys.version_info[1] >= 5:
    from loguru import logger
    logger.remove()
    logger.add(sys.stderr, level="DEBUG")
    logger.add("twcc.log", format="{time:YYYY-MM-DD HH:mm:ss} |【{level}】| {file} {function} {line} | {message}",
            rotation="00:00", retention='20 days', encoding='utf8', level="INFO", mode='a')
else:
    import yaml
    import logging
    import coloredlogs
    import logging.config
    with open('twccli/logging.yml', 'r') as f:
        config = yaml.load(f,Loader=yaml.FullLoader)
    
    logging.config.dictConfig(config)
    logger = logging.getLogger('command')
    coloredlogs.install(level = config['loggers']['command']['level'], fmt=config['formatters']['default']['format'],logger=logger)
    # coloredlogs.install(logger=logger)

  
class Environment(object):
    def __init__(self):
        self.verbose = False

    def log(self, msg, *args):
        """Logs a message to stderr."""
        if args:
            msg %= args
        click.echo("[TWCCLI] "+msg, file=sys.stderr)

    def vlog(self, msg, *args):
        """Logs a message to stderr only if verbose is enabled."""
        if self.verbose:
            self.log(msg, *args)

    def vlogger_info(self, msg):
        if self.verbose:
            return logger.info(msg)

    def get_verbose(self):
        return self.verbose
    

pass_environment = click.make_pass_decorator(Environment, ensure=True)


class TWCCLI(click.MultiCommand):
    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(plugin_folder):
            if filename.endswith('.py'):
                rv.append(filename[:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        ns = {}
        fn = os.path.join(plugin_folder, name + '.py')

        import six
        if six.PY2 == True:
            # FileNotFoundError is only available since Python 3.3
            # https://stackoverflow.com/a/21368457
            FileNotFoundError = IOError
        from io import open

        try:
            with open(fn, 'rb') as f:
                txt = f.read()
        except FileNotFoundError:
            print('Oops.')
        code = compile(txt, fn, 'exec')
        eval(code, ns, ns)
        return ns['cli']

def exception(logger):
    """
    A decorator that wraps the passed in function and logs 
    exceptions should one occur
    
    @param logger: The logging object
    """
    
    def decorator(func):
    
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                # log the exception
                err = "There was an exception in  "
                err += func.__name__
                logger.exception(err)
            
            # re-raise the exception
            raise
        return wrapper
    return decorator

cli = TWCCLI(help='Welcome to TWCC, TaiWan Computing Cloud. '
             'Thanks for using TWCC-CLI https://github.com/TW-NCHC/TWCC-CLI. '
             '-- You Succeed, We Succeed!! --')

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS, cls=TWCCLI)
@click.option("-v", "--verbose", is_flag=True, help="Enables verbose mode.")
@pass_environment
def cli(env, verbose):
    """
        Welcome to TWCC, TaiWan Computing Cloud.

        https://github.com/TW-NCHC/TWCC-CLI

        version: v0.5.x

        -- You Succeed, We Succeed!! --
    """
    env.verbose = verbose
    pass


if __name__ == '__main__':
    cli()
