# Second Pass: Beat the Machine

A ten minute reviewer's game for the George Mason ACFE student chapter. An AI assistant wrote
Halyard's June close commentary, and the player is the second pass on it.

Live at https://fiscalpatriots.github.io/beat-the-machine/ from `main`.

## Versions

| What | Version | Where it is stated |
| --- | --- | --- |
| Product | `second-pass-drill 1.6.1` | the `PRODUCT_VERSION` constant in `index.html`, the footer line under every screen, question A of every posted payload, and the scope block on `review.html` |
| Round one case | `halyard-v4`, 13 September 2026 | `cases/halyard-v4.json`, question A, the local record |
| Round two case | `brightwater-v5`, 13 September 2026 | `cases/brightwater-v5.json`, questions A and C, the local record |
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

Four are machine-checkable where the checker recognizes the claim: arithmetic, wrong direction,
threshold and silence. The checker recomputes the dollar and percent claims it can read under its
accepted grammar against the ledger, tests the direction words it recognizes against the sign of
the movement, lists every account that clears both legs of the materiality threshold, and from
that list names every account no sentence mentions. It prints coverage beside the results, so a
reviewer sees what it could not read before relying on what it checked. `CHECKER.md` sets out the
accepted inputs and the contract.

Two are reviewer judgment: unsupported driver and timing. Both need the facts on file and somebody
who knows the business, so both stay with the human.

The round does not end with the fourteen trained lines. A second company follows, five lines the
player has never seen, scored on its own, and the sheet carries both numbers as two descriptive
results: agreement with the key on the practice case and on an unseen keyed set. Five items with
no baseline cannot show a learning gain, and the findings do not claim one.

**Scope.** The drill is a static case: fourteen lines and five fresh ones, one month, answers
keyed by hand, and it does not run on a live ledger. The checker on this site runs the mechanical
checks on a pasted ledger and memo in the layouts `CHECKER.md` lists under "What goes in", refuses
or flags the inputs that page describes, and leaves driver and timing with the reviewer. Next, the deterministic checks
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
| Decision accuracy by error type | The fourteen "Why" fields each carry the line, the account, the call, the key and the error type, so grouping on the type column gives an accuracy figure per type. In `halyard-v4` the eight flagged lines carry `arithmetic` twice, `unsupported driver` twice, and `timing`, `wrong direction`, `no explanation` and `unsupported attribution` once each; the six clean lines carry `clean line` and are the control. `no explanation` is what the screen calls silence, and threshold is the machine test that decides which lines owe commentary at all rather than a label of its own. |
| Reason category agreement by error type | The same fourteen fields carry `Reason: agrees.` or `Reason: does not agree.` and the card's basis key, so the same grouping gives agreement with the accepted reason categories per type. Question B carries the two round totals beside the attempt identifier. A reason agrees when every chip the player tapped is in the card's basis key and at least one was tapped. |
| False-flag rate | The six lines whose key is `stand` are the denominator. A `flag` call on any of them is a false flag, and question B carries the round's false flag count as well. |
| Elapsed time | The clock runs from the first card to the last call and posts as whole minutes in the elapsed time question. It is elapsed time on the page rather than measured active work, and it is reported under that name. |
| Fresh case accuracy | Question C (`entry.756559246`) opens with `Round2: right call 4/5, right reason 3/5; calls FSFFS; key FSFFS; seconds 61.` The two fractions are the call and reason scores on the five lines of a company the player had never seen, the letter strings are the five calls and the five keyed answers in card order with `F` for flag and `S` for let it stand, and the seconds are the round two clock. |

Read together these say which error types a reviewer agrees with the key on unaided, whether the
basis they gave agrees with the key as well, and how a second unseen memo of five lines was
scored. They do not establish a learning gain, a transfer effect, time saved or an error
prevented in real work. Fourteen practice items and five different assessment items are not
equivalent pre- and post-tests, so the fresh case is reported as a second, unseen set scored the
same way and never as proof of transfer.

### Reading the two headline numbers off the sheet

Both of these come out of the responses sheet with no hand coding, and both are worth stating in
the findings.

**Count by organization.** Question A (`entry.117652481`) opens with `Organizations: ACFE; NABA.`
Test that column for each chapter name, for example `=COUNTIF(H2:H, "*ACFE*")`, and read each
count against the response total as its own denominator, because a player who belongs to two
chapters is counted in both. Rows filed before 12 September 2026 carry the older
`Organisations:` spelling, so reach back with `Organi*ations:` or with the chapter name, which
never changed.

