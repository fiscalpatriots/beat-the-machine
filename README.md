# Second Pass: Beat the Machine

A ten minute reviewer's game for the George Mason ACFE student chapter. An AI assistant wrote
Halyard's June close commentary, and the player is the second pass on it.

Live at https://fiscalpatriots.github.io/beat-the-machine/ from `main`.

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

**Scope.** This build is a static case: fourteen lines, one month, answers keyed by hand. It does
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

Read together these say which error types a reviewer catches unaided, which ones cost them time
they did not have, and how much of the work the deterministic checks could have taken off the
desk before anybody read a sentence.

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

Rows filed in the Google Form before 12 September 2026 were answered against the old key and
are not comparable with anything filed since. The per-card entries still post the player's own
call unchanged, so nothing about the form mapping moved. The source of truth for the new key is
`EXERCISE-case-01-form-rev4.md` in the AINA drafts folder, with the whole case as plain text in
`REVIEW-FLAT-rev1.txt` beside it.

## The track

The progress bar is a race track drawn as one inline SVG in `buildTrack()`. Fourteen segments,
a car that advances one segment per card, a pit lane under the main lane and a chequered flag at
the finish. A right call gives the car a short forward burst with two speed lines behind it, a
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
Eight badges can be earned and the end screen shows at most three of them.

## Spelling

American spelling throughout, in the file and in these notes. The organization chips post as
`Organizations: ...` with a z.

## The end screen

Ranks are Partner at 14, Manager at 13, Senior at 11 or 12, Staff at 9 or 10 and Trainee below
that. The end screen leads with the reward: a trophy drawn to the rank (bronze, silver, gold,
and a starred cup for a clean sweep) with a single rise and shine that respects
`prefers-reduced-motion`, the rank name, the codename, the earned line, the three outcomes as
caught, let stand correctly and false flags, the lap time and the best streak under those three
tiles, then the badges. Only earned badges show, at most three, as a row of medallions with the
icon in green on a paper disc inside a gold ring and the name under it, appearing on a 150ms
stagger that `prefers-reduced-motion` switches off. They are chosen in a fixed order so the best
ones survive the cut: Clean sweep, Hot lap, Nothing over-flagged, Arithmetic hawk, Invented
driver caught, Read the silence, Right account, Timing and drift. A run that earns none prints
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

Card one is inverted on purpose. Its form question asks the player to agree or disagree that
nothing is owed on account 4200, so flagging that line posts `Reject` while flagging any other
line posts `Accept`. Each card carries its own `post` mapping for that reason.

## The placeholders

Four questions the form marks required are no longer asked on screen. Three were intake
questions the three-screen path has no room for, and the fourth was the confidence tap after
the round, which came out so the last card leads straight into the send:

| Form question | Entry id | Posted value |
| --- | --- | --- |
| Expected quality of the commentary | `entry.53437742` | `3` |
| Confidence before the round | `entry.538678778` | `5` |
| Confidence after the round | `entry.439643836` | `5` |
| Month end close experience | `entry.1421470415` | `Once or twice` |

Question B says so in the same cell, in the sentence beginning "Intake scales", so nobody in the
responses sheet reads them as player answers. Filter them out before any analysis. The round one
free text field (`entry.1115022539`) carries the same kind of note, because the ledger screen is
orientation only and collects no picks.

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

## The answer key

The key lives in the `CARDS` array as `key`, which is `flag` on the eight lines that carry a
problem and `stand` on the six clean ones, alongside the error type, the one line reason shown
at the reveal, and the tell the end screen uses when a player misses that line. Anyone who reads
the source can read the key. That is the trade for instant feedback, and it is the reason to
send the link and not the file.

The error types are wrong direction, invented driver, wrong account, timing, arithmetic, no
explanation and clean line. "No explanation" covers the one line where the memo simply says
nothing about an account that owes commentary, which none of the other names fits.

## Deploying

One file, `index.html`. No libraries and no build step. The only outbound request is the Figtree
stylesheet from Google Fonts. Commit to `main` and push;
GitHub Pages serves the root of `main` and the change is live within a minute or two.

```
git add -A && git commit -m "..." && git push
curl -s https://fiscalpatriots.github.io/beat-the-machine/index.html | diff - index.html
```

The source of truth for the content is
`Coach Dashboard HQ/drafts-2026-09-05-aina/EXERCISE-case-01-form-rev4.md`.
