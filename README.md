# Second Pass: Beat the Machine

A ten minute reviewer's game for the George Mason ACFE student chapter. An assistant wrote
Halyard's June close commentary, and the player is the second pass on it.

Round one puts the ledger itself on screen as a tappable table, one row per account with May, June,
the change in dollars and percent and a bar that makes the big movements obvious, and the player
taps up to five lines to record unaided judgement before reading a word of the memo. Then fourteen
accounts come one at a time with the movement drawn as a two bar chart, a one line ledger strip for
the account under review, the sentence the memo wrote about it, and an "On file" panel carrying
every fact the call needs. A Ledger button on every card and reveal opens the full table as a slide
up sheet with the current account highlighted and scrolled into view. The player flags the line or
lets it stand, and the reveal names the error type. Twelve of the fourteen carry a problem and two
are clean lines, and the score is read against the ledger rather than against a machine score.

The end screen leads with the reward: a trophy drawn to the rank (bronze, silver, gold, and a
starred cup for a clean sweep), the rank name, the codename, five badges with the unearned ones
greyed, and the share line with a Copy button. The coaching sits behind one tap under it. Ranks are
Trainee, Staff, Senior, Manager and Partner, off correct calls out of fourteen.

Answers post straight into the existing Google Form's responses, so the leaderboard and the pooled
results are unchanged.

One file, `index.html`. No libraries, no build step, no tracking.

## Publish on GitHub Pages

Create a public repository named `beat-the-machine` under the `fiscalpatriots` account first, with
no readme, no licence and no gitignore. The repository here already has a commit on `main`.

Then, from `C:\Users\Khaled\Documents\beat-the-machine`, two commands:

```
git remote add origin https://github.com/fiscalpatriots/beat-the-machine.git
git push -u origin main
```

Then in the repository on GitHub, open Settings, then Pages, and set Source to "Deploy from a
branch", branch `main`, folder `/ (root)`. Save.

The site appears within a minute or two at:

```
https://fiscalpatriots.github.io/beat-the-machine/
```

That URL is what goes into the chapter message in place of the raw Google Form link.

## Where the data lands

Every answer posts to the live form:

```
https://docs.google.com/forms/d/e/1FAIpQLSfteTMPZrDKhYmRjxPKADAZERjyDntdMLIVZMH-FoIrcHusKg/formResponse
```

All 38 questions are mapped to their `entry.NNNN` ids in the `E` object at the top of the script.
The three pages post as one request with `pageHistory=0,1,2`. If a post fails the player is shown
their answers as copyable text rather than losing them.

Nobody types anything after the round. The fourteen calls post as `Accept` or `Reject` so the
existing multiple choice questions keep working, and every text question receives a generated
summary instead of player prose: the fourteen "Why" fields carry the call, the key and the error
type for that line, question A carries the organisations and the round one overlap, and question B
carries the lines missed, the pattern, the result and the longest run.

Card one is inverted on purpose. Its form question asks the player to agree or disagree that
nothing is owed on account 4200, so flagging that line posts `Reject` while flagging any other line
posts `Accept`. Each card carries its own `post` mapping for that reason.

## Counting the organisations

The intake screen asks which chapters the player belongs to and the taps ride at the front of
question A (`entry.117652481`) behind a fixed prefix, so no new form question was needed. The cell
reads:

```
Organisations: ACFE; NABA. Round one picks that did carry a problem: ...
```

The six chips are Beta Alpha Psi, ACFE, ASM, NABA, AAA and GMU Student, and more than one can be
tapped. To count a chapter in the responses sheet, test that column for the name, for example
`=COUNTIF(H2:H, "*ACFE*")` against the question A column. A player who tapped two chapters counts
in both, which is what a multi-select means.

## If the form is ever rebuilt

Rebuilding the Google Form issues new `entry.NNNN` ids. Fetch the responder page, read the ids out
of the `FB_PUBLIC_LOAD_DATA_` block, and replace the `E` object and `FORM_POST` URL. Nothing else
in the file depends on the form.

## The answer key

The key lives in the `CARDS` array as `key`, which is `flag` on the twelve lines that carry a
problem and `stand` on the two clean ones, alongside the error type, the one line reason shown at
the reveal, and the tell the end screen uses when a player misses that line. Anyone who reads the
source can read the key. That is the trade for instant feedback, and it is the reason to send the
link and not the file.

The error types are wrong direction, invented driver, wrong account, timing, arithmetic, no
explanation and clean line. "No explanation" covers the one line where the memo simply says nothing
about an account that owes commentary, which none of the other names fits.
