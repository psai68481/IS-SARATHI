import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'IS-SARATHI | AI-Powered Indian Standards Recommendation Engine',
  description: 'Automated standard alignment, requirement coverage, and BIS compliance intelligence for public procurement.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="antialiased min-h-screen bg-slate-100">{children}</body>
    </html>
  );
}
