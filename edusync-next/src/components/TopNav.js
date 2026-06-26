'use client';
import React from 'react';

export default function TopNav() {
  return (
    <nav className="layout-navbar container-fluid d-flex justify-content-between align-items-center">
      <div className="d-flex align-items-center">
        <a className="nav-item nav-link px-0 me-xl-4 d-xl-none text-dark layout-menu-toggle" href="javascript:void(0)">
          <i className="bx bx-menu bx-sm"></i>
        </a>
        <h3 className="mb-0 fw-bold d-none d-md-block">Dashboard</h3>
      </div>

      <div className="d-flex align-items-center gap-3">
        <div className="search-bar d-none d-md-flex">
          <i className="bx bx-search text-muted fs-5"></i>
          <input type="text" placeholder="Search" />
        </div>
        <div className="mic-icon d-none d-md-flex">
          <i className="bx bx-microphone fs-5"></i>
        </div>
        
        {/* Profile & Notifications */}
        <div className="d-flex align-items-center ms-md-4">
          <div className="profile-avatar mb-0 me-3" style={{width: '44px', height: '44px', fontSize: '16px'}}>
            <img src="https://ui-avatars.com/api/?name=Admin&background=FFB800&color=FFFFFF" alt="" className="w-100 h-100 rounded-circle" />
          </div>
          <div className="profile-info d-none d-md-block me-3">
            <h6 className="profile-name mb-0" style={{fontSize: '15px', fontWeight: '700'}}>Admin</h6>
            <p className="profile-role mb-0" style={{fontSize: '12px', color: '#94A3B8'}}>Admin</p>
          </div>
          <div className="bell-icon position-relative d-flex align-items-center justify-content-center" style={{width: '40px', height: '40px', fontSize: '20px', color: 'var(--genz-text-main)', cursor: 'pointer', border: 'none', background: '#F8FAFC', borderRadius: '50%'}}>
            <i className="bx bx-bell"></i>
            <span className="bell-dot position-absolute" style={{top: '10px', right: '10px', width: '8px', height: '8px', backgroundColor: '#EF4444', borderRadius: '50%', border: '2px solid #F8FAFC'}}></span>
          </div>
        </div>
      </div>
    </nav>
  );
}
