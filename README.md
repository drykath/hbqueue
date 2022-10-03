# hbqueue
HandBrake Transcoding Queue

Looks for JSON files that the HandBrake GUI exports, and then feeds them
one by one into the HandBrake CLI. It's a fairly simple script, but is
designed to serve a few goals:

* Allow transcoding to happen on different device(s) than where the job
is configred;
* Be a little more resiliant and flexible than leaving the GUI running
somewhere;
* Do what work is available and which needs to be done, when all the
pieces are in place, and then patiently wait for more work to arrive.

The CPU's that are doing the work might be local, elsewhere nearby on
the network, or even far away in the cloud where you could exchange
bandwidth for a reduced power bill.

The script validates it can find the source file using the same absolute
path as defined in each job, and if it can't find it there, looks for
the file in the same directory as the job definition json file. That way
if your filesystem mount paths are different between systems, it should
still find the file. If you're transferring your source files around
make sure to use something that makes the file appear only at the end of
the transfer (i.e. use `rsync` and not `rsync --inplace`.)

Similarly, in case the paths are different, it'll remap the output path
to write everything to a single directory. This will probably be made an
optional parameter soon. If it sees the destination file is already
there it assumes it's done, and skips it. This lets multiple computers
work on the same jobs at once, so long as they can all see the same
output directory.

The glob search and file evaluation is done between each transcode job.
As such it'll usually work on the same json queue file until done, but
occasionally it'll pick up a different queue file if the glob returns
something else first, usually when something is added and the source
directory changes.

It tries to write some status files out. It'll write a "doing" file with
its pid next to the queue json file it's working on, as well as write a
"todo" file there when it's done with a job. The "todo" is written based
on what the script sees when the job *starts*, though, so if you have
multiple instances of the script running, the todo file might not be
accurate. There's a `listoutputs.py` script that prints out the expected
files from a given queue json file so you can make sure you have
everything that you expect.

To use this:

1. Drop your source materials somewhere that can be seen by multiple
systems. This could be on a shared file server or such where the same
files can be seen at the same time, or you can arrange for the files to
be transferred separately.
2. Set up the jobs in the HandBrake GUI. Add the jobs to the queue, but
don't start them. (Unless you really want to have it happen now; I'm not
going to tell you how to live your life.)
3. Bring up the Queue, and then under Options select Export Queue.
4. Save the .json file somewhere it can be found using the glob search
as described above.
5. Clear the Queue so you can start building up the next set of jobs.
6. Patiently wait for the processing to complete.

