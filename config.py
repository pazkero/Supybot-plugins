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

from supybot import conf, registry
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('SPI')
except:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x


def configure(advanced):
    # This will be called by supybot to configure this module.  advanced is
    # a bool that specifies whether the user identified themself as an advanced
    # user or not.  You should effect your configuration by manipulating the
    # registry as appropriate.
    from supybot.questions import expect, anything, something, yn
    conf.registerPlugin('SPI', True)


SPI = conf.registerPlugin('SPI')
# This is where your configuration variables (if any) should go.  For example:
# conf.registerGlobalValue(SPI, 'someConfigVariableName',
#     registry.Boolean(False, _("""Help for someConfigVariableName.""")))

## TODO: All configuration is global because it doesn't matter...
## ...But "channel" should probably be Network specific

conf.registerGlobalValue(SPI, 'channel',
     registry.String("#spi", _("""Channel on which votes and logging happen.""")))
conf.registerGlobalValue(SPI, 'logKeyword',
     registry.String("*GAVEL*", _("""Keyword to begin/stop log collection.""")))
## For GitLab API v4, we need the project ID and the file path + a personal token
conf.registerGlobalValue(SPI, 'pushID',
     registry.String("57556745", _("""Project ID in GitLab for auto-push. Can be gotten from web interface.""")))
conf.registerGlobalValue(SPI, 'pushPath',
     registry.String("meetings/logs", _("""Path in the pushID repository to send files. It should have a folder per year. DO NOT include a trailing slash.""")))
conf.registerGlobalValue(SPI, 'pushToken',
     registry.String("", _("""GitLab Personal Token for pushURL. Project tokens may not work.""")))

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
