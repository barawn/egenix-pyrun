#===========================================================================
#
# PyRun bootloader for #$pyrun (Version #$version)
#
#---------------------------------------------------------------------------
#
# This template is used by makepyrun.py to build the bootloader
# script for PyRun.
#
# It uses these placeholders (all prefixed with "#$", which are filled
# in with the appropriate data by makepyrun.py:
#
# * pyrun    - name of the pyrun executable
# * version  - version of the pyrun executable (the supported Python version)
# * release  - pyrun release version
# * imports  - imports generated by makepyrun.py, so that freeze.py
#              can find all needed modules to include in the
#              pyrun executable
#
# IMPORTANT:
#
# All variables you add to this namespace will end up in the globals()
# namespace of the script that's being run.
#

# Copyright information
COPYRIGHT = """\

    Copyright (c) 1997-2000, Marc-Andre Lemburg; mailto:mal@lemburg.com
    Copyright (c) 2000-2012, eGenix.com Software GmbH; mailto:info@egenix.com

                            All Rights Reserved.

    This software may be used under the conditions and terms of the
    eGenix.com Public License Agreement. You should have received a
    copy with this software (usually in the file LICENSE.PyRun
    located in the package's main directory). Please write to
    licenses@egenix.com to obtain a copy in case you should not have
    received a copy.

"""

### Imports

import sys, os
import pyrun_config
from pyrun_config import (
    pyrun_name,
    pyrun_version,
    pyrun_release,
    pyrun_build,
    pyrun_libversion,
    pyrun_copyright,
    pyrun_executable,
    pyrun_dir,
    pyrun_binary,
    pyrun_prefix,
    pyrun_bindir,
    )

### Globals

# Options
pyrun_verbose = int(os.environ.get('PYRUN_VERBOSE', 0))
pyrun_debug = int(os.environ.get('PYRUN_DEBUG', 0))
pyrun_as_module = False
pyrun_as_string = False
pyrun_bytecode = False
pyrun_ignore_environment = False
pyrun_ignore_pth_files = False
pyrun_skip_site_main = False
pyrun_interactive = False
pyrun_unbuffered = False
pyrun_optimized = 0

### Helpers

def pyrun_update_runtime():

    """ Update the run-time environment after the changes made
        in pyrun_config.py.

    """
    # Reset site settings
    if 'site' in sys.modules:
        import site
        site.PREFIXES = [sys.prefix]
        site.setcopyright()

def pyrun_banner():

    """ Return the banner text to display when starting up pyrun without
        any command line options.

    """
    return (
        '%s %s %s\n'
        'Thank you for using eGenix PyRun. Type "help" or "license" for details.\n'
        % (pyrun_name,
           pyrun_version,
           pyrun_build))

def pyrun_help(extra_lines=()):

    """ Write help text to stderr.

        extra_lines are shown under the help text.

    """
    # Format the help text
    help_text = ("""\
Usage: %s [pyrunoptions] <script> [parameters]

Version: %s %s

Available pyrun options:

-h:   show this help text
-v:   run in verbose mode
-i:   enable interactive mode
-m:   import and run a module <script> available on PYTHONPATH
-c:   compile and run <script> directly as Python code
-b:   run the given <script> file as bytecode
-E:   ignore environment variables (only PYTHONPATH)
-S:   skip running site.main() and disable support for .pth files
-O:   run in optimized mode (-OO also removes doc-strings)
-u:   open stdout/stderr in unbuffered mode
-d:   enable debug mode
-V:   print the pyrun version and exit

Without options, the given <script> file is loaded and run. Parameters
are passed to the script via sys.argv as normal.

""" % (pyrun_name,
       pyrun_version,
       pyrun_build)).splitlines()
    if extra_lines:
        help_text.extend(extra_lines)
    for line in help_text:
        sys.stderr.write('%s\n' % line)

def pyrun_info(extra_lines=()):

    """ Write (debug) info text to stderr.

        extra_lines are shown under the info text.

    """
    info_text = ("""\
### PyRun Debug Information

# Name and version
pyrun_name = %(pyrun_name)r
pyrun_version = %(pyrun_version)r
pyrun_libversion = %(pyrun_libversion)r
pyrun_release = %(pyrun_release)r
pyrun_build = %(pyrun_build)r

# Files and directories
pyrun_executable = %(pyrun_executable)r
pyrun_dir = %(pyrun_dir)r
pyrun_binary = %(pyrun_binary)r
pyrun_prefix = %(pyrun_prefix)r
pyrun_bindir = %(pyrun_bindir)r

# Options
pyrun_verbose = %(pyrun_verbose)r
pyrun_debug = %(pyrun_debug)r
pyrun_as_module = %(pyrun_as_module)r
pyrun_as_string = %(pyrun_as_string)r
pyrun_bytecode = %(pyrun_bytecode)r
pyrun_ignore_environment = %(pyrun_ignore_environment)r
pyrun_ignore_pth_files = %(pyrun_ignore_pth_files)r
pyrun_interactive = %(pyrun_interactive)r
pyrun_unbuffered = %(pyrun_unbuffered)r
pyrun_optimized = %(pyrun_optimized)r

""" % globals()).splitlines()
    if extra_lines:
        info_text.extend(extra_lines)
    for line in info_text:
        sys.stderr.write('%s\n' % line)

def pyrun_log(line):

    """ Log a line to stderr.

    """
    sys.stderr.write('%s: %s\n' % (pyrun_name, line))

def pyrun_log_error(line):

    """ Log an error line to stderr.

    """
    sys.stderr.write('%s error: %s\n' % (pyrun_name, line))

def pyrun_parse_cmdline():

    """ Parse the pyrun command line arguments.

        Sets the various options exposed as globals and corrects
        sys.argv after successfully parsing the pyrun options.

    """
    import getopt

    # Parse sys.argv
    valid_options = 'vVmcbiESdOu3h?'
    try:
        parsed_options, remaining_argv = getopt.getopt(sys.argv[1:],
                                                       valid_options)
    except getopt.GetoptError, reason:
        pyrun_help(['*** Problem parsing command line: %s' % reason])
        sys.exit(1)

    # Process options
    i = 1
    for arg, value in parsed_options:

        if arg == '-v':
            # Run in verbose mode
            global pyrun_verbose
            pyrun_verbose = True

        elif arg == '-m':
            # Run script as module
            global pyrun_as_module
            pyrun_as_module = True
            if not remaining_argv:
                pyrun_log_error(
                    'Missing argument for -m. Try pyrun -h for help.')
                sys.exit(1)
            # -m terminates the option list, just like for Python
            break

        elif arg == '-c':
            # Run argument as command string
            global pyrun_as_string
            pyrun_as_string = True
            if not remaining_argv:
                pyrun_log_error(
                    'Missing argument for -c. Try pyrun -h for help.')
                sys.exit(1)
            # -c terminates the option list, just like for Python
            break

        elif arg == '-b':
            # Run script as bytecode
            global pyrun_bytecode
            pyrun_bytecode = True

        elif arg == '-i':
            # Enable interactive mode
            global pyrun_interactive
            pyrun_interactive = True

        elif arg == '-E':
            # Ignore environment variable settings
            global pyrun_ignore_environment
            pyrun_ignore_environment = True

        elif arg == '-S':
            # Ignore site.py; XXX This is not a true emulation, just
            # an approximation, since it only ignores .pth files, but
            # still applies the rest of the site.py processing
            global pyrun_ignore_pth_files, pyrun_skip_site_main
            pyrun_ignore_pth_files = True
            pyrun_skip_site_main = True

        elif arg == '-d':
            # Show debug info
            global pyrun_debug
            pyrun_debug += 1

        elif arg == '-u':
            # Set stdout and stderr to unbuffered
            global pyrun_unbuffered
            pyrun_unbuffered = True

        elif arg == '-V':
            # Show version and exit
            sys.stdout.write('pyrun %s (release %s)\n' % (
                pyrun_version,
                pyrun_release))
            sys.exit(0)

        elif arg == '-O':
            # Enable optimization
            global pyrun_optimized
            pyrun_optimized += 1

        # XXX Add more standard Python command line options here

        # Note: There's a general problem with some options, since by
        # the time the frozen interpreter gets to this code, many
        # options would normally already have had some effect. We'd
        # have to implement the command line parsing in C to fully
        # support the options.
        #
        # The following options are simply ignored for this reason:
        #
        elif arg in ('-3',
                     ):
            # Ignored option, only here for compatibility with
            # standard Python
            pass

        else:
            # Show help
            if arg in ('-h', '-?'):
                extra_lines = []
                rc = 0
            else:
                extra_lines = ['*** Error: Unknown option %r' % arg]
                rc = 1
            pyrun_help(extra_lines)
            sys.exit(rc)
        i += 1

    # Update Python flags, if needed; note that the sys.flag setting
    # will not get updated by this.
    if pyrun_optimized:
        sys._setflag('optimize', pyrun_optimized)
    if pyrun_debug:
        sys._setflag('debug', pyrun_debug)

    # Remove pyrun options from sys.argv
    sys.argv[:] = remaining_argv

