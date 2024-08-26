#####################################################################
#                                                                   #
# /labscript_devices/AndorSolis/blacs_tabs.py                       #
#                                                                   #
# Copyright 2019, Monash University and contributors                #
#                                                                   #
# This file is part of labscript_devices, in the labscript suite    #
# (see http://labscriptsuite.org), and is licensed under the        #
# Simplified BSD License. See the license.txt file in the root of   #
# the project for the full license.                                 #
#                                                                   #
#####################################################################

from labscript_devices.IMAQdxCamera.blacs_tabs import IMAQdxCameraTab

import pickle

class NuvuCameraTab(IMAQdxCameraTab):
    worker_class = 'user_devices.NuvuCamera.blacs_workers.NuvuCameraWorker'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.connect_restart_receiver(self.on_restart)
    
    def on_restart(self, device_name):
        worker_task = self.queue_work(self.primary_worker, 'restart_close')
        worker_process,worker_function,worker_args,worker_kwargs = worker_task

        worker_arg_list = (worker_function,worker_args,worker_kwargs)
        # This line is to catch if you try to pass unpickleable objects.
        try:
            pickle.dumps(worker_arg_list)
        except Exception:
            self.error_message += 'Attempt to pass unserialisable object to child process:'
            raise

        to_worker = self.workers[worker_process][1]
        from_worker = self.workers[worker_process][2]
        to_worker.put(worker_arg_list)

        from_worker.get()
        return
    