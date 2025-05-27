/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'img.mlbstatic.com',
        pathname: '/mlb-photos/**'
      }
    ]
  }
}

module.exports = nextConfig
