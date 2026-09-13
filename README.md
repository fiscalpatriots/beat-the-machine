# Second Pass: Beat the Machine

A ten minute reviewer's game for the George Mason ACFE student chapter. An AI assistant wrote
Halyard's June close commentary, and the player is the second pass on it.

Live at https://fiscalpatriots.github.io/beat-the-machine/ from `main`.

**Start here for reviewers:** [review.html](review.html), the whole entry on one page, live at
https://fiscalpatriots.github.io/beat-the-machine/review.html

## For reviewers of the AINA entry

The game is the front end of a review workflow rather than a quiz. A close produces a ledger. An
AI assistant drafts the month's commentary from it. Second Pass checks that draft. A reviewer
signs off, and only the reviewer signs off. The screen "How this works in a real close" says the
same thing on the page, one tap from the intro screen and one tap from the end screen, with the
flow drawn as four boxes.

A memo fails in six ways, and they split into two groups that need different things.

Four are machine-checkable: arithmetic, wrong direction, threshold and silence. A script
recomputes every figure and percent in every sentence against the ledger, tests each direction
word against the sign of the movement, lists every account that clears both legs of the
materiality threshold, and from that list names every account no sentence mentions. None of that
needs a person.

Two are reviewer judgment: invented driver and timing. Both need the facts on file and somebody
who knows the business, so both stay with the human.

The entry also has to show learning rather than performance, so the round does not end with the
fourteen trained lines. A second company follows, five lines the player has never seen, scored
on its own, and the sheet carries both numbers so the findings can say whether a catch rate
holds up on material nobody coached them through.

**Scope.** This build is a static case: fourteen lines and five fresh ones, one month, answers
keyed by hand. It does
not run on a live ledger, and the four mechanical checks run on any ledger and memo in the
checker on this site; driver and timing stay with the reviewer. Next, the deterministic checks
run first on every AI memo, and the reviewer's time goes only to the two judgment types.

The code and the pilot records are at https://github.com/fiscalpatriots/second-pass, which is
public: `curl -s -o /dev/null -w "%{http_code}"` returned **200** signed out on 12 September 2026,
as did the game itself at https://fiscalpatriots.github.io/beat-the-machine/.

The sibling page https://fiscalpatriots.github.io/beat-the-machine/checker.html runs the four
deterministic checks on a ledger and a memo the visitor pastes in, and `CHECKER.md` in this
repository documents it. It is linked from the intro screen's link row and from the top of the
"Use it on your own memo" block.

`PROTOCOL.md` is the one page a reviewer works from, and `Second-Pass-Review-Protocol.pdf` is the
same page to print or hand across a desk; both are linked from the "How this works in a real
close" screen. `EVIDENCE-LOG-TEMPLATE.csv` is the log the protocol fills in, and it is the column
order the checker's **Download CSV** writes, so an exported run drops straight into it with the
reviewer columns left blank. `GOVERNANCE-NOTE.md` records who signs and what the tool is not
allowed to decide.

### How the game's data feeds the findings

Every round posts to the Google Form described under "Where the data lands", and four measures
come straight out of the responses sheet without any hand coding.

| Measure | Where it comes from |
| --- | --- |
| Responses by organization | The chapter chips tapped on the second screen, posted in question A. One player may belong to more than one, so the counts sum above the response count and each is read as its own denominator. |
| Catch rate by error type | The fourteen "Why" fields each carry the line, the account, the call, the key and the error type, so grouping on the type column gives a catch rate per type. The eight flagged lines carry `arithmetic` twice, `wrong account` twice, and `wrong direction`, `no explanation`, `invented driver` and `timing` once each; the six clean lines carry `clean line` and are the control. The card labels and the screen's six are close but not word for word the same. `no explanation` is what the screen calls silence, `wrong account` is a form of invented driver where the memo names a driver another account contradicts, and threshold is the machine test that decides which lines owe commentary at all rather than a label of its own. |
| False-flag rate | The six lines whose key is `stand` are the denominator. A `flag` call on any of them is a false flag, and question B carries the round's false flag count as well. |
| Lap time | The clock runs from the first card to the last call and posts as whole minutes in the elapsed time question, off the clock rather than off a tap. |
| Fresh case transfer rate | Question C (`entry.756559246`) opens with `Round2: 4/5; calls FSFSF; key FSFSF; seconds 61.` The fraction is the score on the five lines of a company the player had never seen, the two letter strings are the five calls and the five keyed answers in card order with `F` for flag and `S` for let it stand, and the seconds are the round two clock. Transfer is that fraction over the main fourteen expressed the same way, so a player at 12 of 14 and 4 of 5 reads 85.7 percent trained against 80.0 percent fresh. |

