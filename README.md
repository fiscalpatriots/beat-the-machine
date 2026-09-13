# Second Pass: Beat the Machine

A ten minute reviewer's game for the George Mason ACFE student chapter. An AI assistant wrote
Halyard's June close commentary, and the player is the second pass on it.

Live at https://fiscalpatriots.github.io/beat-the-machine/ from `main`.

## Versions

| What | Version | Where it is stated |
| --- | --- | --- |
| Product | `second-pass-drill 1.3.0` | the `PRODUCT_VERSION` constant in `index.html`, the footer line under every screen, question A of every posted payload, and the scope block on `review.html` |
| Round one case | `halyard-v3`, 13 September 2026 | `cases/halyard-v3.json`, question A, the local record |
| Round two case | `brightwater-v3`, 13 September 2026 | `cases/brightwater-v3.json`, questions A and C, the local record |
| Data notice | `notice-2026-09-13` | the notice screen, question A, the local record |

One constant carries the product version. Change `PRODUCT_VERSION` and every surface follows,
except `review.html` and this file, which state it in prose and have to be edited by hand.

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

Four screens stand between the link and the first card.

1. The opening screen, two short paragraphs. Three candidate wordings live in
   `INTRO-CANDIDATES.md` and the one marked live there is the one in `index.html`.
2. The data notice, read before anything is collected. See "The data notice" below.
3. One screen for the codename and the chapters, on the same screen and both required.
4. The ledger, read once as orientation, with a block under it saying what earns a flag and
   what "Let it stand" means, and one optional step of ledger-only picks. See "The ledger-only
   picks" below.

Nothing else is asked on the way in. After the round the player is offered a local record and a
separate voluntary send, and neither is required to finish.

## The data notice

It sits between the intro and the codename screen, so nothing has been collected by the time it
is read. The four items, word for word as they appear on screen under the heading "What this
records":

> What is collected: the codename you pick, the chapters you tap, your call on each of the
> nineteen lines, the basis chips behind each call, the optional line of your own words, and how
> long each line and each round took you.
>
> A codename is a pseudonym and not anonymity. Anyone who knows which codename you chose can read
> your run, so pick one you are willing to be known by.
>
> Where it goes if you send it: the Google Form responses sheet owned by Khaled Alkurd, who built
> this drill and writes the findings from it.
>
> You can finish the whole run without sending anything. At the end you can save your own record
> as a file, and sending your results to the form is a separate button you do not have to press.

Under those four the screen prints the notice version and the product version. The notice version
rides into question A and into the local record, so a response can be tied to the wording the
player actually read. Change the wording and the version goes up with it.

## The ledger-only picks

**Subject to Khaled's ruling.** This step was added on 13 September 2026 because the build
handoff asks for a short ledger-only judgment before the narrative. It has not been approved as
a permanent part of the path in, and removing it means deleting `prepickBlock`, `wirePrepicks`
and `prepickLine` from `index.html` and restoring the plain Continue on the orientation screen.

Under the statement on the orientation screen: "Before the memo: tap up to three lines you would
ask about first, or skip." Fourteen chips, one per ledger account, capped at three, with Skip and
Continue side by side under them. Once three are tapped the rest go grey until one is released.
Nothing is typed and nothing is scored, so it costs a few seconds. The sticky bar on a phone and
the rail on a desk read "Skip the picks and continue" and record a skip rather than pretending a
player who never scrolled made a pick.

The picks post into the round one free text question, `entry.1115022539`, which collected nothing
before this. The cell reads:

```
Prepicks: 4200; 6000; 6400.
```

A skip posts `Prepicks: skipped.` rather than an empty cell, so a deliberate skip and a missing
answer can be told apart. The picks are also in the local record under `prepicks`, with the
question text and the entry id beside them.

## Test mode

`?test=1` on the URL turns it on, and three taps on the footer line toggle it from inside the
page for a facilitator with no address bar to edit. A band under the Mason header reads "TEST
MODE, nothing is sent" and the footer version line gains ", test mode".

While it is on, "Send my results" builds the payload, writes it into the local record and posts
nothing. The record carries `attempt.testAttempt: true`, `scoring.exclusionReason: "test
attempt"`, and question A of the payload carries "TEST ATTEMPT, exclude from reports." Use it for
every walkthrough, because the live participant dataset must never be seeded from automated runs.

## The participant record

"Save my record" on the end screen downloads `second-pass-<attempt id>.json` and shows the same
text in a copyable box behind it, so a browser that blocks the download still hands the player
their run. The fields are the ones the build handoff calls the minimum attempt record:

