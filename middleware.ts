export const config = {
  matcher: ["/((?!_astro|assets).*)"],
};

// Previously redirected unknown paths to app.figmafolio.com.
// Removed: the Aero site serves its own pages; unknown paths show the 404 page.
export default function middleware(_request: Request) {
  return;
}
