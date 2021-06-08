# -*- python -*-
# ex: set filetype=python:
import os

from buildbot.plugins import *

# This is a sample buildmaster config file. It must be installed as
# 'master.cfg' in your buildmaster's base directory.

# This is the dictionary that the buildmaster pays attention to. We also use
# a shorter alias to save typing.
c = BuildmasterConfig = {}

####### WORKERS

# The 'workers' list defines the set of recognized workers. Each element is
# a Worker object, specifying a unique worker name and password.  The same
# worker name and password must be configured on the worker.
c['workers'] = [worker.Worker("example-worker", "pass")]

# 'protocols' contains information about protocols which master will use for
# communicating with workers. You must define at least 'port' option that workers
# could connect to your master with this protocol.
# 'port' must match the value configured into the workers (with their
# --master option)
c['protocols'] = {'pb': {'port': 9989}}

####### CHANGESOURCES

# the 'change_source' setting tells the buildmaster how it should find out
# about source code changes.  Here we point to the buildbot version of a python hello-world project.

repo_url = 'https://github.com/Mitan/buildbot-test-repo.git'

c['change_source'] = []
c['change_source'].append(changes.GitPoller(
        gitbin='C:/Program Files/Git/cmd/git.exe',
        repourl=repo_url,
        workdir='gitpoller-workdir', branch='init-branch',
        pollInterval=30))

c['buildbotNetUsageData'] = None
####### SCHEDULERS

# Configure the Schedulers, which decide how to react to incoming changes.  In this
# case, just kick off a 'runtests' build

c['schedulers'] = []
c['schedulers'].append(schedulers.SingleBranchScheduler(
                            name="all",
                            change_filter=util.ChangeFilter(branch='master'),
                            treeStableTimer=None,
                            builderNames=["runtests"]))
c['schedulers'].append(schedulers.ForceScheduler(
                            name="force",
                            builderNames=["runtests"]))

####### BUILDERS

# The 'builders' list defines the Builders, which tell Buildbot how to perform a build:
# what steps, and which workers can execute them.  Note that any particular build will
# only take place on one worker.

root_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

step_transfer_flake8_config = steps.FileDownload(mastersrc=os.path.join(root_dir, '.flake8'),
                                                 workerdest='.flake8',
                                                 name=f'download flake8')
factory = util.BuildFactory()

# check out the source
factory.addStep(steps.Git(repourl=repo_url, mode='incremental'))
# run the tests (note that this will require that 'trial' is installed)
factory.addStep(step_transfer_flake8_config)
factory.addStep(steps.ShellCommand(command=["flake8", "--format=html", "--htmldir=./html"],
                                   env={"PYTHONPATH": "."}))

c['builders'] = []
c['builders'].append(
    util.BuilderConfig(name="runtests",
      workernames=["example-worker"],
      factory=factory))

####### BUILDBOT SERVICES

# 'services' is a list of BuildbotService items like reporter targets. The
# status of each build will be pushed to these targets. buildbot/reporters/*.py
# has a variety to choose from, like IRC bots.

c['services'] = []

####### PROJECT IDENTITY

# the 'title' string will appear at the top of this buildbot installation's
# home pages (linked to the 'titleURL').

c['title'] = "Hello World CI"
c['titleURL'] = "https://github.com/Mitan/buildbot-test-repo/"

# the 'buildbotURL' string should point to the location where the buildbot's
# internal web server is visible. This typically uses the port number set in
# the 'www' entry below, but with an externally-visible host name which the
# buildbot cannot figure out without some help.

c['buildbotURL'] = "http://localhost:8010/"

# minimalistic config to activate new web UI
c['www'] = dict(port=8010,
                plugins=dict(waterfall_view={}, console_view={}, grid_view={}))

####### DB URL

c['db'] = {
    # This specifies what database buildbot uses to store its state.
    # It's easy to start with sqlite, but it's recommended to switch to a dedicated
    # database, such as PostgreSQL or MySQL, for use in production environments.
    # http://docs.buildbot.net/current/manual/configuration/global.html#database-specification
    'db_url' : "sqlite:///state.sqlite",
}
