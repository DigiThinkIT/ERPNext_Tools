import subprocess
import sys
import os
import argparse
import frappe


def setup():
    """
    Setup environment for correct tests execution
    """

    frappe.init(site='erpnext.vm',
                sites_path="/home/frappe/frappe-bench/sites")

    frappe.connect()
    frappe.clear_cache()


def execute_cmd_command(cmd):
    """
    Execute command
    """
    p = subprocess.Popen(cmd,
                         shell=True,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT,
                         close_fds=True)
    return p.stdout.read()


def run_all_doc_types():
    """
    Running tests by doc type...
    """
    print run_all_doc_types.__doc__

    all_doc_types = [table[0][3:] for table in frappe.db.sql("SHOW tables;") if table[0][:3] == 'tab']

    for doc in all_doc_types:
        result = execute_cmd_command('bench run-tests --doctype "%s"' % doc)

        print "-" * 70

        if "ImportError: No module named test_" in result:
            print 'DOC TYPE : "%s" (Not implemented tests)\n' % doc
        else:
            print 'DOC TYPE : "%s"\n %s' % (doc, result)


def run_all_modules():
    """
    Running all test modules for each application in (apps)...
    """
    print run_all_modules.__doc__

    application_root = os.path.join(os.path.dirname(os.path.realpath('__file__')), "apps")

    apps_list = os.listdir(application_root)

    for app in apps_list:
        print "=" * 70
        print "\t\t\tAPPLICATION:", app
        print "=" * 70

        app_folder = os.path.join(application_root, app)

        for path, subdirs, files in os.walk(app_folder):
            for filename in files:
                if filename.startswith("test_") and filename.endswith(".py"):

                    module = os.path.join(os.path.relpath(path), filename)
                    module_name = module.replace("/", ".")[:-3].replace("apps.%s." % app, "")

                    result = execute_cmd_command('bench run-tests --module "%s"' % module_name)

                    print "PATH   ::", os.path.join(os.path.abspath(path), filename)
                    print "MODULE ::", module_name
                    print result


if __name__ == '__main__':

    parser = argparse.ArgumentParser('Debug runner for tests execution')
    parser.add_argument('--run', help='doc_type | module')
    args = parser.parse_args()

    setup()

    print "-" * 70

    if args.run == 'doc_type':
        run_all_doc_types()
    elif args.run == 'module':
        run_all_modules()

    sys.exit()
