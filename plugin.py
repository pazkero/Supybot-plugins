###
# Copyright (c) 2024, Software in the Public Interest, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

from supybot import utils, plugins, ircdb, ircutils, callbacks
from supybot.commands import *
from supybot.i18n import PluginInternationalization

import datetime

_ = PluginInternationalization('SPI')

##You will typically obtain the current channel name using the channel converter (in commands with a <channel> argument) or msg.channel (in other methods); and the network name with irc.network.
##self.registryValue('channel')
##self.registryValue('air', '#channel', 'network')

class SPI(callbacks.Plugin):
    """Collection of utilities for Software in the Public Interest, Inc."""

    def __init__(self, irc):
        # Make sure to call the superclass' constructor when you define a custom one
        super().__init__(irc)
        self.logging = False
        self.voting = False
        self.nicklist=[]
        self.votes={}
        self.reason=""

    ###########################################################################
    @wrap(['nonInt', many('anything')])
    def poll(self, irc, msg, args, reason, voters):
        """<question> <voter1> [<voter2> ...]

        Initiates a poll with <question> and with a certain allowed voter list.
        """
        ## Validate the channel as a safeguard
        if not irc.isChannel(self.registryValue('channel')):
            irc.errorInvalid(_('channel'), self.registryValue('channel'), Raise=True)

        ## (Not necessary due to weird setup)
        #if msg.channel != self.registryValue('channel'):
        #    irc.error('Votes cannot be started on this channel.', Raise=True)

        ## Check if a poll is already running
        if self.voting:
            irc.error('A vote is already in progress. Close it with !close', Raise=True, notice=True)

        ## Authentication
        if (not ircdb.checkCapability(msg.prefix, "admin") and
           not ircdb.checkCapability(msg.prefix, "owner")):
            irc.error('You need owner or admin capability to start or close polls.', Raise=True, notice=True)

        ## Begins the poll and configure it
        self.voting = True
        self.nicklist = voters
        self.reason = reason
        nicklist = str(repr(self.nicklist))
        nicklist = nicklist.replace('[','').replace(']','').replace(' ','')

        ## Send the vote start message to the configured channel
        irc.reply("Voting started, %d people (%s) allowed to vote on %s. You may vote yes/no/abstain only, type !vote \$yourchoice now." % (
                  len(self.nicklist),
                  nicklist,
                  self.reason), to=self.registryValue('channel'))

    ###########################################################################
    @wrap(['nonInt'])
    def vote(self, irc, msg, args, vote):
        """<vote>

        Votes in current poll. <vote> must be "yes", "no" or "abstain".
        """

        ## Check if a poll is currently running
        if not self.voting:
            irc.error('No vote is currently running. Start one with !poll', Raise=True, notice=True)

        ## Check if you're allowed to vote
        if not msg.nick in self.nicklist:
            irc.error('You are not allowed to vote on this poll.', Raise=True, notice=True)

        ## Record the vote
        self.votes[msg.nick] = vote

        ## Reply in a notice if it worked or if the vote was invalid
        if vote in ["yes", "no", "abstain"]:
            irc.replySuccess(notice=True)
        else:
            irc.reply('Vote should be "yes", "no" or "abstain".', notice=True)

    ###########################################################################
    @wrap
    def close(self, irc, msg, args):
        """takes no arguments

        Closes the current vote and announce results.
        """

        ## If no vote is running, it cannot be closed
        if not self.voting:
            irc.error('No vote is currently running. Start one with !poll', Raise=True, notice=True)

        ## TODO Authentication
        #if not ircdb.checkCapability(msg.prefix, "admin") and
        #   not ircdb.checkCapability(msg.prefix, "owner"):
        #    irc.error('You need owner or admin capability to start or close polls.', Raise=True, notice=True)

        ## Disable the vote
        self.voting = False

        ## Prepare for tallying
        yes = 0; no = 0; abstain = 0
        nicklist = list(self.nicklist)

        ## Tally the result (ugly~ish code)
        for k in list(self.votes.keys()):
            if self.votes[k].strip().lower() == "yes":
                yes += 1; nicklist.remove(k)
            elif self.votes[k].strip().lower() == "no":
                no += 1; nicklist.remove(k)
            elif self.votes[k].strip().lower() == "no":
                abstain += 1; nicklist.remove(k)

        ## Check who is missing, and send the results
        missing = len(nicklist)
        nicklist = str(repr(nicklist))
        nicklist = nicklist.replace('[','').replace(']','').replace(' ','')
        irc.reply("Current voting results for \"%s\": Yes: %d, No: %d, Abstain: %d, Missing: %d (%s)" % (self.reason, yes, no, abstain, missing, nicklist), to=self.registryValue('channel'))

        ## Announce the vote is over and clean-up
        irc.reply("Voting for \"%s\" closed." % self.reason, to=self.registryValue('channel'))
        self.nicklist=[]
        self.votes={}
        self.reason=""

    ###########################################################################

Class = SPI


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=81:
