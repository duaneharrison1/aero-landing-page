// Aero landing site middleware.
//
// The original figmafolio version redirected any unknown path to
// app.figmafolio.com. That has been removed so the Aero marketing site never
// bounces visitors to figmafolio. All requests now pass straight through to the
// statically built pages (unknown paths fall through to the site's own 404).

export const config = {
  matcher: ["/((?!_astro|assets).*)"],
};

export default function middleware(_request: Request) {
  return;
}
