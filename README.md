# Second Pass: Beat the Machine

A ten minute reviewer's game for the George Mason ACFE student chapter. An AI assistant wrote
Halyard's June close commentary, and the player is the second pass on it.

Live at https://fiscalpatriots.github.io/beat-the-machine/ from `main`.

## The path in

Three screens stand between the link and the first card.

1. The opening screen, two short paragraphs. Three candidate wordings live in
   `INTRO-CANDIDATES.md` and the one marked live there is the one in `index.html`.
2. One screen for the codename and the chapters, on the same screen and both required.
3. The ledger, read once as orientation with a single Continue.

Nothing else is asked on the way in. The one tap after the round is the confidence scale.

## Mason branding

Every screen carries a green band at the top with "George Mason University" and, beneath it,
"Costello College of Business", both set in type. There is no logo file and no Patriot mark in
this repository, because those are trademarks and a text lockup is the safe way to say whose
drill this is. The footer line under every screen reads "A drill by the ACFE student chapter and
Beta Alpha Psi Theta Alpha at Mason".

The colours are the published university values, not approximations:

| Name | Hex | Where it is used |
| --- | --- | --- |
| George Mason Green | `#005239` | the band, headings, the rank, the car, the chequered flag, the travelled track |
| George Mason Gold | `#ffc733` | the rule under the band, the car cabin, the streak flame, earned badges, the top trophy |
| Logo Black | `#333333` | body copy, the two call buttons, badge text on gold |
| Accent, Navy | `#004f71` | the machine's voice, the account strip and the highlighted ledger row |
| Accent, Red | `#cc4824` | the wrong-call verdict and negative changes (darkened to `#a83a1c` where it sets figures) |

Those values come from the Mason brand guide colour page,
https://brand.gmu.edu/brand-guide/brand-colors. The Bynder toolkit page supplied by Khaled
(`gmu.bynder.com/guidelines/guide/bd8609ea.../page/b053e82e...`) redirects to the public Brand
Toolbox root without signing in, so the colour and typography values were taken from the
published brand guide pages instead.

Two brand rules shape the palette here. Accent colours are for emphasis only and never replace
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
Each account occupies two rows: the name, the account number and a slim movement bar scaled to
the largest absolute change in the month, then May, June, Change and Percent underneath it as
four right aligned columns of tabular figures at 15px. Splitting the account name onto its own
row is what lets all four figure columns hold full type with thousands separators inside a
375px phone with no sideways scrolling. Negative changes print in a muted red. Revenue, cost of
sales and operating expenses each carry a subtotal, and a net line closes the statement.

Nothing is tapped there. The Ledger button on every card and every reveal reopens the same
component as a slide up sheet, with the account under review highlighted and scrolled to, and
that account also prints as a strip at the top of its card.

## The round

Fourteen accounts come one at a time. Each card carries the account's ledger strip, a two bar
picture of the movement with no figures repeated on it, the memo's sentence quoted once, and an
"On file" panel holding only facts not already visible above it. The two calls are equal weight
and neutral, with Let it stand on the left and Flag it on the right.

Every card is scored. Flagging a line that was already right costs exactly what missing a
problem costs, and the running pill reads `Right N of M` over the cards seen so far. The split
is twelve problem lines and two clean ones, which is what the source exercise contains, and
neither number is ever printed for the player. A player who flags all fourteen lands on Senior,
which is the point of scoring the clean lines.

## The track

The progress bar is a race track drawn as one inline SVG in `buildTrack()`. Fourteen segments,
a car that advances one segment per card, a pit lane under the main lane and a chequered flag at
the finish. A right call gives the car a short forward burst with two speed lines behind it, a
wrong call drops it into the pit lane for a beat before it rejoins, and three correct calls in a
row light a flame behind it. Every animation is 200ms, there is no sound, and everything is
switched off under `prefers-reduced-motion: reduce`. The bar holds a fixed height from the first
paint, so nothing on the page moves when the car does.

The run is timed from the first card to the fourteenth call. The end screen prints it as
`Lap time 6:42` beside the score, and the same figure rounded to whole minutes is what goes into
the form's elapsed minutes question.

## The end screen

The end screen leads with the reward: a trophy drawn to the rank (bronze, silver, gold, and a
starred cup for a clean sweep) with a single rise and shine that respects
`prefers-reduced-motion`, the rank name, the codename, the earned line, the three outcomes as
caught, let stand correctly and false flags, the lap time under those three tiles, five badges
with the unearned ones greyed, and the share line with a Copy button. The coaching sits behind
one tap under it. Ranks are Trainee, Staff, Senior, Manager and Partner, off correct calls out
of fourteen.

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
type for that line, question A carries the organisations, and question B carries the lines
missed, the pattern, the result and the longest run. The elapsed minutes question receives the
lap time, off the clock rather than a tap.

Card one is inverted on purpose. Its form question asks the player to agree or disagree that
nothing is owed on account 4200, so flagging that line posts `Reject` while flagging any other
line posts `Accept`. Each card carries its own `post` mapping for that reason.

## The placeholders

Three questions the form marks required are no longer asked on screen, because the path to the
first card is three screens and these are not part of it:

| Form question | Entry id | Posted value |
| --- | --- | --- |
| Expected quality of the commentary | `entry.53437742` | `3` |
| Confidence before the round | `entry.538678778` | `5` |
| Month end close experience | `entry.1421470415` | `Once or twice` |

Question B says so in the same cell, in the sentence beginning "Intake scales", so nobody in the
responses sheet reads them as player answers. Filter them out before any analysis. The round one
free text field (`entry.1115022539`) carries the same kind of note, because the ledger screen is
orientation only and collects no picks.

## Counting the organisations

The intake screen asks which chapters the player belongs to, multi-select, at least one. The
taps ride at the front of question A (`entry.117652481`) behind a fixed prefix, so no new form
question was needed. The cell reads:

```
Organisations: ACFE; NABA. Not collected. The ledger screen is orientation only in this version.
```

The six chips are Beta Alpha Psi, ACFE, ASM, NABA, AAA and GMU Student. To count a chapter in
the responses sheet, test the question A column for the name, for example
`=COUNTIF(H2:H, "*ACFE*")`. A player who tapped two chapters counts in both, which is what a
multi-select means, so the chapter counts sum to more than the number of responses. Count
players with `=COUNTA(...)` on the codename column instead.

## If the form is ever rebuilt

Rebuilding the Google Form issues new `entry.NNNN` ids. Fetch the responder page, read the ids
out of the `FB_PUBLIC_LOAD_DATA_` block, and replace the `E` object and `FORM_POST` URL. Nothing
else in the file depends on the form.

## The answer key

The key lives in the `CARDS` array as `key`, which is `flag` on the twelve lines that carry a
problem and `stand` on the two clean ones, alongside the error type, the one line reason shown
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
`Coach Dashboard HQ/drafts-2026-09-05-aina/EXERCISE-case-01-form-rev2.md`.