def pyrun_normpath(path,

                   _home_env='HOME',
                   _home_prefix='~' + os.sep):

    """ Normalize path to make it absolute and also do
        limited tilde expansion (for the home dir).

    """
    path = path.strip()
    
    # Apply limited tilde expansion
    if path == '~':
        path = os.environ.get(_home_env, '~')
        
    elif path[:2] == _home_prefix:
        home = os.environ.get(_home_env, None)
        if home is not None:
            if home.endswith(os.sep):
                path = home + path[2:]
            else:
                path = home + os.sep + path[2:]

    # Convert to an absolute path
    return os.path.abspath(path)

def pyrun_prompt(pyrun_script='<stdin>', banner=None):

    """ Start an interactive pyrun prompt for pyrun_script.

        banner is used as startup text. It defaults to pyrun_banner().

    """
    import code

    # Try to import readline for better keyboard support
    try:
        import readline
    except ImportError:
        pass

    # Defaults
    if banner is None:
        banner = pyrun_banner()

    # Setup globals and run interpreter interactively
    runtime_globals = globals()
    runtime_globals.update(__name__='__main__',
                           __file__=pyrun_script)
    code.interact(banner, raw_input, runtime_globals)

def pyrun_enable_unbuffered_mode():

    """ Enable unbuffered sys.stdout/stderr.

    """
    if pyrun_debug > 1:
        pyrun_log('Enabling unbuffered mode')
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'wb', 0)
    sys.stderr = os.fdopen(sys.stderr.fileno(), 'wb', 0)


def pyrun_run_site_main():

    """ Import the site module

    """
    if pyrun_debug > 1:
        pyrun_log('Importing site.py')
        pyrun_log('  sys.path before importing site:')
        for path in sys.path:
            pyrun_log('    %s' % path)
    import site
    site.PREFIXES = [sys.prefix]
    site.main()
    if pyrun_debug > 1:
        pyrun_log('  sys.path after importing site:')
        for path in sys.path:
            pyrun_log('    %s' % path)

def pyrun_setup_sys_path(pyrun_script=None):

    """ Setup the sys.path in preparation for running pyrun_script.

        pyrun_script may be None in case the script file name is not
        available (e.g. when starting interactive mode or running code
        compiled from the command line parameters).

    """
    exists = os.path.exists
    join = os.path.join
    if pyrun_debug > 1:
        pyrun_log('Setting up sys.path')
        pyrun_log('  sys.path before adjusting it (compile time version):')
        for path in sys.path:
            pyrun_log('    %s' % path)

    # Determine various default locations
    if pyrun_script is not None:
        # Use the script dir as first sys.path dir
        pyrun_script = pyrun_normpath(pyrun_script)
        pyrun_script_dir = os.path.split(pyrun_script)[0]
    else:
        # Use the current directory as first sys.path dir
        pyrun_script_dir = os.getcwd()
    pyrun_script_dir = pyrun_normpath(pyrun_script_dir)
    python_lib = join(pyrun_prefix, 'lib', 'python' + pyrun_libversion)
    if not exists(python_lib):
        python_lib = join(pyrun_dir, 'lib', 'python' + pyrun_libversion)
    python_lib = pyrun_normpath(python_lib)
    python_lib_dynload = join(python_lib, 'lib-dynload')
    python_site_package = join(python_lib, 'site-packages')
    # all path variables should be normalized now

    # Build sys.path; start with the script directory (location of
    # the script to be run)
    sys.path = [pyrun_script_dir]

    # Add PYTHONPATH; note: these are not processed for .pth files
    if not pyrun_ignore_environment:
        pythonpath = os.environ.get('PYTHONPATH', None)
        if pythonpath is not None:
            sys.path.extend([
                pyrun_normpath(path)
                for path in pythonpath.split(os.pathsep)])

    # Add python_lib and python_lib_dynload (location of additional
    # pyrun shared modules)
    sys.path.append(python_lib)
    sys.path.append(python_lib_dynload)

    # Add site packages directory
    if pyrun_ignore_pth_files:
        # Add the standard dirs without any .pth processing
        sys.path.append(python_site_package)
    else:
        # Use site.addsitedir() to add site-package dirs with
        # .pth processing (needed for setuptools/pip et al.)
        import site
        known_paths = site.addsitedir(python_site_package)
        #site.addsitedir(another_site_package, known_paths)

    if pyrun_debug > 1:
        pyrun_log('  sys.path after adjusting it (before cleanup):')
        for path in sys.path:
            pyrun_log('    %s' % path)

    # Finally, remove non-existing entries
    exists = os.path.exists
    sys.path = [dir
                for dir in sys.path
                if exists(dir)]

    if pyrun_debug > 1:
        pyrun_log('  sys.path final version:')
        for path in sys.path:
            pyrun_log('    %s' % path)