**Fresh case accuracy.** Split question C on the semicolons. The fields after `Round2:` are the
call score and the reason score out of five, and `=AVERAGE()` over each column is the pilot's
fresh-case accuracy. Splitting the calls string character by character against the key string
gives a per line figure, and all three flagged lines in `brightwater-v5` are `unsupported
driver`, so the fresh case reads as a causal-evidence set rather than an arithmetic one. Report
it beside the fourteen as two separate descriptive numbers. Calling the difference between them
transfer, learning or improvement would require a planned comparison this pilot does not run.

### The Monday command

The hand formulas above are there so a number can be checked by eye. The whole sheet is read by
one script, and the readout is written against its field names.

```
python tools/findings.py responses.csv
```

Download the responses tab as CSV, put it beside the repository, and run that from the repository
root. It writes `FINDINGS-<today>.md` and prints the same summary to the terminal. Add
`--fields readout-fields.json` to get the readout's field set as JSON as well, or `--fields` on
its own to print it.

The script matches columns by the form's question titles rather than by position, so a reordered
sheet still reads, and any title it cannot find is printed under **Columns not found** with the
measure that needed it skipped rather than guessed. It drops the named test codenames and any row
the page stamped as a test attempt, and it treats two rows carrying one attempt identifier as one
attempt sent twice. The four questions the form asks that this version of the game does not are
excluded from every measure, whether the row carries the literal `not asked` or the older numeric
placeholder.

`READOUT-TEMPLATE.md` prints a field name in every cell it wants filled, and the script's
**Readout fields** section prints exactly those names with the value to copy across: the run fields
once, then one block for each case set the export holds, so the number of fields depends on the cases
played.
A field the responses cannot support prints *not available*, and that cell stays blank on the
readout rather than being estimated.

To see it work before any response exists:

```
python tools/make-sample-csv.py
python tools/findings.py tools/findings-sample.csv --out tools/FINDINGS-sample.md
```

That builds fifteen synthetic responses in the shapes the page posts, including one authored-case
run, one row in the pre-13-September shape and one attempt sent twice, and reads them back.

## The path in

Four screens stand between the link and the first card.

1. The opening screen, two short paragraphs and a drawn three frame strip headed "How to play,
   in twenty seconds": read the line against the ledger and the file behind it, choose whether
   the memo's explanation holds, lock it in and the answer key comes back with the points. The
   frames are inline SVG in `playFrames()` and carry no text of their own, so they scale with the
   column. Three candidate wordings for the paragraphs live in `INTRO-CANDIDATES.md` and the one
   marked live there is the one in `index.html`.
2. The data notice, read before anything is collected. See "The data notice" below.
3. One screen for the codename and the chapters, on the same screen and both required.
4. The ledger, read once as orientation, with a block under it saying what earns a flag and
   what "Let it stand" means, and one optional step of ledger-only picks. See "The ledger-only
   picks" below.

Nothing else is asked on the way in. After the round the player is offered a local record and a
separate voluntary send, and neither is required to finish.

Every screen opens with one line in soft type saying what the player is doing and why, from the
intro through the end screen. The drill loads the shared header and footer from `assets/nav.js`,
the same pair `checker.html` and `review.html` load, so the three pages wear one chrome; the
drill's own footer line under it carries the version stamp and nothing else, and three taps on it
still toggle test mode.

`screenshots/game/` holds the five verification shots at 375: a card mid-call, a right reveal, a
wrong reveal, a level up and the end screen. They are written from the running page by a headless
pass rather than cropped by hand, so a rebuild reproduces them.

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
handoff asks for a short ledger-only judgment before the narrative. It was removed and then
restored the same evening, and it stays until the question of whether the drill needs one decision
taken before the AI's text is read is settled. Removing it means deleting `prepickBlock`,
`wirePrepicks` and `prepickLine` from `index.html` and restoring the plain Continue on the
orientation screen.

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
| `responses` | one per line for all nineteen: item id, round, case version, mode, account and name, error type, original decision, final decision, basis chips, the player's own words, `evidenceSupplied` (the on-file facts the card showed) and `evidenceSelected` (null, the page does not ask what the player read), confidence (null, not asked), assistance revealed, `elapsedSecondsOnCard`, skipped or missing reason, when feedback was revealed, the keyed decision, and whether the call agrees with the key |
| `scoring` | key versions, the round one and round two counts, human rubric scores (null), scorer id (null), out-of-key finding (null), adjudication (null), exclusion reason, final resolution (null) |
| `timing` | round one lap seconds, the whole minutes actually posted, round two seconds, `elapsedSecondsOnCards` summed over the nineteen lines |
| `notAsked` | the four form questions nobody was asked, why a placeholder is posted, and the placeholder mode |
| `payload` | the exact payload, with a note saying whether it was posted, would have been posted, or has not been posted |