| Block | Fields |
| --- | --- |
| `attempt` | id, pseudonym and the note that a codename is not anonymity, organizations, role (null, not collected), notice version, product version, case versions and which path loaded them, form URL, mode per round, first attempt, run index, assistance source, started, completed, submission state, submission attempts, test attempt |
| `prepicks` | picks, skipped, the entry id they post to, the question as it was asked |
| `responses` | one per line for all nineteen: item id, round, case version, mode, account and name, error type, original decision, final decision, basis chips, the player's own words, the on-file facts that were shown, confidence (null, not asked), assistance revealed, elapsed active seconds, skipped or missing reason, when feedback was revealed, the keyed decision, and whether the call agrees with the key |
| `scoring` | key versions, the round one and round two counts, human rubric scores (null), scorer id (null), out-of-key finding (null), adjudication (null), exclusion reason, final resolution (null) |
| `timing` | round one lap seconds, the whole minutes actually posted, round two seconds, elapsed active seconds summed over the nineteen lines |
| `notAsked` | the four form questions nobody was asked, why a placeholder is posted, and the placeholder mode |
| `payload` | the exact payload, with a note saying whether it was posted, would have been posted, or has not been posted |

Nothing in it is invented. The four unasked questions are reported as not asked rather than as
answers, and confidence is `null` on every line because the page never asks for it.

## Sending, and the attempt identifier

"Send my results" is the only thing that posts, it is voluntary, and the run is complete without
it. The hidden frame's load event proves the request left the page and nothing more, so the state
says exactly that:

> Sent. The receiver does not confirm receipt to this page.

Every run gets one attempt identifier, `att-<base36 time>-<four characters>`, generated when the
run starts and reused by every retry of that run. It posts at the front of question B:

```
Attempt id: att-mtze89jf-wrv8, run 1 in this tab.
```

Two rows carrying one attempt id are one attempt sent twice and get counted once. Play again
generates a new id and raises the run index, so a second run is a separate attempt rather than a
retry. A refresh in the middle of a run keeps the id, because the whole run lives in
`sessionStorage` under `btm.run.v1` and the page resumes on the screen it was left on. A send
that was in flight when the tab reloaded comes back as not sent rather than as sent.

## The practitioner route

The organization row carries an eighth chip, "Outside Mason", after Professor. A practitioner
with no campus tie taps it and answers truthfully rather than claiming an affiliation they do not
have. It posts the same way as the others:

```
Organizations: Outside Mason.
```

Count it as its own denominator. A practitioner walkthrough is not a student result and the two
should never be pooled.

## Mason branding

Every screen carries a green band at the top with "George Mason University" and, beneath it,
"Costello College of Business", both set in type. Once the player has entered a codename it
appears in gold on the bottom edge of that band, tracking sideways so it always sits directly
above their car on the track. There is no logo file and no Patriot mark in
this repository, because those are trademarks and a text lockup is the safe way to say whose
drill this is. The footer line under every screen reads "A drill by the ACFE student chapter and
Beta Alpha Psi Theta Alpha at Mason".

Both pages load one stylesheet, `assets/second-pass.css`, and neither repeats what is in it.
That file is the design standard: the tokens, one type scale, a 4px spacing scale, one radius,
one shadow, two buttons, one table, one figure, one status style and one focus ring. The
comment at the top of the file states each rule in a sentence.

Six values carry meaning and nothing else carries colour:

| Name | Hex | Where it is used |
| --- | --- | --- |
| Paper | `#f6f3ec` | the page |
| Ink | `#1a1a1a` | every word, the primary button, the rule that matters |
| Soft ink | `#5f6366` | secondary words, captions, labels, an inert status |
| George Mason Green | `#005239` | the band, the car, the chequered flag, links, agreement, a passed check |
| George Mason Gold | `#ffc733` | three places only: the rule under the band, the trophy, the underline beneath a headline numeral |
| Muted red | `#a33a1c` | a decrease and a failed check |

There are no tinted fills, no coloured left stripes and no coloured pills anywhere in the
product. A status is a word set in small caps in one of four colours, never a badge, and the
checker prints its coverage as one line of tabular counts rather than a wall of tiles.

Those values come from the Mason brand guide color page,
https://brand.gmu.edu/brand-guide/brand-colors. The Bynder toolkit page supplied by Khaled
(`gmu.bynder.com/guidelines/guide/bd8609ea.../page/b053e82e...`) redirects to the public Brand
Toolbox root without signing in, so the color and typography values were taken from the
published brand guide pages instead.

