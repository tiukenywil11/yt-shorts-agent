# Small Change Lab landing page

Static, no build step. Open `index.html` in a browser. Files: `index.html`, `styles.css`, `assets/` (copies of `creative/brand/dp.svg` and `banner.svg`).

## Wire up the signup form
The form in `index.html` posts to a placeholder (`https://example.invalid/REPLACE-WITH-PROVIDER-FORM-URL`). Nothing is collected until you replace it. Keep one email input and set its `name` to what the provider expects.

- **Kit (ConvertKit):** create a Form, choose Embed > HTML, copy the form `action` URL it shows; the email field is named `email_address`.
- **Beehiiv:** Grow > Subscribe Forms > HTML embed; use the `action` and email field name it gives you.
- **Gumroad / Payhip:** these sell products rather than capture plain email POSTs. Make the tracker a free ($0) product and either change the `<form>` to a button link (`<a class="btn" href="PRODUCT_URL">`) or paste the provider's embed snippet.

Check each provider's current docs for exact URLs. Add double opt-in and a privacy policy link before launch.

## Before launch
- Review `privacy.html` against the laws that apply to you; it is a generic template, not legal advice.
- Point the `../tracker/` link at the real tracker location.
- Confirm the domain and add a privacy policy.
- Pillar and series copy is paraphrased from `creative/channel-identity.md`.

## Online tracker (`tracker.html`)
Interactive 30-day tracker, up to 3 habits, no login. Data lives in the visitor's browser (`localStorage`, key `scl-tracker-v1`), so it is per device and per browser; the page warns about this and offers Download/Restore backup (JSON). The email form reuses the same placeholder endpoint as `index.html`: replace it there and here. The printable PDF is `assets/habit-tracker-30day.pdf` (a copy of `../tracker/habit-tracker-30day.pdf`; re-copy if you change the print version).

Analytics are off. `track()` in `tracker.html` calls `window.plausible` if you add a privacy-friendly script; it fires `tracker_first_tick` and `tracker_return_visit`. If you enable analytics, update `privacy.html` first (it currently says no analytics).
