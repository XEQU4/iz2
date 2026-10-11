# README screenshots

Captured from the running IZ2 React workspace and Swagger reference on
11 October 2026, after the graphite design update. These are browser captures,
not generated mockups or edited application screens.

| File           | Screen                                                                                      |
| -------------- | ------------------------------------------------------------------------------------------- |
| `overview.png` | Overview, six checked companies, three current verified people, 24 contracts and two groups |
| `graph.png`    | Three companies, one shared director and a shared address; the director is selected         |
| `company.png`  | Company fields with provenance and separate, missing KGD checks                             |
| `api.png`      | English API reference with the company list endpoint expanded                               |
| `iz2-mark.svg` | Approved square primary emblem for the README header                             |

All displayed entities, identifiers, contacts, dates and relationships come from
an isolated fictional fixture. It contains no working database records, user
accounts, source credentials or real company checks. Source labels illustrate
the interface; no live registry or KGD request was made. Screenshots show saved
template analyses and do not claim a model generated those results.

The fixture contains six companies and three people, with two groups: one formed
by a shared director and address, the other by a shared phone. The screenshot
dataset is not shipped as an installation seed. Private capture scripts and
verification reports stay under ignored `artifacts/readme/`.

When updating the images, use fictional data, wait for fonts, records and heading
animations to finish, and inspect the saved image. Keep names, credentials and
identifiers from the working database out of these public assets. Capture the
running interface; do not alter displayed scores or counts for presentation.

## Logo

The current approved logo is the original transparent 1254 × 1254 PNG.
`frontend/src/assets/branding/iz2-logo.png` is the canonical application asset;
`static/images/iz2-logo.png` and `docs/assets/iz2-logo.png` are byte-identical
copies for Django and the repository README. Do not redraw, crop or re-encode it.
React imports it through Vite; Django templates resolve it through static storage.

The earlier vector source files remain in the frontend branding directory.
Their simplified favicon still serves tabs;
the PNG replaces visible website logos. The screenshots above predate this
logo change and retain their original capture.