**Two fields were renamed in 1.6.1, and the old names ride along for this version only.** The
release review found that `evidenceReferences` held the card's whole supplied file list under a
name that read as the documents the participant used. It is now `evidenceSupplied`, and
`evidenceSelected` was added beside it and left `null`, because the page does not ask which
document the player relied on and will not imply an answer it did not collect.
`elapsedActiveSeconds` measured wall-clock time that does not pause when the tab is in the
background, so it is now `elapsedSecondsOnCard` per line and `elapsedSecondsOnCards` in the
timing block, with a note on the record saying what the clock does and does not do. Both old
names are written beside the new ones in 1.6.1 so a script reading an older export keeps
working, and `renamedFields` on the record names the pairs. They come out in the next version.

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

### The receipt, once one endpoint is set

`receipts/Code.gs` is a Google Apps Script web app that takes the attempt record, writes one row
to a sheet in Khaled's Drive, and answers with a receipt: the sha256 of the record it stored and
the time it wrote the row. The page prints the first twelve characters on screen and writes the
whole receipt into the saved record, so the player's copy and the sheet's copy carry the same
string.

It is off until one constant in `index.html` carries the deployed URL:

```js
var RECEIPT_ENDPOINT = "";
```

While it is empty the page behaves exactly as the section above describes. With a URL in it the
record goes to the endpoint first and to the form straight after, in that order, every time. A
stored record reads `Receipt 4db5710dfcaa. Stored at 8:53:45 AM.` on screen; an endpoint that
fails or times out leaves the wording above untouched and says the receipt endpoint did not
confirm it, so a player whose receipt fails is where they were before this existed and never
worse. Test mode posts nothing anywhere. A retry carries the same attempt id, and the endpoint
answers a repeat with the first receipt and writes no second row.

The four clicks that turn it on, the sentence the data notice gains when it is on, and the way
`tools/findings.py` reads the receipts sheet instead of the form export are in
[`receipts/README.md`](receipts/README.md).

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

Six values carry meaning and nothing else carries color:

| Name | Hex | Where it is used |
| --- | --- | --- |
| Paper | `#f6f3ec` | the page |
| Ink | `#1a1a1a` | every word, the primary button, the rule that matters |
| Soft ink | `#5f6366` | secondary words, captions, labels, an inert status |
| George Mason Green | `#005239` | the band, the car, the chequered flag, links, agreement, a passed check |
| George Mason Gold | `#ffc733` | three places only: the rule under the band, the trophy, the underline beneath a headline numeral |
| Muted red | `#a33a1c` | a decrease and a failed check |

There are no tinted fills, no colored left stripes and no colored pills anywhere in the
product. A status is a word set in small caps in one of four colors, never a badge, and the
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

### The shared header, the footer and the link preview

One template draws the chrome. `assets/nav.js` injects a slim header at the top of the body (the
Second Pass wordmark in green, then Drill, Checker and Review as text links with the current page
marked and underlined in green, all three still visible at 375 with no hamburger) and the footer at
the bottom ("Built by Khaled Alkurd. A drill for the AI-native accounting student." over text links
to the protocol, the provenance note, the facilitator guide and the code). All three pages load it.
A page only adds `<script src="assets/nav.js" defer></script>` to its head; nothing else needs
wiring, since the script carries its own rules.

It carries three more things a page would otherwise have to wire itself. It prints the skip link as
the first thing in the body and points it at that page's main region, taking the page's `<main>`
where there is one and the outer container where there is not, and giving that region a `tabindex`
of -1 so focus lands where the link sends it. And it hides itself, the footer and the skip link in
print media, so the checker's summary sheet prints as the summary sheet alone.

Every page carries the same three metadata lines so a pasted link previews in LinkedIn and in mail:
a `<title>`, a `<meta name="description">`, and the Open Graph and Twitter card block. Only the
title and the description change from page to page; the image, the card type and the site name are
the same everywhere. `review.html` shows the full block. For the other two:

| Page | `<title>` | `<meta name="description">` |
| --- | --- | --- |
| `index.html` | Second Pass: the ten-minute drill | Fourteen ledger lines, eight carrying a planted problem, called against an answer key. A drill on AI-drafted close commentary, built at George Mason. |
| `checker.html` | Second Pass Checker: test the memo against the ledger | Paste a ledger and the memo drafted about it. It checks the dollar, percent and direction claims it recognizes, names every account over the threshold that nobody mentioned, and shows what it could not read. |

The Open Graph block to repeat on each page, with `og:url` pointed at that page:

```html
<meta property="og:type" content="website">
<meta property="og:site_name" content="Second Pass">
<meta property="og:url" content="https://fiscalpatriots.github.io/beat-the-machine/index.html">
<meta property="og:title" content="...the page title...">
<meta property="og:description" content="...the page description...">
<meta property="og:image" content="https://fiscalpatriots.github.io/beat-the-machine/assets/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
```

