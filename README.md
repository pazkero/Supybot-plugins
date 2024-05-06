Collection of utilities for Software in the Public Interest, Inc.

Commands:

- !poll [question] [voters list]
  - [requires capability] Creates a poll
  - example: !poll "should you use this bot?" ChanServ NickServ jack testuser
- !vote <yes/no/abstain>
  - Votes on a poll. You must be in voters list
- !close
  - Closes a running vote
- \*GAVEL\*
  - Triggers log collection, and saves all logs to file once finished.
  - Then it uploads the log file to a git repository and announces the URL.

Configuration variables:
- Supybot.plugins.SPI.channel
  - The channel on which polls and log collection may happen
- Supybot.plugins.SPI.logKeyword
  - The keyword which when said triggers log collection
- Supybot.plugins.SPI.pushID
  - The GitLab Project ID for the log upload
- Supybot.plugins.SPI.pushPath
  - The path in the repository to where the file will be uploaded to. No year and no end slash.
- Supybot.plugins.SPI.pushToken
  - The project token to push the commit. If missing, then log collection will be disabled.

