import fabric
from fabric.api import *

import time
import re

# reduce fabric's verbosity
for i in fabric.state.output:
    fabric.state.output[i] = False


class hadoopHandler(object):
    """
    hadoopHandler(mhost, uname, psswd) -> hadoopHandler instance

    Args:
        mhost (str): master host alias or ip address.
        uname (str): common username for the cluster.
        psswd (str): common password for the cluster.
    """

    def __init__(self, mhost, uname, psswd):
        env.command_prefixes = ['sethdpconf hadoopmulti/confmulti']
        env.warn_only = True
        env.shell = "/bin/bash -l -i -c"

        env.host_string = mhost
        env.user = uname
        env.password = psswd


    def ping(self):
        """
        Tries to connect to host.

        Returns:
            True when succeeds, False if Fabric fails.
        """
        out = run('echo Connected')

        if out.failed:
            return False
        else:
            return True


    def get_slaves(self):
        """
        Get the slave list from the hadoopmulti/confmulti directory.

        Returns:
            List of the slaves.
        """
        out = run('cat ~/hadoopmulti/confmulti/slaves')

        return [i.strip() for i in out.split("\n")[1:]]


    def check(self, host, type="slave"):
        """
        Check if every node is active for the host and type specified.

        Args:
            host (str): host alias or ip address.
            type (str): master or slave (default is slave).
        Returns:
            True when succeeds, False if Fabric fails.
        """
        slave = ['DataNode', 'TaskTracker']
        master = ['JobTracker', 'NameNode']

        with settings(host_string=host):
            out = run('jps')

        if out.failed:
            return False

        # if the demons were too many the commented code below would come in handy
        # master = (master == [i for i in master if i in out])
        # slave = (slave == [i for i in slave if i in out])

        master = master[0] in out and master[1] in out
        slave = slave[0] in out and slave[1] in out

        if type == "master" and master and slave:
            return True
        elif type == "slave" and not master and slave:
            return True
        else:
            return False


    def check_all(self):
        """
        Check if every node is active for every node.

        Returns:
            True if every node is active, False if not.
        """
        for i in self.get_slaves():
            if not(self.check(i, "slave") or self.check(i, "master")):
                return False
        return True


    def start(self):
        """
        Starts all the Nodes and Trackers.

        Returns:
            True when succeeds, False if Fabric fails.
        """
        out = run('start-all.sh')

        time.sleep(65)  # to avoid safe mode

        if out.failed:
            return False
        else:
            # you could do a self.check_all() to confirm all demons running
            return True


    def stop(self):
        """
        Stops all the nodes and Trackers.

        Returns:
            True when succeeds, False if Fabric fails.
        """
        out = run('stop-all.sh')

        if out.failed:
            return False
        else:
            return True


    def job_list(self):
        """
        Lists the jobs (their ids) actually running.

        Returns:
            List of the active job_ids if there are, False if Fabric fails.
        """
        out = run('hadoop job -list')

        job_id = [m.group() for m in re.finditer(r'job_\d+_\d+', out)]

        if out.failed:
            return False
        else:
            return job_id


    def job_status(self, id):
        """
        Gets the status of the job with specified id.

        Returns:
            Tuple with (<map_compl>, <red_compl>) when succeeds, False if Fabric fails.
        """
        out = run('hadoop job -status %s' % id)

        ix = out.find("map() completion:")
        map_compl = float(out[ix+18:ix+21])

        ix = out.find("reduce() completion:")
        red_compl = float(out[ix+21:ix+24])

        if out.failed:
            return False
        else:
            return map_compl, red_compl


    def job_stream(self, exepath, inpath, outpath):
        """
        Launch a streaming job.

        Args:
            exepath (str): path to the executable mapper script
            inpath (str): path to the input file
            outpath (str): path to the output directory
        Returns:
            True when succeeds, False if Fabric fails.
        """

        s = 'hadoop jar /usr/share/hadoop/contrib/streaming/hadoop-streaming-1.1.2.jar \
			-D mapred.reduce.tasks=0 -inputformat \
			org.apache.hadoop.mapred.lib.NLineInputFormat -file %s\
			-mapper %s -input %s -output %s'

        out = run(s % (exepath, exepath, inpath, outpath))

        if out.failed: # to implement "Job Successful" in out
            return False
        else:
            return True


    def pheno_run(self, inpath, outpath, exepath="~/phenomapper.py"):
        """
        Function to easily run phenoripper.
        """
        p1 = self.start()
        if not p1:
            return False

        p2 = self.job_stream(exepath, inpath, outpath)

        if not p2:
            self.stop()
            return False

        self.stop()
        return True


    def dfs_ls(self, path="~"):
        """
        Lists the dir at <path> in the DFS.

        Args:
            path (str): default value is the root of dfs.
        Returns:
            The list of files and dirs at <path>
            list (str) when succeeds, False if Fabric fails.
        """
        out = run('hadoop fs -ls %s' % path)

        if out.failed:
            return False
        else:
            return out


    def dfs_get(self, inpath, outpath):
        """
        Get a file from <inpath> on the DFS to <outpath> in local directory.

        Args:
            inpath (str): path to the file to be pulled
            outpath (str): path to the location to be pulled to
        Returns:
            True when succeeds, False if Fabric fails.
        """
        out = run('hadoop fs -get %s %s' % (inpath, outpath))

        if out.failed:
            return True
        else:
            return False


    def dfs_put(self, inpath, outpath):
        """
        Put a file from <inpath> in the local directory to <outpath> on the DFS.

        Args:
            inpath (str): path to the file to be pushed
            outpath (str): path to the location to tbe pushed to
        Returns:
            True when succeeds, False if Fabric fails.
        """
        out = run('hadoop fs -put %s %s' % (inpath, outpath))

        if out.failed:
            return False
        else:
            return True


    def dfs_rm(self, path):
        """
        Remove the file at <path> in the DFS.

        Args:
            path (str): path to the file to be removed
        Returns:
            True when succeeds, False if Fabric fails.
        """
        out = run('hadoop fs -rm %s' % path)

        if out.failed:
            return False
        else:
            return True


    def dfs_cat(self, path):
        """
        Displays the file located at <path> in the DFS.

        Args:
            path (str): path of the file to have it's content displayed
        Returns:
            content of file when succeeds, False if Fabric fails.
        """
        out = run('hadoop fs -cat %s' % path)

        if out.failed:
            return False
        else:
            return out


    def dfs_format(self):
        """
        Formats the Distributed File System.

        Returns:
            True when succeeds, False if Fabric fails.
        """
        out = run('hadoop namenode -format')

        if out.failed:
            return False
        else:
            return True

#
# if __name__ == "__main__":
#
#     i = hadoopHandler("pc05", "userhadoop", "user")
#     #i = hadoopHandler("pc18", "test", "test")
#     print i.job_status("job_201307180952_0001")
#     #print i.pheno_run("~/input9.txt", "~/output4")