The card art is `assets/og-image.png`, 1200 by 630, a Mason green field carrying the wordmark, the
line "A second pass on AI-drafted close commentary" and the university and college names in small
type. It is rendered from `assets/og-image.svg`; the build command sits in a comment at the top of
that file. The icon is `assets/favicon.svg` with `assets/favicon-32.png` beside it for browsers that
will not take the vector, a ledger page ticked in green on the green field over the gold rule.

`checker.html` and `review.html` both carry the whole block described above. `review.html` is the
one to copy from.

### Site hygiene, and the four lines index.html still needs

Three files sit at the root and cover the whole site, so no page has to repeat them.
`robots.txt` allows every crawler everything and names the sitemap. `sitemap.xml` lists the three
pages and the protocol PDF. `404.html` is the page GitHub Pages serves for an address that matches
nothing: the same paper, the same Mason band, the same shared chrome, and links to the drill, the
checker and the review page, with `<meta name="robots" content="noindex">` on it so the error page
itself never turns up in a search result.

Each page names its own canonical address so a link carrying a tracking parameter does not read as
a second copy of the page. `checker.html`, `review.html` and `404.html` carry theirs already.

All three pages carry the same head block: the title, the description, their own canonical
address, the Open Graph and Twitter card lines with `og:url` on that page, and the two favicon
links. `index.html` took its four on 13 September 2026, and the inline data URI icon it carried
before that is gone, so the drill now shares the favicon and the link preview with the other two
pages.

Nothing else is owed. `assets/nav.js` is already on the page, and the skip link, the main region it
points at, and the print rule that hides the chrome on paper all come from that script, so
`index.html` gets them without another line. Every image on the page needs `width` and `height`
attributes and, below the first screen, `loading="lazy"`; the two audits under `audit/` record how
the other two pages were measured against the same rules.

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
twelve. Neither number is ever printed for the player. Flagging all fourteen scores eight calls,
1,150 points, and lands on Staff.

### The call commits in two steps

Since 13 September 2026 a tap on Flag it or Let it stand does not commit anything. It selects the
call: the button fills, the other one dims and stays live, and the basis row opens underneath it
with the memo, the figures and the On file facts still on screen above. A second control, **Lock
it in**, is what commits. Until it is pressed the player can tap the other button, change chips,
edit their line of words, or press **Back** to reopen the line before this one with its call
uncommitted and its basis and words exactly as they left them. Nothing is scored, the car does
not move and nothing is revealed until the lock.

A committed line wears a small padlock over its segment on the track, so the player can see at a
glance which calls are settled and which one is still theirs to change. The keyboard runs the
same loop: `1` selects Let it stand, `2` selects Flag it, `Enter` locks, `Backspace` goes back,
and `Escape` closes the ledger sheet.

Round one is practice and reveals each call, so a line reopened with Back can be changed after
its verdict has been seen. That is what practice is for, and the attempt record keeps the first
call and the committed one apart on every line (`originalDecision`, `finalDecision` and
`decisionChanged`) so a researcher can see it. The fresh case never reveals anything, so the same
two steps there are a plain change of mind.

### The reveal

The verdict takes the card area for a beat. A call that agrees with the key turns the card over
in 300ms, which `prefers-reduced-motion` serves as a fade, onto a face carrying the error type,
the verdict word (`Caught it` or `Cleared it`), the tell in one line, and the points the line
earned counting up. A call that does not agree gets a calm face: `It got past you` when the key
says flag, `A false flag` when it says stand, then what was actually true in one line, the ask
the reviewer should have made, the line saying no points and which streak ended, and one line of
coaching from the case's tell. Both faces carry the running score and the rank bar underneath.
There is no sound on either.

The two lines the wrong face reads are `truth` and `ask` on each flag card in `cases/`, and
`over` on each clean line. `build-cases.cjs` refuses a flag card without `truth` and `ask` and a
clean line without `over`, so the face can never come up empty.

### Points and the rank ladder

| What | Points |
| --- | --- |
| A call that agrees with the key | 100 |
| A basis that agrees with the key | 50 |
| Every streak step from the third correct call onward | 25 |
| A cover story caught: a right flag on an unsupported driver or an unsupported attribution | 75 |

Since 1.6.1 the ladder is a share of what the case in front of the player is worth, not a fixed
count of points. Fourteen Halyard lines and twelve Kestrel lines cannot be worth the same run, and
while the thresholds were absolute a perfect twelve-line run stopped at Manager. Each rank now
starts at a share of the most that case can give: Staff at 34 percent, Senior at 57, Manager at 76
and Partner at 95. One floor sits under that arithmetic: the Senior line is held above the
blanket-call ceiling, the most a player can score by calling every line the same way without
reading one of them, so a blanket call stops at Staff on any case.

