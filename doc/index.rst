.. RNA Lims Daemon documentation master file, created by
   sphinx-quickstart on Thu Jul 30 14:29:53 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

RNA Lims Daemon
===============

RNA Lims Daemon is a GNU/Linux daemon which updates rna seq pipeline results to a Lims Database using REST web services.


1. Install
----------

Installation is straightforward. Just download `RNA Lims Daemon`_ and run the script.

.. _RNA Lims Daemon: http://daemon.lims


2. Configuration file
---------------------

RNA Lims Daemon uses two important files.

    1. **File Lims** A file were each line is a mapping directory of the rna pipeline. This directory contains the data to be parsed and updated to Lims Database through REST web services.
                     When all lines are processed then the file is removed.

    2. **File log** A file which contains a register of the actions performed by the daemon.

.. warning::
    
    Configuration file name and location

    The configuration file name must be ``configuration.json`` and must be at the same location as the RNA Lims Daemon scripts.

    Do not forget to create the configuration file.

The configuration file must be a json file with two entries. ::

    {
      "file_lims":"/path/to/rna_lims",        
      "file_log":"/path/to/rna_lims.log"
    }


3. Daemon usage
---------------

3.1 Start
`````````

Once you have the configuration (``configuration.json``) file ready then you can **start** the daemon. Every 4 hours the **file_lims** will be checked in order to upload rnaseq data
to the **lims database**.

::

    daemon_rna_lims.py start

If there is data to be uploaded in **file_lims** then is triggered a process to upload rna pipeline data to lims database. 

.. note::
    
    If there is some error when uploading the rna pipeline data to the lims file system then the directory is kept in the **file_lims** to try once again.
    


3.1 Stop
````````

To stop the daemon just run: ::

    daemon_rna_lims.py stop


3.1 Restart
```````````

To stap and start the daemon run: ::

    daemon_rna_lims.py restart


.. note::

    In **file_log** are registered all the commands triggered by the daemon.