def pyrun_execute_script(pyrun_script, mode='file'):

    """ Run pyrun_script with pyrun.

        pyrun_script may point to a Python script file, Python
        bytecode file or a module name, depending on mode:

        mode defines the run method:

        'file'       - run as Python source file (default)
        'path'       - run as Python path, i.e. directory or
                       ZIP file with __main__ module (Python 2.7 only)
        'module'     - lookup as module on sys.path and run as module
        'codefile'   - run as .pyc file (default, if pyrun_script ends
                       with .pyc or .pyo)
        'string'     - run as Python source string
        'codestring' - run as Python byte code string (in .pyc format)

    """
    # Run the pyrun_script
    if pyrun_debug > 1:
        pyrun_log('Executing script %r in mode %r' % (
            pyrun_script, mode))
        pyrun_log('  sys.argv=%r' % sys.argv)
        pyrun_log('  sys.path=%r' % sys.path)
        pyrun_log('  globals()=%r' % globals())

    # Adjust defaults
    if (mode == 'file' and 
        (pyrun_script.endswith('.pyc') or
         pyrun_script.endswith('.pyo'))):
        mode = 'codefile'

    if mode == 'module':

        ### Run pyrun_script as module (much like python -m <module>)

        if pyrun_verbose:
            pyrun_log('Running %r as module' % pyrun_script)
        # sys.argv[0]: runpy will set the sys.argv[0] to the absolute
        # location of the found module
        import runpy
        try:
            runpy.run_module(pyrun_script, globals(), '__main__', True)
        except ImportError, reason:
            pyrun_log_error('Could not run %r: %s' % (pyrun_script, reason))
            sys.exit(1)

    elif mode == 'path':
        
        ### Run pyrun_script as path (much like python <path>)
        #
        # Only supported in Python 2.7. Can handle .py files, ZIP
        # files and directories with __main__.py module.
        #

        if pyrun_verbose:
            pyrun_log('Running %r as path' % pyrun_script)

        # About sys.argv[0]:
        #
        # runpy.run_path() will setup sys.argv[0] in the following
        # way:
        #
        # * if pyrun_script points to a directory with __main__.py
        #   module, to the directory containing __main__.py
        #
        # * if pyrun_script points to a ZIP file, to the name of
        #    the zip file
        #
        # * in case pyrun_script points to a .py file in some subdir,
        #   to the current directory
        #
        #   WARNING: This is different than standard Python, which
        #   places the directory of the .py file in sys.argv[0].
        #
        import runpy
        try:
            runpy.run_path(pyrun_script, globals(), '__main__')
        except ImportError, reason:
            pyrun_log_error('Could not run %r: %s' % (pyrun_script, reason))
            sys.exit(1)

    elif (mode == 'codefile' or mode == 'codestring'):

        ### Run pyrun_script as bytecode file or string

        import imp, marshal
        if mode == 'codefile':
            if pyrun_verbose:
                pyrun_log('Running %r as bytecode file' % pyrun_script)
            if not os.access(pyrun_script, os.R_OK):
                pyrun_log_error('Could not find/read script file %r' %
                                pyrun_script)
                sys.exit(1)
            # sys.argv[0]: should be the same as pyrun_script
            assert sys.argv[0] == pyrun_script
            module_file = open(pyrun_script, 'rb')

        elif mode == 'codestring':
            if pyrun_verbose:
                pyrun_log('Running pyrun_script as bytecode string')
            # sys.argv[0]: We mimic Python when using the -c option
            sys.argv[0] = '-c'
            import cStringIO
            module_file = cStringIO.StringIO(pyrun_script)

        # Check magic
        if module_file.read(4) != imp.get_magic():
            pyrun_log_error('Incompatible bytecode file %r' % pyrun_script)
            sys.exit(1)

        # Skip timestamp (32 bits)
        module_file.read(4)

        # Load code object
        module_code = marshal.load(module_file)

        # Close file
        module_file.close()

        # Exec code in globals
        runtime_globals = globals()
        runtime_globals.update(__name__='__main__',
                               __file__=pyrun_script)
        exec module_code in runtime_globals

    elif mode == 'file':

        ### Run pyrun_script as .py file

        if pyrun_verbose:
            pyrun_log('Running %r as script' % pyrun_script)
        if not os.access(pyrun_script, os.R_OK):
            pyrun_log_error('Could not find/read script file %r' %
                            pyrun_script)
            sys.exit(1)

        # sys.argv[0]: should be the same as pyrun_script
        assert sys.argv[0] == pyrun_script

        # Exec script file in globals
        runtime_globals = globals()
        runtime_globals.update(__name__='__main__',
                               __file__=pyrun_script)
        execfile(pyrun_script, runtime_globals, runtime_globals)

    elif mode == 'string':

        ### Run pyrun_script as source string

        if pyrun_verbose:
            pyrun_log('Running pyrun_script as string')

        # Compile string into code object
        script_path = '<stdin>'
        if not pyrun_script.endswith('\n'):
            # No longer needed in Python 2.7, but better safe than
            # sorry
            pyrun_script += '\n'
        code = compile(pyrun_script, script_path, 'exec')

        # sys.argv[0]: We mimic Python when using the -c option
        sys.argv[0] = '-c'

        # Exec code in globals
        runtime_globals = globals()
        runtime_globals.update(__name__='__main__',
                               __file__=script_path)
        exec code in runtime_globals

    else:
        raise TypeError('unknown execution mode %r' % mode)