Two brand rules shape the palette here. Accent colors are for emphasis only and never replace
green and gold, and gold may not set text on white, so gold never sets type on the paper and appears only as a
rule, the trophy fill and the underline under a headline numeral. Every text pair on the band and on the cards clears
4.5:1 at body size, the lowest being the footer and the earned line at 5.97:1.

The type is Figtree, the university's web typeface, loaded from Google Fonts with the guidance's
own fallbacks behind it: Open Sans, then Franklin Gothic, then the system stack. If the font
request fails the page still sets correctly. Typeface guidance is at
https://brand.gmu.edu/brand-guide/fonts-and-typography.

The two call buttons are the same outlined ink button, side by side. They are never green or
gold and neither is filled, because the choice between them has to read as even.

## The ledger

The ledger screen is a statement, not a list. A header block names the company and the close.
Each account occupies three rows on a phone: the name and the account number, then May and June
on one line and Change and Percent on the next, right aligned tabular figures at 16px on 20px
gutters, with a slim movement bar under them scaled to the largest absolute change in the month.
Stacking the figures two to a line is what lets every column hold full type with thousands
separators inside a 375px phone with no sideways scrolling; from 480px up the four sit on one
line. Negative changes print in a muted red. Revenue, cost of sales, operating expenses and
financing each carry a subtotal, and a net line closes the statement. Interest expense reports
in financing rather than inside operating expense, so total operating expenses reads $1,000,300
in May and $1,188,800 in June and total financing reads $61,200 and $92,400.

Nothing is tapped there. The Ledger button on every card and every reveal reopens the same
component as a slide up sheet, with the account under review highlighted by a tint at three percent and a bolder name, and
scrolled to. That account also prints as a strip at the top of its card.
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
the right holding "What earns a flag" with the six defect types as a list, with Continue at the
foot of both columns. On a phone the legend comes first, collapsed to its title and the six
chips until it is tapped, the ledger follows, and Continue is fixed to the bottom of the
viewport.

## The round

Fourteen accounts come one at a time. Each card carries the account's ledger strip, a two bar
picture of the movement with no figures repeated on it, the memo's sentence quoted once, and an
"On file" panel holding only facts not already visible above it. The two calls are equal weight
and neutral, with Let it stand on the left and Flag it on the right.

Every card is scored. Flagging a line that was already right costs exactly what missing a
problem costs, and the running count reads `Right N of M` over the cards seen so far. The split
is eight problem lines and six clean ones, rebalanced on 12 September 2026 from the twelve and
two the first version carried, because twelve and two let a player flag everything and score
twelve. Neither number is ever printed for the player. Flagging all fourteen now scores eight
and lands on Trainee.

## Round two, the assessment

Round one is practice: every call gets a reveal, a running score and a car that moves. Round two
is an independent assessment on a company the player has never seen, and it is scored at the end.

The bridge screen says so: **"Round two is scored at the end, so you get no hints."** Under that
it prints what the case file calls the assessment note, which tells the player that every figure
ties, every direction word is right and the threshold readings are correct, so the only thing
left on each line is whether the cause the memo names is carried by something on file.

Between the bridge and the results the page suppresses everything that would leak correctness.
There is no reveal after a call, no running score, no streak, no mark, and the whole track
comes off the screen so a car that moved or changed colour cannot answer the question for the
player. The header shows progress and nothing else, as `3 of 5`. The basis chips are still
collected on every line, because the reason a player held is the point of the exercise.

Once the fifth call is in, one results screen prints all five at once: whether the call agrees
with the key, the error type, the full reason, and the player's own basis under it. The end
screen follows.

| Fresh line | Account | May | June | Change | Percent | Owes commentary | Call | Type |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 5210 Dental supplies and lab fees | $138,500 | $191,200 | +$52,700 | 38.1% | yes | Flag | unsupported driver |
| 2 | 6110 Hygienist wages | $214,000 | $268,900 | +$54,900 | 25.7% | yes | Let it stand | clean line |
| 3 | 4220 Orthodontic plan revenue | $96,000 | $138,400 | +$42,400 | 44.2% | yes | Flag | no explanation |
| 4 | 4010 Patient service revenue, net | $742,000 | $803,500 | +$61,500 | 8.3% | no | Flag | unsupported driver |
| 5 | 6610 Marketing and patient outreach | $18,400 | $24,100 | +$5,700 | 31.0% | no | Let it stand | clean line |

The threshold is no shortcut here. Two of the three lines that clear both legs are flags and one
stands, and of the two that clear neither one is a flag and one stands, so a player who reasons
from the threshold alone does no better than chance. `cases/README.md` sets out the evidence on
each line and what would settle it.

