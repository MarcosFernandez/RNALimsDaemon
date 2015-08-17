#!/usr/bin/env python

import sys, time
from daemon import Daemon
from limsRnaSeq import LimsRnaSeq
from time import gmtime, strftime

import os,json
     
class DaemonRnaLims(Daemon):

    def setConfiguration(self,configuration="None"):
        """Update Configuration"""
        self.configuration = configuration

    def run(self):
        while True:
            #locate here daemon code
            self.checkUpdating()
            time.sleep(14400)

    def checkUpdating(self):
        """ Reads file of directories to upload to lims """
        config = {}

        with open(self.configuration) as json_file:
            config = json.load(json_file)

        logError = []

        file_lims = config["file_lims"]       
        file_log = config["file_log"]
        failed_uploads = []
        already_processed = []
        
        if os.path.exists(file_lims):
            with open(file_lims, "r") as rnaLims:
                for line in rnaLims:
                    #1.Create object class LimsRnaSeq File
                    limsRnaSeq = LimsRnaSeq()
                    directory = line.strip('\n')

                    if directory not in already_processed:
                        results = limsRnaSeq.run(directory=directory)
                        if results != "":
                            time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                            logError.append("[%s] Lims updating Error %s"%(time,results))
                            failed_uploads.append(directory)
                        else:
                            time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                            logError.append("[%s] Lims updating succesfully executed." %(time))
 
                        already_processed.append(directory)

            if len(logError) != 0:
                with open(file_log, "a") as log:
                    for line in logError:
                        log.write("%s\n" %(line))

            os.remove(file_lims)

            if len(failed_uploads) > 0:
                with open(file_lims,"w") as fileLims:
                    for line in failed_uploads:
                        fileLims.write("%s\n" %(line))


     
if __name__ == "__main__":
    configuration = os.path.dirname(os.path.realpath(__file__)) + "/configuration.json"
    #daemon = DaemonRnaLims(pidfile='/tmp/daemon-example.pid',stdout="/dev/stdout",stderr="/dev/stderr")
    daemon = DaemonRnaLims(pidfile='/tmp/daemon-example.pid')
    daemon.setConfiguration(configuration)

    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
            sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)