| Case | Lines | Most the case can give | Blanket-call ceiling | Staff | Senior | Manager | Partner |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Halyard | 14 | 2,625 | 1,450 | 893 | 1,496 | 1,995 | 2,494 |
| Kestrel | 12 | 2,200 | 1,200 | 748 | 1,254 | 1,672 | 2,090 |

A case authored in `author.html` gets its own ladder the same way, built when the case loads.

Points and rank are read off the fourteen trained lines. The fresh case runs as an assessment and
is scored on its own, because a points total that moved between those five lines would tell the
player how the last call went.

The header carries the ladder: the rank name, the points, the points the next rank starts at, and
a bar filling toward it. Crossing a rank flashes the bar gold once for 400ms and changes the name
under it, and the reveal face says `New rank, Staff.` beside the points. Verified in test mode on
13 September 2026:

| Run | Right calls | Points | Rank |
| --- | --- | --- | --- |
| Every call and every basis agrees with the key | 14 of 14 | 2,625 | Partner |
| Flag every line | 8 of 14 | 1,150 | Staff |
| Let every line stand | 6 of 14 | 925 | Staff |
| Every call against the key | 0 of 14 | 0 | Trainee |
| Clean run with three calls changed, one of them after its reveal | 14 of 14 | 2,575 | Partner |

## Round two, the assessment

Round one is practice: every call gets a reveal, a running score and a car that moves. Round two
is an independent assessment on a company the player has never seen, and it is scored at the end.

The bridge screen says so: **"Round two is scored at the end, so you get no hints."** Under that
it prints what the case file calls the assessment note, which tells the player that every figure
ties, every direction word is right and the threshold readings are correct, so the only thing
left on each line is whether the cause the memo names is carried by something on file.

Between the bridge and the results the page suppresses everything that would leak correctness.
There is no reveal after a call, no running score, no streak, no mark, and the whole track
comes off the screen so a car that moved or changed color cannot answer the question for the
player. The header shows progress and nothing else, as `3 of 5`. The basis chips are still
collected on every line, because the reason a player held is the point of the exercise.

Once the fifth call is in, one results screen prints all five at once: whether the call agrees
with the key, the error type, the full reason, and the player's own basis under it. The end
screen follows.

| Fresh line | Account | May | June | Change | Percent | Owes commentary | Call | Type |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 5210 Dental supplies and lab fees | $138,500 | $191,200 | +$52,700 | 38.1% | yes | Flag | unsupported driver |
| 2 | 6110 Hygienist wages | $214,000 | $268,900 | +$54,900 | 25.7% | yes | Let it stand | clean line |
| 3 | 4220 Orthodontic plan revenue | $96,000 | $138,400 | +$42,400 | 44.2% | yes | Flag | unsupported driver |
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
that moved or changed color would tell the player how they were doing, so the whole bar leaves
the screen from the bridge through the results and comes back on the end screen with the car at
the finish. There
is a car that advances one segment per card, a pit lane under the main lane and a chequered flag
at the finish that lights once all fourteen are called, and a small padlock over every segment
whose call is committed. A right call gives the car a short forward burst with two speed lines behind it, a
wrong call drops it into the pit lane for a beat before it rejoins, and three correct calls in a
row light a flame behind it. Streaks build in three steps: two in a row gives the car a speed
trail, three adds the flame and the streak line in the points list on the reveal, and five grows both
and lights the track behind the car gold. A wrong call ends the streak, the
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
nobody has seen is a short run. Each line also carries its own `elapsedSecondsOnCard` in the
local record, timed from the card appearing to the basis Continue. It is wall-clock time and it
does not pause for tab inactivity, which is why it no longer carries the word active.

## Spelling

American spelling throughout, in the file and in these notes. The organization chips post as
`Organizations: ...` with a z.

## The end screen

The end screen runs in one order: a trophy drawn to the call score (bronze, silver, gold, and a
starred cup for a clean sweep) with a single rise and shine that respects
`prefers-reduced-motion`, the codename, the earned line reading "Right call 12 of 14. Right
reason 9 of 14.", the points total as the headline numeral under the one gold underline this
screen carries, the rank with how far short of the next one the run finished, the best streak and
the lap time, the counts of caught, let stand correctly and false flags, the fresh case pair, the
badges, the share card, the coaching behind one tap, the record and the send, and Play again
last.