The cards are built from `CARDS2` and the balances from `ROWS2`, and every ledger function takes
the book it is reading, so the "See the full ledger" button on a round two card opens the five
account dental statement in the same sheet component that serves Halyard's fourteen. The five
lines are scored on their own counters and never touch the rank, the trophy or the main score.

`brightwater-v2` was the practice version of this case and is retired. It tested wrong direction,
timing and arithmetic, which the trained fourteen already teach, so it measured a second helping
of the same thing rather than evidence judgment. Responses scored against v2 are not comparable
with responses scored against v3 and must never be pooled with them.

Rows filed in the Google Form before 12 September 2026 were answered against the old key and
are not comparable with anything filed since. The per-card entries still post the player's own
call unchanged, so nothing about the form mapping moved. The source of truth for the new key is
`EXERCISE-case-01-form-rev4.md` in the AINA drafts folder, with the whole case as plain text in
`REVIEW-FLAT-rev1.txt` beside it.

## The track

The progress bar is a race track drawn as one inline SVG in `buildTrack()`. Fourteen segments,
one per trained line, with the finish at card 14. Round two runs as an assessment where a car
that moved or changed colour would tell the player how they were doing, so the whole bar leaves
the screen from the bridge through the results and comes back on the end screen with the car at
the finish. There
is a car that advances one segment per card, a pit lane under the main lane and a chequered flag
at the finish that lights once all fourteen are called. A right call gives the car a short forward burst with two speed lines behind it, a
wrong call drops it into the pit lane for a beat before it rejoins, and three correct calls in a
row light a flame behind it. Streaks build in three steps: two in a row gives the car a speed
trail, three adds the flame and a "Streak 3" line on the reveal, and five grows both and lights
the track behind the car gold under an "On fire" line. A wrong call ends the streak, the
trail and the flame fade out and the car takes the pit lane dip. Every animation is 250ms or
under, there is no sound, and everything is switched off under `prefers-reduced-motion: reduce`. The bar holds a fixed height from the first
paint, so nothing on the page moves when the car does.

The run is timed from the first card to the fourteenth call. The end screen prints it as
`Lap time 6:42` beside the score, with `Best streak 7` next to it, and the lap time rounded to
whole minutes is what goes into the form's elapsed minutes question. A streak of five or more
earns the "Hot lap" badge, and letting all six clean lines stand earns "Nothing over-flagged".
Nine badges can be earned and the end screen shows at most three of them. The streak stops
moving in round two, because a streak that grew or broke between assessment lines would tell the
player how the last call went.

The round two clock is separate from the lap time. It starts on the first fresh card and stops
on the fifth call, and it posts in seconds rather than minutes, because five lines on a company
nobody has seen is a short run. Each line also carries its own elapsed active seconds in the
local record, timed from the card appearing to the basis Continue.

## Spelling

American spelling throughout, in the file and in these notes. The organization chips post as
`Organizations: ...` with a z.

## The end screen

Ranks are Partner at 14, Manager at 13, Senior at 11 or 12, Staff at 9 or 10 and Trainee below
that. The end screen leads with the reward: a trophy drawn to the rank (bronze, silver, gold,
and a starred cup for a clean sweep) with a single rise and shine that respects
`prefers-reduced-motion`, the rank name, the codename, the earned line, the fresh case as
"Fresh case: 4 of 5" under that line, then one line of tabular counts reading caught, let stand
correctly and false flags, and a second reading the lap time and the best streak, then the
badges. Only earned badges show, at most three, as a row of medallions with the icon in ink on a
hairline disc and the name under it, appearing on a 150ms
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

Nothing posts on its own. The send is a button on the end screen, it is voluntary, and the run is
complete whether or not it is pressed. Test mode never posts at all.

All 38 questions are mapped to their `entry.NNNN` ids in the `E` object at the top of the
script, and all 38 are populated on every submission. The three pages post as one request with
`pageHistory=0,1,2`. If the post fails the state line says so and offers a retry, and the retry
reuses the same attempt id so it cannot double count.

Nobody types anything after the round. The fourteen calls post as `Accept` or `Reject` so the
existing multiple choice questions keep working, and every text question receives the player's
basis plus generated metadata rather than player prose: the fourteen "Why" fields carry the
basis, the call, the key and the error type for that line, the round one free text field carries
the ledger-only picks, question A carries the organizations and the three version stamps,
question B carries the attempt id, the lines missed, the pattern, the result and the longest run.
The elapsed minutes question receives the lap time, off the clock rather than a tap.

Round two posts without a new question. The whole fresh case rides in question C
(`entry.756559246`), which asks the player nothing and carried only a placeholder note before 13
September 2026. The cell now opens with `Round2: 4/5; calls FSFSF; key FSFFS; seconds 61.`, then
the five bases, then the company and the case version, so the sheet can be read without opening
the game. The fourteen "Why" fields were left exactly as they were, because the catch rate by
error type is grouped on them.

