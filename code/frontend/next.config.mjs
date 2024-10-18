/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: "/api/process",
        destination: "http://localhost:8000/api/process",
      },
    ];
  },
};

export default nextConfig;