Read together these say which error types a reviewer catches unaided, which ones cost them time
they did not have, how much of the work the deterministic checks could have taken off the desk
before anybody read a sentence, and whether what a player learned on Halyard survives a company
they have never opened.

### Reading the two headline numbers off the sheet

Both of these come out of the responses sheet with no hand coding, and both are worth stating in
the findings.

**Count by organization.** Question A (`entry.117652481`) opens with `Organizations: ACFE; NABA.`
Test that column for each chapter name, for example `=COUNTIF(H2:H, "*ACFE*")`, and read each
count against the response total as its own denominator, because a player who belongs to two
chapters is counted in both. Rows filed before 12 September 2026 carry the older
`Organisations:` spelling, so reach back with `Organi*ations:` or with the chapter name, which
never changed.

**Fresh case transfer rate.** Split question C on the semicolons. The first field after
`Round2:` is the fresh score out of five, and `=AVERAGE()` over that column against the same
average on the main fourteen is the transfer rate for the whole pilot. Splitting the calls string
character by character against the key string gives a per line catch rate on the fresh case, and
the three flagged lines there are `wrong direction`, `timing` and `arithmetic`, which lets a
finding compare a type caught on Halyard with the same type caught cold on Brightwater. The
seconds field is the fresh case clock, so pace on new material can be set beside the lap time.

## The path in

Three screens stand between the link and the first card.

1. The opening screen, two short paragraphs. Three candidate wordings live in
   `INTRO-CANDIDATES.md` and the one marked live there is the one in `index.html`.
2. One screen for the codename and the chapters, on the same screen and both required.
3. The ledger, read once as orientation, with a block under it saying what earns a flag and
   what "Let it stand" means, and a single Continue.

Nothing else is asked, on the way in or after the round.

## Mason branding

Every screen carries a green band at the top with "George Mason University" and, beneath it,
"Costello College of Business", both set in type. Once the player has entered a codename it
appears in gold on the bottom edge of that band, tracking sideways so it always sits directly
above their car on the track. There is no logo file and no Patriot mark in
this repository, because those are trademarks and a text lockup is the safe way to say whose
drill this is. The footer line under every screen reads "A drill by the ACFE student chapter and
Beta Alpha Psi Theta Alpha at Mason".

The colors are the published university values, not approximations:

| Name | Hex | Where it is used |
| --- | --- | --- |
| George Mason Green | `#005239` | the band, headings, the rank, the car, the chequered flag, the traveled track |
| George Mason Gold | `#ffc733` | the rule under the band, the car cabin, the streak flame, earned badges, the top trophy |
| Logo Black | `#333333` | body copy, the two call buttons, badge text on gold |
| Accent, Navy | `#004f71` | the machine's voice, the account strip and the highlighted ledger row |
| Accent, Red | `#cc4824` | the wrong-call verdict and negative changes (darkened to `#a83a1c` where it sets figures) |

Those values come from the Mason brand guide color page,
https://brand.gmu.edu/brand-guide/brand-colors. The Bynder toolkit page supplied by Khaled
(`gmu.bynder.com/guidelines/guide/bd8609ea.../page/b053e82e...`) redirects to the public Brand
Toolbox root without signing in, so the color and typography values were taken from the
published brand guide pages instead.

Two brand rules shape the palette here. Accent colors are for emphasis only and never replace
green and gold, and gold may not set text on white, so gold appears as a fill with Logo Black
text on it and never as type on the paper. Every text pair on the band and on the cards clears
4.5:1 at body size, the lowest being the footer and the earned line at 5.97:1.

