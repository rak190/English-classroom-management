import "./globals.css";
import Sidebar from "@/components/Sidebar";
import TopNav from "@/components/TopNav";

export const metadata = {
  title: "Edusync CMS",
  description: "Modern Classroom Management System",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <head>
        {/* Fonts & CDNs */}
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link href="https://fonts.googleapis.com/css2?family=Public+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400;1,500;1,600;1,700&display=swap" rel="stylesheet" />
        <link href="https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css" rel="stylesheet" />
        
        {/* Core CSS from legacy Django app */}
        <link rel="stylesheet" href="/static/sneat/vendor/css/core.css" className="template-customizer-core-css" />
        <link rel="stylesheet" href="/static/sneat/vendor/css/theme-default.css" className="template-customizer-theme-css" />
        
        {/* Chart.js */}
        <script src="https://cdn.jsdelivr.net/npm/chart.js" async></script>
      </head>
      <body>
        <div className="app-frame">
          <div className="layout-wrapper">
            <div className="layout-container">
              <Sidebar />
              <div className="layout-page">
                <TopNav />
                <div className="content-wrapper">
                  {children}
                </div>
              </div>
            </div>
          </div>
        </div>
      </body>
    </html>
  );
}
