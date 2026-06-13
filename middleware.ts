export const config = {
  matcher: ["/((?!_astro|assets).*)"],
};

export default function middleware(request: Request) {
  const url = new URL(request.url);
  const pathname = url.pathname;

  // Paths that should NOT redirect (stay on landing page)
  const landingPagePaths = ["/", "/about", "/contact", "/pricing", "/how-it-works"];

  if (landingPagePaths.includes(pathname)) {
    return;
  }

  // Prefix matches (blog, features)
  const landingPagePrefixes = ["/blog", "/features"];
  for (const prefix of landingPagePrefixes) {
    if (pathname === prefix || pathname.startsWith(prefix + "/")) {
      return;
    }
  }

  // Favicon files
  if (pathname.startsWith("/favicon")) {
    return;
  }

  // File requests (has extension like .js, .css, .png)
  if (pathname.includes(".")) {
    return;
  }

  // Redirect everything else to app.figmafolio.com
  return Response.redirect(`https://app.figmafolio.com${pathname}`, 302);
}