Only earned badges show, at most three, as a row of medallions with the icon in ink on a hairline
disc and the name under it, appearing on a 150ms stagger that `prefers-reduced-motion` switches
off. They are chosen in a fixed order so the best ones survive the cut: Clean sweep, Cold read,
Hot lap, Steady hand, Second thoughts, Nothing over-flagged, Arithmetic hawk, Unsupported driver
caught, Read the silence, Traced the movement, Timing and drift. "Cold read" is the one badge the
fresh case can earn, at five of five on Brightwater, and it sits second because reading a company
cold is the hardest thing the drill asks. "Steady hand" is a run with no false flag on either
case, and "Second thoughts" is a call the player changed and got right. Nothing over-flagged is
the round one half of Steady hand, so it stands down whenever Steady hand is earned rather than
printing the same fact twice. A run that earns no badge prints one line instead.

The share card is a copyable block: the drill's name, the rank and the points, the call and
reason scores, the fresh case, and the best streak.

The coaching behind that tap has three blocks: the lines that got past you on Halyard, the lines
that got past you on the fresh case, and "Right call, wrong reason", which names every line where
the call agreed with the key and the basis did not, with the chips the player tapped and the
card's basis key beside them.

Play again returns to the codename screen with the codename and the chapter chips still filled
in and the score, the streak and the clock cleared. A second run posts a fresh response through
the same entries, so repeat runs appear in the sheet as separate rows under the same codename.
A codename is not a person. Report received attempts, completed attempts and distinct codenames
as three separate counts, keep a codename's first eligible attempt in the initial results and its
later attempts as reattempts, and count people only from a facilitator's session roster.

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
September 2026. The cell now opens with `Round2: right call 4/5, right reason 3/5; calls FSFFS; key FSFFS; seconds 61.`, then
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
row, which is how you recognize them.

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
taps Flag it or Let it stand, the chip row opens under the two buttons, and Lock it in stays
disabled until at least one chip is tapped. The memo, the figures and the On file facts stay on
screen underneath, so nothing has to be remembered to answer. Switching to the other call keeps
every chip that exists on both rows and drops the ones that do not, and the line of words is
kept either way.

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

### The reason, scored separately from the call

Since 13 September 2026 every card in `cases/` carries `basisKey`, the set of basis chips that
are correct on that card. A chip outside that set contradicts the key for that card. A reason
counts as right when the player tapped at least one chip in the key and no chip outside it. A
card the key lets stand carries `the figure and reason hold` and nothing else, so `wrong account`
on a clean line is a contradiction rather than a weak answer.

The two scores never mix. The running pill shows the call score alone, as `Right 7 of 9`. The end
screen shows both, as `Right call 12 of 14. Right reason 9 of 14.`, and the fresh case carries the
same pair. The badges read the calls alone. The rank does not: an agreeing reason adds 50 points
to a correct call, and the rank is read off total points, so fourteen correct Halyard calls reach
Partner at 2,625 with every reason agreeing and stop at Senior at 1,925 with none. The coach
section names every line where the call was right and the reason was not.

Question B carries both round totals beside the attempt identifier. Each Why field carries
`Reason: agrees.` or `Reason: does not agree.` and the card's basis key after the call verdict.
The downloadable record carries `basisKey` and `reasonResult` on each of the nineteen items and
`rightReason` beside `right` in both rounds.

This exists because an independent release review completed the whole drill on 13 September 2026
while tapping `wrong account` on every one of the nineteen lines, and the page awarded 14 of 14
and 5 of 5. The same run now scores zero on reason.

The reason score is a compatibility check on the stated basis, reported as agreement with the
accepted reason categories. It is not a rubric score, it does not establish that a player reasoned,
and a player who taps `no source on file` on every flag and the hold chip on every stand would
score well on it without having reasoned. The measurement adopted on 13 September 2026 for the
next assessment version, `brightwater-v6`, adds a short written explanation on each of the five
fresh-case items, naming the decisive evidence, why it matters for this period, and the action or
source request that follows. Those explanations are scored blind by an independent educator
against a rubric, the chips are still reported separately, and disagreements with the key are
retained rather than settled by it.

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
distinct codenames with `=COUNTA(UNIQUE(...))` on the codename column, and report that as distinct
codenames rather than as people, because one person can play under two codenames and a codename
can carry several attempts.

## If the form is ever rebuilt

Rebuilding the Google Form issues new `entry.NNNN` ids. Fetch the responder page, read the ids
out of the `FB_PUBLIC_LOAD_DATA_` block, and replace the `E` object and `FORM_POST` URL. Nothing
else in the file depends on the form.

<!-- GAME LANE SECTION START: case selection, the author page, the shared reader. Owned by the
     game lane, 13 September 2026. Nothing outside these markers is edited by this lane. -->

## Picking a case, and authoring one