The type is Figtree, the university's web typeface, loaded from Google Fonts with the guidance's
own fallbacks behind it: Open Sans, then Franklin Gothic, then the system stack. If the font
request fails the page still sets correctly. Typeface guidance is at
https://brand.gmu.edu/brand-guide/fonts-and-typography.

The two call buttons stay neutral Logo Black on white. They are never green or gold, because the
choice between them has to read as even.

## The ledger

The ledger screen is a statement, not a list. A header block names the company and the close.
Each account occupies three rows on a phone: the name and the account number, then May and June
on one line and Change and Percent on the next, right aligned tabular figures at 15px on 20px
gutters, with a slim movement bar under them scaled to the largest absolute change in the month.
Stacking the figures two to a line is what lets every column hold full type with thousands
separators inside a 375px phone with no sideways scrolling; from 480px up the four sit on one
line. Negative changes print in a muted red. Revenue, cost of sales, operating expenses and
financing each carry a subtotal, and a net line closes the statement. Interest expense reports
in financing rather than inside operating expense, so total operating expenses reads $1,000,300
in May and $1,188,800 in June and total financing reads $61,200 and $92,400.

Nothing is tapped there. The Ledger button on every card and every reveal reopens the same
component as a slide up sheet, with the account under review highlighted by a gold left border
and a gold tint, and scrolled to. That account also prints as a strip at the top of its card.
One control opens the sheet and only one: the full width "See the full ledger" button under the
strip on every card and every reveal, taller than 44px. The first card adds a one time hint line
under it.

From 1200px up the same row reads as one line: the account number in a monospace column, the
name at a fixed width that ellipses rather than pushing the figures together, then May and June
at 116px, Change at 112px and Percent at 72px as right aligned tabular columns at 16px on 20px
gutters, and last a 72px column holding the movement bar on its own. The bar is a 6px rounded
track at eight percent ink with a fill scaled to the largest absolute percent, green where the
account rose and a muted red where it fell, and it never sits behind a figure. Subtotal and net
rows carry 14px above and below and no bar. Below 1200px the rows stack as they do on a phone.
Section headers are
small caps in green over a hairline, subtotals carry a rule above them and the net line a
heavier one, and alternate rows take a three percent green fill.

The orientation page is two columns from 900px up: the ledger on the left and a sticky legend on
the right holding "What earns a flag" with the six defect types as chips, with Continue at the
foot of both columns. On a phone the legend comes first, collapsed to its title and the six
chips until it is tapped, the ledger follows, and Continue is fixed to the bottom of the
viewport.

## The round

Fourteen accounts come one at a time. Each card carries the account's ledger strip, a two bar
picture of the movement with no figures repeated on it, the memo's sentence quoted once, and an
"On file" panel holding only facts not already visible above it. The two calls are equal weight
and neutral, with Let it stand on the left and Flag it on the right.

Every card is scored. Flagging a line that was already right costs exactly what missing a
problem costs, and the running pill reads `Right N of M` over the cards seen so far. The split
is eight problem lines and six clean ones, rebalanced on 12 September 2026 from the twelve and
two the first version carried, because twelve and two let a player flag everything and score
twelve. Neither number is ever printed for the player. Flagging all fourteen now scores eight
and lands on Trainee.

## Round two, the fresh case

After the fourteenth reveal the player meets a second company on a one screen bridge that reads
"New company, new memo, same job. Five lines." Brightwater Dental Partners is a four office
dental group, a different industry from Halyard on purpose, and its five accounts carry May and
June balances of their own. Three of its five memo lines carry a planted problem and two are
clean:

| Fresh line | Account | May | June | Change | Percent | Call | Type |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 5210 Dental supplies and lab fees | $138,500 | $191,200 | +$52,700 | 38.1% | Flag | wrong direction |
| 2 | 4010 Patient service revenue, net | $742,000 | $803,500 | +$61,500 | 8.3% | Let it stand | clean line |
| 3 | 4220 Orthodontic plan revenue | $96,000 | $138,400 | +$42,400 | 44.2% | Flag | timing |
| 4 | 6610 Marketing and patient outreach | $18,400 | $24,100 | +$5,700 | 31.0% | Let it stand | clean line |
| 5 | 6110 Hygienist wages | $214,000 | $268,900 | +$54,900 | 25.7% | Flag | arithmetic |

