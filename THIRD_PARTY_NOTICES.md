# Third-party notices

IZ2 includes the following component adaptations and assets. This index points
to retained notices; the full licence texts govern their respective material.
It is not an exhaustive dependency or source-data licence audit.

## Interface components and assets

| Material                                 | Use in IZ2                                                              | Retained notice                                                                                                                                                                                                                         |
| ---------------------------------------- | ----------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| React Bits                               | Text motion, navigation focus frames, particles and card border effects | [MIT + Commons Clause](frontend/licenses/react-bits.txt); [text adaptations](frontend/licenses/text-motion-sources.txt), [Particles](frontend/licenses/particles-sources.txt), [Border Glow](frontend/licenses/border-glow-sources.txt) |
| Lightswind UI                            | Adapted Aurora Background gradient technique                            | [MIT](frontend/licenses/lightswind.txt)                                                                                                                                                                                                 |
| Magic UI                                 | Adapted Border Beam effect                                              | [MIT](frontend/licenses/magic-ui.txt)                                                                                                                                                                                                   |
| OGL                                      | WebGL rendering for the particle background                             | [Unlicense, OGL 1.0.11](frontend/licenses/ogl.txt)                                                                                                                                                                                      |
| Manrope, Space Grotesk and IBM Plex Mono | Self-hosted interface fonts                                             | SIL Open Font License 1.1 in the [distributed notices](frontend/public/third-party-notices.txt); API font copies retain [Manrope](static/fonts/Manrope-OFL.txt) and [IBM Plex](static/fonts/IBM-Plex-OFL.txt) notices                   |
| Radix UI                                 | Icons, dialogs and supporting interface primitives                      | MIT texts in the [distributed notices](frontend/public/third-party-notices.txt)                                                                                                                                                         |
| React, React Router, Motion and D3       | Interface, navigation, motion and graph rendering                       | Package-specific texts in the [distributed notices](frontend/public/third-party-notices.txt)                                                                                                                                            |

React Bits includes an additional Commons Clause condition. Its components must
not be described as unrestricted MIT material. The linked adaptation records
identify the upstream sources and local changes.

Coss UI and UILib informed composition and interaction choices; their source code
was not copied into IZ2. Original interface artwork, the IZ2 mark and the crescent
illustration are separate from the third-party assets listed above.

## API reference and dependency packages

Swagger UI is supplied by `drf-spectacular-sidecar` under Apache License 2.0.
Its `swagger-ui-dist/LICENSE` and `swagger-ui-bundle.js.LICENSE.txt` accompany the
installed and collected static assets. The sidecar package retains its own
licence separately.

The [frontend notice bundle](frontend/public/third-party-notices.txt) also retains
notices for supporting packages. Backend, build and runtime dependencies carry
their own notices in their distributions. This index does not replace those
files or certify every transitive dependency.

## Project code and source data

IZ2's original code and documentation are available under the [MIT licence](LICENSE).
Third-party components and assets retain their respective terms described above;
the project's MIT licence does not replace those terms. The project author's
contact is in the [README](README.md#authors-and-contact).

Procurement records and other collected source data are separate from software
licensing. Their availability through an integration does not grant redistribution
rights or transfer rights to the underlying sources.
