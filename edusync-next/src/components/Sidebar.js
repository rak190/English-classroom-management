'use client';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function Sidebar() {
  const pathname = usePathname();

  const navItems = [
    { name: 'Dashboard', path: '/', icon: 'bx bx-grid-alt' },
    { name: 'Students', path: '/students', icon: 'bx bxs-graduation' },
    { name: 'Classes', path: '/classes', icon: 'bx bx-book-content' },
    { name: 'Attendance', path: '/attendance', icon: 'bx bx-check-square' },
    { name: 'Homework', path: '/homework', icon: 'bx bx-task' },
    { name: 'Schedule', path: '/schedule', icon: 'bx bx-calendar-event' },
    { name: 'Scores', path: '/scores', icon: 'bx bx-award' },
    { name: 'Progress', path: '/progress', icon: 'bx bx-line-chart' },
  ];

  return (
    <aside id="layout-menu" className="layout-menu menu-vertical menu">
      <div className="app-brand">
        <Link href="/" className="d-flex align-items-center text-decoration-none" style={{textDecoration: 'none'}}>
          <div className="app-brand-logo">
            <span className="fw-bold fs-5 text-white d-flex align-items-center justify-content-center h-100 w-100" style={{fontFamily: "'Inter', sans-serif"}}>///</span>
          </div>
          <span className="app-brand-text ms-3">Edusync</span>
        </Link>
      </div>

      <ul className="menu-inner py-1">
        {navItems.map((item) => (
          <li key={item.path} className={`menu-item ${pathname === item.path ? 'active' : ''}`}>
            <Link href={item.path} className="menu-link" style={{textDecoration: 'none'}}>
              <i className={`menu-icon tf-icons ${item.icon}`}></i>
              <div>{item.name}</div>
            </Link>
          </li>
        ))}

        <li className="menu-header mt-4"></li>
        <li className={`menu-item ${pathname === '/ai' ? 'active' : ''}`}>
          <Link href="/ai" className="menu-link" style={{textDecoration: 'none'}}>
            <i className="menu-icon tf-icons bx bx-bot"></i>
            <div>AI Tools</div>
          </Link>
        </li>

        <div style={{flexGrow: 1}}></div>
        
        {/* Bottom Links */}
        <li className="menu-item">
          <a href="#" className="menu-link" style={{textDecoration: 'none'}}>
            <i className="menu-icon tf-icons bx bx-cog"></i>
            <div>Settings</div>
          </a>
        </li>
        <li className="menu-item">
          <a href="#" className="menu-link" style={{textDecoration: 'none'}}>
            <i className="menu-icon tf-icons bx bx-support"></i>
            <div>Support</div>
          </a>
        </li>
        <li className="menu-item">
          <button className="menu-link bg-transparent border-0 w-100 text-start" style={{cursor: 'pointer'}}>
            <i className="menu-icon tf-icons bx bx-log-out"></i>
            <div>Log Out</div>
          </button>
        </li>
      </ul>
    </aside>
  );
}