The threshold rule is the one the player already knows, so both clean lines turn on it: line 2
carries the largest dollar movement on the statement and still fails the percentage leg, and line
4 reads alarming at 31.0 percent and fails the dollar leg. All three types were also planted in
the Halyard memo, which is what makes a catch rate on these five comparable with the trained
fourteen.

The cards are built from `CARDS2` and the balances from `ROWS2`, and every ledger function takes
the book it is reading, so the "See the full ledger" button on a round two card opens the five
account dental statement in the same sheet component that serves Halyard's fourteen. The five
lines are scored on their own counters and never touch the rank, the trophy or the main score.

Rows filed in the Google Form before 12 September 2026 were answered against the old key and
are not comparable with anything filed since. The per-card entries still post the player's own
call unchanged, so nothing about the form mapping moved. The source of truth for the new key is
`EXERCISE-case-01-form-rev4.md` in the AINA drafts folder, with the whole case as plain text in
`REVIEW-FLAT-rev1.txt` beside it.

## The track

The progress bar is a race track drawn as one inline SVG in `buildTrack()`. Nineteen segments
since 13 September 2026, fourteen for the trained lines and five for the fresh case, with the
finish at card 19 and a gold tick at segment fourteen where the second company takes over. There
is a car that advances one segment per card, a pit lane under the main lane and a chequered flag
at the finish that lights once all nineteen are called. A right call gives the car a short forward burst with two speed lines behind it, a
wrong call drops it into the pit lane for a beat before it rejoins, and three correct calls in a
row light a flame behind it. Streaks build in three steps: two in a row gives the car a speed
trail, three adds the gold flame and a "Streak 3" toast on the reveal, and five grows both and
lights the track behind the car gold under an "On fire" toast. A wrong call ends the streak, the
trail and the flame fade out and the car takes the pit lane dip. Every animation is 250ms or
under, there is no sound, and everything is switched off under `prefers-reduced-motion: reduce`. The bar holds a fixed height from the first
paint, so nothing on the page moves when the car does.

The run is timed from the first card to the fourteenth call. The end screen prints it as
`Lap time 6:42` beside the score, with `Best streak 7` next to it, and the lap time rounded to
whole minutes is what goes into the form's elapsed minutes question. A streak of five or more
earns the "Hot lap" badge, and letting all six clean lines stand earns "Nothing over-flagged".
Nine badges can be earned and the end screen shows at most three of them. The streak carries on
into the fresh case so the car behaves the same way, and the best streak the end screen prints
stops at what the fourteen trained lines earned, because that is the number "Hot lap" reads.

The round two clock is separate from the lap time. It starts on the first fresh card and stops
on the fifth call, and it posts in seconds rather than minutes, because five lines on a company
nobody has seen is a short run.

## Spelling

American spelling throughout, in the file and in these notes. The organization chips post as
`Organizations: ...` with a z.

## The end screen

Ranks are Partner at 14, Manager at 13, Senior at 11 or 12, Staff at 9 or 10 and Trainee below
that. The end screen leads with the reward: a trophy drawn to the rank (bronze, silver, gold,
and a starred cup for a clean sweep) with a single rise and shine that respects
`prefers-reduced-motion`, the rank name, the codename, the earned line, the fresh case as
"Fresh case: 4 of 5" in a gold ringed pill under that line, the three outcomes as
caught, let stand correctly and false flags, the lap time and the best streak under those three
tiles, then the badges. Only earned badges show, at most three, as a row of medallions with the
icon in green on a paper disc inside a gold ring and the name under it, appearing on a 150ms
stagger that `prefers-reduced-motion` switches off. They are chosen in a fixed order so the best
ones survive the cut: Clean sweep, Cold read, Hot lap, Nothing over-flagged, Arithmetic hawk,
Invented driver caught, Read the silence, Right account, Timing and drift. "Cold read" is the
one badge the fresh case can earn, at five of five on Brightwater, and it sits second because
reading a company cold is the hardest thing the drill asks. A run that earns none prints
one line instead. Under that sit the share line with a Copy button and a Play again button, and
the coaching sits behind one tap below them.

