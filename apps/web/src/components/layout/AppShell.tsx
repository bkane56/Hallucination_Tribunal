import type { ReactNode } from "react";
import { SiteFooter, SiteHeader, PrivacyBanner } from "./SiteChrome";

export function AppShell({ children }: { children: ReactNode }) {
  return (
    <div className="flex min-h-screen flex-col">
      <SiteHeader />
      <PrivacyBanner />
      <main className="mx-auto w-full max-w-6xl flex-1 px-4 py-8">{children}</main>
      <SiteFooter />
    </div>
  );
}