The drill is no longer one case. The intro screen carries a quiet **Case** control, a plain
select, and it only appears when more than one case is actually available:

| Option | Where it comes from | Fresh case |
| --- | --- | --- |
| Halyard Provisioning | `cases/halyard-v4.json`, the default, 14 lines | Brightwater, assessment |
| Kestrel IT Services | `cases/kestrel-v1.json`, 12 lines, offered only when that file answers | Brightwater, assessment |
| My own case | this browser's `localStorage`, written by `author.html` | only if its author wrote one |

`?case=halyard`, `?case=kestrel` and `?case=own` in the address pick a case before the intro
screen is drawn, which is how the author page's Preview button arrives. The address wins over a
saved run. Changing the select reloads the case and starts the run clean, because a call indexes
a line and the two sets are different lines.

The chosen case's id rides into question A beside the version, as
`Case: kestrel, version kestrel-v1 (practice, 12 lines) and brightwater-v5 (assessment, 5 lines)`,
and into the local record at `scoring.caseId`, `attempt.caseId` and on every item. An own case
posts its id as `own:<name>:<version>`. **Whoever writes the findings script has to group on
that id and never pool rows from different cases**, the same rule that already applies to
versions.

Two things stopped being hard-wired to Halyard's fourteen lines on 13 September 2026.

**The line count.** Every screen number is derived from the loaded case rather than counted from
three to sixteen. A case of any length runs, and a case with no fresh set goes from its last line
straight to the end screen. The form carries fourteen per-line questions, so a case longer than
that posts its first fourteen lines into those fields and the whole run into the local record.

**The two month names.** A case file names its own columns in `columns`, as
`"columns": ["June", "July"]`, and the ledger headings, the figure strip on each card, the chart
and the orientation statement all read them. `halyard-v4` and `brightwater-v5` predate the field
and fall back to May against June, which is what they have always been.

Two badges stopped naming their lines by number at the same time, because line 12 does not exist
on a seven-line case. Each now reads the error type: a badge is earned when every line of that
type agreed with the key and the case has at least one. On Halyard a perfect run earns the same
set it always did.

### author.html, building a case from your own ledger

`author.html` takes a ledger and a memo in the same shapes the checker takes, runs the mechanical
checks over them, and hands back a card for each memo sentence it binds to a ledger line plus one
for every account that clears the rule with nothing written about it. Each sentence carries the
checker's own status, and a call is suggested only where that status settles one; a sentence held
for review or not checked comes back with no suggestion. A sentence that binds to no ledger line is
kept as an open item and holds the save until it is left out with a written reason or rewritten and
read again, and any change to the inputs after a read turns Save and Preview off until the case is
read again.

The checks suggest; the author decides. A failed arithmetic check pre-selects flag with the type
`arithmetic`, the chip `figure does not tie` and the checker's own sentence as the why; a
direction word against the sign pre-selects `wrong direction`; a silent line pre-selects
`no explanation`. Every one of those is a suggestion sitting in a control the author can change,
and the two lines a player reads at the reveal, the why and the tell, are written by hand.

Saving refuses until every card carries a call, an error type, at least one basis chip, a why and
a tell, and it names what is missing rather than saying no. It enforces the basis-key contract
`cases/README.md` states: a stand carries the hold chip and nothing else, a flag carries no hold
chip, a stand is a clean line and a flag is not. Every card's figures are checked back against the
ledger row it points at. Saving then writes the case into this browser under `btm.owncase.v1`,
which is the key the drill reads for **My own case**, and downloads the same JSON so the case can
be committed to `cases/` or handed to somebody else. An optional second block authors a fresh set
the same way, and can run it as an assessment.

Nothing pasted into that page leaves the browser. There is no upload, and the saved case lives in
that one browser on that one device.

### assets/second-pass-core.js, and a decision to record

The four mechanical checks are the checker's, not a second implementation of them.
`assets/second-pass-core.js` holds the checker's reader, copied verbatim out of `checker.html`
(lines 501-504, 513-1490, 1591-1614 and 2092-2159 as that file stood on 13 September 2026), with
nothing in it that touches the DOM.

**`checker.html` was not changed and does not load it.** The extraction the build called for
would have edited a file the checker lane owns, against whose code the fixtures in
`tests/run-checker-tests.cjs` are scored, so the copy path was taken instead and is recorded here
rather than left to be discovered. `author.html` loads the module; `checker.html` still carries
its own copy.

**The task to unify:** point `checker.html` at `assets/second-pass-core.js`, delete its own copy
of those functions, run `node tests/run-checker-tests.cjs` and confirm every fixture still passes. Until
that lands a fix made in one copy has to be made in the other, and the comment at the top of the
module says so.

### What was verified, 13 September 2026