Play again returns to the codename screen with the codename and the chapter chips still filled
in and the score, the streak and the clock cleared. A second run posts a fresh response through
the same entries, so repeat runs appear in the sheet as separate rows under the same codename.
Count distinct codenames, not rows, when the question is how many people played.

## Where the data lands

Every answer posts to the live form:

```
https://docs.google.com/forms/d/e/1FAIpQLSfteTMPZrDKhYmRjxPKADAZERjyDntdMLIVZMH-FoIrcHusKg/formResponse
```

All 38 questions are mapped to their `entry.NNNN` ids in the `E` object at the top of the
script, and all 38 are populated on every submission. The three pages post as one request with
`pageHistory=0,1,2`. If the post fails the player is shown their answers as copyable text and a
Try sending again button that reruns the post rather than losing the round.

Nobody types anything after the round. The fourteen calls post as `Accept` or `Reject` so the
existing multiple choice questions keep working, and every text question receives a generated
summary instead of player prose: the fourteen "Why" fields carry the call, the key and the error
type for that line, question A carries the organizations, and question B carries the lines
missed, the pattern, the result and the longest run. The elapsed minutes question receives the
lap time, off the clock rather than a tap.

Round two posts without a new question. The whole fresh case rides in question C
(`entry.756559246`), which asks the player nothing and carried only a placeholder note before 13
September 2026. The cell now opens with `Round2: 4/5; calls FSFSF; key FSFSF; seconds 61.` and
then names the company, so the sheet can be read without opening the game. The fourteen "Why"
fields were left exactly as they were, because the catch rate by error type is grouped on them.

Card one is inverted on purpose. Its form question asks the player to agree or disagree that
nothing is owed on account 4200, so flagging that line posts `Reject` while flagging any other
line posts `Accept`. Each card carries its own `post` mapping for that reason.

## The four questions that are not asked

Four questions the form marks required are not asked on screen. Three were intake questions the
three-screen path has no room for, and the fourth was the confidence tap after the round, which
came out so the last card leads straight into the send.

Until 13 September 2026 all four carried fixed values, which arrived in the responses sheet
looking exactly like participant answers and could not support any analysis. They now carry the
literal string `not asked`:

| Form question | Entry id | Posted value |
| --- | --- | --- |
| Expected quality of the commentary | `entry.53437742` | `not asked` |
| Confidence before the round | `entry.538678778` | `not asked` |
| Confidence after the round | `entry.439643836` | `not asked` |
| Month end close experience | `entry.1421470415` | `not asked` |

Empty would have been the cleaner value. The form does not take it: all four questions are marked
required, three of them are linear scales and the fourth is multiple choice, so an empty value and
an off-list string are both refused by Google Forms. **Google Forms will very probably reject a
response carrying `not asked` on these four, and the hidden iframe cannot tell a stored response
from a rejected one, so the drill may show a completion screen for a response the sheet never
received.** The player always has the local copy on the fallback screen.

The fix belongs on the form, not in the page: make those four questions optional, or delete them.
Once they are optional, change `NOT_ASKED` in `index.html` to `""`. Whoever maintains the findings
script needs to know that these four columns now read `not asked` and must not be pooled with the
numbers earlier responses carry.

The round one free text field (`entry.1115022539`) carries its own note, because the ledger screen
is orientation only and collects no picks. Question C (`entry.756559246`) was a placeholder of the
same kind until 13 September 2026 and now carries the round two string and the round two basis, so
it is the one former placeholder that is real data.

## The basis a player gives

Since 13 September 2026 every line asks for a basis between the call and the reveal. The player
taps Flag it or Let it stand, the two buttons are replaced in place by a chip row, and the reveal
waits until at least one chip is tapped. The memo, the figures and the On file facts stay on
screen underneath, so nothing has to be remembered to answer.

The chips are: figure does not tie; direction wrong; no source on file; wrong period; wrong
account; nothing written where owed. A let-it-stand also offers "the figure and reason hold",
first in the row. More than one chip is allowed and at least one is required. On a flag, an
optional single line field, "In your words (optional)", appears under the chips. It never blocks.

Both ride into the fourteen per-line Why fields the form already has, ahead of the generated
metadata, in this shape:

