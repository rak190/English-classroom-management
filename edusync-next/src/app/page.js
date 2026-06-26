import { prisma } from '@/lib/prisma';
export const dynamic = 'force-dynamic';
import Link from 'next/link';

export default async function Dashboard() {
  const totalStudents = await prisma.management_student.count();
  const activeClasses = await prisma.management_course.count();
  
  // Dummy data for today since SQLite queries with dynamic dates can be tricky
  // We'd ideally query attendance where date = today and status = 'Present'
  const todayAttendancePresent = 42; 
  
  const hwSubmitted = await prisma.management_homeworksubmission.count({
    where: { status: 'Submitted' }
  });

  const recentNotices = await prisma.management_notice.findMany({
    take: 3,
    orderBy: { created_at: 'desc' }
  });

  return (
    <>
      <div className="row">
        {/* Top Metrics Row */}
        <div className="col-md-3 mb-4">
          <Link href="/students" className="text-decoration-none d-block h-100">
            <div className="card card-metric card-metric-orange">
              <div className="metric-value">{totalStudents}</div>
              <div className="metric-label">Students</div>
              <div className="metric-arrow">
                <i className='bx bx-right-top-arrow-circle' style={{fontSize: '20px'}}></i>
              </div>
            </div>
          </Link>
        </div>
        <div className="col-md-3 mb-4">
          <Link href="/classes" className="text-decoration-none d-block h-100">
            <div className="card card-metric card-metric-orange">
              <div className="metric-value">{activeClasses}</div>
              <div className="metric-label">Classes</div>
              <div className="metric-arrow">
                <i className='bx bx-right-top-arrow-circle' style={{fontSize: '20px'}}></i>
              </div>
            </div>
          </Link>
        </div>
        <div className="col-md-3 mb-4">
          <Link href="/attendance" className="text-decoration-none d-block h-100">
            <div className="card card-metric card-metric-orange">
              <div className="metric-value">{todayAttendancePresent}</div>
              <div className="metric-label">Attendance</div>
              <div className="metric-arrow">
                <i className='bx bx-right-top-arrow-circle' style={{fontSize: '20px'}}></i>
              </div>
            </div>
          </Link>
        </div>
        <div className="col-md-3 mb-4">
          <Link href="/homework" className="text-decoration-none d-block h-100">
            <div className="card card-metric card-metric-blue">
              <div className="metric-value">{hwSubmitted}</div>
              <div className="metric-label">Homework</div>
              <div className="metric-arrow">
                <i className='bx bx-right-top-arrow-circle' style={{fontSize: '20px'}}></i>
              </div>
            </div>
          </Link>
        </div>
      </div>

      <div className="row">
        {/* Charts Row 1 */}
        <div className="col-md-4 mb-4">
          <div className="card h-100 p-4">
            <div className="d-flex justify-content-between align-items-center mb-4">
              <h5 className="card-title-small mb-0">Students</h5>
              <span className="badge" style={{background: 'var(--genz-bg)', color: 'var(--genz-text-muted)'}}>Grade 7 <i className='bx bx-chevron-down'></i></span>
            </div>
            <div className="position-relative d-flex justify-content-center align-items-center" style={{height: '200px'}}>
              {/* <canvas id="studentsChart"></canvas> */}
              <div className="text-muted">Chart Component Here</div>
            </div>
          </div>
        </div>
        
        <div className="col-md-8 mb-4">
          <div className="card h-100 p-4">
            <div className="d-flex justify-content-between align-items-center mb-4">
              <h5 className="card-title-small mb-0">Academic Progress</h5>
              <span className="badge" style={{background: 'var(--genz-bg)', color: 'var(--genz-text-muted)'}}>Last 8 Months <i className='bx bx-chevron-down'></i></span>
            </div>
            <div style={{height: '200px'}} className="d-flex justify-content-center align-items-center">
               <div className="text-muted">Chart Component Here</div>
            </div>
          </div>
        </div>
      </div>

      <div className="row">
        {/* Notice Board */}
        <div className="col-md-6 mb-4">
          <div className="card h-100 p-4">
            <div className="d-flex justify-content-between align-items-center mb-4">
              <h5 className="card-title-small mb-0">Notice Board</h5>
              <span className="text-muted" style={{fontSize: '12px'}}>Sort by: <strong>Latest</strong> <i className='bx bx-chevron-down'></i></span>
            </div>
            
            <div className="notice-list">
              {recentNotices.length > 0 ? recentNotices.map((notice) => (
                <div key={notice.id} className="list-item-modern">
                  <div className="item-icon-square">
                    <i className='bx bx-notepad'></i>
                  </div>
                  <div className="item-content">
                    <h6 className="item-title">{notice.title}</h6>
                    <p className="item-desc mb-0">by {notice.author_name || 'Admin'}</p>
                  </div>
                  <div className="item-meta">
                    {new Date(notice.created_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
                  </div>
                </div>
              )) : (
                <div className="list-item-modern">
                  <div className="item-icon-square">
                    <i className='bx bx-calendar-event'></i>
                  </div>
                  <div className="item-content">
                    <h6 className="item-title">School Event Reminder</h6>
                    <p className="item-desc mb-0">by Ms. Harper, Event Coordinator</p>
                  </div>
                  <div className="item-meta">
                    May 29, 2025
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