Every run below was played through the page's own handlers, click by click, in test mode.

| Run | Result |
| --- | --- |
| Halyard, every call matching the key | Partner, 14 of 14 and 5 of 5, badges unchanged |
| Halyard, flag every line | Staff, 8 of 14 and 3 of 5 |
| Kestrel, every call matching the key | 12 of 12 and 5 of 5, Partner at 2,200 of 2,200, `caseId` `kestrel` |
| An own case authored from the Kestrel sample | 7 of 7, `caseId` `own:Kestrel IT Services:v1`, round two skipped |

A perfect Kestrel run reaches Partner on twelve lines, as a perfect Halyard run does on fourteen,
because the ladder is read as a share of what each case can give rather than as a fixed count of
points. A rank still compares runs of one case and never runs of two, since the cases differ in
length and in how much of the score a blanket call can reach.

No console errors on any run. No horizontal scrolling on `index.html`, `author.html` or
`checker.html` at 320, 375, 768 or 1280, measured as `scrollWidth` against `clientWidth` at every
screen of a full run. The nav marks Drill current on the drill. `index.html` carries no `<img>`
element at all, every figure on it being drawn SVG, so the width, height and lazy-loading rule has
nothing on that page to apply to.

Screenshots are in `screenshots/game/` and `screenshots/author/`, each at 375 and 1280.

One thing found and not fixed, because it is not this lane's file: at 320 pixels `checker.html`
has a 14 pixel internal overflow on `#out` after a run. The page itself does not scroll sideways.

<!-- GAME LANE SECTION END -->

## The answer key and the case files

Since 13 September 2026 both cases live outside the page, in `cases/halyard-v4.json` and
`cases/brightwater-v5.json`. Each file carries the company, the threshold policy, the ledger
rows, the memo sentences, the On file facts as verified case assumptions, the key, the error
type, the basis key, the reveal reason, the tell, its own version and date, and a `changeLog`
recording what moved from the version before it. An assessment case also carries
`"mode": "assessment"` and the assessment note the bridge prints. The superseded `halyard-v3`,
`brightwater-v4`, `brightwater-v3` and `brightwater-v2` files stay in the folder because responses were scored
against them. `cases/README.md` explains the format, the basis-key contract, the evidence on each
assessment line, what a shortcut scores on the assessment case, the differences from the
checker's Halyard sample, and what changed in this revision.

The page fetches both files at load. When the fetch fails, which is what happens when the file is
opened from a folder rather than served, it falls back to a generated copy written into
`index.html` between the `BUILD:CASES-START` and `BUILD:CASES-END` markers. Edit the JSON, then
run `node build-cases.cjs` to rewrite that copy. The script refuses to write if a card points at
an account that is not in the ledger, if a card's figures do not tie, if a card is missing its
key, its reason or its tell, if a card has no basis key, if a stand carries anything but the hold
chip, if a flag carries the hold chip, or if a key names a chip the page does not offer. On an
assessment case it also refuses if a memo states a dollar figure the account does not produce,
states a percent that is not the movement, uses a direction word against the sign, if a line
carries no memo sentence, or if a line is a no-explanation line.

The key is `flag` on eight of the fourteen Halyard lines and `stand` on the six clean ones; three
of the five Brightwater lines are `flag` and two are `stand`. Anyone who reads the source can read
the key, in the JSON as easily as in the page. That is the trade for instant feedback, and it is
the reason to send the link and not the file.

The error types are wrong direction, unsupported driver, unsupported attribution, timing,
arithmetic, no explanation and clean line. `halyard-v4` uses all seven. `brightwater-v5` uses two
of them, unsupported driver three times and clean line twice, because every line in an assessment
case has to test a named cause. "No explanation" covers a line where the memo says nothing about
an account that owes commentary, which is why it belongs in the practice case and not in the
scored one. "Unsupported driver" replaced "invented driver" on 13 September 2026, because a
sentence with nothing behind it is not established from the supplied evidence, which is a
different and smaller claim than saying it was fabricated.

A flag can be correct while the reason behind it is wrong. The reveals credit the call and correct
the reasoning separately, the page scores the two separately, and they ask for a bridge (billing
bridge, payroll bridge, reserve rollforward, depot revenue bridge) rather than handing the player
a derived cause. A stand can be provisional as well: Halyard 13 carries a `stillOpen` line saying
the calculation holds and the mix cause stays a hypothesis until the category bridge is on file,
and the reveal prints it whichever way the call went.

The version and date of both cases ride into question A and into the local copy, so a response can
always be tied to the key it was scored against. Never pool responses scored against different
case versions.

## Deploying

`index.html`, `cases/halyard-v4.json` and `cases/brightwater-v5.json`. No libraries. The only
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
