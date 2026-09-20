/** @type {import('next').NextConfig} */
// Local dev: Next.js proxies /api/v1/* to the local FastAPI backend on :8000.
// Production (Vercel Services): routing to the container API service is done by
// the root vercel.json rewrites, so no localhost proxy is configured here.
const isProd = process.env.NODE_ENV === 'production';

const nextConfig = {
  reactStrictMode: true,
  async rewrites() {
    if (isProd) return [];
    const target = process.env.BACKEND_ORIGIN || 'http://localhost:8000';
    return [
      {
        source: '/api/v1/:path*',
        destination: `${target}/api/v1/:path*`,
      },
    ];
  },
};

module.exports = nextConfig;