Card one is inverted on purpose. Its form question asks the player to agree or disagree that
nothing is owed on account 4200, so flagging that line posts `Reject` while flagging any other
line posts `Accept`. Each card carries its own `post` mapping for that reason.

## The four questions that are not asked

Four questions the form marks required are not asked on screen. Three were intake questions the
three-screen path has no room for, and the fourth was the confidence tap after the round, which
came out so the last card leads straight into the send.

For part of 13 September 2026 all four posted the literal string `not asked`. That string is not
one of the values any of these four questions accepts, so it was withdrawn the same day. All four
now post the placeholder value they accepted before that change:

| Form question | Entry id | Question type | Accepted values | Posted value |
| --- | --- | --- | --- | --- |
| Expected quality of the commentary | `entry.53437742` | Linear scale, required | 1 to 5 | `3` |
| Confidence before the round | `entry.538678778` | Linear scale, required | 0 to 10 | `5` |
| Confidence after the round | `entry.439643836` | Linear scale, required | 0 to 10 | `5` |
| Month end close experience | `entry.1421470415` | Multiple choice, required | Never, Once or twice, Regularly | `Once or twice` |

Read every one of those four as **not asked; placeholder value posted until the form questions are
made optional**. They are not participant answers. Whoever writes the findings script has to drop
these four columns rather than average them, and the columns carry the same placeholder in every
row, which is how you recognise them.

### For Khaled: the one change that retires the placeholders

Open the form in the form editor and make these four questions **not required** (or delete them).
The switch on the page is one word. In `index.html`, at the top of the payload and submit section:

```js
var PLACEHOLDER_MODE = "numeric";   // change to "empty" after the form change
```

Set it to `"empty"` and all four fields post nothing at all, which is the value the responses sheet
should carry for a question nobody was asked. Nothing else in the page has to change.

A Node probe against the live `formResponse` endpoint on 13 September 2026 returned the form's own
confirmation page ("Done. Scores are computed against the key after the close...") with HTTP 200
for the restored values. A submission that genuinely fails validation comes back as HTTP 400 with
the form re-rendered and "This is a required question" in the body, which is how the two are told
apart from the outside. The hidden iframe the page uses cannot read either one, so the probe is
the only way to check this from a script.

Two former placeholders now carry real data. The round one free text field
(`entry.1115022539`) carries the ledger-only picks, and question C (`entry.756559246`) carries
the round two string, the round two basis and the case version. Rows filed before 13 September
2026 carry the old placeholder note in both.

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

The eight chips are Beta Alpha Psi, ACFE, ASM, NABA, AAA, GMU Student, Professor and Outside
Mason, which is the practitioner route added on 13 September 2026. To count a chapter in
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
`cases/brightwater-v3.json`. Each file carries the company, the threshold policy, the ledger
rows, the memo sentences, the On file facts as verified case assumptions, the key, the error
type, the reveal reason, the tell, and its own version and date. An assessment case also carries
`"mode": "assessment"` and the assessment note the bridge prints. `cases/README.md` explains the
format, the evidence on each assessment line, the differences from the checker's Halyard sample,
and what changed in this revision.

The page fetches both files at load. When the fetch fails, which is what happens when the file is
opened from a folder rather than served, it falls back to a generated copy written into
`index.html` between the `BUILD:CASES-START` and `BUILD:CASES-END` markers. Edit the JSON, then
run `node build-cases.cjs` to rewrite that copy. The script refuses to write if a card points at
an account that is not in the ledger, if a card's figures do not tie, or if a card is missing its
key, its reason or its tell. On an assessment case it also refuses if a memo states a dollar
figure the account does not produce, states a percent that is not the movement, uses a direction
word against the sign, or if the case does not carry exactly one no-explanation line with an
empty memo.

The key is `flag` on eight of the fourteen Halyard lines and `stand` on the six clean ones; three
of the five Brightwater lines are `flag` and two are `stand`. Anyone who reads the source can read
the key, in the JSON as easily as in the page. That is the trade for instant feedback, and it is
the reason to send the link and not the file.

The error types are wrong direction, unsupported driver, unsupported attribution, wrong account,
timing, arithmetic, no explanation and clean line. brightwater-v3 uses three of them:
unsupported driver twice, no explanation once, and clean line twice. "No explanation" covers the one line where the
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

`index.html`, `cases/halyard-v3.json` and `cases/brightwater-v3.json`. No libraries. The only
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
