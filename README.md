# Second Pass: Beat the Machine

A ten minute reviewer's game for the George Mason ACFE student chapter. Fourteen accept or reject
calls on a machine written month end memo, instant feedback on every card, and a running score
against the machine. Answers post straight into the existing Google Form's responses, so the
leaderboard and the pooled results are unchanged.

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

## If the form is ever rebuilt

Rebuilding the Google Form issues new `entry.NNNN` ids. Fetch the responder page, read the ids out
of the `FB_PUBLIC_LOAD_DATA_` block, and replace the `E` object and `FORM_POST` URL. Nothing else
in the file depends on the form.

## The answer key

The key lives in the `CARDS` array as `answer` and `trap`, because the game reveals it a card at a
time. Anyone who reads the source can read the key. That is the trade for instant feedback, and it
is the reason to send the link and not the file.
