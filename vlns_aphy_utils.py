import traceback
import subprocess
import os

class Utils(object):
    @staticmethod
    def format_exception(ex):
        return ''.join(traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__))

    # Writes report and stdout, Raises an exception if exitcode not 0
    @staticmethod
    def subprocess_result_handle(subprocess_result, report_fd):
        # Append report
        os.write(report_fd, str.encode("".join(subprocess_result.args) + "\n"))
        os.write(report_fd, subprocess_result.stdout)
        # Append stdout
        print("".join(subprocess_result.args))
        print(subprocess_result.stdout.decode("utf-8"))
        
        # Handle errors
        if subprocess_result.stderr:
            os.write(report_fd, subprocess_result.stderr)
            print(subprocess_result.stderr.decode("utf-8"))
        
        if subprocess_result.returncode != 0:
            raise Exception("Exited with code " + str(subprocess_result.returncode))

    @staticmethod
    def subprocess_run(args_list, **kwargs):
        print(f"Running {' '.join(args_list)}")
        return subprocess.run(args_list, **kwargs)
