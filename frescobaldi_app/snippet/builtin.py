# This file is part of the Frescobaldi project, http://www.frescobaldi.org/
#
# Copyright (c) 2008 - 2011 by Wilbert Berendsen
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
# See http://www.gnu.org/licenses/ for more information.

"""
Builtin snippets.
"""

from __future__ import unicode_literals

import __builtin__
import collections

# postpone translation
_ = lambda *args: lambda: __builtin__._(*args)


T = collections.namedtuple("Template", "title text")


builtin_snippets = {

'blankline': T(_("Blank Line"),
r"""
$CURSOR
"""),


'quotes_s': T(_("Single Typographical Quotes"),
"""-*- menu: quotes;
\u2018$SELECTION\u2019"""),


'quotes_d': T(_("Double Typographical Quotes"),
"""-*- menu: quotes;
\u201C$SELECTION\u201D"""),


'voice1': T(None,
r"""-*- name: v1;
\voiceOne"""),


'voice2': T(None,
r"""-*- name: v2;
\voiceTwo"""),


'voice3': T(None,
r"""-*- name: v3;
\voiceThree"""),


'voice4': T(None,
r"""-*- name: v4;
\voiceFour"""),


'1voice': T(None,
r"""-*- name: 1v;
\oneVoice"""),


'times23': T(_("Tuplets"),
r"""-*- menu: blocks; selection: strip;
\times 2/3 { $SELECTION }"""),


'onceoverride': T(None,
r"""-*- name: oo;
\once \override """),


'm22': T(_("Modern 2/2 Time Signature"),
r"""-*- name: 22;
\numericTimeSignature
\time 2/2"""),


'm44': T(_("Modern 4/4 Time Signature"),
r"""-*- name: 44;
\numericTimeSignature
\time 4/4"""),


'tactus': T(_("Tactus Time Signature (number with note)"),
r"""-*- name: tac;
\once \override Staff.TimeSignature #'style = #'()
\once \override Staff.TimeSignature #'stencil = #ly:text-interface::print
\once \override Staff.TimeSignature #'text = \markup {
  \override #'(baseline-skip . 0.5)
  \column { \number $CURSOR1$ANCHOR \tiny \note #"2" #-.6 }
}
"""),


'ly_version': T(_("LilyPond Version"),
r"""-*- menu;
\version "$LILYPOND_VERSION"
"""),


'repeat': T(_("Repeat"),
r"""-*- menu: blocks; name: rep; selection: strip; symbol: bar_repeat_start;
\repeat volta 2 { $SELECTION }"""),


'relative': T(_("Relative Music"),
r"""-*- name: rel;
\relative c$CURSOR'$ANCHOR {
""" '  ' r"""  
}"""),


'uppercase': T(_("Upper case selection"),
r"""-*- python; selection: yes, keep;
text = text.upper()
"""),


'lowercase': T(_("Lower case selection"),
r"""-*- python; selection: yes, keep;
text = text.lower()
"""),


'titlecase': T(_("Title case selection"),
r"""-*- python; selection: yes, keep;
text = text.title()
"""),


'markup': T(_("Markup"),
r"""-*- name: m; selection: strip;
\markup { $SELECTION }"""),


'markup_lines_selection': T(_("Markup lines"),
r"""-*- name: l; python; selection: yes, keep, strip;
text = '\n'.join(r'\line { %s }' % l for l in text.splitlines())
if state[-1] != 'markup':
    text = '\\markup {\n%s\n}' % text
"""),


'markup_column': T(_("Markup column"),
r"""-*- name: c; selection: yes, keep, strip;
\column { $SELECTION }"""),


'tagline_date_version': T(_("Tagline with date and LilyPond version"),
r"""tagline = \markup {
  Engraved at
  \simple #(strftime "%Y-%m-%d" (localtime (current-time)))
  with \with-url #"http://lilypond.org/"
  \line { LilyPond \simple #(lilypond-version) (http://lilypond.org/) }
}
"""),


'header': T(_("Header Template"),
r"""-*- name: h;
\header {
  title = "$CURSOR"
  composer = ""
  tagline = \markup {
    Engraved at
    \simple #(strftime "%Y-%m-%d" (localtime (current-time)))
    with \with-url #"http://lilypond.org/"
    \line { LilyPond \simple #(lilypond-version) (http://lilypond.org/) }
  }
}
"""),


'no_tagline': T(_("No Tagline"),
r"""-*- name: nt; python;
text = 'tagline = ##f'
if state[-1] != 'header':
    text = '\\header {\n%s\n}' % text
"""),


'no_barnumbers': T(_("No Barnumbers"),
r"""-*- name: nb; python;
text = r'\remove "Bar_number_engraver"'
if state[-1] not in ('context', 'with'):
    text = '\\context {\n\\Score\n%s\n}' % text
    if state[-1] != 'layout':
        text = '\\layout {\n%s\n}' % text
"""),


'staff_size': T(_("Staff Size"),
r"""-*- name: ss; python;
if state[-1] == 'music':
    text = (
        "\\set Staff.fontSize = #-1\n"
        "\\override Staff.StaffSymbol #'staff-space = #(magstep -1)\n")
else:
    text = (
        "fontSize = #-1\n"
        "\\override StaffSymbol #'staff-space = #(magstep -1)")
    if state[-1] == 'new':
        text = '\\with {\n%s\n}' % text
    elif state[-1] not in ('context', 'with'):
        text = '\\context {\n\\Staff\n%s\n}' % text
        if state[-1] != 'layout':
            text = '\\layout {\n%s\n}' % text
"""),


'comment': T(_("Comment"),
r"""-*- python; indent: no;
# determine state
for s in state[::-1]:
  if s in ('lilypond', 'html', 'scheme'):
    break
else:
  s = 'lilypond'

def html():
  if text:
    return '<!-- ' + text + ' -->'
  else:
    return ['<!-- ', CURSOR, ' -->']

def lilypond():
  if text:
    return '%{ ' + text + '%}'
  else:
    return '% '

def scheme():
  if text:
    return '; ' + text.replace('\n', '\n; ')
  else:
    return '; '

if s == 'lilypond':
  text = lilypond()
elif s == 'html':
  text = html()
elif s == 'scheme':
  text = scheme()
"""),


'paper_a5': T(_("A5 Paper"),
r"""-*- name: a5; python;
text = r'#(set-paper-size "a5")'
if state[-1] != 'paper':
    text = '\\paper {\n%s\n}' % text
"""),


'last_note': T(_("Last note or chord"),
r"""-*- python; menu: music; symbol: note_4d;
# This snippet reads back the last entered note or chord and 
# inserts it again. It removes the octave mark from a note of the first
# note of a chord if the music is in relative mode.

from PyQt4.QtGui import QTextCursor
import cursortools
import tokeniter
import ly.lex.lilypond as lp

# look back
block = cursortools.block(cursor)
tokens = tokeniter.partition(cursor).left

# space needed before cursor?
beforecursor = block.text()[:cursor.selectionStart()-block.position()]
spaceneeded = bool(beforecursor and beforecursor[-1] not in "\t ")

chordstart, chordend = None, None
notestart = None
relative = False
found = False

while True:
  pos = block.position()
  for t in tokens[::-1]:
    if t == '\\relative':
      relative = True
      break
    elif isinstance(t, (lp.Score, lp.Book, lp.BookPart, lp.Name)):
      break
    if found:
      continue
    if chordend is not None:
      if isinstance(t, lp.ChordStart):
        chordstart = pos + t.pos
        found = True
      continue
    if isinstance(t, lp.ChordEnd):
      chordend = pos + t.pos + len(t)
    elif isinstance(t, lp.Note) and t not in ('R' ,'q', 's', 'r'):
      notestart = pos + t.pos
      found = True
  block = block.previous()
  if block.isValid():
    tokens = tokeniter.tokens(block)
    continue
  break

if found:
  c = QTextCursor(block)
  if chordstart is not None:
    text = []
    removeOctave = 1 if relative else 0
    c.setPosition(chordstart)
    c.setPosition(chordend, c.KeepAnchor)
    for t in tokeniter.Source.selection(c):
      # remove octave from first pitch in relative
      if isinstance(t, lp.Note):
        removeOctave -= 1
      elif isinstance(t, lp.Octave) and removeOctave == 0:
        continue
      text.append(t)
    text = ''.join(text)
  elif notestart is not None:
    text = []
    c.setPosition(notestart)
    for t in tokeniter.Source.fromCursor(c):
      if isinstance(t, lp.Note):
        text.append(t)
      elif not relative and isinstance(t, lp.Octave):
        text.append(t)
      else:
        break
    text = ''.join(text)
  if spaceneeded:
    text = " " + text
"""),


'color_dialog': T(_("Color"),
r"""-*- name: col; python; icon: applications-graphics;

# Insert a color from a dialog


from PyQt4.QtGui import QColorDialog
colors = {
    (0, 0, 0): "black",
    (255, 255, 255): "white",
    (255, 0, 0): "red",
    (0, 255, 0): "green",
    (0, 0, 255): "blue",
    (0, 255, 255): "cyan",
    (255, 0, 255): "magenta",
    (255, 255, 0): "yellow",
    (128, 128, 128): "grey",
    (128, 0, 0): "darkred",
    (0, 128, 0): "darkgreen",
    (0, 0, 128): "darkblue",
    (0, 128, 128): "darkcyan",
    (128, 0, 128): "darkmagenta",
    (128, 128, 0): "darkyellow",
}

color = QColorDialog.getColor()
rgb = color.getRgb()[:-1]

if rgb in colors:
    text = '#' + colors[rgb]
else:
    rgb = tuple(map(lambda v: format(v / 255.0, ".4"), rgb))
    text = "#(rgb-color {0} {1} {2})".format(*rgb)
"""),


}

