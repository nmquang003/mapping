# Bếp An Toàn — visual upgrade

Canvas renderer, 1000×640 logical pixels, web desktop/touch. Preserve kitchen layout and collision rectangles. Smooth sampling for hand-painted raster sprites; no pixel-art conversion.

Style target: the existing ImageGen cover, warm Vietnamese school fair, rounded silhouettes, fine dark green/brown contours, cream/mint/teal/coral palette. Slightly elevated orthographic front view for objects, cardinal-facing characters. Light from top left. No text baked into assets. Environment low contrast; characters and food retain contrast at actual display size.

Characters: Linh (ponytail, mint apron), Nam (short hair, blue-green apron), white shirts and red school scarves. Native on-map height approximately 80 logical px. Shared bottom-center anchor per frame, two gait poses per direction; additional breathing/bob, carrying and work effects in code. Do not claim fully frame-authored action animations.

Stations: twelve coherent standalone sprites; fit existing footprints without enlarging collision. Runtime labels, selection rings, temperatures, progress and failure states remain code-native. Stock foods and prepared foods share UI imagery but distinguish stage through text and separate raw/cooked assets.

Normalization: inspect actual sheet geometry and alpha; slice equal cells only after verification; trim transparent margins; uniform scale per character across frames; feet anchor consistent. Generate preview sheet. Preserve original ImageGen files in art/source, ship normalized assets under assets/sprites.

Acceptance: check character identity, station readability, no clipping, background alpha, source file provenance, correct order/frame mapping; view actual gameplay on narrow and desktop sizes; run existing gameplay tests/build.
