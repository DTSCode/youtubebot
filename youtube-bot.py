#!/usr/bin/env python2.7

import sys, re, pafy

from twisted.words.protocols import irc
from twisted.internet import protocol, reactor

class YoutubeBot(irc.IRCClient):
  def _get_nickname(self):
    return self.factory.nickname

  nickname = property(_get_nickname)

  def signedOn(self):
    self.join(self.factory.channel)
    print 'Signed on as %s.' % (self.nickname,)

  def joined(self, channel):
    print 'Joined %s.' % (channel,)

  def privmsg(self, user, channel, msg):
    youtube_urls = re.findall('http[s]?:\/\/(www\.youtube\.com\/watch\?v=[a-zA-Z0-9_\-]*)|(youtu\.be/[a-zA-Z0-9_\-]*)+', msg)
    response = []

    for url in youtube_urls:
        video = pafy.new(url)
        response.append("[{video_title} ({duration})]".format(video_title=video.title, duration=video.duration))

    self.msg(channel, ' '.join(response))
    
    print msg

class YoutubeBotFactory(protocol.ClientFactory):
  protocol = YoutubeBot

  def __init__(self, channel, nickname):
    self.channel = channel
    self.nickname = nickname

if __name__ == '__main__':
  reactor.connectTCP('irc.freenode.net', 6667, YoutubeBotFactory(sys.argv[2], sys.argv[1]))
  reactor.run()
