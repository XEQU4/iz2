# README screenshots

Captured from the running IZ2 React workspace and Swagger reference on
11 October 2026. All four screens use the approved graphite and silver design,
shared cosmic background and original transparent PNG logo. These are browser captures, not generated
mockups or edited application screens.

| File           | Screen                                                                                      |
| -------------- | ------------------------------------------------------------------------------------------- |
| `overview.png` | Overview, six checked companies, three current verified people, 24 contracts and two groups |
| `graph.png`    | Three companies, one shared director and a shared address; the director is selected         |
| `catalog.png`  | Company directory, six fictional companies and saved-profile filters                       |
| `api.png`      | English API reference filtered to Companies, with its two GET endpoints visible             |
| `iz2-logo.png` | Approved transparent square PNG used in both README headers                                |

Overview is captured at 1440 × 650, the graph at 1440 × 1160, and the catalogue
and API at 1440 × 1040. The graph view is scrolled to show the complete explorer
and evidence panel. Captures contain only the browser viewport, with no browser
chrome, desktop, image compositing or changes to the interface for presentation.

All displayed entities, identifiers, contacts, dates and relationships come from
an isolated fictional fixture. It contains no working database records, user
accounts, source credentials or real company checks. Source labels illustrate
the interface; no live registry or KGD request was made. Screenshots show saved
template analyses and do not claim a model generated those results.

The fixture contains six companies and three people, with two groups: one formed
by a shared director and address, the other by a shared phone. The screenshot
dataset is not shipped as an installation seed. Private capture scripts and
verification reports stay under ignored `artifacts/readme/` and
`artifacts/noir-design/`.

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
Their simplified favicon still serves tabs; the PNG replaces visible website
logos. All four screenshots use the current logo and palette.

`iz2-mark.svg` is a retained earlier vector asset, not the current README logo.
`company.png` remains referenced by the archived README and is retained outside
the current screenshot gallery.