### Entry point

if __name__ == '__main__':

    # Parse the command line and get the script name
    pyrun_parse_cmdline()

    # Enable unbuffered mode
    if pyrun_unbuffered:
        pyrun_enable_unbuffered_mode()

    # Update run-time environment
    pyrun_update_runtime()
    
    # Show debug info
    if pyrun_debug > 1:
        pyrun_info()

    # Start the runtime
    if not sys.argv and sys.stdin.isatty():

        ### Enter interactive mode

        # Setup sys.path
        pyrun_setup_sys_path()
        
        # Import site module and run site.main() (which is not run by
        # pyrun per default like in standard Python; see makepyrun.py)
        if not pyrun_skip_site_main:
            pyrun_run_site_main()

        # Setup sys.argv for interactive mode
        if not sys.argv:
            sys.argv = ['']

        # Enter interactive mode
        pyrun_prompt()

    else:

        ### Run a script

        # Setup script to run
        if not sys.argv:
            # Filter mode: read the script from stdin
            if pyrun_as_string or pyrun_as_module:
                # Missing script argument
                pyrun_log_error(
                    'Missing argument for -c/-m. Try pyrun -h for help.')
                sys.exit(1)
            else:
                global pyrun_script
                pyrun_as_string = True
            pyrun_script = sys.stdin.read()
            sys.argv = ['']

        elif sys.argv[0] == '-' and not (pyrun_as_string or pyrun_as_module):
            # Read the script from stdin
            global pyrun_script
            pyrun_as_string = True
            pyrun_script = sys.stdin.read()

        else:
            # Default operation: run the script given as first
            # argument
            pyrun_script = sys.argv[0]

        # Setup paths & mode
        script_path = pyrun_script
        if pyrun_as_module:
            mode = 'module'
            script_path = None
        elif pyrun_as_string:
            mode = 'string'
            script_path = None
        else:
            if pyrun_version < '2.7.0':
                mode = 'file'
            # Python 2.7 and later
            elif (pyrun_script.endswith('.py') or
                  pyrun_script.endswith('.pyw')):
                mode = 'file'
            else:
                # Use path mode for all other files, since this
                # provides support for directories, ZIP files, etc.
                mode = 'path'

        # Setup sys.path
        pyrun_setup_sys_path(script_path)

        # Import site module and run site.main() (which is not run by
        # pyrun per default like in standard Python; see makepyrun.py)
        if not pyrun_skip_site_main:
            pyrun_run_site_main()

        # Run the script
        try:
            pyrun_execute_script(pyrun_script, mode)
        except Exception, reason:
            if pyrun_interactive:
                import traceback
                traceback.print_exc()
                pyrun_prompt(banner='')
            else:
                raise
        else:
            # Enter interactive mode, in case wanted
            if pyrun_interactive:
                pyrun_prompt()

    # Exit
    sys.exit(0)

# Should not get here...
sys.exit(0)

### freeze.py Hooks

# This is unreachable code used as hook for freeze.py to include
# the standard Python library.
#$imports

# PyRun specific modules to include
import pyrun_config
import pyrun_extras