```
Basis: no source on file; wrong period | Words: the freight moved || Line 12, account 4000.
Called: flag. Key: flag. Type: unsupported attribution. Correct.
```

Split the cell on ` || ` to separate what the player said from what the page computed. The five
fresh lines have no Why field of their own, so their basis rides at the end of question C.

## Counting the organizations

The intake screen asks which chapters the player belongs to, multi-select, at least one. The
taps ride at the front of question A (`entry.117652481`) behind a fixed prefix, so no new form
question was needed. The cell reads:

```
Organizations: ACFE; NABA. Not collected. The ledger screen is orientation only in this version.
```

The prefix used to read `Organisations:` with an s. Rows filed before 12 September 2026, which
includes the AUDIT-TEST-DELETE test row, carry that older British form, so a count that has to
reach back through them should test for `Organi*ations:` or simply for the chapter name, which
is unchanged either way.

The seven chips are Beta Alpha Psi, ACFE, ASM, NABA, AAA, GMU Student and Professor. To count a chapter in
the responses sheet, test the question A column for the name, for example
`=COUNTIF(H2:H, "*ACFE*")`. A player who tapped two chapters counts in both, which is what a
multi-select means, so the chapter counts sum to more than the number of responses. Count
players with `=COUNTA(...)` on the codename column instead.

## If the form is ever rebuilt

Rebuilding the Google Form issues new `entry.NNNN` ids. Fetch the responder page, read the ids
out of the `FB_PUBLIC_LOAD_DATA_` block, and replace the `E` object and `FORM_POST` URL. Nothing
else in the file depends on the form.

## The answer key and the case files

Since 13 September 2026 both cases live outside the page, in `cases/halyard-v3.json` and
`cases/brightwater-v2.json`. Each file carries the company, the threshold policy, the ledger
rows, the memo sentences, the On file facts as verified case assumptions, the key, the error
type, the reveal reason, the tell, and its own version and date. `cases/README.md` explains the
format, the differences from the checker's Halyard sample, and what changed in this revision.

The page fetches both files at load. When the fetch fails, which is what happens when the file is
opened from a folder rather than served, it falls back to a generated copy written into
`index.html` between the `BUILD:CASES-START` and `BUILD:CASES-END` markers. Edit the JSON, then
run `node build-cases.cjs` to rewrite that copy. The script refuses to write if a card points at
an account that is not in the ledger, if a card's figures do not tie, or if a card is missing its
key, its reason or its tell.

The key is `flag` on eight of the fourteen Halyard lines and `stand` on the six clean ones; three
of the five Brightwater lines are `flag` and two are `stand`. Anyone who reads the source can read
the key, in the JSON as easily as in the page. That is the trade for instant feedback, and it is
the reason to send the link and not the file.

The error types are wrong direction, unsupported driver, unsupported attribution, wrong account,
timing, arithmetic, no explanation and clean line. "No explanation" covers the one line where the
memo says nothing about an account that owes commentary. "Unsupported driver" replaced "invented
driver" on 13 September 2026, because a sentence with nothing behind it is not established from
the supplied evidence, which is a different and smaller claim than saying it was fabricated.

A flag can be correct while the reason behind it is wrong. The reveals credit the call and correct
the reasoning separately, and they ask for a bridge (billing bridge, payroll bridge, reserve
rollforward, depot revenue bridge) rather than handing the player a derived cause.

The version and date of both cases ride into question A and into the local copy, so a response can
always be tied to the key it was scored against. Never pool responses scored against different
case versions.

## Deploying

`index.html`, `cases/halyard-v3.json` and `cases/brightwater-v2.json`. No libraries. The only
build step is `node build-cases.cjs`, which refreshes the inline fallback inside `index.html` and
has to be run after any edit to either case file. The only outbound request is the Figtree
stylesheet from Google Fonts. Commit to `main` and push;
GitHub Pages serves the root of `main` and the change is live within a minute or two.

```
git add -A && git commit -m "..." && git push
curl -s https://fiscalpatriots.github.io/beat-the-machine/index.html | diff - index.html
```

The source of truth for the content is
`Coach Dashboard HQ/drafts-2026-09-05-aina/EXERCISE-case-01-form-rev4.md`.
