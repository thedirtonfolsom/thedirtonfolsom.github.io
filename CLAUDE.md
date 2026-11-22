# The Dirt on Folsom — site repo

Jekyll site served by GitHub Pages from `main` at https://thedirtonfolsom.github.io. Pushing to `main` publishes.

## Publishing a weekly issue
1. Add `_posts/YYYY-MM-DD-slug.html` (date = the issue's Thursday). Front matter: `layout: issue`, `issue` (next number), `title`, `dek`, `top_stories` (3 items: `title`, `summary`). Copy the structure of the newest post: `story` sections with `id="story-N"`, `explainer` boxes, `homes`, `callout` for the notable listing, `sources` lines.
2. Update `_data/market.yml` (only real, sourced numbers; no placeholders), `_data/pipeline.yml` (statuses), `_data/meetings.yml` (drop past meetings, add new ones, summarize posted agendas).
3. Test build if possible (`bundle exec jekyll build`), then commit and push to `main`.

## Editorial rules
- Every item: where it is, backstory, why it matters, source links.
- Explainer boxes for places/terms readers may not know.
- Summaries and links only for other outlets' stories; never copy articles. No scraping Zillow/Redfin listing pages.
- No invented facts or placeholder data. If unsure, leave it out.
- Large readable text; audience includes older readers.
- No sponsor line unless `sponsor:` is set in the post's front matter.

## Email version (sent from Kit, reviewed by the owner before sending)
- Each issue is also sent as a Kit broadcast. End every email with this note just above Kit's footer:
  "The mailing address below belongs to our newsletter service, Kit. Anti-spam law requires every newsletter to list one. To reach us, email thedirtonfolsom@gmail.com or just reply to this email."
